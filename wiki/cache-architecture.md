# Cache Architecture

**Summary**: Kueue's in-memory cache stores the live state of ClusterQueues, Cohorts, and admitted workloads; the scheduler takes an immutable per-cycle snapshot of this cache to make admission decisions without holding locks.

**Sources**: `raw/kueue/pkg/cache/scheduler/`, `raw/kueue/pkg/cache/hierarchy/`, `raw/kueue/pkg/cache/queue/`

**Last updated**: 2026-04-28

---

## Overview

Kueue has two distinct caches:

| Cache | Package | Purpose |
|---|---|---|
| **Scheduler cache** | `pkg/cache/scheduler` | Tracks admitted workloads and quota usage per ClusterQueue/Cohort |
| **Queue manager** | `pkg/cache/queue` | Tracks pending workloads and their queue assignments |

Both are in-memory; they are populated by controller-runtime informers watching Kubernetes objects and kept consistent through reconcile events. (source: pkg/cache/scheduler/)

## Scheduler cache

The `Cache` struct (in `pkg/cache/scheduler`) maintains the current "admitted" state:
- Per-ClusterQueue: nominal quota, usage (reserved + admitted), flavor assignments, admission check states.
- Per-Cohort: aggregated usage across member ClusterQueues, borrowable capacity.

### Snapshot

At the start of each scheduling cycle, the scheduler calls `cache.Snapshot()` to get an immutable copy:

```go
snapshot, err := s.cache.Snapshot(ctx, snapshotOpts...)
```

The snapshot contains `ClusterQueueSnapshot` and `CohortSnapshot` objects — deep copies of the live cache state at a point in time. All flavor assignment and quota arithmetic during the cycle operates on the snapshot, not the live cache. This means:
- No locks needed during scheduling.
- Quota updates between two cycles are picked up in the next cycle's snapshot.
- The snapshot can diverge from etcd for one cycle, which is intentional.

(source: pkg/cache/scheduler/)

### Hierarchy manager

The `pkg/cache/hierarchy` package provides a generic `Manager[CQ, C]` type that models the ClusterQueue ↔ Cohort tree. It is used by both the scheduler cache and the admission check logic. Key types:

- `ClusterQueue[C]`: a ClusterQueue node; knows its parent Cohort (if any).
- `Cohort[CQ, C]`: a Cohort node; references its member ClusterQueues and parent Cohort (for hierarchical cohorts).
- `Manager[CQ, C]`: owns the map of all nodes; enforces parent-child invariants; detects cycles in the hierarchy.

(source: pkg/cache/hierarchy/)

### Cycle detection

When a Cohort's parent is set or changed, the hierarchy manager checks for cycles (a Cohort being its own ancestor). A cycle is a fatal configuration error and is rejected. (source: pkg/cache/hierarchy/)

## Queue manager

The queue manager (`pkg/cache/queue`) is the pending queue:
- Holds all workloads that are not yet admitted.
- Provides `Heads()` — one workload per ClusterQueue, the highest-priority pending workload.
- Tracks inadmissible workloads separately (workloads that failed nomination); they are re-evaluated when a relevant change occurs (quota freed, flavor added).
- Implements the requeueing reasons (`PendingPreemption`, `Inadmissible`, `PreemptionGated`) that determine whether a workload re-enters the active queue immediately or after a delay.

(source: pkg/cache/queue/)

## Consistency with etcd

Both caches are populated from controller-runtime informer caches, not direct API calls. The flow:

1. An object (Workload, ClusterQueue, etc.) is created/updated/deleted in etcd.
2. The API server notifies the informer.
3. The informer triggers a reconcile event on the relevant controller.
4. The controller updates the in-memory cache.

There is a brief window where the in-memory cache lags behind etcd. For quota accounting, this means Kueue may transiently over-admit by one workload if two admission cycles fire in rapid succession before a quota-consuming write is reconciled. This is mitigated by the expectations store (used by preemption) which tracks in-flight changes. (source: pkg/scheduler/scheduler.go)

## Snapshot vs. live cache divergence

The scheduler only reads the snapshot. After a workload is admitted (`s.admit()` call), the admission is written to the live cache via `cq.AddUsage(usage)` on the snapshot — but this is a local mutation. The live cache is updated when the Workload controller processes the newly admitted workload and reconciles it back. (source: pkg/scheduler/scheduler.go)

## Debugging cache state

The `pkg/debugger` package can dump the in-memory cache state. This is exposed via the Kueue manager's debug HTTP endpoint when enabled. Useful for diagnosing why the scheduler's view of quota doesn't match what you see in `kubectl get clusterqueue -o yaml`. (source: pkg/scheduler/scheduler.go)

## Related pages

- [[scheduler-internals]]
- [[cluster-queue]]
- [[cohort]]
- [[admission]]
- [[workload]]
- [[performance-and-scale]]
