# Scheduler Internals

**Summary**: The Kueue scheduler runs a continuous scheduling cycle that snapshots the cluster state, assigns resource flavors to pending workloads, and admits or preempts them according to quota and fair-sharing rules.

**Sources**: `raw/kueue/pkg/scheduler/scheduler.go`, `raw/kueue/pkg/scheduler/flavorassigner/flavorassigner.go`, `raw/kueue/pkg/scheduler/logging.go`

**Last updated**: 2026-04-28

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
8. **WorkloadSlice replacement** — handle elastic job slice replacement.
9. **Admit** — write the `QuotaReservation` and `Admitted` conditions; toggle `.spec.suspend = false` on the job.

(source: pkg/scheduler/scheduler.go)

### Phase 6: Requeue

All entries not `assumed` (successfully admitted) or `evicted` are re-queued with appropriate reasons: `PendingPreemption`, `PreemptionFailed`, `Inadmissible`, `PreemptionGated`. The queue manager uses these reasons to decide delay and ordering. (source: pkg/scheduler/scheduler.go)

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

## Quota tiers

The scheduler evaluates three tiers of capacity in order:

1. **Nominal** — quota the ClusterQueue owns outright; never needs borrowing or preemption.
2. **Borrowing** — unused nominal quota from other ClusterQueues in the same [[cohort]]; requires borrowing.
3. **Preemption** — quota held by lower-priority workloads; requires evicting them.

If a workload can fit in tier 1 → `Fit`. If it needs tier 3 → `Preempt`. If none fit → `NoFit`.

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
