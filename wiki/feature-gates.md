# Feature gates

**Summary**: Kueue follows the Kubernetes feature-gate convention: new features land alpha → beta → GA, with a named gate (`--feature-gates=Foo=true|false`) controlling the on/off switch. Each graduation updates the default (alpha defaults off, beta defaults on, GA locked on).

**Sources**: `raw/github/kubernetes-sigs__kueue/`, `raw/kueue/site/data/featuregates/versioned_feature_list.yaml`, `raw/kueue/site/data/featuregates/removed_feature_list.yaml`, `raw/kueue/pkg/features/kube_features.go`, pr-15889.md, pr-15562.md, pr-15623.md, pr-16235.md, pr-15000.md, pr-15503.md, pr-15734.md, pr-16059.md, pr-13063.md, pr-13706.md, pr-13719.md, pr-16347.md, pr-16362.md, pr-16436.md, pr-17167.md, pr-17285.md, pr-16035.md, pr-16340.md, pr-17295.md, pr-17296.md, pr-17370.md (open), raw/kueue/CHANGELOG/CHANGELOG-0.20.md, raw/kueue/CHANGELOG/CHANGELOG-0.19.md, pr-16460.md, pr-16493.md, pr-15280.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, raw/kueue/CHANGELOG/CHANGELOG-0.19.md (kube_features.go read at kueue@8922c563e), pr-13316.md, pr-16470.md, pr-16343.md

**Last updated**: 2026-10-28

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
- **`MultiKueueOrchestratedPreemption`** (KEP-8303) — **Beta, on by default since v0.20** (Alpha v0.17-v0.19, [[pr-16235]]). Serializes preemption across MultiKueue worker clusters via preemption gates. See [[multikueue-orchestrated-preemption]].
- **`ElasticJobsViaWorkloadSlices`** (KEP-77) — graduating to **Beta**; [[pr-11300]] adds the webhook validations that guard the workload-slice elastic-job path (invalid configurations are now rejected at admission time), and [[pr-11327]] hardens the slice-normalization invariant exercised under beta stress testing. See [[elastic-jobs]].
- **`ConcurrentAdmission`** (KEP-8691) — **Alpha**. Lets one Workload pursue multiple ResourceFlavors concurrently via Variant Workloads. See [[concurrent-admission]].
- **AdmissionCheck retries** (KEP-3258) — no feature gate; disabled through the Configuration API (`AdmissionCheckRetry` is an API type, not a gate). See [[admission-check]].
- **`AdmissionGatedBy`** (KEP-6915) — **Beta, on by default since v0.19** (Alpha 0.17–0.18). Honors the `kueue.x-k8s.io/admission-gated-by` annotation so external controllers can delay admission. See [[admission-gated-by-annotation]].
- **`PriorityBoost`** (KEP-7990) — **Alpha**. Honors the `kueue.x-k8s.io/priority-boost` annotation; computes effective priority for scheduling and preemption candidate selection. See [[preemption-cost]].
- **`FailureRecoveryPolicy`** (KEP-6757) — **Alpha**. Force-deletes zombie pods stuck `Terminating` after node failure when the pod opted in via `safe-to-forcefully-delete`. See [[failure-recovery]].
- **Maximum execution time** (KEP-3125) — no feature gate; Beta since v0.9, GA in v0.19. Enforces `spec.maximumExecutionTimeSeconds` per Workload. See [[workload-max-execution-time]].
- **`ManagedJobsNamespaceSelectorAlwaysRespected`** (KEP-3589) — strengthens `managedJobsNamespaceSelector` so jobs in non-matching namespaces are never managed even if labeled. See [[manage-jobs-selectively]].
- **`KueueDRAIntegration` (was `DynamicResourceAllocation`) / KEP-2941** — **Beta, on by default since v0.18** (#10996). DRA support for [[resource-flavor]] / partitionable devices ([[pr-3071]] — DRA design; [[pr-8734]] — extended resources design for DRA integration; [[pr-10283]] — partitionable devices). The gate was **renamed** in v0.18 to avoid a name collision with the *upstream Kubernetes* `DynamicResourceAllocation` gate, which broke the scheduler-library integration ([[pr-11255]], fixes [[issue-11248]]). See [[dra]].
- **`KueueDRAIntegrationExtendedResource` (was `DRAExtendedResources`)** (KEP-2941) — **Alpha (v0.18), off by default.** Companion gate that enables the extended-resource path for DRA; validation at startup (`validateDRAFeatureGateDependencies`) **rejects** enabling it unless `KueueDRAIntegration` is also enabled. See [[dra]].
- **DRA gate rename (v0.18)** — the old gate names `DynamicResourceAllocation` and `DRAExtendedResources` are **deprecated and `LockToDefault: true`** in v0.18 (slated for removal in v0.19). `cmd/kueue/main.go` calls `MigrateDeprecatedDRAFeatureGates` *before* config validation: it logs a deprecation warning and maps old→new. If an operator sets both an old and its new gate to conflicting values, the **new (canonical)** gate wins (decided via an `ExplicitlySet` check). ([[pr-11255]])
- **`SparkApplicationIntegration`** — **Alpha**. Enables the Kueue integration for Kubeflow Spark Operator v2 SparkApplication. See [[integration-spark]].
- **`FairSharingPrioritizeNonBorrowing`** — see [[fair-sharing]] ([[issue-10126]]).
- **`BorrowWithinCohort` policies** — `LowerPriorityBorrowersOnly` proposed to protect nominal quota ([[issue-10171]]); its PR #10211 is not merged, so only `Never`/`LowerPriority` exist.
- **`FinishOrphanedWorkloads`** — **Beta, default-on** once the structural fix landed. When enabled, the workload controller marks Workloads whose owning Job/JobSet/etc. cannot be found as `Finished=True` with `OwnerNotFound`. Was promoted to Beta as part of the [[pr-10274]] fix for stuck Deployment-evicted workloads, but a race between the JobReconciler's structured informer and the workload-controller's `PartialObjectMetadata` informer caused brand-new Workloads to be finished within milliseconds of creation. [[pr-11010]] temporarily downgraded the gate to Alpha (off by default) in v0.18.0 / v0.16.8 / v0.17.3 to stop the bleeding, and [[pr-11014]] independently strengthened `Manager.RequeueWorkload` to refuse to requeue Workloads that are already `Finished`. The structural fix is [[pr-11296]]: `ReconcileGenericJob` (`pkg/controller/jobframework/reconciler.go`) now *finishes* an orphaned Workload only under the proper conditions (rather than right after owner creation), and the gate's spec was flipped back from `{0.18, Default:false, Alpha}` to `{0.18, Default:true, Beta}`. Tracked in [[issue-10901]]. See [[scheduler-internals#Admitted workloads must leave preemptionExpectations]] for the requeue-guard context and [[workload-garbage-collection]].
- **`QuotaCheckStrategy`** — **Alpha (new in v0.18)**. Gates the `resources.quotaCheckStrategy` configuration field on the [[cluster-queue]]; setting it to `IgnoreUndeclared` admits Workloads requesting resources the CQ does not list (those resources don't count against quota). PR #9808.
- **`RejectUpdatesToCQWithInvalidOnFlavors`** — **Alpha (new in v0.18, action-required)**. When enabled, ClusterQueue updates that reference invalid flavors in `AdmissionCheckStrategy.OnFlavors` are rejected at the validation webhook. Operators must fix any pre-existing invalid references before flipping the gate on.
- **`SchedulingEquivalenceHashing`** — **Beta, default on, since v0.18** ([[pr-11097]], fixes [[issue-10005]]). When a Workload can't be admitted and is requeued to the inadmissible set, Workloads with the same scheduling hash are bulk-moved together instead of re-evaluated one at a time — an admission-throughput optimization. v0.18 **narrows** the trigger to two requeue reasons only — `RequeueReasonNoFit` and `RequeueReasonPreemptionNoCandidates` — so namespace-mismatched or preemption-gated Workloads are no longer incorrectly bulk-moved (the prior bug). See [[scheduler-internals]]. Trade-off: a single Workload that consumes ~100% of a CQ's quota regresses on time-to-admission (it waits for the requeue batch / a capacity event). [[pr-11399]] folds each PodSet's **effective** `TotalRequests.Requests` (key `"requests"`) into `computeSchedulingHash`, not just the PodSet spec shape — necessary because [[dra]] preprocessing rewrites a device-class resource into its DeviceClass-mapped logical resource in `TotalRequests` *without* mutating the pod spec, so two semantically different DRA Workloads would otherwise hash identically and wrongly share an equivalence-cache result.
- **`TASHandleOverlappingFlavors`** — **Beta, on by default since v0.18** ([[pr-11210]]; review discussed Alpha, but the merged commit 7b57e1111 registers `{0.18, Beta, on}`). Fixes node over-subscription when two TAS [[resource-flavor]]s reference the same Topology and share the same hostname-leaf nodes. The whole aggregation path is guarded by this gate; with it off the old per-flavor usage tracking remains. See [[topology-aware-scheduling]].
- **`TASReplaceNodeOnNodeTaints`** — gates TAS NodeHotSwap on node taints: when a node assigned to an admitted Workload gains a `NoExecute`/`NoSchedule` taint the Workload's pods are relocated. [[pr-11185]] fixed it to evaluate taints against the Workload's **effective** tolerations (PodSet template + assigned ResourceFlavor + AdmissionCheck `PodSetUpdates`), not just the raw PodSet template. See [[topology-aware-scheduling]].
- **`MultiKueueManagerQuotaAutomation`** — **Alpha (new in v0.18), off by default** ([[pr-11141]], KEP-9988 "Alpha1" scope). When enabled (and opted in per-config via `MultiKueueConfig.spec.quotaManagement: Automated`; the field defaults to `Manual`. **Correction (2026-10-21):** this page earlier named the field `spec.quotaAutomation.mode`, which does not exist (source: raw/kueue/apis/kueue/v1beta2/multikueue_types.go)), a manager [[cluster-queue]]'s nominal quota is kept equal to the sum of the corresponding worker-cluster quotas. See [[multikueue]].
- **`MultiKueueIncrementalDispatcherConfig`** — **Beta, on by default** ([[pr-11208]], KEP-9270, registered at v0.19). Enables the `multiKueue.incrementalDispatcherConfig.stepSize` config field controlling how many worker clusters the Incremental Dispatcher nominates per round (default 3, minimum 1). See [[multikueue]].
- **`KubeRayAccountForRedisCleanup`** — never shipped: proposed as a Beta bailout in [[pr-11260]] and dropped before merge. When KubeRay GCS fault tolerance is enabled, the Redis-cleanup Job requests (200m CPU / 256Mi memory) are always folded into the Ray head PodSet. See [[integration-rayjob]].
- **`WorkloadIdentifierAnnotations`** — **default-enabled** ([[pr-11409]], cherry-picked to release-0.17 as the CP of #10311). Lets Kueue's PodGroup identifiers — `kueue.x-k8s.io/pod-group-name` and `kueue.x-k8s.io/prebuilt-workload-name` — be supplied as either labels (the existing API) **or** annotations. Motivation: setting them as *labels* meant they were subject to the 63-character label-value limit, so a [[integration-leaderworkerset]] whose name exceeded 39 characters failed pod creation with `metadata.labels: Invalid value`. With the gate on, LWS uses the annotation counterparts, raising the supported name length to 52 characters; manual PodGroup definition via labels remains valid. See [[integration-plain-pod]].

### v0.18 graduations

The following gates graduated to **Stable** in v0.18.0 (per [[issue-10861]] release notes):

- `MultiKueueRedoAdmissionOnEvictionInWorker` (#10695) — see [[multikueue]].
- `MultiKueueWaitForWorkloadAdmitted` (#10656) — see [[multikueue]].
- `SkipFinalizersForPodsSuspendedByParent` (#10645) — Pod-integration internal: don't add Kueue finalizers on pods that the parent has already suspended. **Removed in v0.20** (pr-13316): it had been GA/locked since 0.18, and the StatefulSet/LWS legacy finalizer cleanup was removed with it (see [[integration-statefulset]]); the gate no longer exists in `kube_features.go` at kueue@8922c563e.

> Configuration-only knobs (not feature gates) used by the new pages:
> - `objectRetentionPolicies.workloads.afterFinished` / `afterDeactivatedByKueue` — controls [[workload-garbage-collection]] (KEP-1618).
> - `integrations.frameworks` (with `"statefulset"`, `"trainjob"`) — enables [[integration-statefulset]] / [[integration-trainjob]]; both are framework toggles, not gates.

## User-specified gate parameters are validated

Feature-gate names and values supplied by the operator (via the Kueue Configuration `featureGates` map or `--feature-gates`) are now **verified** rather than silently accepted. The fix originated on main as #10931 and was cherry-picked to the release branches as [[pr-11288]] (release-0.17) and [[pr-11291]] (release-0.16) — release note: "FeatureGates: Fixed a bug that user-specified feature gate parameters are not verified." After the fix, an unknown gate name or an invalid value is rejected at startup instead of being ignored.

## When a gate graduates

Graduation is primarily a documentation + defaults change; the code typically stays the same. Missed graduation issues ([[issue-9633]]) are usually about forgetting to flip the stage annotation in the code so release tooling knows the new status.

Reviewer expectations seen in this batch (source: pr-13063.md, pr-16493.md, pr-13719.md):

- **At Beta, update tests to the new default instead of pinning the gate off.** Pinning makes the later GA step non-mechanical, and a GA gate (`LockToDefault: true`) can no longer be disabled in tests at all.
- **Keep the earlier spec when adding a new one** (`{0.18 Alpha off}, {0.20 Beta on}`) so the versioned list stays accurate; regenerate `site/data/featuregates/*.yaml` with `make generate-featuregates`.
- **At GA, remove the gate checks** from the code path (pr-16493 dropped the `Enabled(MetricForWorkloadCreationLatency)` guards) and bump the KEP stage.
- Gates that add API writes graduate separately from gates that only change reporting, so either can be rolled back alone.

## Gates added or changed in v0.19 / v0.20

All entries below are **merged and shipped**. Where a gate has a different stage on `main` (v0.20) than on the release branches, both are given — this asymmetry is deliberate and is described under "Registering a gate on a release branch" below.

### Scheduling / preemption

- **`PrioritizePreemptorWorkloads`** — **Alpha, off by default** ([[pr-13797]], fixes #13662; cherry-picks [[pr-14682]]/0.19, [[pr-14683]]/0.18). Sorts a ClusterQueue's tracked *preemptor* Workload to the head of the scheduling iterator so the quota freed by staggered evictions is re-locked into the snapshot before competitors can steal it. Cures preemption thrashing when a preemptor needs several victims that finish evicting at different times. See [[scheduler-internals#Preemptor prioritization]] and [[preemption]].
- **`RecomputeAssignmentUponPreemptionTargetsOverlap`** — **Beta** ([[pr-14246]]/0.19, [[pr-14248]]; original #13863, fixes #13320). Recomputes an assignment produced during nomination when its preemption targets overlap targets already claimed earlier in the *same* cycle, instead of skipping the entry. Fixes starvation of a large "hero" Workload on a busy cluster. Previously such an entry was simply marked `skipped` (Phase 5, step 4 of [[scheduler-internals]]).
- **`TASRecomputeAssignmentWithinSchedulingCycle`** — the TAS counterpart. **Action required**: it could previously be enabled while `TopologyAwareScheduling` was off, which is meaningless; [[pr-14256]] (original #14237) makes it *depend* on `TopologyAwareScheduling`. If you disable TAS you must also set `TASRecomputeAssignmentWithinSchedulingCycle=false` before upgrading, or the manager refuses the configuration.
- **`FairSharingReevaluatePreemptionCandidates`** — **Alpha, off by default in v0.20 and the 0.19/0.18 backports; Beta/on at 0.21 on main** (pr-17285; [[pr-14128]], fixes [[issue-14122]]; cherry-picks [[pr-14767]], [[pr-14768]]). Re-runs the first fair-sharing strategy over the retry candidates when the first pass did not fit *and* it preempted Workloads from the preemptor's own ClusterQueue (which lowers the preemptor's DRS and can make previously-unfair candidates fair). The release note warns that enabling it increases exposure to the known fair-sharing preemption loop [[issue-14543]]. **Update (2026-10-21)**: that loop is fixed by pr-16343 behind `FairSharingVerifyFinalTargets` (Beta/on; shipped in v0.20.1 and v0.19.8). See [[fair-sharing]] and [[fair-sharing#Re-evaluating candidates after preempting from the preemptor's own CQ]].
- **`SchedulingEquivalenceHashingIgnorePodSetName`** — **Beta, on by default on main (registered at 0.20)**; **Alpha, off by default on release-0.19** ([[pr-14784]]; branch variants [[pr-14804]], [[pr-14805]]). Excludes each PodSet's `Name` from the scheduling-equivalence hash, because flavor assignment never reads it. Requires `SchedulingEquivalenceHashing`. Motivation: the Pod-group integration derives the PodSet name from the client-settable `kueue.x-k8s.io/role-hash` annotation, so a client that stamps a unique role hash per Workload got one equivalence class per Workload and the bulk-move-to-inadmissible optimization never matched. PodSet *ordering* and resource shape remain significant.

### TAS

- **`TASCacheTopologyTree`** — **Beta, on by default on main**; **Alpha, off by default on release-0.19** ([[pr-13819]], part of #12580; cherry-picks [[pr-14639]], [[pr-14644]]). Caches an immutable topology tree per TAS flavor and reuses it across scheduler snapshots while scheduling-relevant Node data (labels, taints, allocatable) is unchanged. Measured on 2,500 nodes × 15 TAS flavors: **−71.7% CPU, −61.0% allocated bytes, −64.5% allocations** when the tree is reused; **+5.6% CPU** in the pathological case where it is invalidated every cycle. See [[topology-aware-scheduling#Cached topology trees]].

### Integrations

- **`ValidateRayAndSparkJobUpdates`** — **Beta, on by default** ([[pr-13293]]; cherry-picks [[pr-14666]], [[pr-14676]]). Rejects removal of the `kueue.x-k8s.io/queue-name` label from RayJob / RayCluster / RayService / SparkApplication. See [[integration-rayjob]].
- **`MultiKueueBatchJobClearingTTLSecondsAfterFinishedOnWorkerCluster`** — **Alpha, off by default (registered at 0.20)**. **Correction (2026-10-21)**: this bullet said Beta/on on main; it was introduced that way by [[pr-14734]] (branch variants [[pr-14827]], [[pr-14828]] off) but #15126 changed it to Alpha/off before v0.20.0 ("Enable it explicitly to omit `ttlSecondsAfterFinished` from worker Jobs"), which is what `kube_features.go` at the snapshot and the table below show (source: CHANGELOG-0.20.md). Omits `spec.ttlSecondsAfterFinished` when MultiKueue creates the remote worker Job. See [[multikueue#Worker Job TTL]]. GA graduation is tracked in [[issue-14826]].
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

## Gates added or changed in v0.20: core scheduling, admission and configuration

Stages below are read from `pkg/features/kube_features.go` and the generated list (see the full table at the end of this page).

- **`ConfigurablePreemptions`** — **Alpha, off, new in 0.20** (pr-15889). Enables cluster-scoped `PreemptionConfig` rules referenced from a ClusterQueue annotation. No gate dependency. See [[configurable-preemptions]].
- **`DynamicQuotaOrchestration`** — **Alpha, off, new in 0.20**. Registers the DynamicQuotaOrchestrator controller and makes `status.effectiveQuotas` effective. See [[dynamic-quota-orchestration]].
- **`MultiKueueOrchestratedPreemption`** — graduated to **Beta/on in 0.20** ([[multikueue-orchestrated-preemption]]).
- **`MultiKueueReuseClientConnectionConfigForWorkers`** — **Beta, on, new in 0.20**, depends on `MultiKueue`. Applies `clientConnection` QPS/Burst to worker-cluster clients ([[multikueue]]).
- **`MultiKueueRayInTreeAutoscaling`** — **Alpha, off, new in 0.20**, depends on `MultiKueue`, `ElasticJobsViaWorkloadSlices` and, since v0.20.1, `SkipChildJobSuspension` (pr-16470; KEP-13243). Enabling it without `SkipChildJobSuspension` is a startup configuration error. See [[multikueue]].
- **`MultiKueueRemoteSpecSync`** — **Beta, on, new in 0.20**. Forwards manager-side spec edits (RayService `serveConfigV2`) to the worker copy.
- **`WorkloadLevelWaitForPodsReady`** — **Alpha, off, 0.20**. Per-Workload `kueue.x-k8s.io/wait-for-pods-ready` override (pr-15503). See [[wait-for-pods-ready]].
- **`WaitForPodsReadyUnscheduledTimeout`** — **Alpha, off, 0.20** (KEP-13502): separate timeout for unscheduled Pods.
- **`WaitForPodsReadyMaxNotReady`** — **Alpha, off, 0.20** (KEP-15423, pr-16059): `pod-group-max-not-ready-count` for Pod groups.
- **`PodIntegrationCountSucceededPodsAsReady`** — **Beta, on, 0.20** (pr-15734, cherry-picked to 0.19/0.18): a Succeeded Pod counts as ready.
- **`DisableWaitForPodsReady`** — **Alpha, off, since 0.19**; deprecated migration switch (removal planned in 0.21) for the fact that `waitForPodsReady` is now defaulted on. Enabling `WorkloadLevelWaitForPodsReady` or `WaitForPodsReadyUnscheduledTimeout` together with it is a startup error.
- **`UnadmittedWorkloadsObservability`** — **Beta, on in 0.20** (Alpha 0.19); pr-15562/pr-15623 corrected the declared stage (the release branches had it as Beta but off). **`UnadmittedWorkloadsExplicitStatus`** — Alpha, off, 0.19; depends on the former. See [[unadmitted-workloads-observability]].
- **`AdmissionFairSharingAnchorAtQuotaReservation`** — **Beta, on, 0.20**, depends on `AdmissionFairSharing` (pr-15000): AFS charges and samples at quota reservation instead of admission ([[admission-fair-sharing]]).
- **`FlavorFungibilityPreserveScanProgress`** — Beta, on, 0.20, depends on `FlavorFungibility`.
- **`FairSharingRefill`** — Alpha, off, 0.20 (KEP-14596 fair-sharing refill; the queue-side prep is the per-Workload inflight map, pr-15844).
- **`RecomputeAssignmentUponPreemptionTargetsOverlap`** and **`PrioritizePreemptorWorkloads`**: see the scheduling section above; stages in the table below.
- **Moved to the removed list with an end version of 0.20** (per `removed_feature_list.yaml`; treat as removed from the 0.20 registry, the file records `from`/`to` version ranges): `PropagateBatchJobLabelsToWorkload`, `MultiKueueWaitForWorkloadAdmitted`, `MultiKueueRedoAdmissionOnEvictionInWorker` (GA before removal), `SchedulerLongRequeueInterval`, `SchedulerTimestampPreemptionBuffer` (Alpha, dropped). Earlier removals include `LendingLimit`, `HierarchicalCohorts`, `ObjectRetentionPolicies`, `MultiKueueBatchJobWithManagedBy`, `QueueVisibility`.

### Stage corrections to older bullets on this page

The generated list (main, v0.20) disagrees with several stages stated earlier on this page, which were true when written: `AdmissionGatedBy` is **Beta/on since 0.19**; `KueueDRAIntegration` is **Beta/on since 0.18** and `KueueDRAIntegrationExtendedResource`/`PartitionableDevices` **Beta/on since 0.19**; `QuotaCheckStrategy` is **Beta/on since 0.19**; `TASHandleOverlappingFlavors` is **Beta/on since 0.18**; `WorkloadPriorityClassDefaulting` is Beta/on in 0.20; `MultiKueueKubeConfigPathValidation` is Beta/on in 0.20; `ManagedJobsNamespaceSelectorAlwaysRespected` is **GA (locked)** since 0.19; `TLSOptions` GA in 0.20. `MaxExecTime` and `KubeRayAccountForRedisCleanup` never existed as registered gates (see the corrected bullets above).

### Gate changes shipped in v0.20.0, v0.20.1 and on main (2026-10 batch)

Stages verified against `kube_features.go` at kueue@8922c563e (main, v0.21 dev) and the release changelogs.

#### Graduations

| Gate | Change | Effect / action |
|---|---|---|
| `UnadmittedWorkloadsObservability` | Alpha → **Beta/on in 0.20** (pr-13063) | tiered `QuotaReserved` reasons + `kueue_unadmitted_workloads`. `UnadmittedWorkloadsExplicitStatus` deliberately stays Alpha because it adds API writes ([[unadmitted-workloads-observability]]) |
| `MultiKueueKubeConfigPathValidation` | Alpha 0.19 → **Beta/on 0.20** (pr-13706, fixes #13704) | `locationType: Path` kubeconfigs must live under `/etc/multikueue/kubeconfigs/`; disabling restores "any file path", which the docs flag as a way to expose sensitive files ([[multikueue]], [[security-authn-authz]]) |
| `WorkloadPriorityClassDefaulting` | Alpha 0.18 → **Beta/on 0.20** (pr-13719, fixes #13689) | Workloads without a priority class get the WorkloadPriorityClass named `default`. Defaulting stays in the **Job webhook** (like `LocalQueueDefaulting`); moving it to the Workload level was moved to the GA criteria rather than dropped (review by @tenzen-y). 0.18/0.19 still need explicit enablement ([[workload-priority]]) |
| `MetricForWorkloadCreationLatency` | Beta 0.18 → **GA/locked 0.21** (pr-16493, main only) | metric always recorded ([[metrics]]) |

#### New gates

| Gate | Stage | What it does |
|---|---|---|
| `MultiKueueReuseClientConnectionConfigForWorkers` | Beta/on 0.20 (pr-15280, fixes #14973); depends on `MultiKueue` | applies `clientConnection` QPS/Burst to worker-cluster REST clients instead of client-go's 5/10 fallback. Was drafted as `MultiKueueClientConnection` Alpha; review (@kshalot) made it Beta/on for 0.20 and off in 0.18/0.19 cherry-picks — the release-note history shows both stage names, so trust the code ([[multikueue]]) |
| `HighMaxParallelismWithinReconcile` | Beta/on 0.20 (#16336); also shipped in v0.19.7 (#16387) and v0.18.11 (#16388) | max concurrent API updates per reconcile 8 → 32 ([[performance-and-scale]]) |
| `SkipChildJobSuspension` | **Alpha/off 0.20** (#16370, then pr-16436 downgraded it "to have more time to evaluate") | when on, Kueue no longer suspends managed child jobs based on the ancestor Workload's state and leaves that to the ancestor's controller — avoids suspending a running child during MultiKueue workload-slice replacement when the owner lookup briefly finds no unfinished ancestor Workload. Backported to 0.19/0.18 (pr-16460, pr-16461) with the spec rewritten to `0.19` Alpha; shipped in v0.19.8. `MultiKueueRayInTreeAutoscaling` now **depends on it** (v0.20.1, #16814): enabling the Ray gate without it is a startup error ([[job-framework-interface]]) |
| `ElasticJobsViaWorkloadSlicesFlavorChangeFromZero` | Alpha/off 0.20 (#16400) | a replacement slice may get a different ResourceFlavor for a PodSet that had zero Pods in the replaced slice (otherwise the Workload stayed Pending forever) ([[elastic-jobs]]) |
| `KueueDRAIntegrationPrioritizedList` | Alpha/off 0.20 (#14130) | charges a DRA `firstAvailable` request once when every alternative asks for the same count on one logical resource; other shapes are refused; MultiKueue unsupported ([[dra]]) |
| `RayServiceValidateUpgradeStrategy` | Beta/on 0.20 (#16094), **ACTION REQUIRED** | Kueue-managed RayServices using zero-downtime upgrades must enable `ElasticJobsViaWorkloadSlices` and set `kueue.x-k8s.io/elastic-job: "true"`, or set `spec.upgradeStrategy.type: None` ([[integration-rayjob]]) |
| `SchedulerLibraryDeepIntegration` | Alpha/off, **0.21, main only** (pr-16347); depends on `SchedulerLibraryIntegration` | uses scheduler-library `ScheduleWorkload()` to plan Pod placement, i.e. TAS topology assignments and preemption targets |
| `KubeRayEvictOnInconsistentTopologyRequest` | Alpha/off (0.21 spec on main; shipped in v0.20.1 / v0.19.8 with #15677) | strict `ComparePodSets` on Ray TopologyRequest index/subgroup fields; off = relaxed comparison so Workloads created before rank-based ordering are not evicted |
| `KubeRayServiceUsingTopLevelSuspend` | **main: 0.21 Beta/on; release-0.20 (v0.20.1, #16882): Alpha/off** | use the top-level RayService `spec.suspend`; requires KubeRay ≥ 1.7 — disable on older KubeRay |
| `FairSharingVerifyFinalTargets` | Beta/on, 0.21 spec on main (the fix itself shipped in v0.20.1, #16912) | re-verifies fair-sharing preemption targets after `fillBackWorkloads` against the final simulated state, preventing loops from temporary share deflation (issue #14543) ([[fair-sharing]]) |
| `PodIntegrationVerifyRoleRequests` | Beta/on, 0.21, main (pr-13382) | before ungating a pod-group Pod, check it fits the PodSet its name maps to; an oversized Pod stays gated with a Warning event (off = a forged role hash can run an oversized Pod under a cheaper role's reservation) ([[integration-plain-pod]]) |

#### Dependency changes

- **`SchedulerLibraryIntegration` → `TopologyAwareScheduling`** (pr-16362, v0.20.0; split from pr-16347 so it could be cherry-picked). The PR text says enabling the first "automatically enables" TAS; that is true only of the test helper `SetFeatureGatesDuringTest`, which enables dependencies recursively. At runtime the dependency map is registered with `AddDependencies` and a violation is a configuration error, like the other dependencies (source: raw/kueue/pkg/features/kube_features.go). The resulting TAS modes (pr-16347): TAS off → non-TAS scheduling; TAS on, `SchedulerLibraryIntegration` off → `tas-internal`; on, Deep off → `tas-schedlib-feasibility`; Deep on → `tas-schedlib-deep`. During review @kannon92 raised graduating `TopologyAwareScheduling` itself to GA; not done as of the snapshot.

### Gate changes in the 2026-10-21 batch (kueue@3bbb8cce4)

| Gate | Change | Effect / notes |
|---|---|---|
| `TASValidateWorkloadSliceSize` | 0.20 Beta/on → **0.21 GA, locked** (pr-17167, main) | webhook validation of `podSetSliceSize` and `podSetSliceRequiredTopology` is always on; code comment says the gate is removed in 0.22 ([[topology-aware-scheduling]]) |
| `FairSharingReevaluatePreemptionCandidates` | 0.20 Alpha/off → **0.21 Beta/on** (pr-17285, main; fixes #14122 after #14543 was resolved) | fair-sharing preemption re-evaluates candidates by default on main ([[fair-sharing]]) |
| `MetricsAccessControl` | **new, 0.21 Alpha/off** (pr-16035, main) | allows `metrics.accessControlMode: None` on a loopback bind address; setting the field with the gate off is a validation error ([[metrics]]) |
| `ClassicalPreemptionCandidateOrderCache` | **new, 0.21 Beta/on** on main (pr-16340); **Alpha/off** in the release-0.20 / release-0.19 backports (pr-17296, pr-17295, merged after v0.20.2 / v0.19.9) | reuses each ClusterQueue's candidate ordering across preemptors in one cycle and generates candidates lazily instead of re-sorting per preemptor ([[preemption]]) |
| `PodIntegrationVerifyRoleRequests` | release branches: shipped in **v0.20.2 / v0.19.9 as Alpha/off** (backports #17123 / #17124); main stays 0.21 Beta/on | on those releases the role-hash quota-bypass check runs only if you enable the gate ([[integration-plain-pod]]) |

Not merged at this snapshot: an Alpha `LogLevelForSchedulerMainLoop` gate proposed only for the release-branch backports of the scheduler V(2)→V(3) log change (pr-17370, pr-17371 open); on main the change is unconditional (pr-17227).

### Full stage table at kueue@3bbb8cce4 (main, v0.21 development)

Read from `defaultVersionedFeatureGates` in `pkg/features/kube_features.go` at the snapshot (re-verified 2026-10-21; the previous table was at kueue@8922c563e). Entries with a `0.21` spec exist only on main; v0.20.x carries the gate (if at all) with a branch-specific spec (see below).

| Gate | Stage history (Kueue version, stage, default) |
|---|---|
| `AdmissionFairSharing` | 0.12 Alpha off → 0.15 Beta on |
| `AdmissionFairSharingAnchorAtQuotaReservation` | 0.20 Beta on |
| `AdmissionGatedBy` | 0.17 Alpha off → 0.19 Beta on |
| `AssignQueueLabelsForPods` | 0.17 Beta on |
| `ClassicalPreemptionCandidateOrderCache` | 0.21 Beta on |
| `CleanupProvisioningRequestsOnEviction` | 0.19 Beta on |
| `ConcurrentAdmission` | 0.18 Alpha off |
| `ConfigurablePreemptions` | 0.20 Alpha off |
| `CustomMetricLabels` | 0.17 Alpha off |
| `DeferRayServiceFinalizationForRedisCleanup` | 0.19 Beta on → 0.20 Deprecated off |
| `DeploymentJobUIDLabel` | 0.20 Beta on |
| `DisableWaitForPodsReady` | 0.19 Alpha off |
| `DynamicQuotaOrchestration` | 0.20 Alpha off |
| `ElasticJobsViaWorkloadSlices` | 0.13 Alpha off → 0.18 Beta on |
| `ElasticJobsViaWorkloadSlicesFlavorChangeFromZero` | 0.20 Alpha off |
| `ElasticJobsViaWorkloadSlicesForProvisioningRequests` | 0.20 Alpha off |
| `ElasticJobsViaWorkloadSlicesWithPartialReplicaScaleUp` | 0.20 Alpha off |
| `ElasticJobsViaWorkloadSlicesWithTAS` | 0.17 Alpha off |
| `EnforceProvisioningPodTemplateContents` | 0.20 Beta on |
| `FailureRecoveryPolicy` | 0.15 Alpha off |
| `FairSharingPreemptWithinNominal` | 0.17 Beta on |
| `FairSharingPrioritizeNonBorrowing` | 0.17 Beta on |
| `FairSharingReevaluatePreemptionCandidates` | 0.20 Alpha off → 0.21 Beta on |
| `FairSharingRefill` | 0.20 Alpha off |
| `FairSharingVerifyFinalTargets` | 0.21 Beta on |
| `FastQuotaReleaseInPodIntegration` | 0.17 Alpha off |
| `FinalizeTerminatingPodGroups` | 0.20 Beta on (Beta/on since v0.20.0; Alpha/off only on release-0.19) |
| `FinishOrphanedWorkloads` | 0.18 Beta on |
| `FlavorFungibility` | 0.5 Beta on |
| `FlavorFungibilityPreserveScanProgress` | 0.20 Beta on |
| `HighMaxParallelismWithinReconcile` | 0.20 Beta on |
| `KubeRayEvictOnInconsistentTopologyRequest` | 0.21 Alpha off |
| `KubeRayServiceUsingTopLevelSuspend` | 0.21 Beta on |
| `KueueDRADeviceFeasibility` | 0.20 Alpha off |
| `KueueDRAIntegration` | 0.18 Beta on |
| `KueueDRAIntegrationConsumableCapacity` | 0.19 Alpha off |
| `KueueDRAIntegrationDeviceTaints` | 0.20 Alpha off |
| `KueueDRAIntegrationExtendedResource` | 0.18 Alpha off → 0.19 Beta on |
| `KueueDRAIntegrationPartitionableDevices` | 0.18 Alpha off → 0.19 Beta on |
| `KueueDRAIntegrationPrioritizedList` | 0.20 Alpha off |
| `KueueDRARejectWorkloadsWhenDRADisabled` | 0.18 Beta on |
| `LocalQueueMetrics` | 0.10 Alpha off → 0.17 Beta on |
| `LWSImmutableGroupSize` | 0.20 Beta on |
| `ManagedJobsNamespaceSelectorAlwaysRespected` | 0.13 Alpha off → 0.15 Beta on → 0.19 GA on (locked) |
| `MetricForWorkloadCreationLatency` | 0.18 Beta on → 0.21 GA on (locked) |
| `MetricsAccessControl` | 0.21 Alpha off |
| `MetricsForCohorts` | 0.18 Beta on |
| `MultiKueue` | 0.6 Alpha off → 0.9 Beta on |
| `MultiKueueAdaptersForCustomJobs` | 0.14 Alpha off → 0.15 Beta on |
| `MultiKueueBatchJobClearingTTLSecondsAfterFinishedOnWorkerCluster` | 0.20 Alpha off |
| `MultiKueueClusterProfile` | 0.15 Alpha off |
| `MultiKueueIncrementalDispatcherConfig` | 0.19 Beta on |
| `MultiKueueIncrementalDispatcherRespectConfigOrder` | 0.19 Beta on |
| `MultiKueueKubeConfigPathValidation` | 0.19 Alpha off → 0.20 Beta on |
| `MultiKueueManagerQuotaAutomation` | 0.18 Alpha off |
| `MultiKueueOrchestratedPreemption` | 0.17 Alpha off → 0.20 Beta on |
| `MultiKueueRayInTreeAutoscaling` | 0.20 Alpha off |
| `MultiKueueRemoteSpecSync` | 0.20 Beta on |
| `MultiKueueReuseClientConnectionConfigForWorkers` | 0.20 Beta on |
| `PartialAdmission` | 0.4 Alpha off → 0.5 Beta on |
| `PodGroupSchedulingShapeOrdering` | 0.20 Beta on (backports Alpha off in v0.19.7 / v0.18.11: pr-16358, pr-16365) |
| `PodIntegrationCountSucceededPodsAsReady` | 0.20 Beta on |
| `PodIntegrationValidateGroupOwner` | 0.18 Beta on |
| `PodIntegrationVerifyRoleRequests` | 0.21 Beta on |
| `PrioritizePreemptorWorkloads` | 0.20 Alpha off |
| `PriorityBoost` | 0.17 Alpha off |
| `PrioritySortingWithinCohort` | 0.6 Beta on |
| `QuotaCheckStrategy` | 0.18 Alpha off → 0.19 Beta on |
| `RayServiceValidateUpgradeStrategy` | 0.20 Beta on |
| `ReclaimablePods` | 0.15 Beta on |
| `RecomputeAssignmentUponPreemptionTargetsOverlap` | 0.20 Beta on |
| `RejectUpdatesToCQWithInvalidOnFlavors` | 0.18 Alpha off → 0.20 Beta on |
| `RemoveFinalizersWithStrictPatch` | 0.17 Beta on |
| `ReservedResourceNameValidation` | 0.20 Beta on |
| `SchedulerLibraryDeepIntegration` | 0.21 Alpha off |
| `SchedulerLibraryIntegration` | 0.19 Alpha off |
| `SchedulingEquivalenceHashing` | 0.17 Beta off → 0.18 Beta on |
| `SchedulingEquivalenceHashingIgnorePodSetName` | 0.20 Beta on |
| `ShortWorkloadNames` | 0.17 Alpha off |
| `SkipAncestorCheckForDeletedWorkloads` | 0.20 Beta on |
| `SkipChildJobSuspension` | 0.20 Alpha off |
| `SkipReassignmentForPodOwnedWorkloads` | 0.19 Beta on |
| `SparkApplicationIntegration` | 0.17 Alpha off |
| `TASAssignmentsEncodingByHostnamePrefix` | 0.19 Beta on |
| `TASBalancedPlacement` | 0.15 Alpha off |
| `TASCacheNodeMatchResults` | 0.19 Beta on |
| `TASCacheTopologyTree` | 0.20 Beta on |
| `TASCachingRemainingResources` | 0.19 Beta on |
| `TASFailedNodeReplacement` | 0.12 Alpha off → 0.14 Beta on |
| `TASFailedNodeReplacementFailFast` | 0.13 Alpha off → 0.14 Beta on |
| `TASGroupedPodSetSlicing` | 0.20 Beta on |
| `TASHandleOverlappingFlavors` | 0.18 Beta on |
| `TASLeaderPodSetFeasibility` | 0.20 Beta on |
| `TASMultiLayerTopology` | 0.17 Alpha off → 0.19 Beta on |
| `TASNodeFeasibilityForAllLevels` | 0.20 Beta on |
| `TASPartialSlices` | 0.20 Beta on |
| `TASProfileMixed` | 0.10 Alpha off → 0.15 Beta on |
| `TASRecomputeAssignmentWithinSchedulingCycle` | 0.19 Beta on |
| `TASRejectFalseUnconstrainedTopology` | 0.20 Alpha off |
| `TASReplaceMultipleFailedNodes` | 0.20 Alpha off |
| `TASReplaceNodeDueToNotReadyOverFixedTime` | 0.17 Beta on → 0.19 Deprecated off |
| `TASReplaceNodeOnNodeTaints` | 0.17 Beta on |
| `TASReplaceNodeOnPodTermination` | 0.13 Alpha off → 0.14 Beta on |
| `TASRespectNodeAffinityPreferred` | 0.18 Alpha off |
| `TASTopologySpreading` | 0.20 Alpha off |
| `TASValidateWorkloadSliceSize` | 0.20 Beta on → 0.21 GA on (locked) |
| `TLSOptions` | 0.16 Beta on → 0.20 GA on (locked) |
| `TopologyAwareScheduling` | 0.9 Alpha off → 0.14 Beta on |
| `UnadmittedWorkloadsExplicitStatus` | 0.19 Alpha off |
| `UnadmittedWorkloadsObservability` | 0.19 Alpha off → 0.20 Beta on |
| `ValidateRayAndSparkJobUpdates` | 0.18 Beta on |
| `VectorizedResourceRequests` | 0.19 Beta on |
| `VisibilityOnDemand` | 0.6 Alpha off → 0.9 Beta on |
| `WaitForPodsReadyMaxNotReady` | 0.20 Alpha off |
| `WaitForPodsReadyUnscheduledTimeout` | 0.20 Alpha off |
| `WorkloadIdentifierAnnotations` | 0.18 Beta on |
| `WorkloadLevelWaitForPodsReady` | 0.20 Alpha off |
| `WorkloadPriorityClassDefaulting` | 0.18 Alpha off → 0.20 Beta on |
| `WorkloadRequestUseMergePatch` | 0.14 Alpha off |
| `WorkloadValidateResourcesAreNonNegative` | 0.20 Beta on |
| `WorkloadValidationForPodSetMetadata` | 0.20 Beta on |


## Registering a gate on a release branch

Kueue never sets an emulation version, so the effective version used by `featureSpecAtEmulationAndMinCompatVersion` is Kubernetes' `DefaultKubeBinaryVersion` (1.36 at the time of writing), **not** the Kueue version. `featureSpecAtEmulationAndMinCompatVersion` selects the highest spec at or below that version, so a spec written as `{0.20, Default: true, Beta}` is still selected on a release-0.19 build and the gate lands **enabled by default there too**. A cherry-pick that wants the gate off on the branch must therefore rewrite the spec as `{0.19, Default: false, Alpha}` rather than reuse the main spec. ([[pr-14804]])

Examples: `ClassicalPreemptionCandidateOrderCache` is `{0.21, Beta, on}` on main and Alpha/off in its 0.20/0.19 backports (pr-17295, pr-17296); `PodIntegrationVerifyRoleRequests` shipped Alpha/off in v0.20.2 / v0.19.9. Earlier: `SkipChildJobSuspension` is `{0.20, Alpha, off}` on main but its 0.19/0.18 backports (pr-16460, pr-16461) rewrite the introduction version to `0.19`; `KubeRayServiceUsingTopLevelSuspend` is `{0.21, Beta, on}` on main but shipped in v0.20.1 as Alpha/off (source: pr-16460.md, CHANGELOG-0.20.md). Always read the gate stage from the branch you run, not from main.

Gate *dependencies* are also tracked differently per branch: `main` uses the `defaultFeatureGateDependencies` map in `pkg/features`, while release branches use `validateFeatureGateDependency` in `pkg/config/validation.go`. Both surface as a startup configuration error. ([[pr-14804]], [[pr-14256]])

## Related pages

- [[release-process]] — when gates graduate.
- [[fair-sharing]], [[topology-aware-scheduling]], [[multikueue]], [[elastic-jobs]] — feature-area pages that reference their gates.
