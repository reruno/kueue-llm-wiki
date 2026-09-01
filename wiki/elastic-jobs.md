# Elastic jobs

**Summary**: Elastic jobs let an already-admitted [[workload]] change its Pod count (scale up or down) without going back through admission from scratch. Implemented via **WorkloadSlices** (KEP-77), the feature splits a Workload's quota into slices so that a scale-down releases quota immediately and a scale-up only needs incremental admission.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-09-01

---

## Why this is hard

A vanilla Kueue [[admission]] is binary: a Workload is either Admitted (quota reserved for its full size) or not. If a user wants to scale the underlying job — e.g. a RayCluster auto-scaling up, a Deployment scaling replicas — there's no good path: evicting and re-admitting a whole training job to change its replica count is too disruptive.

WorkloadSlices (feature gate `ElasticJobsViaWorkloadSlices`) decouples admission into slices. The initial admission creates slice 1. A scale-up creates slice 2 that gets independently admitted against the remaining quota; scale-down releases the newest slices.

**Enablement is keyed off an annotation, not a label.** A managed Job opts into workload slicing via the `kueue.x-k8s.io/elastic-job` annotation (`workloadslicing.EnabledAnnotationKey`), and that annotation is **immutable** on an existing managed Job — the webhook (`validatedUpdateForEnabledWorkloadSlice` in `pkg/controller/jobframework/validation.go`) rejects adding/removing it with `apivalidation.FieldImmutableErrorMsg`. [[pr-11342]] fixed the validation to report the error against the correct field path `metadata.annotations[kueue.x-k8s.io/elastic-job]` (it previously pointed at `metadata.labels[...]`).

## Opt-in per integration

Elastic behavior is opt-in per Workload / integration. The initial implementation tracks a couple of integrations:

- **RayCluster** — add/remove worker replicas dynamically ([[issue-10170]] — RayCluster with elastic jobs via workload-slices support should support scheduling pending workload after freeing capacity on scale-down).
- **batch/v1 Job with parallelism changes** — scale parallelism while running ([[issue-6161]] — flaky integration test for elastic Job scale-down/up).

KEP-77 adoption was tracked under [[issue-5528]] (Initial implementation of KEP-77: Elastic Jobs via WorkloadSlices).

## Scheduling gates as the vehicle

For Pod-level integrations (plain Pods, RayCluster's dynamic Pods), Kueue uses Pod scheduling gates rather than `.spec.suspend`. Gates can be removed per-Pod, so new Pods appearing during a scale-up can be independently gated and admitted.

Bugs have clustered around gate removal edge cases:

- "Kueue sometimes does not inject scheduling gates for elastic jobs" ([[issue-10167]]).
- "Kueue does not remove the scheduling gate from Ray's redis-cleanup jobs" ([[issue-8443]]).
- "Kueue will say a workload is admitted if its scheduling gates are removed" — externally removing the gate confuses the accounting ([[issue-9482]]).
- Kubernetes 1.30 behavior change broke gate removal temporarily ([[issue-2029]]).

## WorkloadSlice replacement correctness (v0.18)

Scale-up replaces the old admitted slice with a new, larger one. Two ordering/sorting bugs here caused **quota leaks**, both fixed in v0.18:

- **Admit-first, finish-old-after** ([[pr-11195]], fixes #9015). The scheduler previously finished the old slice *before* the new slice's admission was confirmed. Admission is asynchronous, so if it then failed, the old slice was already `Finished` while the new one was not admitted — the job kept running unsuspended with no admitted slice holding quota. `replaceOldWorkloadSlice` now runs **inside `admit`'s success path** (after `PatchAdmissionStatus`). See [[scheduler-internals]]. Residual window: if the *finish* of the old slice fails after the new one is admitted, both slices sit admitted in the cache until the job reconciler's `EnsureWorkloadSlices` finishes the old one on the next reconcile — this is conservative **over-counting** (sum, not max), which can cause brief excessive preemptions but never over-commits.

- **Sort comparator antisymmetry** ([[pr-11198]], fixes [[issue-11166]]). The `slices.SortFunc` comparator inside `FindNotFinishedWorkloads` had a one-sided tiebreaker on the `WorkloadSliceReplacementFor` annotation: when two slices had **equal `CreationTimestamp`** and neither replaced the other, `cmp(a,b)==1` *and* `cmp(b,a)==1`, violating the strict-weak-ordering contract `slices.SortFunc` requires. The undefined ordering made `EnsureWorkloadSlices` swap old/new and **finish the wrong slice**, leaking quota. The fix adds the symmetric reverse check and returns `0` for the neutral case. Repro: a `v1→v2→v3` chain where `v2` is finished but `v1` is not, so `FindNotFinishedWorkloads` returns `[v1, v3]` and `v3` points to `v2` (not `v1`).

- **Duplicate replacement slices under rapid scaling** ([[pr-11327]], surfaced during beta stress testing). Rapidly scaling an elastic Job could leave duplicate replacement slices admitted indefinitely, leaking/reserving quota. The old two-active-slice `case 2` handling in `pkg/workloadslicing/workloadslicing.go` was replaced by a generic `normalizeActiveSlices()` that enforces the invariant: **exactly one** non-evicted admitted Workload (the latest), **at most one** non-evicted pending replacement directly replacing it, the newest non-evicted Workload kept when none is admitted, and **evicted Workloads always Finished** — reason `WorkloadFinishedReasonOutOfSync`, message "The workload slice is out of sync with its parent job" — so their quota is released. Note: "latest-admitted" (LA) selection deliberately *excludes* evicted workloads to preserve the preemption flow, and the slice DAG is **not necessarily linear** (forked replacements are possible).

## Interaction with TAS

Elastic + [[topology-aware-scheduling]] is genuinely complex: a scale-up needs to add replicas to the same topology domain. "Job controller with TAS and ElasticJobsViaWorkloadSlices should scale up an elastic job with TAS unconstrained topology" ([[issue-9341]]) captures the bridge work.

## Interaction with gang scheduling

Elastic is almost the opposite of [[gang-scheduling]]'s all-or-nothing: one says "partial is fine, add/remove on the fly," the other says "evict if any Pod isn't ready." Integrations must pick one; enabling both on the same CQ is nonsensical for training jobs but reasonable for services-on-Kueue patterns.

## Documentation gap

Elastic Jobs documentation has lagged the implementation ([[issue-6349]] — Document the feature of Elastic Jobs / Workloads).

## `PodSet.minCount` may be zero

The OpenAPI `Minimum` for `PodSet.minCount` was 1 while `PodSet.count` already allowed 0, so the combination `count=0, minCount=0` — needed for partial scale-up of elastic workload slices — was rejected. [[pr-14720]] (fixes [[issue-14719]]) lowers the minimum to **0** in both `v1beta1` and `v1beta2`; the CEL rule `minCount <= count` is unchanged, as is all scheduler and controller behaviour. CRDs and Helm charts were regenerated.

## The ungater counts admitted pods, not PodSet pods

The elastic-job ungater used to ungate `podSet.count` Pods. [[pr-14835]] makes it read the count from **`status.admission.podSetAssignments[].count`** instead, so it never ungates more Pods than the admission actually granted. This matters once partial scale-up exists, where `admission.count` can be lower than `podSet.count`; it also fixes accounting after a scale-down. Workloads with no admission data, or with an unset count, fall back safely. Scale-down coverage was added in [[pr-14897]] / [[pr-14899]] / [[pr-14900]] ([[issue-14896]]).

## Partial scale-up (Alpha, RayCluster only so far)

[[pr-14909]] (part of #12100) adds the Alpha, off-by-default gate **`ElasticJobsViaWorkloadSlicesWithPartialReplicaScaleUp`** plus two annotation constants:

- `kueue.x-k8s.io/elastic-job` — marks a Job as elastic (existing).
- `kueue.x-k8s.io/elastic-job-scale-up-strategy` — `atomic` (default) or `partial`.

When the gate is on, the annotation is `partial`, and the RayCluster worker group sets `minReplicas`, `BuildPodSets` sets the worker PodSet's `MinCount` to the effective minimum worker count. With the gate off there is no behaviour change.

## MultiKueue rejects an autoscaling elastic RayCluster

An elastic RayCluster (`ElasticJobsViaWorkloadSlices`) dispatched through [[multikueue]] with `enableInTreeAutoscaling` set is now **rejected at admission** ([[pr-14061]], original #13244). Previously it was accepted and then deleted immediately after admission, because the autoscaler sidecar was accounted for inconsistently between the manager and the worker cluster.

## TAS interaction: the leader keeps its placement

Resizing an elastic Workload with a leader/workers PodSet group no longer recomputes the leader's `TopologyAssignment` — see [[topology-aware-scheduling#Elastic workloads: the leader's assignment is preserved]] ([[pr-14064]], [[pr-14076]]).

Open gap worth knowing: a fully reclaimed elastic Workload can switch [[resource-flavor]] when it is re-admitted at count zero ([[issue-14792]], open).

## Related pages

- [[workload]] — gets sliced when elastic.
- [[admission]] — per-slice.
- [[integration-rayjob]] — primary elastic consumer.
- [[gang-scheduling]] — the anti-pattern.
