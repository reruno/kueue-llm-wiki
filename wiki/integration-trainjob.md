# Integration: TrainJob

**Summary**: Kueue integrates with the Kubernetes Training Operator v2's `TrainJob` CRD, delegating PodSet discovery to the child JobSet and supporting MultiKueue cross-cluster dispatch with full status synchronization.

**Sources**: `raw/kueue/pkg/controller/jobs/trainjob/trainjob_controller.go`, `raw/kueue/pkg/controller/jobs/trainjob/trainjob_multikueue_adapter.go`, `raw/kueue/pkg/controller/jobs/trainjob/trainjob_webhook.go`

**Last updated**: 2026-09-29

---

> **Stage: Alpha** — `TrainJob` is the new Kubernetes Training Operator v2 API (`trainer.kubeflow.org/v1alpha1`); currently alpha both in the upstream project and in Kueue's integration.

## What is TrainJob?

`TrainJob` is the v2 CRD from the [Kubernetes Training Operator](https://github.com/kubeflow/training-operator), API group `trainer.kubeflow.org/v1alpha1`. It replaces the individual `PyTorchJob`, `TFJob`, etc. from v1 with a unified API backed by a `TrainingRuntime` (or `ClusterTrainingRuntime`) that defines the actual pod topology. (source: pkg/controller/jobs/trainjob/trainjob_controller.go)

## PodSets

TrainJob delegates PodSet discovery to its child **JobSet**. The TrainJob controller materializes a JobSet from the referenced `TrainingRuntime`/`ClusterTrainingRuntime`, then Kueue's TrainJob integration calls the JobSet integration's `PodSets()` method. Each replicated job in the JobSet becomes one PodSet (e.g. `chief`, `worker`, `parameter-server`). (source: pkg/controller/jobs/trainjob/trainjob_controller.go)

## Suspend / resume

TrainJob has a `spec.suspend` field. On admission, Kueue calls `RunWithPodSetsInfo()` which:
1. Writes node selectors, tolerations, annotations, and scheduling gates back via `spec.runtimePatches` — specifically a Kueue-owned `RuntimePatch` with manager `kueue.x-k8s.io/manager`.
2. Sets `spec.suspend = false`.

(source: pkg/controller/jobs/trainjob/trainjob_controller.go)

## Reclaimable pods

The TrainJob integration implements `JobWithReclaimablePods`: completed replicated jobs (e.g. a parameter-server that finishes early) can release their quota back to the queue, while the remaining replicas continue running. This is the same mechanism used by [[elastic-jobs]]. (source: pkg/controller/jobs/trainjob/trainjob_controller.go)

## MultiKueue support

**Supported** — a `multiKueueAdapter` exists with full status synchronization:
- On dispatch: `spec.managedBy` is cleared on the remote (worker cluster) copy so the worker's TrainJob controller takes ownership.
- Status sync: the manager cluster copies `status` back from the worker replica.
- The `MultiKueue` feature gate controls whether the [[multikueue]] webhook auto-sets `spec.managedBy` to point to the MultiKueue AdmissionCheck.

(source: pkg/controller/jobs/trainjob/trainjob_multikueue_adapter.go)

## JobWithManagedBy

The TrainJob integration implements `JobWithManagedBy`: the `spec.managedBy` field indicates which controller is managing the job at any given time. When set to a MultiKueue AdmissionCheck's name, the manager cluster takes over dispatch. (source: pkg/controller/jobs/trainjob/trainjob_controller.go)

## Mutating webhook scope (v0.18.0)

Earlier versions of the integration's mutating webhook patched the **referenced `TrainingRuntime` / `ClusterTrainingRuntime`** with the `kueue.x-k8s.io/queue-name` label. This was a leftover from when the TrainJob integration reached into the underlying JobSet for PodSet shape; the integration now delegates PodSet discovery via the JobSet integration directly and never inspects the runtime template. [[pr-10829]] removes the runtime patch from the webhook (Fixes #10099). The webhook still labels the **TrainJob** itself, but the runtime is left untouched — important if the same `TrainingRuntime` is referenced by multiple TrainJobs in different namespaces, since the previous code would race and clobber each other's queue label.

## Relationship to Kubeflow v1 integrations

`TrainJob` is the successor to the v1 integrations ([[integration-kubeflow]] — PyTorchJob, TFJob, etc.). For new workloads, TrainJob is preferred; the v1 integrations remain supported for backward compatibility.

## Updates use a JSON merge patch, not `Update`

`RunWithPodSetsInfo` and `Stop` in the TrainJob controller called `c.Update()`, which sends a **full replace** of the object as Kueue's vendored typed struct sees it. Against a cluster running a newer Kubeflow Trainer whose TrainJob CRD has fields Kueue does not model, that replace **drops those fields** — and the observed symptom was TrainJobs stuck unadmitted, because Kueue overwrote the older TrainJob scheme with the vendored one on admission.

[[pr-14836]] (cherry-picks [[pr-14841]], [[pr-14842]]; related to [[issue-14722]]) switches both call sites to `clientutil.Patch` (JSON merge patch via `client.MergeFrom`), matching the pattern `RestorePodSetsInfo` already used. A merge patch carries only the fields that actually changed, so unmodelled fields are never touched.

This is the general "preserve unmodelled spec fields" hazard for any integration that vendors a third-party CRD's Go types; the MultiKueue counterpart is [[issue-14837]] (open). Validating TrainJob CRD compatibility at setup and documenting a minimum Trainer version is [[issue-14819]] (open).

## `Stop` is idempotent

`TrainJob.Stop` always returned `true` and always sent the restore patch, so every reconcile while a TrainJob stayed evicted or unadmitted re-sent a no-op PATCH and made the framework emit another `Stopped` event. `Stop` now tracks whether it actually suspended the TrainJob, and `RestorePodSetsInfo` reports whether it changed anything (as the `GenericJob` contract documents) so `clientutil.Patch` skips no-op patches (source: pr-15652.md; backports pr-15754.md, pr-15755.md). `RuntimePatchWrapper` gained `Clone()` for tests (pr-15773.md).

## RBAC: delete permission

Kueue lacked `delete` on JAXJob and TrainJob, so jobs deactivated by Kueue were not deleted after `objectRetentionPolicies.workloads.afterDeactivatedByKueue` (source: pr-15567.md, pr-15568.md, backports of pr-15565).

## Related pages

- [[integrations]]
- [[integration-kubeflow]]
- [[integration-jobset]]
- [[job-framework-interface]]
- [[workload]]
- [[multikueue]]
- [[elastic-jobs]]
- [[admission]]
- [[feature-gates]]
