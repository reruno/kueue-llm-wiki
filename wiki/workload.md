# Workload

**Summary**: A Workload is the Kueue-internal CRD that wraps an underlying job (Job, JobSet, RayJob, …) and exposes the fields Kueue needs: PodSets, priority, queue-name, admission state, conditions. Every admitted job has exactly one Workload, owned by the job via an ownerReference.

**Sources**: `raw/github/kubernetes-sigs__kueue/`, pr-16479.md, pr-14520.md, pr-13671.md, pr-16627.md, pr-13956.md, pr-17069.md, issue-16486.md, pr-16779.md, pr-16881.md, pr-17147.md, pr-17215.md, pr-17220.md, pr-17269.md, issue-14811.md, issue-17221.md, pr-17090.md, pr-17201.md, pr-17202.md, issue-13991.md, raw/kueue/pkg/controller/jobframework/reconciler.go, raw/kueue/pkg/webhooks/workload_webhook.go, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, raw/kueue/CHANGELOG/CHANGELOG-0.19.md

**Last updated**: 2026-10-21

---

## Shape

Key fields:

- `spec.queueName` — which [[local-queue]] this Workload targets.
- `spec.priorityClassName` / `spec.priorityClassSource` / `spec.priority` — see [[workload-priority]]. `priorityClassSource` distinguishes a stock `scheduling.k8s.io/PriorityClass` from a `kueue.x-k8s.io/WorkloadPriorityClass` ([[issue-7342]]).
- `spec.podSets[]` — one entry per distinct Pod template the job needs, with `count` and `template`. A Workload has multiple PodSets when the job is multi-template (e.g. a JobSet, RayJob with head + workers, PyTorchJob with master + workers).
- `spec.active` — can be flipped to `false` to deactivate a Workload (stop it from being admitted again after eviction).
- `status.admissionChecks[].podSetUpdates[]` (`AdmissionCheckState.PodSetUpdates`) — mutations that [[admission-check]]s applied (additional tolerations, node selectors, labels, annotations) before admission, so the integration can patch them into the job's Pod template when unsuspending. **Correction (2026-10-21)**: this page listed it as `spec.podSetUpdates`; there is no such spec field (source: apis/kueue/v1beta2/workload_types.go at kueue@8922c563e).
- `status.admission` — populated after QuotaReservation; records which CQ admitted the Workload and the flavor assignment per PodSet.
- `status.conditions[]` — `QuotaReserved`, `Admitted`, `Evicted`, `Requeued`, `Finished`, `PodsReady`. See [[admission]] for the state machine.

## Who creates a Workload

Never the user. Integration controllers (one per supported job type — see [[integrations]]) watch their respective job objects, and when they see a job labeled with a queue-name, they create an owned Workload. On job deletion the Workload is garbage-collected.

There was historical discussion about letting users supply a Workload directly via PodTemplate references ([[issue-1004]]), but it was closed as not-planned — integration controllers remain the canonical authors.

## PodSets and counts

Each PodSet has a `count` (replica count) and a `template` (full `PodTemplateSpec`). Kueue sizes quota requests per PodSet: if PodSet A needs 8 GPUs×4 replicas, that's 32 GPUs. Total Workload quota is the sum across PodSets.

The `PodSetAssignments` in `status.admission.podSetAssignments[]` mirrors the PodSet array and records the flavor chosen per PodSet ([[issue-1163]]). PodSetAssignments count must equal PodSet count.

**Maximum PodSets per Workload.** `spec.podSets` is length-validated; the cap was raised from **8 to 10** in [[pr-11388]] (fixes/relates to [[issue-11379]], which requested 16). The cap is deliberately conservative rather than unbounded because [[topology-aware-scheduling]] flavor-assignment cost scales roughly as `flavors × PodSets`. The practical motivation is Ray: one PodSet is reserved for the Ray head group, so raising the cap to 10 lets a RayCluster/RayJob/RayService declare up to **9 worker groups** (was 7). See [[integration-rayjob]].

For TAS-enabled flavors, each assignment also includes a `topologyAssignment` listing domain→count tuples — see [[topology-aware-scheduling]].

**Request arithmetic is exact.** The scheduler's `workload.Info.TotalRequests` (per PodSet `Requests`, plus `PerPodRequests` for pending PodSets) are `resources.Amount` values since pr-16479 (v0.20.1/v0.19.8), so `count x per-pod` totals past `int64` are no longer saturated to `MaxInt64`. Partial admission rebuilds a reduced PodSet as `PerPodRequests x newCount` (`PodSetResources.ScaledTo`, pr-14520) instead of dividing the total. The API record is still a `Quantity`: `podSetAssignments[].resourceUsage` caps a non-CPU total at `MaxInt64`, and the webhook's "`resourceUsage` divisible by `count`" rule can then reject the admission repeatedly (issue-16486, open). See [[scheduler-internals#Quota arithmetic and integer-overflow safety]].

The "invalid PodSet info" error now reports the expected and actual PodSet counts in the right order (pr-13671).

## Priority

A Workload's priority is derived once, at creation, from either a stock PriorityClass or a WorkloadPriorityClass. It's stored as an int32 in `spec.priority`. Priority is traditionally immutable after creation ([[issue-2593]] — why PriorityClassName is immutable while priority integer is mutable) though in-place mutation of priority class has been added and then expanded ([[issue-5004]], [[issue-7138]]). See [[workload-priority]].

## Eviction, requeueing, deactivation

When an admitted Workload is preempted, or when [[gang-scheduling]]'s WaitForPodsReady timeout fires, the Workload is evicted: `status.conditions.Evicted=True`, `status.admission` cleared, job re-suspended. If `requeuingStrategy` permits, the Workload is re-added to the queue with a backoff. After too many evictions it can be deactivated ([[issue-2174]]). Eviction detail: a preemption sets `Evicted` with reason `Preempted` plus a separate `Preempted` condition whose reason names the trigger (including the Alpha `ConfigurablePreemption`), and `status.schedulingStats.evictions[]` counts evictions per `reason` and `underlyingCause` (for configurable preemption the `PreemptionConfig` name; for `PodsReadyTimeout` the `WaitForStart`/`WaitForRecovery`/`WaitForScheduling` phase) ([[configurable-preemptions]], [[wait-for-pods-ready]]). If `spec.active` is false, the Workload stays dormant.

## `reclaimablePods` must not block eviction (pr-17147, fixes issue-14811)

The Workload webhook refuses to **lower** `status.reclaimablePods` while the Workload holds quota (both "cannot be removed" when an entry disappears and "cannot be less than N" when a count drops; the `scaledDownPodSets` exemption applies only to elastic slices). `JobReconciler.ReconcileGenericJob` updates reclaimable counts (step 4) **before** it handles eviction, and returned on that rejected update, so eviction never released quota: the job was suspended and its Pods deleted, yet `status.admission` stayed populated with `Admitted`, `QuotaReserved` and `Evicted` all `True`, and the Workload was never requeued. The ClusterQueue kept charging the reservation indefinitely (source: issue-14811.md).

Trigger seen in production: a JobSet with `failurePolicy.restartStrategy: Recreate` recreated child Jobs that had already succeeded (their reclaimable count went back down), then a `waitForPodsReady` recovery timeout (`underlyingCause: WaitForRecovery`) evicted the Workload. An elastic batch Job shrink with fixed completions hit the same path (source: issue-14811.md).

Fix: the reconciler skips the reclaimable-pods update when the Workload is evicted **and** still holds a quota reservation (`evictedAndHoldingQuota`), so the eviction path runs, suspends the job, clears `status.admission` once Pods are inactive, and the stale reclaimable entries go away with the reservation (source: raw/kueue/pkg/controller/jobframework/reconciler.go, pr-17147.md). Release note: "JobSet: Fixed a bug where an evicted Workload could keep its quota reserved, and was not requeued, if a JobSet restart had recreated child Jobs that had already succeeded." Shipped in **v0.20.2 (#17215)** and **v0.19.9 (#17220)**. An envtest regression test with the real webhook followed (pr-17269, fixes issue-17221; backports pr-17426/0.20, pr-17425/0.19) (source: raw/kueue/CHANGELOG/CHANGELOG-0.20.md, CHANGELOG-0.19.md, pr-17269.md).

Invariant for job-framework code: any status write that the webhook can reject while quota is reserved must not run ahead of eviction handling, or eviction can deadlock on it.

## Negative Pod overhead is rejected (pr-17090, fixes issue-13991)

`spec.podSets[].template.spec.overhead` is added to the per-Pod requests charged against quota, but `WorkloadValidateResourcesAreNonNegative` (Beta, on; introduced in v0.20.0 and v0.19.1 per the changelogs) only checked container requests, so a negative overhead could offset them and admit a Workload with too little quota charged. The Workload webhook now runs `validatePodSetOverhead` under the same gate: on create, any negative overhead quantity is rejected; on update, only **new or changed** negative quantities are rejected, so an existing object can still be updated (for example to remove Kueue's finalizer). With the gate off, negative overhead is accepted as before. Release note: "Workload: Reject negative Pod overhead when WorkloadValidateResourcesAreNonNegative is enabled." Shipped in **v0.20.2 (#17201)** and **v0.19.9 (#17202)** (source: pr-17090.md, raw/kueue/pkg/webhooks/workload_webhook.go, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, CHANGELOG-0.19.md).

## Annotations that change Workload behaviour (v0.20)

- `kueue.x-k8s.io/wait-for-pods-ready` (JSON `timeoutSeconds`/`recoveryTimeoutSeconds`) is copied from the job onto the Workload under gate `WorkloadLevelWaitForPodsReady` and overrides the cluster-wide timeouts ([[wait-for-pods-ready]]).
- `kueue.x-k8s.io/workload-allowed-resource-flavors` marks a ConcurrentAdmission Variant's flavor ([[concurrent-admission]]).
- `status.conditions[QuotaReserved]` reasons are tiered when `UnadmittedWorkloadsObservability` is on ([[unadmitted-workloads-observability]]); `PodsScheduled` exists with `WaitForPodsReadyUnscheduledTimeout`.
- The `Info` used by the scheduler carries an *effective* PodSpec view (LimitRange, RuntimeClass, pod-level requests) that is never written back to the object ([[workload-resource-adjustment]]).
- The `Info` also carries in-memory `FlavorScanState` (tried flavors per PodSet/resource, CQ generation, scheduling cycle, equivalence hash) that lets the flavor search resume across cycles; it is kept across Workload updates unless the scheduling shape changed ([[scheduler-internals#Flavor scan progress across cycles (`FlavorScanState`)]]).
- A Workload whose preemption is blocked by a closed preemption gate carries `QuotaReserved=False` reason `PreemptionGated` plus `BlockedOnPreemptionGates=True` (pr-16627).
- Kueue's internal labels (MultiKueue origin, ConcurrentAdmission parent, job UID) and internal annotations are never copied from the job onto the Workload, whatever `labelKeysToCopy` says; naming one there only logs a startup warning. See [[job-framework-interface#Internal labels and annotations are never inherited]] (source: pr-16779.md, pr-16881.md).

## Finalizer and GC

A Workload carries a finalizer so quota accounting stays consistent while the underlying job is being torn down. Cases where the finalizer wasn't removed (plain Pods, PodGroups) have historically blocked GC ([[issue-6919]]).

## `minCount` may be zero

`PodSet.minCount` accepts **0** since [[pr-14720]] (fixes [[issue-14719]]); the OpenAPI `Minimum` was previously 1 even though `count` already allowed 0, so `count=0, minCount=0` — the shape partial scale-up of elastic workload slices needs — was rejected. The CEL rule `minCount <= count` is unchanged and no scheduler behaviour changed. Applies to both `v1beta1` and `v1beta2`.

The maximum number of PodSets per Workload remains **10**.

## `priorityClassRef` is frozen once quota is reserved

The Workload CRD's CEL rules freeze `priorityClassRef` for a Workload that has reserved quota: it cannot be **added**, cannot be **removed**, its **group** and **kind** cannot change, and for a Pod `PriorityClass` neither can its **name**.

`classifyWorkloadsForPriorityUpdate` only skipped the *addition* case, so a reserved Workload whose owner dropped its `WorkloadPriorityClass` label was written with a ref the API server refuses; the reconcile failed and retried for as long as the reservation was held. In a batch this splits the set: unreserved components take the transition, reserved ones are refused forever. [[pr-14565]] (fixes [[issue-14482]]) adds `priorityRefTransitionAllowed`, consulted **in the write loop** next to the existing `priorityStateEqual` skip — it cannot live in the classifier, which only receives the class *name*; the target's group and kind do not exist until `ExtractPriority` has resolved the ref, which happens after classification. A Workload **without** a reservation is unconstrained and still follows its owner. See [[workload-priority]].

## Reactivation matches deactivation reasons by prefix

Deactivation reasons follow a `DeactivatedDueTo<Cause>` pattern (e.g. `DeactivatedDueToRequeuingLimitExceeded`). `WorkloadReconciler.Reconcile` matched only the exact base reason `WorkloadDeactivated` ("Deactivated"), so a Workload carrying a *derived* reason on its `WorkloadRequeued=False` condition never took the reactivation path: the stale requeue condition stayed and the Workload was never re-queued after `spec.active` was flipped back on.

[[pr-14874]] (fixes [[issue-14870]]; cherry-picks [[pr-14878]], [[pr-14879]]) converts the expression `switch` on `cond.Reason` into a condition `switch` and matches with `strings.HasPrefix(cond.Reason, kueue.WorkloadDeactivated)`. The eviction-backoff cases (`WorkloadEvictedByPodsReadyTimeout`, `WorkloadEvictedByAdmissionCheck`) are unchanged. This is a follow-up to [[pr-14309]].

## Extended resources declared only in `limits` are indexed

The core Workload indexer only looked at container `requests` when indexing extended resources, so a Workload whose containers declare an extended resource **only** in `limits` (legal Kubernetes — `requests` defaults from `limits`) was missing from the index. [[pr-14808]] (fixes [[issue-14801]]; cherry-picks [[pr-14887]], [[pr-14888]]) reads both.

## Related pages

- [[admission]] — the Workload state machine.
- [[integrations]] — which controllers author Workloads.
- [[workload-priority]] — priority fields and immutability.
- [[gang-scheduling]] — PodsReady condition.
- [[workload-garbage-collection]] — **[Stable]** retention policies for finished/deactivated Workloads.
- [[workload-max-execution-time]] — **[Beta]** `spec.maximumExecutionTimeSeconds` enforcement.
- [[concurrent-admission]] — **[Alpha]** Parent/Variant Workload model for racing flavors.
- [[workload-resource-adjustment]] — how the requests that count against quota are recomputed from LimitRange defaults, and the raw-vs-adjusted split in `workload.Info`.
