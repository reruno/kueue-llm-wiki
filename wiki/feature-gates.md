# Feature gates

**Summary**: Kueue follows the Kubernetes feature-gate convention: new features land alpha → beta → GA, with a named gate (`--feature-gates=Foo=true|false`) controlling the on/off switch. Each graduation updates the default (alpha defaults off, beta defaults on, GA locked on).

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-05-08

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
- **`ElasticJobsViaWorkloadSlices`** (KEP-77) — see [[elastic-jobs]].
- **`ConcurrentAdmission`** (KEP-8691) — **Alpha**. Lets one Workload pursue multiple ResourceFlavors concurrently via Variant Workloads. See [[concurrent-admission]].
- **`AdmissionCheckRetry`** — see [[admission-check]]; governs retry-across-flavors semantics (claim needs verification — no ingested source confirms this gate or its exact semantics).
- **`AdmissionGatedBy`** (KEP-6915) — **Alpha**. Honors the `kueue.x-k8s.io/admission-gated-by` annotation so external controllers can delay admission. See [[admission-gated-by-annotation]].
- **`WorkloadPriorityBoost`** (KEP-7990) — **Alpha**. Honors the `kueue.x-k8s.io/priority-boost` annotation; computes effective priority for scheduling and preemption candidate selection. See [[preemption-cost]].
- **`FailureRecovery`** (KEP-6757) — **Alpha**. Force-deletes zombie pods stuck `Terminating` after node failure when the pod opted in via `safe-to-forcefully-delete`. See [[failure-recovery]].
- **`MaxExecTime`** (KEP-3125) — **Beta**, on by default since v0.9. Enforces `spec.maximumExecutionTimeSeconds` per Workload. See [[workload-max-execution-time]].
- **`ManagedJobsNamespaceSelectorAlwaysRespected`** (KEP-3589) — strengthens `managedJobsNamespaceSelector` so jobs in non-matching namespaces are never managed even if labeled. See [[manage-jobs-selectively]].
- **`DynamicResourceAllocation` / KEP-2941** — DRA support for [[resource-flavor]] / partitionable devices ([[pr-3071]] — DRA design; [[pr-8734]] — extended resources design for DRA integration; [[pr-10283]] — partitionable devices). See [[dra]].
- **`DRAExtendedResources`** (KEP-2941) — **Alpha**. Companion gate that enables the extended-resource path for DRA; requires `DynamicResourceAllocation` also enabled. See [[dra]].
- **`SparkApplicationIntegration`** — **Alpha**. Enables the Kueue integration for Kubeflow Spark Operator v2 SparkApplication. See [[integration-spark]].
- **`FairSharingPrioritizeNonBorrowing`** — see [[fair-sharing]] ([[issue-10126]]).
- **`BorrowWithinCohort` policies** — `LowerPriorityBorrowersOnly` added to protect nominal quota ([[issue-10171]]).
- **`FinishOrphanedWorkloads`** — **Alpha (downgraded from Beta in v0.18.0)**. When enabled, the workload controller marks Workloads whose owning Job/JobSet/etc. cannot be found as `Finished=True` with `OwnerNotFound`. Was promoted to Beta as part of the [[pr-10274]] fix for stuck Deployment-evicted workloads, but a race between the JobReconciler's structured informer and the workload-controller's `PartialObjectMetadata` informer caused brand-new Workloads to be finished within milliseconds of creation. [[pr-11010]] downgrades the gate to Alpha (off by default) in v0.18 / v0.16.7 / v0.17.2 so the regression no longer hits users by default; [[pr-11014]] independently strengthens `Manager.RequeueWorkload` to refuse to requeue Workloads that are already `Finished` (so even with the gate enabled, they no longer block fair-sharing). Tracked in [[issue-10901]]; the planned structural fix is to query the actual owner kind instead of `PartialObjectMetadata`.
- **`QuotaCheckStrategy`** — **Alpha (new in v0.18)**. Gates the `resources.quotaCheckStrategy` configuration field on the [[cluster-queue]]; setting it to `IgnoreUndeclared` admits Workloads requesting resources the CQ does not list (those resources don't count against quota). PR #9808.
- **`RejectUpdatesToCQWithInvalidOnFlavors`** — **Alpha (new in v0.18, action-required)**. When enabled, ClusterQueue updates that reference invalid flavors in `AdmissionCheckStrategy.OnFlavors` are rejected at the validation webhook. Operators must fix any pre-existing invalid references before flipping the gate on.

### v0.18 graduations

The following gates graduated to **Stable** in v0.18.0 (per [[issue-10861]] release notes):

- `MultiKueueRedoAdmissionOnEvictionInWorker` (#10695) — see [[multikueue]].
- `MultiKueueWaitForWorkloadAdmitted` (#10656) — see [[multikueue]].
- `SkipFinalizersForPodsSuspendedByParent` (#10645) — Pod-integration internal: don't add Kueue finalizers on pods that the parent has already suspended.

> Configuration-only knobs (not feature gates) used by the new pages:
> - `objectRetentionPolicies.workloads.afterFinished` / `afterDeactivatedByKueue` — controls [[workload-garbage-collection]] (KEP-1618).
> - `integrations.frameworks` (with `"statefulset"`, `"trainjob"`) — enables [[integration-statefulset]] / [[integration-trainjob]]; both are framework toggles, not gates.

## When a gate graduates

Graduation is primarily a documentation + defaults change; the code typically stays the same. Missed graduation issues ([[issue-9633]]) are usually about forgetting to flip the stage annotation in the code so release tooling knows the new status.

## Related pages

- [[release-process]] — when gates graduate.
- [[fair-sharing]], [[topology-aware-scheduling]], [[multikueue]], [[elastic-jobs]] — feature-area pages that reference their gates.
