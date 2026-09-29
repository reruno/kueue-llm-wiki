# Issue #8564: MultiKueue: performance testing

**Summary**: MultiKueue: performance testing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8564

**Last updated**: 2026-09-21T10:15:37Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-13T16:35:01Z
- **Updated**: 2026-09-21T10:15:37Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-soon`, `area/multikueue`
- **Assignees**: [@YQ-Wang](https://github.com/YQ-Wang)
- **Comments**: 11

## Description

**What would you like to be added**:

Performance test for MultiKueue . 

We would like to observe the rate of processing workloads assuming there are 3 (or so) worker clusters.

I imagine this is a dedicated CI job. It will be hard in OSS on kind to get beyond 3 clusters probably, or otherwise we will anyway saturate the resources of the host node running the CI job.



**Why is this needed**:

To allow detecting performance regressions in MultiKueue.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-14T13:31:01Z

/priority important-soon

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-02-16T10:50:32Z

/area multikueue

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-05-17T11:20:52Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-06-16T12:01:25Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@YQ-Wang](https://github.com/YQ-Wang) — 2026-07-31T09:09:43Z

/remove-lifecycle rotten

### Comment by [@YQ-Wang](https://github.com/YQ-Wang) — 2026-07-31T09:09:46Z

/assign

### Comment by [@YQ-Wang](https://github.com/YQ-Wang) — 2026-07-31T18:27:25Z

I have implemented the MultiKueue performance benchmark proposed here. Summary of where it landed:

- One manager and three worker `envtest` control planes, measuring admitted Workloads per second. The baseline admits 120 Workloads at about 1.31/s; five consecutive runs spanned 1.289 to 1.335.
- No production code change. The benchmark configures nothing that a deployed manager does not already configure, and the diff is confined to `test/performance/multikueue/` plus two Make target files.
- The reason the number is small is worth stating up front: MultiKueue's worker-cluster clients run at client-go's default of 5 QPS per Kind, and that limiter is what bounds dispatch. Raising it does not reveal MultiKueue's processing capacity as it moves the bound onto the manager's own `clientConnection` limiter, which is a production default too. Details and measurements below.
- On the completion requirements: this comment is the `Design doc`, and `Docs update` is `test/performance/multikueue/README.md`, which is how `test/performance/scheduler` is documented today.

The implementation is on [`feat/8564-multikueue-performance`](https://github.com/YQ-Wang/kueue/tree/feat/8564-multikueue-performance) in my fork. I will open the PR shortly; I wanted the design and the rate-limit finding on the record here first.

> Disclosure: AI tooling was used to implement the benchmark, run the measurements, and draft this write-up, per the [Kubernetes AI tool usage policy](https://www.kubernetes.dev/docs/guide/pull-requests/#ai-guidance). I have reviewed the code and reproduced the numbers.

<details>
<summary>Full design document</summary>

## Goal

Detect performance regressions in MultiKueue's control plane by measuring the rate at which a manager cluster dispatches Workloads to, and gets them admitted on, three worker clusters.

## Non-goals

- Measuring Kubernetes Job or Pod execution. Nothing is unsuspended and no pod runs, so the numbers are not end-to-end job latency.
- Measuring the manager's scheduler. That is already covered by `test/performance/scheduler`. Manager-side quota reservation is recorded here only as a baseline to subtract.
- Absolute numbers comparable across machines, although the baseline turns out to be more portable than expected; see *What bounds the measurement*.

## Topology, and why envtest rather than kind

The issue notes that going beyond ~3 clusters on kind will saturate the CI host. Rather than spend that budget on container runtimes, the benchmark starts four `envtest` control planes (one manager, three workers) from a single benchmark process, with the API servers raised to `max-requests-inflight=5000` and `max-mutating-requests-inflight=2500`. This also follows what `test/performance/scheduler` already does.

The whole target — build, unit tests, 120-workload run, regression check — finishes in about 150 seconds on a 32-core host, with no images to pull and no container runtime.

The tradeoff is that there is no kubelet and no kube-scheduler, so a worker admits a Workload but nothing runs. That is the boundary we want: it isolates MultiKueue's dispatch cost from pod-startup noise, which would otherwise dominate and be far more variable than the signal.

Fidelity gaps worth naming, both in the direction of understating load:

- No webhooks on any cluster, and no job framework reconcilers. The runner creates the Job and its Workload directly rather than letting the Job reconciler derive the Workload, so the measured window starts at a Workload that already exists.
- The mirrored Job is created on the winning worker but never reconciled or unsuspended.

`MultiKueueManagerQuotaAutomation` is left at its production default of off, so remote ClusterQueue and LocalQueue reads go uncached here exactly as they do in a deployed manager.

## What is measured

For each Workload on the manager, the runner records:

1. **Quota reservation** — the manager's own scheduler reserving quota. This is manager-side work and is the one series here that does not track dispatch throughput.
2. **Admission** — the Workload becoming `Admitted`, which under MultiKueue means a worker reserved quota, the manager observed it, and the MultiKueue AdmissionCheck went `Ready`.

The gap between the two is MultiKueue's cost. In the baseline quota reservation P95 is about 0.1s against an admission P95 of about 90s, so the measurement is overwhelmingly MultiKueue rather than the manager.

Timestamps come from the runner observing its own Workload watch, not from condition `lastTransitionTime`, because those are serialised to one-second granularity. Percentiles use nearest-rank.

The headline number is **throughput**: workloads admitted per second across the run.

### A caveat on the latency percentiles

The runner submits as fast as the API server accepts, so the run is saturated by design. The latency percentiles therefore measure a workload's position in the drain queue, not per-workload service time: admission P95 is approximately `0.95 × N / throughput`. The latency bounds in the range spec are loose sanity limits rather than independent signals; throughput is the guard that binds.

## Baseline scenario

120 workloads, 3 worker clusters, 20 concurrent creators, 1m CPU per workload, all-at-once dispatcher (the production default). Committed at `test/performance/multikueue/configs/baseline.yaml`.

Measured on a 32-core host, five consecutive runs:

| Metric | Value |
| --- | --- |
| Throughput | 1.289 – 1.335 workloads/s (~3.6% spread) |
| Quota reservation P95 | 73 – 112 ms |
| Admission P95 | 88.0 – 91.2 s |
| Run wall time | ~95 s |

## What bounds the measurement

This needs explicit treatment, because it determines what the benchmark can detect, and the intuitive answer turns out to be wrong.

Two client-side rate limits bound the run. The manager's own client uses a single shared token bucket configured by `clientConnection`, defaulting to 300 QPS and burst 500; `cmd/kueue/main.go` installs that limiter explicitly, because otherwise controller-runtime would give each API type its own. MultiKueue's worker-cluster clients get no such treatment: `clustersReconciler` builds one controller-runtime client per worker from a kubeconfig Secret or a ClusterProfile, and that `rest.Config` carries no QPS, burst, or shared `RateLimiter`. Since controller-runtime lazily creates an underlying REST client per GVK, each of those falls back to client-go's default of 5 QPS and burst 10. So the remote side is not one 5 QPS budget per worker — it is 5 QPS per worker per Kind.

My first instinct was to lift the remote limit so the benchmark would measure MultiKueue's processing capacity instead of a throttle. Measuring it shows that this does not happen. The rows below were taken at 120, 1000 and 500 workloads respectively, each sized to give that regime a long enough run to reach steady state; once a limiter is saturated throughput barely moves with the workload count, which the first regime shows directly at 1.30/s for 1000 workloads against 1.31/s for 120:

| Remote QPS per REST client | Manager QPS | Throughput | What binds |
| --- | --- | --- | --- |
| 5 (client-go default) | 300 (Kueue default) | 1.31 /s | the remote limiter |
| 300 | 300 (Kueue default) | 38.0 /s | the manager's shared limiter |
| 300 | 3000 | 95.3 /s | neither limiter |

Raising the remote limit moves the constraint onto the manager's own limiter rather than removing it. The middle row is not a processing-capacity measurement; it is 300 QPS divided by the roughly 7.9 requests each Workload makes against the manager's shared bucket. Both regimes count requests per Workload against a fixed token rate, and differ only in which request count they respond to. Since the remote regime needs no production code and is what a deployed Kueue actually runs, the baseline measures there.

Two arithmetic cross-checks, both consistent with tracing the dispatch path by hand: at 300 manager QPS and 38.0 workloads/s a Workload spends about 7.9 tokens on the manager's shared bucket; at 5 remote QPS and 1.31 workloads/s it spends about 3.8 tokens on the busiest remote Kind. Neither number counts all requests — the first excludes remote traffic, the second covers one Kind of it — so I would not quote either as "requests per Workload".

Because the remote limiter releases tokens at a fixed rate whatever the host is doing, the baseline is less host-dependent than a processing measurement would be. That is what lets the throughput floor be set tightly: at 3.8 tokens per Workload, one added remote request on the busiest Kind would take throughput from ~1.31 to ~1.04, so the committed floor is 1.10 — about 15% below the slowest observed run, and deliberately tight, since a generous floor would detect nothing.

What this baseline cannot see is a regression that leaves the busiest remote Kind's request count unchanged: CPU work, lock contention, or extra traffic to some other Kind.

Nothing here asserts anything about the garbage collection or worker-loss paths either. Worker-loss detection cannot trigger, since its timeout is 15 minutes. The garbage collector does run, though: its interval is one minute against a drain of about 95 seconds, so it fires once inside the measured window, listing Workloads on each worker and reading the local copy of each one it finds. Against the run's token budget that is a small cost, but it is not zero, and where it lands relative to the run's progress varies, so it contributes to the run-to-run spread. I left it enabled because a deployed manager runs it.

## Reconcile concurrency

One thing I had to fix, worth flagging because it is easy to get wrong in any harness. controller-runtime resolves each controller's concurrency from the manager's `GroupKindConcurrency` map and otherwise runs a single reconcile at a time. The benchmark did not set that map, so the MultiKueue workload reconciler was running single-threaded, against `Workload.kueue.x-k8s.io: 10` in the MultiKueue e2e configuration and in the documented MultiKueue setup. The runner now matches the e2e configuration.

At the committed baseline this does not move the number, because the remote limiter binds either way. It matters for fidelity, and it matters for anything measured with the limiter lifted: at 300 remote QPS, going from one to ten took throughput from 24.8/s to 38.0/s. `workloadConcurrency` is recorded in the summary and matched exactly by the checker so it cannot drift silently.

## Regression detection

`make test-performance-multikueue` runs the benchmark and then a checker that compares the summary against a committed range spec. The checker matches every scenario field exactly — worker count, dispatcher, reconcile concurrency, GC interval, worker-lost timeout, events batch period, and both local and remote client rate limits — and only then applies the throughput floor and latency ceilings. A run whose configuration differs from the range spec fails rather than being silently compared, because these numbers are only comparable at identical settings.

The checker imports the runner's own result schema, so the two cannot drift apart and a renamed field fails the decode instead of quietly reading zero.

## Watch handling

The measurement depends on a Workload watch, and an API server terminates a watcher it cannot deliver events to. The loop receiving events therefore does nothing but timestamp them and hand them to a buffer; taking the timestamp any later would charge the runner's own queuing to MultiKueue. Before that change, roughly one run in three died with a lost watch.

If the watch still ends early, the runner resumes it from the last resource version it saw and counts the gap in `watchGaps`. A resumed watch replays what it missed, but those transitions are then timestamped on arrival, so a run with gaps reports latencies inflated by up to the length of the gaps — which is why the count is reported rather than swallowed. The range spec tolerates one gap, since the inflation lands in bounds it already checks, and fails beyond that. A watch error ends the run instead: it usually means the resource version has expired, which no retry recovers. No gap occurred in any of the five calibration runs.

## Alternatives considered

- **kind clusters.** Closest to production and would exercise real kubelets, but the issue already anticipates host saturation at three clusters, and pod scheduling noise would swamp the dispatch signal.
- **Reusing `test/performance/scheduler`.** Its generator and recorder are built around a single cluster and ClusterQueue classes. Sharing them would mean generalising both for one caller; a separate runner in the same shape is simpler. The regression-check structure and the Make target layout do follow the scheduler benchmark.
- **Lifting the remote rate limit to measure processing capacity.** Implemented, measured, and then dropped, for the reason in *What bounds the measurement*: it does not measure processing capacity, and it cost a `SetupOption` in `pkg/controller/admissionchecks/multikueue` that no production caller used. The benchmark now changes no production code.
- **Failing the run on a lost watch instead of resuming.** That was the earlier behaviour. Resuming with the gap counted keeps the run useful while still making a disturbed measurement visible.

## Open questions

1. **Resource usage is not measured, and the current structure is why.** All four controller managers run in the benchmark process, so a process profile cannot attribute cost to the manager versus an individual worker. A regression that doubles CPU per Workload while throughput stays flat would be invisible. The scheduler benchmark avoids this by running Kueue as a separate `minimalkueue` process. If that matters for this gate, it is worth doing before the job is calibrated rather than after.
2. **Baseline size.** 120 workloads at ~1.31/s is a 95-second run, ~150 seconds for the whole target. Happy to trade that down if CI budget is the binding constraint.
3. **The periodic job lives in `kubernetes/test-infra`, not here.** I would land this non-alerting first and recalibrate the committed thresholds from at least five runs on the actual CI worker before enabling alerting.
4. **`verify-test-performance-multikueue-runner` is currently in `verify-checks`**, which is the only reason the runner's unit tests execute in CI at all before the periodic exists. That is asymmetric with the scheduler runner, whose tests are not in CI. It could be generalised to `./test/performance/...`, but the scheduler's `TestScalability` calls `t.Fatal` rather than skipping when its flags are absent, so that needs a small fix first. Happy to do either.

## Rollout

1. Land the runner and the regression-check target, non-alerting.
2. Add a dedicated periodic in `kubernetes/test-infra` that invokes `make test-performance-multikueue` and publishes `ARTIFACTS`.
3. Recalibrate the committed ranges from at least five runs on that worker.
4. Enable TestGrid alerting once variance is shown to be stable.
5. Follow-ups: worker disconnect/reconnect scenarios, dispatcher-specific scenarios (only all-at-once is covered), and worker-side job framework reconcilers for a fuller load picture.

</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2026-09-07T12:31:28Z

This is also related to https://github.com/kubernetes-sigs/kueue/pull/15206

### Comment by [@kvnloo](https://github.com/kvnloo) — 2026-09-20T17:35:20Z

AI-assisted: I used an AI assistant to help inspect the related performance work and organize this measurement question; I reviewed the thread and numbers myself.

The rate-limit finding makes me wonder whether this benchmark would benefit from two modes rather than a single admitted-workloads/sec number.

With the current production-like defaults, the result is valuable operationally, but if throughput is bounded by the worker client-go 5 QPS limit (and then by the manager clientConnection limit), changes in MultiKueue's own processing cost could be masked below that ceiling.

Would it make sense to keep:

1. a **production-default mode**, preserving the real rate limits and catching end-to-end regressions operators would experience; and
2. a **high-budget diagnostic mode**, raising the API budgets enough that the bottleneck moves into MultiKueue itself?

Then a change could be classified more clearly:

* default throughput regressed, diagnostic throughput unchanged → likely API-budget/request-amplification change;
* both regress → likely controller/dispatch processing regression;
* diagnostic regresses while default is flat → internal regression currently hidden by the production limiter.

It may also be useful to record workload admission latency / queue-drain time in addition to average throughput, especially for burst workloads. That would line up naturally with the admission-latency / dispatch-round observability being discussed in #11132.

If this distinction is useful, I'd be happy to help with the smallest benchmark/config change rather than changing the existing benchmark design wholesale.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-09-21T10:12:28Z

> With the current production-like defaults, the result is valuable operationally, but if throughput is bounded by the worker client-go 5 QPS limit (and then by the manager clientConnection limit), changes in MultiKueue's own processing cost could be masked below that ceiling.

@kvnloo we recently bumped the QPS  for MultiKueue client re-using the same configuration as for the core Kueue: https://github.com/kubernetes-sigs/kueue/pull/15280

I hope with this change "production-default mode, = high-budget diagnostic mode". 

@YQ-Wang is there anything more here that you have on your ToDo list?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-09-21T10:14:23Z

If nothing more in ToDo then I think we can close the issue, and open dedicated issues. I will open one for the flakes here: https://testgrid.k8s.io/sig-scheduling#periodic-kueue-test-multikueue-perf-main

Opened: https://github.com/kubernetes-sigs/kueue/issues/15891
