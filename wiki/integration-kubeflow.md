# Integration: Kubeflow training jobs

**Summary**: Kueue integrates with the Kubeflow Training Operator's job types — PyTorchJob, TFJob, MPIJob, MXJob, PaddleJob, XGBoostJob, JAXJob. Each has its own controller and its own replica-type decomposition; Kueue's per-integration adapter maps replica types to PodSets.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

---

## The common pattern

Kubeflow training jobs share a shape: `spec.replicaSpecs[ReplicaType]` defines per-role replica counts and templates (e.g. `Master`, `Worker`, `PS`, `Chief`, `Launcher`). Kueue produces one PodSet per replica type.

All support `.spec.runPolicy.suspend` (mirroring `batch/v1.Job`), which Kueue toggles exactly the same way as the batch Job integration.

## Per-type notes

### MPIJob

Oldest Kubeflow integration (source: issue-65.md — Support kubeflow's MPIJob, source: issue-577.md). Has Launcher + Workers. The `managedBy` feature allows delegating lifecycle to Kueue under MultiKueue (source: issue-3257.md). Common friction: Pod `nodeSelector` not matching the MPIJob-level selector (source: issue-3400.md). Error messages when the CRD isn't installed were weak (source: issue-665.md).

### PyTorchJob

Has Master + Workers. Gang scheduling is frequently requested (source: issue-2796.md). Early integration didn't propagate ResourceFlavor nodeLabels onto the Pods (source: issue-1407.md). Docs caught up in sample-pytorchjob refreshes (source: issue-1910.md). Cleanup-on-completion edges: "Consider pytorchJob cleanPodPolicy in kueue" (source: issue-1574.md).

### TFJob

Legacy TensorFlow operator job. Known preemption edge: "Broken preemption on TFJob with non default `runPolicy.ttlSecondsAfterFinished`" (source: issue-2923.md). Considered together with PyTorchJob in early adoption discussions (source: issue-652.md — Can we use tfjob or pytorchjob in kueue?).

### XGBoostJob, MXJob, PaddleJob, JAXJob

Lighter traffic; adapters follow the same pattern. Representative MultiKueue flake: "[Flaky] Should run a kubeflow XGBoostJob" (source: issue-2838.md). PaddleJob test flakes (source: issue-2901.md). JAXJob is the most recent addition.

## Gang scheduling caveats

Training jobs benefit from `WaitForPodsReady` (see [[gang-scheduling]]), but specific replica-type ordering (e.g. Launcher starts before Workers in MPIJob) can interact with PodsReady counting. Platform teams enable it per CQ.

## ProvisioningRequest

"MPIJobs can't run with ProvisioningRequest with DWS" (source: issue-2260.md) is an example of an [[admission-check]] that couldn't fully reserve the gang's capacity for the replica-typed PodSets.

## MultiKueue

Each Kubeflow type needs its own MultiKueue adapter; adoption has been incremental. PyTorchJob and MPIJob E2E coverage on worker clusters grew over time (source: issue-5258.md for PyTorchJob E2E). MultiKueue + priority-class mutation on Kubeflow workloads (source: issue-7429.md).

## TAS

Topology-aware PyTorchJobs (source: issue-1476.md — pytorchjobs scheduling unaware of node resource topology) were an explicit motivator for [[topology-aware-scheduling]]. MPIJob + TAS flakes are actively tracked (source: issue-3696.md).

## Related pages

- [[integrations]] — integration mechanics.
- [[workload]] — per-replica-type PodSets.
- [[gang-scheduling]] — WaitForPodsReady.
- [[topology-aware-scheduling]] — placement for bandwidth-sensitive training.
- [[multikueue]] — cross-cluster dispatch.
