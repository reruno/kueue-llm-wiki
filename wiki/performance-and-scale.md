# Performance and scale

**Summary**: Kueue's throughput is bounded by its single scheduling loop, the cost of its in-memory cache updates, and the cost of the [[visibility-api]] snapshot. Scale pain has clustered around [[topology-aware-scheduling]] (per-domain accounting), cohort hierarchy updates, and visibility under load.

**Sources**: `raw/github/kubernetes-sigs__kueue/`, pr-15538.md, pr-15949.md, pr-16282.md, pr-15026.md, issue-15957.md, issue-15537.md, issue-14608.md, issue-16338.md, pr-16340.md, pr-16463.md, pr-17218.md, pr-17231.md, pr-17414.md, pr-17448.md, issue-17412.md, pr-17461.md, pr-17424.md, pr-17157.md, pr-17227.md, pr-16630.md, raw/kueue/pkg/controller/admissionchecks/multikueue/multikueuecluster.go; `raw/kueue/CHANGELOG/CHANGELOG-0.20.md`; `raw/kueue/apis/config/v1beta2/defaults.go`.

**Last updated**: 2026-10-28

---

## Where the loop spends time

Per scheduling cycle, cost drivers:

- Walking the per-CQ heap to pick candidates.
- For each candidate, computing the flavor-by-resource-group assignment.
- For TAS, computing the per-topology-domain fit.
- On preemption, collecting candidates and marking them evicted.

At moderate scale (hundreds of CQs, thousands of pending Workloads) the loop fits comfortably. At larger scale, hot spots appear:

- **TAS reconcile cost.** Listing all Workloads in the Node reconciler is expensive ([[issue-10037]] — TAS NodeHotSwap: Fix performance issue due to listing all Workloads in Reconcile).
- **TAS memory footprint.** "Optimize memory usage of TAS" ([[issue-3522]]) tracks the cache shape.
- **Visibility snapshot lock.** "Release the lock as soon as possible when computing the snapshot for CQ visibility" ([[issue-1098]]).
- **Cohort hierarchy updates.** "Unexport access to Cohorts and ClusterQueues maps in hierarchy.Manager" ([[issue-2996]]) was a cleanup that tightened mutation patterns so accesses could be made faster.
- **Terminating-pod accounting.** "TAS capacity accounting doesn't track Terminating pods" ([[issue-10076]]) caused false-negative admission decisions.

## Scale-oriented features

- **TAS NodeHotSwap** — a path for node replacement that avoids full re-reconcile.
- **Hierarchical cohort validation** — cheap checks that catch malformed trees before they enter the cache.
- **Subtree borrowing accounting** — correct subtree math was a bug ([[issue-10615]] — Subtree borrowing ignored when scheduling) whose fix also tightened the iteration hot path.

## Known non-linearities

- **`ClusterQueue.spec.resourceGroups` size.** Each resource group is walked per admission attempt; very wide groups multiply the cost per Workload.
- **Hierarchical cohort depth.** Borrowing walks upward at admission and preemption; deep trees pay that cost each time.
- **Number of TAS domains.** Per-domain accounting scales with the fanout at the innermost topology level.

## Integration-side scale

RayCluster with many worker groups, or a JobSet with many replicated jobs, creates multi-PodSet Workloads. Per-PodSet admission cost is linear; cohort-level preemption candidates include all admitted Workloads in the cohort, so CQ-per-namespace deployments keep this set small.

## Client-side rate limiting

Throughput is frequently bounded not by the scheduling loop but by the client-go token bucket in front of the API server.

- **Kueue's own client** is configured from the Configuration field `clientConnection` (`qps`, `burst`), which defaults to **`qps: 1000` / `burst: 1000`** (`DefaultClientConnectionQPS`/`DefaultClientConnectionBurst` in `apis/config/v1beta2/defaults.go`). **Correction (2026-10-21)**: this page used to say `300`/`500` in `apis/config/v1beta1/defaults.go`. The defaults were raised to 1000/1000 across client connections in v0.20.0 (#15206; source: CHANGELOG-0.20.md), and config `v1beta1` is gone in v0.20 (see [[api-versions]]). `cmd/kueue/main.go` installs a shared `flowcontrol.NewTokenBucketRateLimiter(qps, burst)` **only when `qps >= 0`**; a **negative `qps` deliberately disables** client-side rate limiting altogether.
- **MultiKueue's worker clients** inherited client-go's defaults of **QPS 5 / Burst 10** until v0.20. Gate `MultiKueueReuseClientConnectionConfigForWorkers` (Beta, **on by default since v0.20**) now applies the same `clientConnection` `qps`/`burst` to each worker cluster with its own per-cluster token bucket; on older versions or with the gate off this remains a large, easily-missed bottleneck — see [[multikueue#Manager → worker clients: `clientConnection` QPS/Burst now applies (v0.20, Beta)]].
- **Leader-election lease client (pr-15538, fixes issue-15537).** With `leaderElection.leaderElect: true` the Lease renewal client used to share the controllers' rate limiter object (`cmd/kueue/main.go` sets one explicit `kubeConfig.RateLimiter`; controller-runtime's fallback `rest.CopyConfig` copies the pointer). Under a low `clientConnection.qps`/`burst`, a reconcile burst (for example the startup replay of retained finished Workloads) starved the Lease update past `renewDeadline`, the manager exited with `leader election lost`, and the Deployment crash-looped while nothing was admitted. `config.SetLeaderElectionConfig` now sets `ctrl.Options.LeaderElectionConfig` to a copy of the manager `rest.Config` **without** the shared `RateLimiter`, so the lease client builds its own bucket from the same `qps`/`burst` (negative `qps` still disables throttling; behaviour with leader election off is unchanged). If you see `leader election lost` right after start-up on a large cluster, check the version and `clientConnection`.

**Gotcha — zero is accepted and breaks the client.** `qps`/`burst` are pointers defaulted with `cmp.Or`, so an explicit `0` survives defaulting, and nothing validates it (source: pr-14442.md, open):

- `burst: 0` → every request fails immediately at the limiter with `rate: Wait(n=1) exceeds limiter's burst 0`.
- `qps: 0` with a non-zero burst → the first `burst` requests succeed, then the bucket never replenishes and later requests **block until their context is cancelled or times out** (indefinitely if it has neither).

Keep `qps > 0` and `burst > 0`, or set a negative `qps` if the intent is to remove the limiter.

## Parallel API writes within one reconcile

Controllers that fan out API updates within one reconcile can run up to **32** concurrent updates instead of 8 with the `HighMaxParallelismWithinReconcile` gate. It is Beta and on by default in v0.20 (`pkg/features/kube_features.go`: `{0.20, Default: true, Beta}`), and the gate was also backported to v0.19.7 and v0.18.11 (source: CHANGELOG-0.20.md #16336; CHANGELOG-0.19.md #16387; CHANGELOG-0.18.md #16388). With 32 parallel writes the controller depends even more on the client token bucket above.

## Many flavors and Variant Workloads

Flavor assignment cost grows with the number of flavors in a ResourceGroup, and with ConcurrentAdmission each flavor also becomes a Variant Workload. The API comments on ClusterQueue `flavors` now warn about the performance impact of many flavors (pr-16282), and the ConcurrentAdmission cap was raised from 16 to 32 with a docs caution about very many ClusterQueues (pr-15949; [[concurrent-admission]]).

## Known hot spots (open or not merged in this batch)

- Fair-sharing preemption recomputed cohort lendable capacity once per candidate (~11% of CPU on preemption-heavy clusters, issue-15957.md). **Fixed**: #15955 precomputes lendable Cohort capacity, making preemption up to 20% faster. Shipped in v0.20.0, v0.19.7 and v0.18.11 (source: CHANGELOG-0.20.md, CHANGELOG-0.19.md, CHANGELOG-0.18.md); see [[fair-sharing#Performance note: lendable capacity is precomputed per Cohort]].
- Classical preemption collects and sorts the candidate pool even when preemption provably cannot help (issue-14608.md, still open). Not fixed. Related: the sorting cost (issue-16338) was fixed by pr-16340, which caches candidate ordering per ClusterQueue for the scheduling cycle and merges candidates lazily (gate `ClassicalPreemptionCandidateOrderCache`, Beta/on at 0.21 on main, Alpha/off in the 0.20/0.19 backports pr-17296/pr-17295). Reported 18-36 to 104-117 scheduling ops/s in a 10,000-Workload reclaim benchmark ([[preemption#Classical preemption reuses a per-cycle candidate ordering (`ClassicalPreemptionCandidateOrderCache`)]]).
- Exact big-integer quota amounts add cost only beyond `int64`; the `int64` fast path allocates nothing, but `ResourceNodeClone` grew ~20% (pr-15026, [[cache-architecture#Quota amounts are exact past int64 (pr-15026)]]).

## Event-path CPU fixes in the October 2026 wave

Measured with `make run-performance-scheduler` CPU profiles (source: the PRs cited):

| Hot spot | Fix | Effect |
|---|---|---|
| `reportLQPendingWorkloads` scanned every pending Workload of the CQ per queue change, under the queue lock (O(N^2) to drain) | per-LocalQueue counts in `PendingWorkloads` (pr-17414), per-LocalQueue custom-label trackers (pr-17448) | 9.0% of Kueue CPU (more than `schedule`) to gone; with one custom label 31.6% to 2.7% ([[cache-architecture#Queue manager: per-LocalQueue pending counts (pr-17414, pr-17448)]]) |
| Scheduling hash computed for every Info, also outside the queue | `WithSkipSchedulingHash()` for cache, unadmitted-condition and DRA Infos (pr-17461) | 1.79 s to 0 (about 1.7% of CPU) |
| Workload controller built a full Info for the DRA check and compared whole PodSpecs | build only when a DeviceClass backs an extended resource; compare only adjusted fields (pr-17424) | `Info.Update` 8.49 s to 4.98 s ([[workload-resource-adjustment]]) |
| MultiKueue workers wrote and lost a `Closed` preemption-gate state per replicated Workload | stop writing `Closed` states (pr-17157) | fixes a regression (CI fell from about 46 to 33 workloads/s when the gate went on); locally 99-100 vs 86-94 workloads/s, same as gate off ([[multikueue-orchestrated-preemption]]) |

All are backported to release-0.20 (and most to 0.19) after v0.20.2 / v0.19.9. Separately, on main the eight per-cycle scheduler progress log lines moved from V(2) to V(3) (pr-17227); a Workload waiting for preemption could otherwise produce about 740 log lines per second at the default verbosity ([[scheduler-internals#Scheduler progress logs are at V(3) (pr-17227, main only)]]).

**Startup.** Since pr-16630 the scheduler waits for the cache-filling event handlers' initial lists before its first cycle. On a cold start with many objects the first cycle starts later, but no longer decides on a partial cache; a warm follower does not wait ([[scheduler-internals#Phase 0: wait for the initial cache sync (pr-16630)]]).

**Performance scheduler tool.** pr-16463 (backports pr-17218/0.20, pr-17231/0.19) extended `test/performance/scheduler` with nested Cohorts, ClusterQueue `lendingLimit`, delayed Workload-set submission (`initialDelayMs`), configurable runner QPS/burst and Workload concurrency, and scheduled CPU profiling, to reproduce preemption-heavy scenarios such as issue-16338; see [[testing-performance]] (source: pr-16463.md, raw/kueue/test/performance/scheduler/runner/generator/generator.go).

## Interpreting metrics

`kueue_admission_attempt_duration_seconds` and `kueue_admission_attempts_total` are the primary signals for loop health (see [[metrics]]). A climbing p99 with stable attempt count means per-attempt cost is rising (flavor groups grew, TAS domains grew, cohort deepened). A climbing attempt count with stable duration means demand is rising; tune queue strategy or split CQs.

## Related pages

- [[architecture]] — where the cache and queue live.
- [[metrics]] — scheduling-loop instrumentation.
- [[topology-aware-scheduling]] — main source of scale work.
- [[visibility-api]] — snapshot cost.
- [[testing-performance]] — how to run the scheduler perf benchmarks that substantiate the claims on this page.
- [[multikueue]] — the manager→worker leg, whose clients are throttled separately.
