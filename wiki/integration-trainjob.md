# Integration: TrainJob

**Summary**: Kueue integrates with the Kubernetes Training Operator v2's `TrainJob` CRD, delegating PodSet discovery to the child JobSet and supporting MultiKueue cross-cluster dispatch with full status synchronization.

**Sources**: `raw/kueue/pkg/controller/jobs/trainjob/trainjob_controller.go`, `raw/kueue/pkg/controller/jobs/trainjob/trainjob_multikueue_adapter.go`, `raw/kueue/pkg/controller/jobs/trainjob/trainjob_webhook.go`, pr-17563.md, pr-17571.md, pr-17572.md, pr-17862.md, pr-17871.md, pr-17872.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, raw/kueue/CHANGELOG/CHANGELOG-0.19.md, pr-18730.md

**Last updated**: 2026-11-24

---

> **Stage: Alpha** — `TrainJob` is the new Kubernetes Training Operator v2 API (`trainer.kubeflow.org/v1alpha1`); currently alpha both in the upstream project and in Kueue's integration.

## What is TrainJob?

`TrainJob` is the v2 CRD from the [Kubernetes Training Operator](https://github.com/kubeflow/training-operator), API group `trainer.kubeflow.org/v1alpha1`. It replaces the individual `PyTorchJob`, `TFJob`, etc. from v1 with a unified API backed by a `TrainingRuntime` (or `ClusterTrainingRuntime`) that defines the actual pod topology. (source: pkg/controller/jobs/trainjob/trainjob_controller.go)

## PodSets

TrainJob delegates PodSet discovery to its child **JobSet**. The TrainJob controller materializes a JobSet from the referenced `TrainingRuntime`/`ClusterTrainingRuntime`, then Kueue's TrainJob integration calls the JobSet integration's `PodSets()` method. Each replicated job in the JobSet becomes one PodSet (e.g. `chief`, `worker`, `parameter-server`). (source: pkg/controller/jobs/trainjob/trainjob_controller.go)

### PodSet defaulting uses a dry-run Workload with a generated name

`TrainJob.PodSets()` must return **defaulted** PodSets, because Workloads read from the API server are defaulted and the reconciler compares the two to match an existing Workload. To get the defaults it builds a throwaway Workload from the PodSets and sends a dry-run `Create` (`DryRun: All`). It then uses the PodSets from the response. The throwaway Workload used to be named after the TrainJob. A dry-run create still fails with `AlreadyExists` when a Workload with that name exists in the namespace, for example a pod-group or prebuilt Workload. Every reconcile of that TrainJob failed, and it never got a Workload or admission. Since [[pr-17563]] the Workload has an empty `name` and `generateName: <trainjob-name>-` (source: pr-17563.md, raw/kueue/pkg/controller/jobs/trainjob/trainjob_controller.go). Shipped in **v0.20.3** ([[pr-17571]]) and **v0.19.10** ([[pr-17572]]) (source: raw/kueue/CHANGELOG/CHANGELOG-0.20.md, CHANGELOG-0.19.md).

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
- The `MultiKueue` feature gate controls whether the [[multikueue]] webhook sets `spec.managedBy: kueue.x-k8s.io/multikueue` when the job's ClusterQueue has a MultiKueue AdmissionCheck.

(source: pkg/controller/jobs/trainjob/trainjob_multikueue_adapter.go)

## JobWithManagedBy

The TrainJob integration implements `JobWithManagedBy`: the `spec.managedBy` field indicates which controller is managing the job at any given time. When set to `kueue.x-k8s.io/multikueue`, the manager cluster takes over dispatch. (source: pkg/controller/jobs/trainjob/trainjob_controller.go)

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

## TAS: grouped TrainJobs

Rank-ordered ungating for TrainJob Pods in a `kueue.x-k8s.io/podset-group-name` group was fixed by [[pr-17862]]. When the resolved Pod template is grouped and has no `kueue.x-k8s.io/pod-index-offset`, Kueue adds `"0"` to its `ReplicatedJobPatch` annotations. Annotations that come from admission take precedence (source: pr-17862.md). Backports pr-17871 (0.20) and pr-17872 (0.19) are merged and pending the next patch. See [[topology-aware-scheduling]].

## RBAC: delete permission

Kueue lacked `delete` on JAXJob and TrainJob, so jobs deactivated by Kueue were not deleted after `objectRetentionPolicies.workloads.afterDeactivatedByKueue` (source: pr-15567.md, pr-15568.md, backports of pr-15565).

## Shared Kueue runtime patch helper (pr-18730)

The Kueue runtime patch manager name and the helper that finds the Kueue runtime patch in a TrainJob now live once in `pkg/util/trainjob` (previously duplicated in the integration and in the test wrappers). The controller, webhook, MultiKueue adapter, test wrappers and tests use it; it cannot sit in the integration package because that package's unit tests import the wrappers (import cycle). Refactor only, no behaviour change (source: pr-18730.md).

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
