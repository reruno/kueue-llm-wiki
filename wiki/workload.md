# Workload

**Summary**: A Workload is the Kueue-internal CRD that wraps an underlying job (Job, JobSet, RayJob, …) and exposes the fields Kueue needs: PodSets, priority, queue-name, admission state, conditions. Every admitted job has exactly one Workload, owned by the job via an ownerReference.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

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

For TAS-enabled flavors, each assignment also includes a `topologyAssignment` listing domain→count tuples — see [[topology-aware-scheduling]].

## Priority

A Workload's priority is derived once, at creation, from either a stock PriorityClass or a WorkloadPriorityClass. It's stored as an int32 in `spec.priority`. Priority is traditionally immutable after creation ([[issue-2593]] — why PriorityClassName is immutable while priority integer is mutable) though in-place mutation of priority class has been added and then expanded ([[issue-5004]], [[issue-7138]]). See [[workload-priority]].

## Eviction, requeueing, deactivation

When an admitted Workload is preempted, or when [[gang-scheduling]]'s WaitForPodsReady timeout fires, the Workload is evicted: `status.conditions.Evicted=True`, `status.admission` cleared, job re-suspended. If `requeuingStrategy` permits, the Workload is re-added to the queue with a backoff. After too many evictions it can be deactivated ([[issue-2174]]). If `spec.active` is false, the Workload stays dormant.

## Finalizer and GC

A Workload carries a finalizer so quota accounting stays consistent while the underlying job is being torn down. Cases where the finalizer wasn't removed (plain Pods, PodGroups) have historically blocked GC ([[issue-6919]]).

## Related pages

- [[admission]] — the Workload state machine.
- [[integrations]] — which controllers author Workloads.
- [[workload-priority]] — priority fields and immutability.
- [[gang-scheduling]] — PodsReady condition.
