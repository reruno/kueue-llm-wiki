# Integration: TrainJob

**Summary**: Kueue integrates with the Kubernetes Training Operator v2's `TrainJob` CRD, delegating PodSet discovery to the child JobSet and supporting MultiKueue cross-cluster dispatch with full status synchronization.

**Sources**: `raw/kueue/pkg/controller/jobs/trainjob/trainjob_controller.go`, `raw/kueue/pkg/controller/jobs/trainjob/trainjob_multikueue_adapter.go`, `raw/kueue/pkg/controller/jobs/trainjob/trainjob_webhook.go`

**Last updated**: 2026-04-28

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

## Relationship to Kubeflow v1 integrations

`TrainJob` is the successor to the v1 integrations ([[integration-kubeflow]] — PyTorchJob, TFJob, etc.). For new workloads, TrainJob is preferred; the v1 integrations remain supported for backward compatibility.

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
