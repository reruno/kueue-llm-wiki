# Workload

**Summary**: A Workload is the Kueue-internal CRD that wraps an underlying job (Job, JobSet, RayJob, …) and exposes the fields Kueue needs: PodSets, priority, queue-name, admission state, conditions. Every admitted job has exactly one Workload, owned by the job via an ownerReference.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-09-01

---

## Shape

Key fields:

- `spec.queueName` — which [[local-queue]] this Workload targets.
- `spec.priorityClassName` / `spec.priorityClassSource` / `spec.priority` — see [[workload-priority]]. `priorityClassSource` distinguishes a stock `scheduling.k8s.io/PriorityClass` from a `kueue.x-k8s.io/WorkloadPriorityClass` ([[issue-7342]]).
- `spec.podSets[]` — one entry per distinct Pod template the job needs, with `count` and `template`. A Workload has multiple PodSets when the job is multi-template (e.g. a JobSet, RayJob with head + workers, PyTorchJob with master + workers).
- `spec.active` — can be flipped to `false` to deactivate a Workload (stop it from being admitted again after eviction).
- `spec.podSetUpdates` — mutations that [[admission-check]]s applied (additional tolerations, node selectors, annotations) before admission, so the integration can patch them into the job's Pod template when unsuspending.
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

## Priority

A Workload's priority is derived once, at creation, from either a stock PriorityClass or a WorkloadPriorityClass. It's stored as an int32 in `spec.priority`. Priority is traditionally immutable after creation ([[issue-2593]] — why PriorityClassName is immutable while priority integer is mutable) though in-place mutation of priority class has been added and then expanded ([[issue-5004]], [[issue-7138]]). See [[workload-priority]].

## Eviction, requeueing, deactivation

When an admitted Workload is preempted, or when [[gang-scheduling]]'s WaitForPodsReady timeout fires, the Workload is evicted: `status.conditions.Evicted=True`, `status.admission` cleared, job re-suspended. If `requeuingStrategy` permits, the Workload is re-added to the queue with a backoff. After too many evictions it can be deactivated ([[issue-2174]]). If `spec.active` is false, the Workload stays dormant.

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
