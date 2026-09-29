# Workload effective resources (LimitRange, RuntimeClass, pod-level requests)

**Summary**: Before a [[workload]]'s requests are counted against quota or validated, Kueue derives an *effective* PodSpec from external inputs (RuntimeClass overhead, limits-as-requests, namespace `LimitRange` defaults). Since pr-15284 (v0.20) this effective view is stored in `workload.Info` and constructed in one place; the old per-call `AdjustResources` on a deep-copied Workload is gone from production code. The stored API object is never rewritten.

**Sources**: pr-15284.md, pr-16129.md, pr-16047.md, pr-15736.md, pr-14958.md, issue-14964.md, issue-14965.md, issue-14255.md, issue-15702.md, issue-13911.md, issue-16095.md, raw/kueue/pkg/workload/effective_resources.go, raw/kueue/pkg/workload/workload.go, raw/kueue/pkg/controller/core/workload_controller.go

**Last updated**: 2026-09-29

---

## One construction path: `workload.Info` holds the effective view (pr-15284)

Previously each producer had to remember to deep-copy the Workload and call `AdjustResources`; a missed entry point gave the same Workload different requests on creation, requeue or restart, and validation and DRA could consume different views (bugs #10158, #9939, #14433; umbrella issue-14964.md). Now:

- `Info.Obj` keeps the **API representation** unchanged. `Info.EffectivePodSpecs` holds full effective PodSpecs, stored **only when they differ** from the originals; `Info.PodSpec(i)` / `PodSpecByName(name)` return the effective (read-only) spec or fall back to the raw one.
- `NewInfoFromClient(ctx, client, wl, opts...)` / `Info.UpdateFromClient` resolve the inputs and build the view in one go: `ResolveAdjustmentInputs` reads the RuntimeClasses referenced by PodSets that have no explicit `overhead` (`overhead.podFixed`) and lists the namespace's LimitRanges that have container- or pod-type items (via the `LimitRangeHasContainerOrPodType` index), then `applyAdjustmentsToPodSpec` applies, **in this order**: RuntimeClass overhead; limits copied into missing requests (mirrors API-server defaulting, including pod-level `resources` when `PodLevelResources` is used); LimitRange `Default` and `DefaultRequest` for whatever is still unset (mirrors the LimitRanger plugin; pod-type items apply to pod-level resources). `NewInfo` with `WithAdjustmentInputs` is the client-free variant.
- The effective view feeds validation, DRA request detection/conversion, the scheduling hash, TAS accounting and the WAS simulation template ([[dra]], [[topology-aware-scheduling]], [[scheduler-internals]]). Defaults are refreshed on normal updates; the same snapshot is deliberately kept across DRA preprocessing and enqueueing (including requeue after backoff), scheduler *assume*, and TAS cache resync so a Workload cannot change requests mid-cycle.
- Reserved quota still comes from `status.admission.podSetAssignments[].resourceUsage`, not from the effective view. `resourceTransformations` stay at the existing total-request stage ([[resource-transformer]]). There are no CRD changes.
- Because effective requests can change independently of the Workload object, the scheduling-equivalence hash folds `TotalRequests.Requests` in ([[scheduler-internals#Scheduling-equivalence hash: what it does and does not include]], pr-14958).
- The old `AdjustResources` survives only as a test oracle.

## Pod-level requests never undercount containers (pr-16047)

For a hand-written Workload with `PodLevelResources`, `resourcehelpers.PodRequests` let an explicit pod-level request *replace* the container total, so `resources.requests.cpu: "0"` next to a container asking for 8 CPU reserved zero quota (the apiserver rejects that shape on a Pod, but nothing checks it on `podSets[].template.spec`). The shared `PodRequests` helper now takes the effective pod-level request, keeps **at least Kubernetes' `AggregateContainerRequests`** (regular, init and restartable init containers), then adds Pod overhead. Valid PodSpecs are unaffected; already-admitted Workloads keep the usage recorded in `status.admission` (source: pr-16047.md, issue-14255.md).

Open, pre-existing: `UseLimitsAsMissingRequestsInPod` defaults a missing pod-level *request* from the pod-level *limit* even when the aggregate container request is smaller, so Kueue can charge 4 CPU where the API server would create the Pod with a pod-level request of 1 CPU (source: issue-15702.md).

## LimitRange constraints are enforced at admission only

The scheduler validates a candidate with `workload.ValidateAdmissibility` → `ValidateLimitRange`. A Workload whose requests exceed a container `max` (or fall below `min`) is rejected with **`resources didn't satisfy LimitRange constraints`** (reason `Misconfigured` with [[unadmitted-workloads-observability]] on). `max`/`min` are constraints, not defaults, so they leave **no trace in the effective resources**: a constraint-only LimitRange change produces a byte-identical effective spec (source: issue-14965.md).

## LimitRange changes now wake rejected and in-flight Workloads

The earlier gotcha (relaxing `max`/`min` or deleting a LimitRange did not requeue rejected Workloads because `PushOrUpdate` only woke a parked Workload when the recomputed spec differed) is **fixed in the code at the analysed commit** (the raw copies of issue-14965.md and of the proposing PR-14967.md still show *open*, so the exact PR that introduced the constraint-field comparison is not identifiable from the raw files; pr-16129 is the last change to it). `resourceUpdatesHandler` on the Workload controller (watches LimitRange and RuntimeClass) now, on create/update/delete of a LimitRange, calls `notifyForLimitRangeSchedulingChange`, which compares each `LimitRangeItem`'s `Type`, `Max`, `Min`, `Default`, `DefaultRequest` and `MaxLimitRequestRatio`; if any changed it calls `retryInadmissibleForNamespace`, listing pending Workloads (index `WorkloadQuotaReservedKey=False`) in the namespace and issuing `NotifyRetryInadmissible` for each ClusterQueue that has them. It also runs `queueReconcileForPending`, which refreshes each pending Workload's `Info` (skipping DRA Workloads, which are re-reconciled instead) (source: raw/kueue/pkg/controller/core/workload_controller.go).

pr-16129 (fixes issue-16095; backports pr-16243/0.19, pr-16244/0.18) closed the remaining race: a Workload popped by the scheduler ("in flight") while a LimitRange changed could become inadmissible from a stale evaluation because nobody told the queue to retry. LimitRange create/update/delete events now go through the scheduling-change notification (the comparison includes `Default` and `DefaultRequest`) and it also records the change for Workloads currently checked out by the scheduler, so they return to the active queue instead of being parked. The flaky integration spec `Scheduling hash freshness across LimitRange changes` was the symptom. (A proposal to cache RuntimeClasses in the queue manager, issue-13911.md, is closed, but `ResolveAdjustmentInputs` in this snapshot still reads them through the client.)

## Inflight bookkeeping is per Workload (pr-15844)

The queue layer used to track a single inflight (popped) Workload per ClusterQueue. pr-15844 keys `inflight` by `workload.Reference` (`ForgetInflightByKey`, `HasInflight`, `DumpInflight`), adjusts lifecycle and scheduling-hash handling, and adds inflight state to the queue dump. Scheduling behaviour is unchanged; it is prep work so the fair-sharing refill KEP can pop several heads per cycle. See [[cache-architecture#`RequeueWorkload` owns the inflight cleanup]].

## Webhook message for non-divisible usage (pr-15736)

Validation of `admission.podSetAssignments[].resourceUsage` (must be a multiple of the assigned count) formatted the `*int32` pointer instead of the count ("is not a multiple of 21678974853132"); it now prints the actual count (source: issue-15735.md, pr-15736.md).

## Large amounts

A PodSet total is `per-pod * count` with saturating multiplication; the `Unlimited` sentinel problem that used to make a total landing exactly on `MaxInt64` corrupt usage accounting was removed by making amounts exact. See [[cache-architecture#Quota amounts are exact past int64 (pr-15026)]].

## Related pages

- [[workload]] — where `Info` lives.
- [[admission]] — where `ValidateAdmissibility` runs.
- [[queueing-strategy]] — why the requeue reason decides whether a rejection is a stall.
- [[cache-architecture]] — queue manager caches and the quota `Amount` type.
- [[dra]] — consumer of the effective view.
- [[resource-transformer]] — the other rewrite of workload requests into quota units.
