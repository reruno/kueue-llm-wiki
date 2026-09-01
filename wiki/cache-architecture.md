# Cache Architecture

**Summary**: Kueue's in-memory cache stores the live state of ClusterQueues, Cohorts, and admitted workloads; the scheduler takes an immutable per-cycle snapshot of this cache to make admission decisions without holding locks.

**Sources**: `raw/kueue/pkg/cache/scheduler/`, `raw/kueue/pkg/cache/hierarchy/`, `raw/kueue/pkg/cache/queue/`

**Last updated**: 2026-09-01

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

### Snapshot is strictly read-only

`Snapshot()` is taken while holding only the cache **read lock**, so it must never mutate cache state. [[pr-11286]] (cherry-picked to release-0.16 / release-0.17) made this contract explicit after a TAS bug: the snapshot path used to call the *mutating* `ensureTASIsSynced()` while holding the read lock. The fix removes that call from the read path; the per-ClusterQueue TAS usage sync is now the exclusive responsibility of the **write-lock** paths (`Cache.AddOrUpdateTopology` / `AddOrUpdateResourceFlavor` → `updateClusterQueues` → `cq.UpdateWithFlavors` → `updateQueueStatus` → `ensureTASIsSynced`).

A ClusterQueue that cannot be scheduled this cycle is *skipped* via a `skipInactiveCQReason()` helper that returns one of:

- `inactiveCQReasonNotActive` — CQ is not Active.
- `inactiveCQReasonHasCycle` — CQ's cohort hierarchy contains a cycle.
- `inactiveCQReasonTASUsageNotSynced` — **new**; returned when `features.Enabled(features.TopologyAwareScheduling) && len(cq.tasFlavors) > 0 && !cq.isTASSynced`.

Edge case: under [[multikueue]] the `Topology` object is created on the *management* cluster, so on a worker `isTASSynced` could otherwise stay false and silently exclude the CQ.

### Hierarchy manager

The `pkg/cache/hierarchy` package provides a generic `Manager[CQ, C]` type that models the ClusterQueue ↔ Cohort tree. It is used by both the scheduler cache and the admission check logic. Key types:

- `ClusterQueue[C]`: a ClusterQueue node; knows its parent Cohort (if any).
- `Cohort[CQ, C]`: a Cohort node; references its member ClusterQueues and parent Cohort (for hierarchical cohorts).
- `Manager[CQ, C]`: owns the map of all nodes; enforces parent-child invariants; detects cycles in the hierarchy.

(source: pkg/cache/hierarchy/)

### Cycle detection

When a Cohort's parent is set or changed, the hierarchy manager checks for cycles (a Cohort being its own ancestor). A cycle is a fatal configuration error and is rejected. (source: pkg/cache/hierarchy/)

**Ordering invariant, currently violated.** A ClusterQueue is registered in the hierarchy manager (`hm.AddClusterQueue`) *before* its scheduler-cache state is fully populated, so a `updateClusterQueue` that fails part-way leaves a cached CQ with a **nil `NamespaceSelector`**. `MatchingClusterQueues` dereferences it on the next Namespace event and the manager **panics**. Two paths reach that state: `updateCohortTreeResources` returning `ErrCohortHasCycle` before the selector is assigned, and `LabelSelectorAsSelector` failing on an unparsable selector (after `AddClusterQueue` has already run). Open bug #13553 (source: pr-13571.md, open). Anyone adding a fallible step to `updateClusterQueue` should assign the selector before it, or default it to `labels.Nothing()`.

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

## Quota amount type and overflow safety

Quota quantities stored in the scheduler cache are wrapped in **`resources.Amount`** (`pkg/resources/amount.go`, introduced by [[pr-11156]], fixes #9843) rather than raw `int64`. The shipped representation is `type Amount struct { value int64 }` with a sentinel `var Unlimited = Amount{value: math.MaxInt64}` for effectively-infinite quota; bounded amounts must never equal `math.MaxInt64`.

Why it exists: a CPU quota like `1E` whose milliCPU exceeds `int64` used to **collapse to 0** (making a CQ look like it had zero quota), and cohort aggregation of huge sibling quotas could wrap **negative**. `AmountFromQuantity(name, q)` instead returns `Unlimited` at/over the boundary (`maxCPUQuantityForAmount = MaxInt64/1000` for CPU, `maxNonCPUQuantityForAmount = MaxInt64` otherwise). `Add`/`Sub` propagate `Unlimited` and **saturate** bounded overflow (delegating to the `pkg/util/math` saturating helpers); `Cmp` treats `Unlimited` as greater than any bounded amount.

- **Where it's stored**: `ResourceQuota` (`pkg/cache/scheduler/resource.go`) changed `Nominal`, `BorrowingLimit`, `LendingLimit` from `int64`/`*int64` to `Amount`/`*Amount`; the `SubtreeQuota` and `Usage` maps (`FlavorResourceQuantities`) hold `Amount`. Cohort math in `resource_node.go` (`available`, `potentialAvailable`, `accumulateFromChild`, `addUsage`, `removeUsage`) is rewritten over `Amount` methods.
- **Equality gotcha**: `Amount` has an unexported field, so Kubernetes' `equality.Semantic.DeepEqual` (a forked `reflect`) **panics** on it. The fix adds a `ResourceQuota.Equal` method (+`equalAmountPtr`) and `updateQuotasAndResourceGroups` uses `maps.EqualFunc(..., ResourceQuota.Equal)` instead of `DeepEqual`. Anyone adding a struct with unexported fields into cached types must supply an `Equal` method for the same reason.

See [[scheduler-internals#Quota arithmetic and integer-overflow safety]] for the workload-request-side overflow fixes that preceded this refactor.

## Workload usage can reach the `Unlimited` sentinel

The invariant in `amount.go` — *bounded amounts must never equal `math.MaxInt64`* — is enforced on the **quota** boundary only (`AmountFromQuantity`). The **usage** boundary is unguarded, so the sentinel is reachable from a workload's own requests (source: issue-14105.md, open bug, measured at `cead7dee`):

- `totalRequestsFromPodSets` ends with a **saturating** `Requests.Mul(int64(count))`, so e.g. 4 pods × 2⁶² of a countable resource saturates to exactly `9223372036854775807`. Neither factor is past `int64` on its own.
- `Info.ResourceUsage` folds that into the tree with `ru.Assigned[fr] = ru.Assigned[fr].AddInt64(q)`. `AddInt64` also saturates, so the result is a *bounded* usage that nothing downstream can distinguish from `Unlimited`.

`Amount` arithmetic is then **asymmetric**, and this is the damaging part: `AddInt64` returns early on an unlimited receiver (later workloads' usage is silently not counted), while `Sub` still subtracts. Measured through the cache with one saturating Workload plus one ordinary 7-unit Workload, usage went `MaxInt64` → `MaxInt64` (the 7 swallowed) → `0` (saturating workload removed) → **`-7`**. The ClusterQueue is left believing 7 units *fewer* are in use than ever were, i.e. with more available capacity than it has, until the process restarts and the cache is rebuilt.

It is not a permanent wedge — `Sub` answers bounded zero when both sides are unlimited, so the saturating Workload's own removal clears the sentinel; what survives is the drift left by the swallowed additions. Whether the scheduler would *admit* such a Workload in band is unestablished; the reproduction hands an already-admitted Workload to the cache, which is the path `AddOrUpdateWorkload` takes on resync without rechecking quota. See [[workload-resource-adjustment]].

## Debugging cache state

The `pkg/debugger` package can dump the in-memory cache state. This is exposed via the Kueue manager's debug HTTP endpoint when enabled. Useful for diagnosing why the scheduler's view of quota doesn't match what you see in `kubectl get clusterqueue -o yaml`. (source: pkg/scheduler/scheduler.go)

## Cached TAS topology trees

With `TASCacheTopologyTree` (Beta/on from v0.20) the cache holds an **immutable topology tree per TAS flavor** and hands it to successive scheduler snapshots instead of rebuilding it each cycle. Mutable scheduling state stays in the snapshot, so concurrently created snapshots remain isolated; invalidation is driven by semantic node changes only (labels, taints, allocatable). Measured −71.7% CPU and −61.0% allocated bytes on a 2,500-node / 15-flavor benchmark. See [[topology-aware-scheduling#Cached topology trees]] ([[pr-13819]]).

## `RequeueWorkload` owns the inflight cleanup

Inflight bookkeeping is cleared **inside `Manager.RequeueWorkload`, before `info.Update` clears the source ClusterQueue** ([[pr-13885]]). Doing it there rather than at the call sites also fixes the `requeueAndUpdate` path and LocalQueue retargeting, where the previous ClusterQueue kept counting a moved Workload as pending. See [[scheduler-internals#Popped heads must survive a snapshot failure]].

## Related pages

- [[scheduler-internals]]
- [[cluster-queue]]
- [[cohort]]
- [[admission]]
- [[workload]]
- [[performance-and-scale]]
