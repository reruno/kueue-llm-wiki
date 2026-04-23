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

Oldest Kubeflow integration ([[issue-65]] — Support kubeflow's MPIJob, [[issue-577]]). Has Launcher + Workers. The `managedBy` feature allows delegating lifecycle to Kueue under MultiKueue ([[issue-3257]]). Common friction: Pod `nodeSelector` not matching the MPIJob-level selector ([[issue-3400]]). Error messages when the CRD isn't installed were weak ([[issue-665]]).

### PyTorchJob

Has Master + Workers. Gang scheduling is frequently requested ([[issue-2796]]). Early integration didn't propagate ResourceFlavor nodeLabels onto the Pods ([[issue-1407]]). Docs caught up in sample-pytorchjob refreshes ([[issue-1910]]). Cleanup-on-completion edges: "Consider pytorchJob cleanPodPolicy in kueue" ([[issue-1574]]).

### TFJob

Legacy TensorFlow operator job. Known preemption edge: "Broken preemption on TFJob with non default `runPolicy.ttlSecondsAfterFinished`" ([[issue-2923]]). Considered together with PyTorchJob in early adoption discussions ([[issue-652]] — Can we use tfjob or pytorchjob in kueue?).

### XGBoostJob, MXJob, PaddleJob, JAXJob

Lighter traffic; adapters follow the same pattern. Representative MultiKueue flake: "[Flaky] Should run a kubeflow XGBoostJob" ([[issue-2838]]). PaddleJob test flakes ([[issue-2901]]). JAXJob is the most recent addition.

## Gang scheduling caveats

Training jobs benefit from `WaitForPodsReady` (see [[gang-scheduling]]), but specific replica-type ordering (e.g. Launcher starts before Workers in MPIJob) can interact with PodsReady counting. Platform teams enable it per CQ.

## ProvisioningRequest

"MPIJobs can't run with ProvisioningRequest with DWS" ([[issue-2260]]) is an example of an [[admission-check]] that couldn't fully reserve the gang's capacity for the replica-typed PodSets.

## MultiKueue

Each Kubeflow type needs its own MultiKueue adapter; adoption has been incremental. PyTorchJob and MPIJob E2E coverage on worker clusters grew over time ([[issue-5258]] for PyTorchJob E2E). MultiKueue + priority-class mutation on Kubeflow workloads ([[issue-7429]]).

## TAS

Topology-aware PyTorchJobs ([[issue-1476]] — pytorchjobs scheduling unaware of node resource topology) were an explicit motivator for [[topology-aware-scheduling]]. MPIJob + TAS flakes are actively tracked ([[issue-3696]]).

## Related pages

- [[integrations]] — integration mechanics.
- [[workload]] — per-replica-type PodSets.
- [[gang-scheduling]] — WaitForPodsReady.
- [[topology-aware-scheduling]] — placement for bandwidth-sensitive training.
- [[multikueue]] — cross-cluster dispatch.
