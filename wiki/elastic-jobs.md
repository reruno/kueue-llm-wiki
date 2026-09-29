# Elastic jobs

**Summary**: Elastic jobs let an already-admitted [[workload]] change its Pod count (scale up or down) without going back through admission from scratch. Implemented via **WorkloadSlices** (KEP-77), the feature splits a Workload's quota into slices so that a scale-down releases quota immediately and a scale-up only needs incremental admission.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-09-29

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

> **Superseded detail.** The `minReplicas` requirement above no longer holds: since [[#Partial scale-up: the baseline/target model]] (pr-16209), `BuildPodSets` bootstraps a worker group's `MinCount` to its own `Replicas` whenever the partial annotation is set, and `MinReplicas` is not consulted at all (source: pr-16209.md).

## MultiKueue rejects an autoscaling elastic RayCluster

An elastic RayCluster (`ElasticJobsViaWorkloadSlices`) dispatched through [[multikueue]] with `enableInTreeAutoscaling` set is now **rejected at admission** ([[pr-14061]], original #13244). Previously it was accepted and then deleted immediately after admission, because the autoscaler sidecar was accounted for inconsistently between the manager and the worker cluster.

## TAS interaction: the leader keeps its placement

Resizing an elastic Workload with a leader/workers PodSet group no longer recomputes the leader's `TopologyAssignment` — see [[topology-aware-scheduling#Elastic workloads: the leader's assignment is preserved]] ([[pr-14064]], [[pr-14076]]).

Formerly open gap: a fully reclaimed elastic Workload could switch [[resource-flavor]] when re-admitted at count zero ([[issue-14792]]). Fixed, see [[#Zero-count PodSets and flavor selection]].

## Partial scale-up: the baseline/target model

Applies to multi-PodSet elastic jobs (RayCluster worker groups, RayJob) with the Alpha `ElasticJobsViaWorkloadSlicesWithPartialReplicaScaleUp` gate and the `partial` scale-up strategy. The replacement slice's `spec.podSets[i]` carries `count` = **target** (what the job now asks for) and `minCount` = **baseline** (the count the job last ran at), so each PodSet's admissible range is `[baseline, target]`.

- **Progress is required once per Workload, not once per PodSet.** Originally the controller set `minCount = granted + 1` on every growing PodSet, forcing every group to grow in the same admission. That blocked scale-up when one group had no room, sent spare capacity to the wrong group, and could stop an evicted job from being re-admitted at its old size. `minCount` is now the granted count itself, and `PodSetReducer.Reduce` takes a `mustGrow` flag that rejects the all-at-baseline assignment. The check runs **after** the give-back phase (with independently constrained flavors the ordered shrink often only fits once everything is at baseline) and applies **only while the replaced slice still holds quota**, so classic `PartialAdmission` (user-authored `minCount`) is unaffected (source: pr-15776.md).
- **`mustGrow` only when the predecessor is actually admitted.** The old code used `mustGrow := replaceableWorkloadSlice != nil`. If the predecessor held reserved quota but was still waiting on an AdmissionCheck (no replicas running), growth beyond `minCount` was demanded even when quota could not fit it, stalling the scale-up. Now the replacement may first be admitted at `minCount`; the larger target stays in `count` for later scale-up (source: pr-15855.md). `PodSetReducer` was later simplified: the `R` type parameter and the `refine` field were removed, and `giveBack` itself reports whether counts grew above the admitted baseline (source: pr-15887.md).
- **`minCount` is copied forward, never ratcheted.** `prepareWorkloadSliceForScaleUp` copies the predecessor's *recorded* `minCount` verbatim, so it traces back to the chain's origin. Before, each step recomputed it from the predecessor's live grant, so a later quota shrink below the most recent grant (even to a level the job had already run at) left the probe pending. The scheduler's `effectiveReducerPodSets` swaps the live granted count in as the reducer baseline for the single `mustGrow` check, without mutating the persisted `MinCount` (source: pr-16209.md).
- **PodSets are matched by name, not position.** Reordering worker groups used to swap minima between groups (RayCluster `analytics`/`serving` example) and adding a PodSet could panic or break the scale-up-probe naming chain. A matched PodSet inherits the predecessor's `minCount`; a new PodSet keeps its initialised `minCount` (source: pr-16216.md, pr-16242.md). A helper `PreviousAdmittedPodSetCounts` in `pkg/workloadslicing` extracts the previous counts (source: pr-16206.md).
- **`minCount` is capped at the PodSet's own `count`.** If one group shrinks while another grows in the same update, the copied-forward `minCount` could exceed `count`, giving the reducer a negative shrink budget and leaving the scale-up pending (source: pr-16289.md).
- **Eviction mid scale-up needs no special code.** An evicted slice whose probe sibling is still pending: `normalizeActiveSlices` finishes only the evicted slice and keeps the probe as an ordinary pending replacement. Once the predecessor is gone, `mustGrow` no longer applies and the probe can be admitted at its own `minCount` floor. Known gap (covered by an integration spec): if ClusterQueue quota shrinks below what the job held before eviction, the probe stays pending until quota is restored to at least that floor (source: pr-15417.md, issue-15399.md).

## Evicted slices drain before quota is released

An elastic Job with a pending scale-up slice used to lose its reservation when preempted while its Pods still ran, so a higher-priority Job could be admitted before the victim stopped (with TAS on or off). The evicted slice is now returned to the Job reconciler while it still holds quota, unless an **admitted, non-evicted** replacement has taken over; the normal eviction path then suspends the Job and waits for it to become inactive before clearing the reservation. A replacement that only has quota reserved (waiting on admission checks) does not count as having taken over (source: pr-15661.md; backported to release-0.19 in pr-15667.md/pr-15700.md).

## Zero-count PodSets and flavor selection

With `count = 0` every request is scaled to zero, so every flavor "fits" and the first flavor in the ClusterQueue wins by position. Its `nodeLabels` are then stamped into the Job's pod template at unsuspend, and elastic Jobs never re-suspend, so a later scale-up can never be admitted elsewhere. This happens when an elastic Job is created at `parallelism: 0` as well as after a full drain. The fix probes each flavor against **one pod** of the PodSet (potential capacity, not currently available quota; the probe never enters the request map, so accounted usage stays zero) and skips flavors that cannot hold a single pod. If no flavor passes, assignment falls back to the old behaviour with a warning event, so workloads with only zero-count PodSets are still admitted. It does not repair an already-stuck Job because the damage is in the pod template (source: pr-15444.md; fixes issue-14792.md; backports pr-16078.md, pr-16079.md). A related TAS fix covers mixed groups containing zero-count PodSets (source: pr-16174.md).

## Pod tracking and TAS across slices

- The tracker controller follows only the **active** WorkloadSlice; before, pod tracking could follow a finished or deleted origin slice (source: pr-15531.md).
- With TAS, Pod annotations keep pointing at the **origin** slice. The topology ungater now resolves the latest active slice before reading its admission and records ungating expectations under the stable origin name; previously grown Pods stayed gated or reconcile reported `pending ungate operations` (source: pr-15578.md, backport pr-15693.md/pr-15706.md).
- Growing an elastic TAS Workload (e.g. 2 to 4 one-CPU Pods on a 4-CPU node) was classified as needing preemption because the snapshot already charged the old slice and elastic placement counted it again. The replaced slice's TAS usage is temporarily removed during placement, then the snapshot is restored (source: pr-15579.md, backports pr-15586.md/pr-15634.md).

## MultiKueue and elastic slices

- An evicted, quota-less scale-up slice was always treated as "scale-up in progress", so reconciliation returned before deleting its remote Workload and job. Evicted slices are now excluded from that shortcut so the normal no-quota-reservation path removes the remote objects (source: pr-15871.md; backports pr-16178.md, pr-16179.md).
- For an autoscaling **RayJob** on a worker cluster, the live replica counts sit in the child RayCluster that KubeRay creates. MultiKueue now queues the manager Workload directly from child RayCluster events instead of waiting for KubeRay to mirror the change into `RayJob.status`. KubeRay copies the origin/prebuilt-workload markers onto the child; after the remote job is repointed to a replacement slice the child's marker is stale (names the finished origin), so the handler resolves it through the slice chain (index from pr-14703) and queues the **currently admitted** slice (source: pr-16315.md; issue-13243.md). See [[multikueue]].

## Known open gaps

Slice replacement can overcommit cohort quota ([[issue-16118]]); a replaced slice can remain in the TAS snapshot ([[issue-16119]]); the scheduler can panic when an elastic TAS PodSet group scales workers 0 to 1 ([[issue-16239]]); `SchedulingEquivalenceHashing` does not yet handle slice-replacement state ([[issue-14230]]) (all open at the time of writing; source: the cited issue files).

## Related pages

- [[workload]] — gets sliced when elastic.
- [[admission]] — per-slice.
- [[integration-rayjob]] — primary elastic consumer.
- [[gang-scheduling]] — the anti-pattern.
