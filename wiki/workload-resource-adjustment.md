# Workload effective resources (LimitRange, RuntimeClass, pod-level requests)

**Summary**: Before a [[workload]]'s requests are counted against quota or validated, Kueue derives an *effective* PodSpec from external inputs (RuntimeClass overhead, limits-as-requests, namespace `LimitRange` defaults). Since pr-15284 (v0.20) this effective view is stored in `workload.Info` and constructed in one place; the old per-call `AdjustResources` on a deep-copied Workload is gone from production code. The stored API object is never rewritten.

**Sources**: pr-15284.md, pr-16129.md, pr-16047.md, pr-15736.md, pr-14958.md, issue-14964.md, issue-14965.md, issue-14255.md, issue-15702.md, issue-13911.md, issue-16095.md, pr-14520.md, raw/kueue/pkg/workload/effective_resources.go, raw/kueue/pkg/workload/workload.go, raw/kueue/pkg/controller/core/workload_controller.go, pr-17354.md, pr-17424.md, pr-17443.md, pr-17444.md, issue-17422.md, pr-17090.md

**Last updated**: 2026-10-21

---

## One construction path: `workload.Info` holds the effective view (pr-15284)

Previously each producer had to remember to deep-copy the Workload and call `AdjustResources`; a missed entry point gave the same Workload different requests on creation, requeue or restart, and validation and DRA could consume different views (bugs #10158, #9939, #14433; umbrella issue-14964.md). Now:

- `Info.Obj` keeps the **API representation** unchanged. `Info.EffectivePodSpecs` holds full effective PodSpecs, stored **only when they differ** from the originals; `Info.PodSpec(i)` / `PodSpecByName(name)` return the effective (read-only) spec or fall back to the raw one.
- `NewInfoFromClient(ctx, client, wl, opts...)` / `Info.UpdateFromClient` resolve the inputs and build the view in one go: `ResolveAdjustmentInputs` reads the RuntimeClasses referenced by PodSets that have no explicit `overhead` (`overhead.podFixed`) and lists the namespace's LimitRanges that have container- or pod-type items (via the `LimitRangeHasContainerOrPodType` index), then `applyAdjustmentsToPodSpec` applies, **in this order**: RuntimeClass overhead; limits copied into missing requests (mirrors API-server defaulting, including pod-level `resources` when `PodLevelResources` is used); LimitRange `Default` and `DefaultRequest` for whatever is still unset (mirrors the LimitRanger plugin; pod-type items apply to pod-level resources). `NewInfo` with `WithAdjustmentInputs` is the client-free variant.
- The effective view feeds validation, DRA request detection/conversion, the scheduling hash, TAS accounting and the WAS simulation template ([[dra]], [[topology-aware-scheduling]], [[scheduler-internals]]). Defaults are refreshed on normal updates; the same snapshot is deliberately kept across DRA preprocessing and enqueueing (including requeue after backoff), scheduler *assume*, and TAS cache resync so a Workload cannot change requests mid-cycle.
- Reserved quota still comes from `status.admission.podSetAssignments[].resourceUsage`, not from the effective view. `resourceTransformations` stay at the existing total-request stage ([[resource-transformer]]). There are no CRD changes.
- Because effective requests can change independently of the Workload object, the scheduling-equivalence hash folds `TotalRequests.Requests` in ([[scheduler-internals#Scheduling-equivalence hash: what it does and does not include]], pr-14958).
- The old `AdjustResources` survives only as a test oracle.
- **Release lines.** pr-15284 shipped in v0.20.0. It was backported to **release-0.19** as pr-17354 (merged 2026-10-16, after v0.19.9; release note NONE), adapted because DRA requeue pairing (#14562) and the flavorassigner TAS-usage extraction had landed there in the meantime; e.g. `requeueWorkloadLocked` now builds a fresh Info with `NewInfoFromClient` and reuses its `EffectivePodSpecs` (source: pr-17354.md).
- **"Differs" is a narrow comparison (pr-17424).** `effectivePodSpecs` decides whether to store effective specs with `adjustedFieldsDiffer`, which compares only the fields `applyAdjustmentsToPodSpec` writes: `Overhead`, pod-level `Resources`, and each init and regular container's `Resources`. Comparing whole PodSpecs dominated the cost of building an Info (`effectivePodSpecs` 2.54 s to 0.76 s, `Info.Update` 8.49 s to 4.98 s in the performance scheduler; 5.7x faster on a pod with init container, sidecar, env and volumes). Invariant: keep `adjustedFieldsDiffer` in sync with `applyAdjustmentsToPodSpec` when adding an adjustment. The same PR makes the Workload controller's DRA check build a full Info only when a DeviceClass backs an extended resource ([[dra]]). Backports pr-17444 (0.20) and pr-17443 (0.19), merged after v0.20.2 / v0.19.9 (source: pr-17424.md, raw/kueue/pkg/workload/effective_resources.go).
- **Overhead sign.** Since pr-17090 the Workload webhook rejects negative `overhead` under `WorkloadValidateResourcesAreNonNegative`, so overhead can no longer offset container requests in the charge ([[workload#Negative Pod overhead is rejected (pr-17090, fixes issue-13991)]]).

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

A PodSet total is `per-pod * count`; since pr-16479 (v0.20.1 / v0.19.8) the in-memory `Requests` are exact `resources.Amount` values, not saturating `int64` (see [[scheduler-internals]]). The `Unlimited` sentinel problem that used to make a total landing exactly on `MaxInt64` corrupt usage accounting was removed by making amounts exact. See [[cache-architecture#Quota amounts are exact past int64 (pr-15026)]].

**Partial admission scales from the per-Pod request** (source: pr-14520.md, part of issue-14371; shipped v0.20.1 / v0.19.8 as #16519 / #16520 per CHANGELOG). At the time, PodSet `Requests` was an `int64` sum that saturated at `MaxInt64`. `PodSetResources.ScaledTo` rebuilt the request for a smaller count as `total / oldCount * newCount`, which is meaningless once the total has saturated. Example: 3 Pods at 4e18 each saturate the total; against a 7e18 quota, partial admission tried 2 Pods, computed `MaxInt64/3*2 = 6148914691236517204`, saw it fit, and admitted 2 Pods that really need 8e18. The pending path now multiplies the stored per-Pod request (`PerPodRequests`) by the new count. The admitted path (`totalRequestsFromAdmission`) has no per-Pod value and still divides the admitted total. Because partial admission now depends on `PerPodRequests`, `computeSchedulingHash` and `sameHashedRequests` read it too. Otherwise two pending Workloads that differ only in per-Pod **DRA** charges (DRA charges only through the total) could share an equivalence hash once saturated, and in `BestEffortFIFO` one could drag the other to inadmissible. **Correction (2026-10-21)**: `Requests` themselves became exact when pr-16479 merged (fixes issue-16405), so the quota check now sees the real total. What remains is the API write: the admitted total is stored in `status.admission.podSetAssignments[].resourceUsage` as a `Quantity`, which caps a non-CPU total at `MaxInt64`. The webhook rejects that value when it is not a multiple of the count, and the scheduler retries endlessly without setting a condition. Known gap, open as of this snapshot (source: issue-16486.md, pr-16479.md).

## Related pages

- [[workload]] — where `Info` lives.
- [[admission]] — where `ValidateAdmissibility` runs.
- [[queueing-strategy]] — why the requeue reason decides whether a rejection is a stall.
- [[cache-architecture]] — queue manager caches and the quota `Amount` type.
- [[dra]] — consumer of the effective view.
- [[resource-transformer]] — the other rewrite of workload requests into quota units.
