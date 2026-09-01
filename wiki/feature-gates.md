# Feature gates

**Summary**: Kueue follows the Kubernetes feature-gate convention: new features land alpha → beta → GA, with a named gate (`--feature-gates=Foo=true|false`) controlling the on/off switch. Each graduation updates the default (alpha defaults off, beta defaults on, GA locked on).

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-09-01

---

## Canonical lifecycle

For each gate:

1. **Alpha.** Off by default. Breaking API changes permitted. Code shipped but opt-in.
2. **Beta.** On by default, opt-out remains. API considered stable; changes are deprecation-worthy.
3. **GA.** Locked on; the gate is deprecated and then removed.

The graduation of gates is tracked via dedicated issues per gate per release — e.g. "KEP 2936 (LocalQueueDefaulting): stage not updated for GA promotion" ([[issue-9633]]) caught a missed graduation update.

## Gates that have shipped

Representative subset (not exhaustive):

- **`QueueVisibility`** — the original [[visibility-api]] gate; later deprecated ([[issue-2256]] — Deprecate the QueueVisibility feature gate and corresponding API).
- **`LocalQueueDefaulting`** (KEP-2936) — allows a namespace to designate a default LocalQueue for jobs without the `queue-name` label. Graduated to GA in v0.17 ([[issue-9633]] — confirms v0.17 GA). See [[local-queue-defaulting]].
- **`FairSharing`** — see [[fair-sharing]] and KEP-1714 ([[pr-1773]]).
- **`AdmissionFairSharing`** (KEP-4136) — **Beta**. Admission-time ordering by historical usage; orthogonal to `FairSharing` (which is preemption-based). See [[admission-fair-sharing]].
- **`TopologyAwareScheduling`** — see [[topology-aware-scheduling]], Alpha-to-Beta tracked in [[issue-3450]].
- **`MultiKueue`** — see [[multikueue]]; the MultiKueue admission check and its controller sit behind the gate.
- **`MultiKueueOrchestratedPreemption`** (KEP-8303) — **Alpha**. Serializes preemption across MultiKueue worker clusters via preemption gates. See [[multikueue-orchestrated-preemption]].
- **`ElasticJobsViaWorkloadSlices`** (KEP-77) — graduating to **Beta**; [[pr-11300]] adds the webhook validations that guard the workload-slice elastic-job path (invalid configurations are now rejected at admission time), and [[pr-11327]] hardens the slice-normalization invariant exercised under beta stress testing. See [[elastic-jobs]].
- **`ConcurrentAdmission`** (KEP-8691) — **Alpha**. Lets one Workload pursue multiple ResourceFlavors concurrently via Variant Workloads. See [[concurrent-admission]].
- **`AdmissionCheckRetry`** — see [[admission-check]]; governs retry-across-flavors semantics (claim needs verification — no ingested source confirms this gate or its exact semantics).
- **`AdmissionGatedBy`** (KEP-6915) — **Alpha**. Honors the `kueue.x-k8s.io/admission-gated-by` annotation so external controllers can delay admission. See [[admission-gated-by-annotation]].
- **`WorkloadPriorityBoost`** (KEP-7990) — **Alpha**. Honors the `kueue.x-k8s.io/priority-boost` annotation; computes effective priority for scheduling and preemption candidate selection. See [[preemption-cost]].
- **`FailureRecovery`** (KEP-6757) — **Alpha**. Force-deletes zombie pods stuck `Terminating` after node failure when the pod opted in via `safe-to-forcefully-delete`. See [[failure-recovery]].
- **`MaxExecTime`** (KEP-3125) — **Beta**, on by default since v0.9. Enforces `spec.maximumExecutionTimeSeconds` per Workload. See [[workload-max-execution-time]].
- **`ManagedJobsNamespaceSelectorAlwaysRespected`** (KEP-3589) — strengthens `managedJobsNamespaceSelector` so jobs in non-matching namespaces are never managed even if labeled. See [[manage-jobs-selectively]].
- **`KueueDRAIntegration` (was `DynamicResourceAllocation`) / KEP-2941** — **Alpha (v0.18), off by default.** DRA support for [[resource-flavor]] / partitionable devices ([[pr-3071]] — DRA design; [[pr-8734]] — extended resources design for DRA integration; [[pr-10283]] — partitionable devices). The gate was **renamed** in v0.18 to avoid a name collision with the *upstream Kubernetes* `DynamicResourceAllocation` gate, which broke the scheduler-library integration ([[pr-11255]], fixes [[issue-11248]]). See [[dra]].
- **`KueueDRAIntegrationExtendedResource` (was `DRAExtendedResources`)** (KEP-2941) — **Alpha (v0.18), off by default.** Companion gate that enables the extended-resource path for DRA; validation at startup (`validateDRAFeatureGateDependencies`) **rejects** enabling it unless `KueueDRAIntegration` is also enabled. See [[dra]].
- **DRA gate rename (v0.18)** — the old gate names `DynamicResourceAllocation` and `DRAExtendedResources` are **deprecated and `LockToDefault: true`** in v0.18 (slated for removal in v0.19). `cmd/kueue/main.go` calls `MigrateDeprecatedDRAFeatureGates` *before* config validation: it logs a deprecation warning and maps old→new. If an operator sets both an old and its new gate to conflicting values, the **new (canonical)** gate wins (decided via an `ExplicitlySet` check). ([[pr-11255]])
- **`SparkApplicationIntegration`** — **Alpha**. Enables the Kueue integration for Kubeflow Spark Operator v2 SparkApplication. See [[integration-spark]].
- **`FairSharingPrioritizeNonBorrowing`** — see [[fair-sharing]] ([[issue-10126]]).
- **`BorrowWithinCohort` policies** — `LowerPriorityBorrowersOnly` added to protect nominal quota ([[issue-10171]]).
- **`FinishOrphanedWorkloads`** — **Beta, default-on** once the structural fix landed. When enabled, the workload controller marks Workloads whose owning Job/JobSet/etc. cannot be found as `Finished=True` with `OwnerNotFound`. Was promoted to Beta as part of the [[pr-10274]] fix for stuck Deployment-evicted workloads, but a race between the JobReconciler's structured informer and the workload-controller's `PartialObjectMetadata` informer caused brand-new Workloads to be finished within milliseconds of creation. [[pr-11010]] temporarily downgraded the gate to Alpha (off by default) in v0.18 / v0.16.7 / v0.17.2 to stop the bleeding, and [[pr-11014]] independently strengthened `Manager.RequeueWorkload` to refuse to requeue Workloads that are already `Finished`. The structural fix is [[pr-11296]]: `ReconcileGenericJob` (`pkg/controller/jobframework/reconciler.go`) now *finishes* an orphaned Workload only under the proper conditions (rather than right after owner creation), and the gate's spec was flipped back from `{0.18, Default:false, Alpha}` to `{0.18, Default:true, Beta}`. Tracked in [[issue-10901]]. See [[scheduler-internals#Admitted workloads must leave preemptionExpectations]] for the requeue-guard context and [[workload-garbage-collection]].
- **`QuotaCheckStrategy`** — **Alpha (new in v0.18)**. Gates the `resources.quotaCheckStrategy` configuration field on the [[cluster-queue]]; setting it to `IgnoreUndeclared` admits Workloads requesting resources the CQ does not list (those resources don't count against quota). PR #9808.
- **`RejectUpdatesToCQWithInvalidOnFlavors`** — **Alpha (new in v0.18, action-required)**. When enabled, ClusterQueue updates that reference invalid flavors in `AdmissionCheckStrategy.OnFlavors` are rejected at the validation webhook. Operators must fix any pre-existing invalid references before flipping the gate on.
- **`SchedulingEquivalenceHashing`** — **Beta, default on, since v0.18** ([[pr-11097]], fixes [[issue-10005]]). When a Workload can't be admitted and is requeued to the inadmissible set, Workloads with the same scheduling hash are bulk-moved together instead of re-evaluated one at a time — an admission-throughput optimization. v0.18 **narrows** the trigger to two requeue reasons only — `RequeueReasonNoFit` and `RequeueReasonPreemptionNoCandidates` — so namespace-mismatched or preemption-gated Workloads are no longer incorrectly bulk-moved (the prior bug). See [[scheduler-internals]]. Trade-off: a single Workload that consumes ~100% of a CQ's quota regresses on time-to-admission (it waits for the requeue batch / a capacity event). [[pr-11399]] folds each PodSet's **effective** `TotalRequests.Requests` (key `"requests"`) into `computeSchedulingHash`, not just the PodSet spec shape — necessary because [[dra]] preprocessing rewrites a device-class resource into its DeviceClass-mapped logical resource in `TotalRequests` *without* mutating the pod spec, so two semantically different DRA Workloads would otherwise hash identically and wrongly share an equivalence-cache result.
- **`TASHandleOverlappingFlavors`** — **Alpha (new in v0.18), off by default** ([[pr-11210]]). Fixes node over-subscription when two TAS [[resource-flavor]]s reference the same Topology and share the same hostname-leaf nodes. The whole aggregation path is guarded by this gate; with it off the old per-flavor usage tracking remains (avoids a perf regression on large TAS clusters). See [[topology-aware-scheduling]].
- **`TASReplaceNodeOnNodeTaints`** — gates TAS NodeHotSwap on node taints: when a node assigned to an admitted Workload gains a `NoExecute`/`NoSchedule` taint the Workload's pods are relocated. [[pr-11185]] fixed it to evaluate taints against the Workload's **effective** tolerations (PodSet template + assigned ResourceFlavor + AdmissionCheck `PodSetUpdates`), not just the raw PodSet template. See [[topology-aware-scheduling]].
- **`MultiKueueManagerQuotaAutomation`** — **Alpha (new in v0.18), off by default** ([[pr-11141]], KEP-9988 "Alpha1" scope). When enabled (and opted in per-config via `MultiKueueConfig.spec.quotaAutomation.mode: Automated`), a manager [[cluster-queue]]'s nominal quota is kept equal to the sum of the corresponding worker-cluster quotas. See [[multikueue]].
- **`MultiKueueIncrementalDispatcherConfig`** — **Beta, on by default** ([[pr-11208]], KEP-9270, registered at v0.19). Enables the `multiKueue.incrementalDispatcherConfig.stepSize` config field controlling how many worker clusters the Incremental Dispatcher nominates per round (default 3, minimum 1). See [[multikueue]].
- **`KubeRayAccountForRedisCleanup`** — **Beta, on by default** ([[pr-11260]], introduced at v0.19, GA targeted v0.21). When KubeRay GCS fault tolerance is enabled, folds the hardcoded Redis-cleanup Job requests (200m CPU / 256Mi memory) into the Ray head PodSet so they count against quota. Acts as a bailout for clusters that set `ENABLE_GCS_FT_REDIS_CLEANUP=false` on the KubeRay operator. See [[integration-rayjob]].
- **`WorkloadIdentifierAnnotations`** — **default-enabled** ([[pr-11409]], cherry-picked to release-0.17 as the CP of #10311). Lets Kueue's PodGroup identifiers — `kueue.x-k8s.io/pod-group-name` and `kueue.x-k8s.io/prebuilt-workload-name` — be supplied as either labels (the existing API) **or** annotations. Motivation: setting them as *labels* meant they were subject to the 63-character label-value limit, so a [[integration-leaderworkerset]] whose name exceeded 39 characters failed pod creation with `metadata.labels: Invalid value`. With the gate on, LWS uses the annotation counterparts, raising the supported name length to 52 characters; manual PodGroup definition via labels remains valid. See [[integration-plain-pod]].

### v0.18 graduations

The following gates graduated to **Stable** in v0.18.0 (per [[issue-10861]] release notes):

- `MultiKueueRedoAdmissionOnEvictionInWorker` (#10695) — see [[multikueue]].
- `MultiKueueWaitForWorkloadAdmitted` (#10656) — see [[multikueue]].
- `SkipFinalizersForPodsSuspendedByParent` (#10645) — Pod-integration internal: don't add Kueue finalizers on pods that the parent has already suspended.

> Configuration-only knobs (not feature gates) used by the new pages:
> - `objectRetentionPolicies.workloads.afterFinished` / `afterDeactivatedByKueue` — controls [[workload-garbage-collection]] (KEP-1618).
> - `integrations.frameworks` (with `"statefulset"`, `"trainjob"`) — enables [[integration-statefulset]] / [[integration-trainjob]]; both are framework toggles, not gates.

## User-specified gate parameters are validated

Feature-gate names and values supplied by the operator (via the Kueue Configuration `featureGates` map or `--feature-gates`) are now **verified** rather than silently accepted. The fix originated on main as #10931 and was cherry-picked to the release branches as [[pr-11288]] (release-0.17) and [[pr-11291]] (release-0.16) — release note: "FeatureGates: Fixed a bug that user-specified feature gate parameters are not verified." After the fix, an unknown gate name or an invalid value is rejected at startup instead of being ignored.

## When a gate graduates

Graduation is primarily a documentation + defaults change; the code typically stays the same. Missed graduation issues ([[issue-9633]]) are usually about forgetting to flip the stage annotation in the code so release tooling knows the new status.

## Gates added or changed in v0.19 / v0.20

All entries below are **merged and shipped**. Where a gate has a different stage on `main` (v0.20) than on the release branches, both are given — this asymmetry is deliberate and is described under "Registering a gate on a release branch" below.

### Scheduling / preemption

- **`PrioritizePreemptorWorkloads`** — **Alpha, off by default** ([[pr-13797]], fixes #13662; cherry-picks [[pr-14682]]/0.19, [[pr-14683]]/0.18). Sorts a ClusterQueue's tracked *preemptor* Workload to the head of the scheduling iterator so the quota freed by staggered evictions is re-locked into the snapshot before competitors can steal it. Cures preemption thrashing when a preemptor needs several victims that finish evicting at different times. See [[scheduler-internals#Preemptor prioritization]] and [[preemption]].
- **`RecomputeAssignmentUponPreemptionTargetsOverlap`** — **Beta** ([[pr-14246]]/0.19, [[pr-14248]]; original #13863, fixes #13320). Recomputes an assignment produced during nomination when its preemption targets overlap targets already claimed earlier in the *same* cycle, instead of skipping the entry. Fixes starvation of a large "hero" Workload on a busy cluster. Previously such an entry was simply marked `skipped` (Phase 5, step 4 of [[scheduler-internals]]).
- **`TASRecomputeAssignmentWithinSchedulingCycle`** — the TAS counterpart. **Action required**: it could previously be enabled while `TopologyAwareScheduling` was off, which is meaningless; [[pr-14256]] (original #14237) makes it *depend* on `TopologyAwareScheduling`. If you disable TAS you must also set `TASRecomputeAssignmentWithinSchedulingCycle=false` before upgrading, or the manager refuses the configuration.
- **`FairSharingReevaluatePreemptionCandidates`** — **Alpha, off by default** ([[pr-14128]], fixes [[issue-14122]]; cherry-picks [[pr-14767]], [[pr-14768]]). Re-runs the first fair-sharing strategy over the retry candidates when the first pass did not fit *and* it preempted Workloads from the preemptor's own ClusterQueue (which lowers the preemptor's DRS and can make previously-unfair candidates fair). The release note warns that enabling it increases exposure to the known fair-sharing preemption loop [[issue-14543]] (still open). See [[fair-sharing#Re-evaluating candidates after preempting from the preemptor's own CQ]].
- **`SchedulingEquivalenceHashingIgnorePodSetName`** — **Beta, on by default on main (registered at 0.20)**; **Alpha, off by default on release-0.19** ([[pr-14784]]; branch variants [[pr-14804]], [[pr-14805]]). Excludes each PodSet's `Name` from the scheduling-equivalence hash, because flavor assignment never reads it. Requires `SchedulingEquivalenceHashing`. Motivation: the Pod-group integration derives the PodSet name from the client-settable `kueue.x-k8s.io/role-hash` annotation, so a client that stamps a unique role hash per Workload got one equivalence class per Workload and the bulk-move-to-inadmissible optimization never matched. PodSet *ordering* and resource shape remain significant.

### TAS

- **`TASCacheTopologyTree`** — **Beta, on by default on main**; **Alpha, off by default on release-0.19** ([[pr-13819]], part of #12580; cherry-picks [[pr-14639]], [[pr-14644]]). Caches an immutable topology tree per TAS flavor and reuses it across scheduler snapshots while scheduling-relevant Node data (labels, taints, allocatable) is unchanged. Measured on 2,500 nodes × 15 TAS flavors: **−71.7% CPU, −61.0% allocated bytes, −64.5% allocations** when the tree is reused; **+5.6% CPU** in the pathological case where it is invalidated every cycle. See [[topology-aware-scheduling#Cached topology trees]].

### Integrations

- **`ValidateRayAndSparkJobUpdates`** — **Beta, on by default** ([[pr-13293]]; cherry-picks [[pr-14666]], [[pr-14676]]). Rejects removal of the `kueue.x-k8s.io/queue-name` label from RayJob / RayCluster / RayService / SparkApplication. See [[integration-rayjob]].
- **`MultiKueueBatchJobClearingTTLSecondsAfterFinishedOnWorkerCluster`** — **Beta, on by default on main (v0.20)**; **Alpha, off by default on release-0.18/0.19** ([[pr-14734]]; branch variants [[pr-14827]], [[pr-14828]]). Omits `spec.ttlSecondsAfterFinished` when MultiKueue creates the remote worker Job. See [[multikueue#Worker Job TTL]]. GA graduation is tracked in [[issue-14826]].
- **`ElasticJobsViaWorkloadSlicesWithPartialReplicaScaleUp`** — **Alpha, off by default** ([[pr-14909]], part of #12100). Opt-in per job via the `kueue.x-k8s.io/elastic-job-scale-up-strategy` annotation (`atomic` — the default — or `partial`). When enabled *and* the annotation is `partial` *and* `minReplicas` is set, the RayCluster worker PodSet gets `MinCount` = effective minimum worker count instead of a fixed count. No behaviour change with the gate off. See [[elastic-jobs]].

### Configuration validation

- **`ReservedResourceNameValidation`** — **Beta, on by default on main (registered at 0.20)** ([[pr-14778]]); **Alpha, off by default on release-0.18 and release-0.19** ([[pr-14773]], [[pr-14774]], fixes [[issue-14763]]). Gates the refusal of `pods` as a [[dra]] `deviceClassMappings[].name` or in any of the three [[resource-transformer]] positions (`input`, `multiplyBy`, `outputs`). The gate exists purely as an **upgrade escape hatch**: Kueue configuration validation failure calls `os.Exit`, so a cluster whose config named `pods` (accepted by every release up to v0.18.6 / v0.19.2) would crash-loop the manager immediately on upgrade with no way to fix it at rollout time. Registering the name on `main` as well is required because `Set`/`SetFromMap` return `unrecognized feature gate` for an unregistered name and `main.go` exits on that — so an operator who set the gate on 0.18/0.19 would otherwise crash-loop one release later. See [[dra#The reserved `pods` resource name]].
- **`RejectUpdatesToCQWithInvalidOnFlavors`** — graduated **Alpha → Beta, on by default** ([[pr-14776]]).

### Removed

- **`LendingLimit`** — the gate is **removed** ([[pr-13067]]); `lendingLimit` is now unconditional. See [[borrowing-and-lending]].
- **`MultiKueueBatchJobWithManagedBy`**, **`HierarchicalCohorts`**, **`ObjectRetentionPolicies`** — checked off as removed in the gate-cleanup umbrella below, i.e. the corresponding behaviour is unconditional; the removal PRs themselves are not in the ingested corpus. See [[multikueue]], [[cohort]], [[workload-garbage-collection]].

### The gate-cleanup umbrella ([[issue-12927]])

@mimowo audits `pkg/features/kube_features.go` periodically and batches the mechanical graduations/removals into one issue. Status of that list as of 2026-09-01 (source: issue-12927.md; items marked done there are shipped, the rest are not — do not rely on them):

| Gate | Target | Done? |
|---|---|---|
| `ManagedJobsNamespaceSelectorAlwaysRespected` | Stable | yes |
| `LendingLimit`, `MultiKueueBatchJobWithManagedBy`, `HierarchicalCohorts`, `ObjectRetentionPolicies` | removed | yes |
| `MultiKueueKubeConfigPathValidation` | Beta | yes (#13706) |
| `RejectUpdatesToCQWithInvalidOnFlavors` | Beta | yes ([[pr-14776]]) |
| `QuotaCheckStrategy` | Beta | yes |
| `WorkloadPriorityClassDefaulting` | Beta (default-on at v0.20) | yes |
| `TASProfileMixed`, `AssignQueueLabelsForPods` | Stable | no |
| `PriorityBoost` | Beta | no — deliberately deferred |

Two things worth carrying forward from the discussion: bundling is only appropriate for gates whose graduation is mechanical (removal always is; Beta/Stable promotion has per-feature criteria — `PartialAdmission` is the standing counter-example), and an opt-in-by-Configuration feature is treated as safe enough to promote without broad alpha feedback because the config field is the second switch. `PriorityBoost`'s promotion is held pending the direction of configurable preemption rules, since that mechanism may subsume boost scoping ([[preemption-cost]]).

### Workload-aware scheduling (WAS) — alpha, opt-in

- **`SchedulerLibraryIntegration`** — **Alpha, off by default**. Delegates work to the upstream `scheduler-library` instead of re-implementing it in Kueue.
  - [[pr-14203]] / [[pr-14613]]: TAS no longer applies node-readiness and `spec.unschedulable` filtering when building the TAS node cache; the scheduler library does it.
  - [[pr-14551]] / [[pr-14796]]: Pods created by Kueue-managed jobs get the `kueue.x-k8s.io/workload` annotation (previously only `TopologyAwareScheduling` added it), so a Workload can be matched back to its Pods in the library's cluster cache. Resolution order is workload → prebuilt-workload → group → slice annotation.

## Registering a gate on a release branch

Kueue never sets an emulation version, so the effective version used by `featureSpecAtEmulationAndMinCompatVersion` is Kubernetes' `DefaultKubeBinaryVersion` (1.36 at the time of writing), **not** the Kueue version. `featureSpecAtEmulationAndMinCompatVersion` selects the highest spec at or below that version, so a spec written as `{0.20, Default: true, Beta}` is still selected on a release-0.19 build and the gate lands **enabled by default there too**. A cherry-pick that wants the gate off on the branch must therefore rewrite the spec as `{0.19, Default: false, Alpha}` rather than reuse the main spec. ([[pr-14804]])

Gate *dependencies* are also tracked differently per branch: `main` uses the `defaultFeatureGateDependencies` map in `pkg/features`, while release branches use `validateFeatureGateDependency` in `pkg/config/validation.go`. Both surface as a startup configuration error. ([[pr-14804]], [[pr-14256]])

## Related pages

- [[release-process]] — when gates graduate.
- [[fair-sharing]], [[topology-aware-scheduling]], [[multikueue]], [[elastic-jobs]] — feature-area pages that reference their gates.
