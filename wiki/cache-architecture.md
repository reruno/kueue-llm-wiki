# Cache Architecture

**Summary**: Kueue's in-memory cache stores the live state of ClusterQueues, Cohorts, and admitted workloads; the scheduler takes an immutable per-cycle snapshot of this cache to make admission decisions without holding locks.

**Sources**: `raw/kueue/pkg/cache/scheduler/`, `raw/kueue/pkg/cache/hierarchy/`, `raw/kueue/pkg/cache/queue/`, pr-16375.md, pr-16438.md, pr-16360.md, pr-16479.md, pr-16492.md, pr-16527.md, pr-16738.md, pr-15040.md, pr-15107.md, pr-16382.md

**Last updated**: 2026-10-21

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

When a Cohort's parent is set or changed, the hierarchy manager checks for cycles (a Cohort being its own ancestor). (source: pkg/cache/hierarchy/)

**Correction (2026-10-21)**: a cycle is *not* rejected. The cache applies the new parent and returns `ErrCohortHasCycle`; ClusterQueues under the cycle go `Active=False` with reason `CohortCycleDetected`, their usage is updated on their own node only (the recursive ancestor walk would not terminate), and ancestor usage is rebuilt once the cycle is resolved (#13774, backports pr-16375/pr-16376). Since pr-16438 the Cohort reconciler also records the cyclic parent in the **queue manager**, which tolerates cycles, so the two hierarchies stay identical when another Cohort later resolves the cycle. See [[cohort#Cycles in the Cohort hierarchy]] (source: pr-16375.md, pr-16438.md, raw/kueue/pkg/cache/scheduler/cache.go).

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

## Quota amounts are exact past int64 (pr-15026)

Quota quantities in the scheduler cache are `resources.Amount` (`pkg/resources/amount.go`, introduced by pr-11156). The **first** design (`Amount{value int64}` with `Unlimited = MaxInt64` as a sentinel, saturating add/sub) is **gone**. Since pr-15026 (fixes issue-14105; v0.20) `Amount` is an **exact integer**: an `int64` (`small`) while the value fits, otherwise an immutable `*big.Int` (`large`), and back to `int64` when a result returns to range, so equal amounts are always stored the same way. `math.MaxInt64` is now an ordinary amount and nothing manufactures an infinity, so add/remove of usage is reversible at any magnitude (source: pr-15026.md, raw/kueue/pkg/resources/amount.go).

Why it changed: with the sentinel, a workload whose usage reached `MaxInt64` was indistinguishable from "unlimited"; adding it, then a 7-unit workload, then removing the first left usage at `-7` (`Sub(Unlimited, Unlimited)` was defined as bounded zero). The queue then believed 7 units fewer were in use than ever were until a restart (issue-14105.md).

Rules to keep when touching accounting code:

- **`Amount` is uncomparable** (`_ [0]func()`): `==` and use as a map key are compile errors. Use `Equal`/`Cmp`. `resources.Unlimited` and `Amount.Int64()` no longer exist; an amount leaves the package as a `Quantity` via `AmountQuantity` or as text via `String`. Structs with unexported fields in cached types still need an `Equal` method because `equality.Semantic.DeepEqual` panics on them (`ResourceQuota.Equal`).
- The stored `big.Int` never leaves `pkg/resources` and is **never mutated**; that is what makes the shallow map clones in `resourceNode.Clone` and `FlavorResourceQuantities.Clone` safe when snapshots share it with the cache. The `int64` path allocates nothing (measured `UpdateFlavorUsage` -2.9%, `ResourceNodeClone` +19.6% and 1.46 to 1.84 KiB, large fair-share ratio 3 to 17 allocs).
- `AmountFromQuantity` reads the decimal the `Quantity` holds (not `Value()`/`MilliValue()`, which overflow; at the smallest `int64` milli `MilliValue` returns zero). The API boundary applies the resource's scale **before** narrowing: a Quantity holds at most `MaxInt64` in the unit it reports (cores for CPU), so up to `MaxInt64` cores (about 9.2x10^21 milli) are representable and reportable; past that the value is capped with its sign. The same bound applies on the way in, so `8Ei` and `9223372036854775808` are one quota. `10P` of CPU is `10^19` milli, no longer reported as `9223372036854775807m`.
- `updateFlavorUsage` adds/subtracts `Amount`s; `FlavorResourceQuantities.ToResourceList` sums flavors and converts each total once (`FlattenFlavors` was removed); the fair-sharing ratio uses the exact operands.

Behaviour changes operators can observe ([[borrowing-and-lending]], [[metrics]]):

- **Oversized limits.** `1E` nominal with a `10P` `lendingLimit` used to turn both into `Unlimited` (nothing stayed local); now `990P` stays local. A `borrowingLimit` past `int64` used to equal everything the Cohort had spare; now it bounds what the ClusterQueue can reach. An *unset* limit is still unset.
- **Metrics** report `+Inf` for an amount at or past `MaxInt64`, as before; for CPU the threshold moved from `MaxInt64/1000` cores to `MaxInt64` milli (0.807 cores apart).
- **Fair sharing** is otherwise unchanged: a share that underflows to zero still reads as within quota, and `weightedShare` still goes through `int64(math.Ceil(...))`. (Saturating share conversion and the underflow floor were split into a separate follow-up.)

**Correction (2026-10-21)**: the workload-request side is no longer saturating. Since pr-16479 (v0.20.1/v0.19.8) `MapRequests` and `SliceRequests` store `Amount`, so totals stay exact past `int64` and quota fit checks see the real total; `AmountFromQuantity` keeps in-range non-negative values on an allocation-free `int64` path (pr-16492) and routes far-exponent values to the decimal path without building 10^n (pr-16527). The remaining cap is the API boundary: a non-CPU `resourceUsage` past `MaxInt64` is still written as `MaxInt64` (issue-16486, open). See [[scheduler-internals#Quota arithmetic and integer-overflow safety]] and [[workload-resource-adjustment]].

## Per-Cohort lendable capacity is cached (#15955)

`resourceNode.Lendable` is maintained by `updateCohortLendable` alongside `SubtreeQuota` on every Cohort mutation and copied into `CohortSnapshot`; fair-sharing DRS reads the parent's `Lendable` instead of walking the tree per candidate (`computeLendable` is the fresh derivation, used by tests to assert the stored value stays in sync, including across `DeleteCohort`). Shipped v0.19.7/v0.18.11 via pr-16361/pr-16360 (source: pr-16360.md). `CohortSnapshot` also gained `Borrowing(fr)` (= `BorrowingWith(fr, 0)`, i.e. `SubtreeQuota[fr] < Usage[fr]`) and `DRS` gained `IsBorrowingOnAny(frs)` for contested-resource pruning in fair-sharing preemption (pr-16738).

## Effective resource groups (DQO, Alpha)

With `DynamicQuotaOrchestration` on and `status.effectiveQuotas` set, the cache builds ClusterQueue and Cohort quotas from `resourcegroups.EffectiveResourceGroups(cq)` / `EffectiveCohortResourceGroups(cohort)` (`pkg/util/resourcegroups/effective.go`) instead of `spec.resourceGroups`; the same helper is used by the pending-workloads view, ClusterQueue metrics, the ResourceFlavor and ClusterQueue/Cohort controllers' change predicates, admission-check flavor lists and ConcurrentAdmission. Webhooks, MultiKueue quota automation, kueueviz and the importer still read `spec` (source: pr-15040.md, pr-15107.md). See [[dynamic-quota-orchestration]].

Minor (queue manager, `pkg/cache/queue`): `newClusterQueue`/`newClusterQueueImpl` no longer take an unused `client.Client`, left over after pr-16241 stopped reading LocalQueues during sorts (#16309; backports pr-16382/0.19, pr-16383/0.18).

## Queue manager: inflight and LocalQueue weights

The queue manager keeps popped ("inflight") Workloads keyed by `workload.Reference` per ClusterQueue rather than a single slot (pr-15844; dump includes inflight state), and a per-ClusterQueue `lqWeights` map (default `1.0`) used by both the heap comparator and the visibility snapshot; `Snapshot()` clones it under the read lock ([[fair-sharing#LocalQueue weight lookup: one cached path for heap and snapshot (AFS ordering)]]). `PopFrom` and `HasQueuedWorkloads` share one helper for "look up the ClusterQueue and check it is active" (pr-15994). The queue cache also feeds `kueue_unadmitted_workloads` ([[unadmitted-workloads-observability]]).

## Debugging cache state

The `pkg/debugger` package can dump the in-memory cache state. This is exposed via the Kueue manager's debug HTTP endpoint when enabled. Useful for diagnosing why the scheduler's view of quota doesn't match what you see in `kubectl get clusterqueue -o yaml`. (source: pkg/scheduler/scheduler.go)

## Cached TAS topology trees

With `TASCacheTopologyTree` (Beta/on from v0.20) the cache holds an **immutable topology tree per TAS flavor** and hands it to successive scheduler snapshots instead of rebuilding it each cycle. Mutable scheduling state stays in the snapshot, so concurrently created snapshots remain isolated; invalidation is driven by semantic node changes only (labels, taints, allocatable). Measured −71.7% CPU and −61.0% allocated bytes on a 2,500-node / 15-flavor benchmark. See [[topology-aware-scheduling#Cached topology trees]] ([[pr-13819]]).

## `RequeueWorkload` owns the inflight cleanup

Inflight bookkeeping is cleared **inside `Manager.RequeueWorkload`, before `info.Update` clears the source ClusterQueue** ([[pr-13885]]). Doing it there rather than at the call sites also fixes the `requeueAndUpdate` path and LocalQueue retargeting, where the previous ClusterQueue kept counting a moved Workload as pending. See [[scheduler-internals#Popped heads must survive a snapshot failure]].

## Related pages

- [[workload-resource-adjustment]] — the effective-resource view stored in `workload.Info`.
- [[scheduler-internals]]
- [[cluster-queue]]
- [[cohort]]
- [[admission]]
- [[workload]]
- [[performance-and-scale]]
