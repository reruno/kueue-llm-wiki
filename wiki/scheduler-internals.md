# Scheduler Internals

**Summary**: The Kueue scheduler runs a continuous scheduling cycle that snapshots the cluster state, assigns resource flavors to pending workloads, and admits or preempts them according to quota and fair-sharing rules.

**Sources**: `raw/kueue/pkg/scheduler/scheduler.go`, `raw/kueue/pkg/scheduler/flavorassigner/flavorassigner.go`, `raw/kueue/pkg/scheduler/logging.go`

**Last updated**: 2026-06-29

---

## The scheduling cycle

The scheduler runs as a single goroutine via `wait.UntilWithBackoff`. Each call to `schedule()` is one cycle. The cycle number is tracked in `schedulingCycle` for log correlation. (source: pkg/scheduler/scheduler.go)

### Phase 1: Get heads

```go
headWorkloads := s.queues.Heads(ctx)  // blocks while queue is empty
```

`Heads()` returns one workload per ClusterQueue — the highest-priority workload at the front of each queue. If any ClusterQueue has borrowing candidates, those are also included as additional heads. (source: pkg/scheduler/scheduler.go)

### Phase 2: Snapshot

```go
snapshot, err := s.cache.Snapshot(ctx, snapshotOpts...)
```

An immutable snapshot of all ClusterQueue/Cohort usage and quotas is taken. The scheduler works entirely against this snapshot — it does not re-read from the live cache during a cycle. If [[admission-fair-sharing]] is enabled, AFS penalties and consumed-resource data are injected into the snapshot here. (source: pkg/scheduler/scheduler.go)

`Snapshot()` runs under the cache's **read lock** and must not mutate cache state. A TAS ClusterQueue whose TAS usage is not yet synced is therefore *skipped* rather than synced inline — see [[cache-architecture#Snapshot is strictly read-only]] ([[pr-11286]]). (source: pkg/scheduler/scheduler.go)

### Phase 3: Nominate

```go
entries, inadmissibleEntries := s.nominate(ctx, headWorkloads, snapshot)
```

For each head workload, the FlavorAssigner runs (see below). Workloads that cannot fit (NoFit) are immediately moved to `inadmissibleEntries`. Workloads that can fit or preempt become `entries`. (source: pkg/scheduler/scheduler.go)

### Phase 4: Iterator

```go
iterator := makeIterator(ctx, entries, s.workloadOrdering, fairsharing.Enabled(s.fairSharing))
```

The iterator orders `entries` for processing. With [[fair-sharing]] disabled, entries are processed in priority+timestamp order. With fair sharing enabled, a `fairSharingIterator` interleaves ClusterQueues by weighted DRS share, so no single CQ monopolizes the cycle. (source: pkg/scheduler/scheduler.go)

### Phase 5: processEntry (per workload)

For each entry the iterator yields, `processEntry` runs the admission pipeline:

1. **TAS unhealthy node check** — if topology assignment requires a failing node and mode is not Fit, the workload is evicted.
2. **NoFit** — skip immediately.
3. **Preemption gate** — if mode is Preempt and the workload has a closed preemption gate (MultiKueueOrchestratedPreemption), mark `preemptionGated` and return.
4. **Overlapping targets** — if this cycle already issued preemptions that overlap with this workload's targets, mark `skipped`.
5. **Fits check** — verify the snapshot still accommodates this workload (earlier admissions in this cycle may have consumed quota).
6. **Issue preemptions** (Preempt mode) — send delete requests to preemption targets; mark entry as pending.
7. **WaitForPodsReady** — block admission if the previous workload cycle left pods not ready.
8. **Admit** — write the `QuotaReservation` and `Admitted` conditions; toggle `.spec.suspend = false` on the job. Admission is **asynchronous** (`admissionRoutineWrapper.Run()` launches a goroutine; `admit` returns `nil` before `PatchAdmissionStatus` completes).
9. **WorkloadSlice replacement** — for elastic jobs, finish the *old* slice. As of [[pr-11195]] (fixes #9015) this happens **inside `admit`'s success path**, after `PatchAdmissionStatus` succeeds — i.e. the old slice is finished only once the new (larger) slice is confirmed admitted. Doing it before admission could leave the old slice `Finished` while the new one failed to admit, leaking quota (the job keeps running unsuspended with no admitted slice holding quota). `admit` now takes the `oldWorkloadSlice *preemption.Target`; `replaceOldWorkloadSlice` is fire-and-forget (logs on failure). See [[elastic-jobs]].

(source: pkg/scheduler/scheduler.go)

### Phase 6: Requeue

All entries not `assumed` (successfully admitted) or `evicted` are re-queued with appropriate reasons: `PendingPreemption`, `PreemptionFailed`, `Inadmissible`, `PreemptionGated`. The queue manager uses these reasons to decide delay and ordering.

**Scheduling-equivalence bulk requeue.** When the `SchedulingEquivalenceHashing` gate is on (**Beta, default on, since v0.18** — [[pr-11097]]), a Workload requeued to the inadmissible set carries its other scheduling-equivalent Workloads (same `SchedulingHash`) with it, so they aren't re-evaluated one-by-one. v0.18 **narrows** this to two requeue reasons only — `RequeueReasonNoFit` and `RequeueReasonPreemptionNoCandidates`. The earlier broad `!immediate` condition also bulk-moved `NamespaceMismatch` and `PreemptionGated` Workloads, which was wrong: it cross-contaminated namespace-mismatched Workloads and broke MultiKueue per-item processing ([[issue-10005]]). Side effect: a single Workload that needs ~100% of a CQ's quota now waits for the requeue batch (≈1s) or a capacity event, so its time-to-admission regresses. (source: pkg/scheduler/scheduler.go)

### Inadmissible-workload requeue guard

`Manager.RequeueWorkload` is called from many places (eviction, condition flips, finished-cleanup). It must refuse to enqueue Workloads that have already become inadmissible — specifically, anything where `workload.IsAdmissible(&w)` is false (e.g. `Finished=True`, deactivated, owner gone). Without this guard, a Workload that is concurrently marked Finished can be re-added to the queue and then keep winning the fair-sharing tournament in subsequent cycles, blocking other Workloads from making progress (the scheduler skips it once it sees the Finished condition, but the head-slot is consumed). [[pr-11014]] tightens `RequeueWorkload` to drop inadmissible Workloads. Part of [[issue-10901]].

The same issue motivated the [[failure-recovery]]-related FG **`FinishOrphanedWorkloads`** to be downgraded to Alpha in [[pr-11010]] (release note: "Fix the bug that Kueue may mark workloads as finished immediately after their creation, which could result in blocking the queues by such a workload"). The root cause is that `workload_controller` queries owners via `PartialObjectMetadata`, which has its own informer separate from the structured per-kind informer used by the JobReconciler — the JobReconciler can already see the JobSet and create the Workload before the metadata informer has caught up, so the workload controller sees an absent owner and finishes the Workload as orphaned. The structural fix landed in [[pr-11296]] (`ReconcileGenericJob` only *finishes* an orphaned Workload under the proper conditions instead of finishing it right after owner creation), and the gate was re-graduated to **Beta, default-on at v0.18** as part of the same PR. See [[workload-garbage-collection]] and [[feature-gates]].

### Admitted workloads must leave `preemptionExpectations`

When the scheduler issues preemptions for a workload, it records the targets in an in-memory `preemptionExpectations` map and refuses to re-issue the same preemption until it has *observed* the eviction (this is what produces the "Preemption already issued, waiting for observation" head-of-line behaviour). Because admission is asynchronous (Phase 8), a subtle race existed ([[issue-11480]], fixed by [[pr-11502]] on main; manual cherry-picks [[pr-11648]]/0.17, [[pr-11647]]/0.16): the admission patch for a lower-priority workload `wl1` is written with Server-Side Apply and **omits** the `Evicted` condition, so a lagging admission goroutine from an earlier cycle could overwrite a concurrent eviction of `wl1` triggered by a higher-priority `wl2`. The consequences were severe and observed in production:

- **Stuck preemption / head-of-line blocking** — `wl1` keeps its quota reservation, `wl2`'s eviction is never observed in `preemptionExpectations`, so `wl2` waits indefinitely and the ClusterQueue stops admitting entirely.
- **Quota oversubscription** — alternatively, the goroutine admits an already-evicted workload with no quota check.

The fix guarantees that once a workload is Admitted it is removed from `preemptionExpectations` (a new `scheduler.WithPreemptionExpectations(...)` option wires this and is now required by the inadmissible integration suite). See [[preemption]].

## FlavorAssigner

The `flavorassigner.FlavorAssigner` runs during Phase 3. For each [[workload]]'s PodSets, it evaluates ResourceGroups in the [[cluster-queue]] and assigns a [[resource-flavor]] to each resource.

### Assignment modes

| Mode | Meaning |
|---|---|
| `Fit` | Workload fits within nominal quota (no borrowing, no preemption needed) |
| `Preempt` | Workload can fit if some lower-priority workloads are preempted |
| `NoFit` | Workload cannot fit regardless |

The "representative mode" across all PodSets determines the entry's overall mode. (source: pkg/scheduler/flavorassigner/flavorassigner.go)

### Flavor scoring

Within a ResourceGroup, flavors are tried in order. The assigner scores each flavor:
- Prefer flavors that don't require borrowing.
- Prefer flavors that don't require preemption.
- Within a tie, follow the order defined in the ClusterQueue's `resourceGroups[*].flavors` list.

The `FlavorFungibility` field (`whenCanPreempt`, `whenCanBorrow`) controls how aggressively the assigner searches beyond the first candidate. (source: pkg/scheduler/flavorassigner/flavorassigner.go)

### Second-pass seeding (multi-resource workloads)

`assignFlavors` runs in two passes for workloads that already hold a partial reservation: the first pass picks flavors from scratch; the second pass seeds the result with whatever the workload had previously reserved (used by ProvisioningRequests and TAS NodeHotSwap re-admission). The seed loop must copy **every** preexisting flavor for each PodSet — copying only the first one (the original behaviour) leaves the remaining resources unassigned, and they fall through to `fitsResourceQuota`, which double-counts the workload's own first-pass reservation. The result was that a multi-resource workload (e.g. CPU + memory) could fail second-pass admission for a resource it had already correctly reserved. Fixed in [[pr-11005]] (Fixes #9048); the TAS scheduler test harness was updated to seed reserved-but-not-admitted workloads into `cqCache` so the regression is observable in unit tests. See [[topology-aware-scheduling#Multi-resource second-pass double-counting]].

## Quota tiers

The scheduler evaluates three tiers of capacity in order:

1. **Nominal** — quota the ClusterQueue owns outright; never needs borrowing or preemption.
2. **Borrowing** — unused nominal quota from other ClusterQueues in the same [[cohort]]; requires borrowing.
3. **Preemption** — quota held by lower-priority workloads; requires evicting them.

If a workload can fit in tier 1 → `Fit`. If it needs tier 3 → `Preempt`. If none fit → `NoFit`.

## Quota arithmetic and integer-overflow safety

Quota arithmetic is done in `int64` (milli-units for CPU, absolute units otherwise). Several v0.18 fixes hardened this against wraparound, which was a real **quota-limit bypass**: when a sum or product overflowed `int64` it wrapped *negative*, and a negative value silently passes the "fits within quota" comparison, so an over-large Workload got admitted.

- **`flavorassigner.fitsResourceQuota`** ([[pr-11137]]): `assumedUsage + requestUsage` could overflow when two PodSets' combined requests exceed `MaxInt64`; replaced with an overflow-checked add (extracted to a `pkg/util` helper).
- **`resources.ResourceValue`** ([[pr-11139]]): converting a near-`MaxInt64` CPU quantity to milliCPU multiplies by 1000 and overflowed; now **clamps/saturates** to `math.MaxInt64`/`MinInt64` via `SafeMilliValue` (`pkg/util/math/math.go`).
- **`TotalRequests`** ([[pr-11182]]): per-pod-request × pod-count overflowed for a Workload with many pods; now uses a saturating multiply `SaturatingMul(a, b int64) int64` (overflow detected via `res/b != a`, returns `MaxInt64`/`MinInt64` by sign).

The strategic consolidation is the **`resources.Amount`** quota type ([[pr-11156]], fixes #9843) — quota *storage* now flows through one saturating type with an `Unlimited` sentinel, so per-site clamps become a type-enforced invariant. Note `ResourceValue` (the workload-*request* path) deliberately keeps legacy truncate-on-overflow behaviour; only the quota side migrated to `Amount`. See [[cache-architecture#Quota amount type and overflow safety]].

## Fair-sharing iterator

When fair sharing is enabled, the iterator uses DRS (Dominant Resource Share) to order ClusterQueues. The queue with the lowest share (least over its nominal quota) gets to admit next. This prevents any single ClusterQueue from monopolizing borrowable capacity across a cycle. See [[fair-sharing]] for the DRF algorithm details.

## Speed signal

The `schedule()` function returns `KeepGoing` if at least one workload was admitted, and `SlowDown` otherwise. The `wait.UntilWithBackoff` caller uses this to add a brief pause when no progress was made, reducing wasted CPU cycles. (source: pkg/scheduler/scheduler.go)

## What triggers a new cycle

- A new workload enters the queue.
- A workload is evicted or preempted (freeing quota).
- A ClusterQueue's `nominalQuota` or `borrowingLimit` is updated.
- A ResourceFlavor is created/deleted.
- A cohort membership changes.
- A WaitForPodsReady timeout fires.

## Related pages

- [[admission]]
- [[cluster-queue]]
- [[resource-flavor]]
- [[cohort]]
- [[preemption]]
- [[fair-sharing]]
- [[admission-fair-sharing]]
- [[topology-aware-scheduling]]
- [[cache-architecture]]
- [[workload]]
- [[concurrent-admission]] — Variant Workloads racing in the same scheduling cycle.
- [[debugging-guide]] — translating scheduler decisions into operator-visible symptoms.
