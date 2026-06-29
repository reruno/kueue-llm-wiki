# Feature gates

**Summary**: Kueue follows the Kubernetes feature-gate convention: new features land alpha → beta → GA, with a named gate (`--feature-gates=Foo=true|false`) controlling the on/off switch. Each graduation updates the default (alpha defaults off, beta defaults on, GA locked on).

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-06-29

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

## Related pages

- [[release-process]] — when gates graduate.
- [[fair-sharing]], [[topology-aware-scheduling]], [[multikueue]], [[elastic-jobs]] — feature-area pages that reference their gates.
