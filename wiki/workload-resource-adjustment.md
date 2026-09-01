# Workload resource adjustment (AdjustResources)

**Summary**: Before a [[workload]]'s requests are counted against quota or checked at admission, Kueue recomputes them from external inputs — chiefly the namespace's `LimitRange` defaults — through `workload.AdjustResources`. The adjusted ("effective") requests live only in the in-memory `workload.Info`, never in the stored object, and different call paths hand downstream consumers either the raw or the adjusted view. That asymmetry is the root of a recurring class of bugs.

**Sources**: `raw/github/kubernetes-sigs__kueue/issue-14964.md`, `issue-14965.md`, `issue-14105.md`, `pr-14958.md`.

**Last updated**: 2026-09-01

---

## Where the adjustment happens

`workload.AdjustResources(ctx, client, wl)` rewrites a Workload's PodSet templates in place, so every caller must hand it a **deep copy** — otherwise the adjusted values would be written back to the API object. That copy is a per-call allocation cost on hot paths, and it is one of the reasons the helper is a standing cleanup target (source: issue-14964.md).

The LimitRange half of the adjustment is `handlePodLimitRange` (`pkg/workload/resources.go:76-113`). It merges the namespace LimitRange's **`Default` and `DefaultRequest`** into each container through `mergeResourceList` (`pkg/util/resource/resource.go:31-34`). It never reads `Max` or `Min` — those are constraints, not defaults, and they are only consumed later, at admission (source: issue-14965.md).

PodSet-level aggregation is `totalRequestsFromPodSets`, whose last step is `setRes.Requests.Mul(int64(count))`. `Mul` **saturates** rather than wrapping (source: issue-14105.md); see the sentinel gotcha below.

`NewInfo` / `Info.Update` then store the aggregated effective requests on `workload.Info`. Because effective requests can change *independently* of the Workload object (through `AdjustResources` and `InfoOptions`), the scheduling-equivalence hash folds `TotalRequests.Requests` in rather than hashing the PodSet spec alone (source: pr-14958.md; see [[scheduler-internals#Scheduling-equivalence hash: what it does and does not include]]).

## Consumers see either the raw or the adjusted view

There is no single "effective resources" value in the tree; each consumer receives whatever the call path gave it (source: issue-14964.md):

| Consumer | Needs | Gets today |
|---|---|---|
| [[dra]] / extended resources (`NeedsDRAReconcile`, `ResolveExtendedResourceQuota`) | container-level effective requests | raw *or* adjusted, depending on the path |
| Validation (`Scheduler.nominate`, `getQueueBlocker`) | container / PodSpec requests and limits | reads `Info.Obj`, which may be raw or adjusted |
| `NewInfo` / `Info.Update` | PodSet-level aggregates | usually adjusted (seven identified paths) |

Per-path behaviour:

- `RequeueWorkload`, `queueReconcileForPending` — adjusted for both DRA and `Info`; ordering between the two therefore matters for correctness.
- `addLocalQueueLocked`, `Create`, `Update`, `deviceClassHandler.reconcileWorkloads` — **raw** for DRA, adjusted for `Info`, so the two observe different requests.
- `Reconcile → NeedsDRAReconcile(raw) → handleDRA → AdjustResources → DRA processing → NewInfo` — initial DRA detection runs on the raw view, the subsequent processing on the adjusted one.

Bugs that came out of this shape: #10158, #9939, #14433. Consolidating the paths behind one explicit effective-resource view (so `AdjustResources` can be deleted) is tracked in [[issue-14964]] (open).

## LimitRange constraints are enforced at admission only

The scheduler validates a candidate with `workload.ValidateAdmissibility` → `ValidateLimitRange` (`pkg/scheduler/scheduler.go:705`). A Workload whose requests exceed a container `max` (or fall below `min`) is rejected with **`resources didn't satisfy LimitRange constraints`**, and the requeue reason is left at **`RequeueReasonGeneric`** (source: issue-14965.md).

Consequences of that reason:

- **BestEffortFIFO** — the Workload is parked in `inadmissibleWorkloads` and only re-evaluated when something requeues the ClusterQueue's inadmissible set.
- **StrictFIFO** — `RequeueReasonGeneric` requeues immediately (`pkg/cache/queue/cluster_queue.go:836-848`), so the stall below does not occur.

Because `max`/`min` are read only here, they leave **no trace in the effective resources**: a constraint-only LimitRange change produces a byte-identical adjusted spec.

## Gotcha: relaxing or deleting a LimitRange does not wake the Workloads it rejected

The wake-up chain exists but its last link does not fire (source: issue-14965.md, open bug; reproduced with three integration specs on `main` at `9c85f631f`):

1. The workload controller **does** watch LimitRange (`pkg/controller/core/workload_controller.go:1612`). On any event it lists the namespace's pending Workloads, recomputes them with `AdjustResources`, and calls `AddOrUpdateWorkload` (`workload_controller.go:1703-1736`).
2. `PushOrUpdate` (`pkg/cache/queue/cluster_queue.go:393-412`) wakes a parked Workload only if the recomputed spec **differs**. A `max`/`min` change yields no diff, so the Workload is returned to `inadmissibleWorkloads` untouched and stays inadmissible indefinitely — until an unrelated cluster event happens to requeue the whole ClusterQueue.
3. A `defaultRequest` change *does* alter the adjusted spec and *does* wake the Workload. That asymmetry (covered by the existing "LimitRanges are defined and change" integration spec) is why the constraint case reads as an oversight rather than a design choice.

Deleting the LimitRange only *appears* to work, and does so by accident: while the LimitRange exists, `mergeResourceList` materializes empty `ResourceList{}` maps onto containers that had `nil`; after deletion the recomputed spec keeps `nil`, and that spurious nil-vs-empty diff is what defeats the `PushOrUpdate` guard. A Workload whose containers set **explicit limits** produces no such diff and stays stuck even after the LimitRange is gone.

Practical consequence for operators: after relaxing a LimitRange, expect to nudge the ClusterQueue (any event that requeues its inadmissible set) unless you run StrictFIFO.

## Gotcha: a PodSet total can land exactly on the `Unlimited` sentinel

Because `totalRequestsFromPodSets` multiplies with a saturating `Mul`, a large per-pod request times a pod count can saturate to `math.MaxInt64` — which `resources.Amount` reserves as the "unlimited quota" sentinel. See [[cache-architecture#Workload usage can reach the `Unlimited` sentinel]].

## Related pages

- [[workload]] — the object being adjusted, and where `Info` lives.
- [[admission]] — where `ValidateAdmissibility` runs in the cycle.
- [[queueing-strategy]] — why the requeue reason decides whether a rejection is a stall.
- [[cache-architecture]] — `workload.Info`, the quota `Amount` type and the sentinel collision.
- [[dra]] — the consumer most affected by the raw-vs-adjusted split.
- [[resource-transformer]] — the other rewrite of workload requests into quota units.
