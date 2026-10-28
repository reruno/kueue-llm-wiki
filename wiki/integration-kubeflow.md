# Integration: Kubeflow training jobs

**Summary**: Kueue integrates with the Kubeflow Training Operator's job types — PyTorchJob, TFJob, MPIJob, PaddleJob, XGBoostJob, JAXJob (MXJob support was removed in v0.11, #4077). Each has its own controller and its own replica-type decomposition; Kueue's per-integration adapter maps replica types to PodSets.

**Sources**: `raw/github/kubernetes-sigs__kueue/`., pr-16972.md, pr-16973.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, raw/kueue/CHANGELOG/CHANGELOG-0.19.md, pr-16982.md, pr-17843.md, pr-17869.md, issue-16974.md, pr-17689.md, pr-17640.md, pr-17730.md, pr-17731.md, pr-17666.md, pr-17672.md

**Last updated**: 2026-10-28

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

### XGBoostJob, PaddleJob, JAXJob

Lighter traffic; adapters follow the same pattern. Representative MultiKueue flake: "[Flaky] Should run a kubeflow XGBoostJob" ([[issue-2838]]). PaddleJob test flakes ([[issue-2901]]). JAXJob is the most recent addition.

The PaddleJob "Workload creation timeout" flake ([[issue-16974]]) was not specific to PaddleJob. `ReconcileGenericJob` dropped the reconcile when the job's Namespace was not yet in the informer cache, so the job stayed suspended without a Workload. Since [[pr-16982]] the reconcile is requeued instead. This applies to every integration. See [[job-framework-interface#A Namespace missing from the cache requeues the job]] (source: pr-16982.md).

## Gang scheduling caveats

Training jobs benefit from `WaitForPodsReady` (see [[gang-scheduling]]), but specific replica-type ordering (e.g. Launcher starts before Workers in MPIJob) can interact with PodsReady counting. Platform teams enable it per CQ.

## ProvisioningRequest

"MPIJobs can't run with ProvisioningRequest with DWS" ([[issue-2260]]) is an example of an [[admission-check]] that couldn't fully reserve the gang's capacity for the replica-typed PodSets.

## MultiKueue

Each Kubeflow type needs its own MultiKueue adapter; adoption has been incremental. PyTorchJob and MPIJob E2E coverage on worker clusters grew over time ([[issue-5258]] for PyTorchJob E2E). MultiKueue + priority-class mutation on Kubeflow workloads ([[issue-7429]]).

## TAS

Topology-aware PyTorchJobs ([[issue-1476]] — pytorchjobs scheduling unaware of node resource topology) were an explicit motivator for [[topology-aware-scheduling]]. MPIJob + TAS flakes are actively tracked ([[issue-3696]]).

Rank-ordered ungating for grouped Kubeflow v1 jobs and MPIJobs (`kueue.x-k8s.io/podset-group-name`) was fixed by [[pr-17689]] and [[pr-17640]]. See [[topology-aware-scheduling]] for the full rules. In short:

- **Kubeflow v1 grouped PodSets** (e.g. PyTorchJob Master + Worker) now get `kueue.x-k8s.io/pod-index-offset: "0"` in `RunWithPodSetsInfo`, applied after `podset.Merge`. The same default applies to **MPIJob without `runLauncherAsWorker`** (source: pr-17689.md). Backports pr-17730 (0.20) and pr-17731 (0.19) are merged and pending the next patch.
- **MPIJob with `runLauncherAsWorker: true`** gets no default. When it is grouped, the MPIJob webhook accepts an unset or `"1"` Worker `pod-index-offset` and rejects any other value. This fixes a regression from #17289, which shipped in v0.20.3 / v0.19.10: grouped MPIJobs whose Worker offset is `"1"` stayed suspended (source: pr-17640.md). Backports pr-17666 (0.20) and pr-17672 (0.19) are pending the next patch.

## MPIJob: nil replica specs

`orderedReplicaTypes()` in `pkg/controller/jobs/mpijob/mpijob_controller.go` checked only key presence in `MPIJobSpec.MPIReplicaSpecs`, so a key with a nil `*ReplicaSpec` value (e.g. `Launcher`) would panic in `PodSets()`. It now skips nil specs. This is defense in depth: the CRD schema is not `nullable`, so API-server pruning already strips null values, and the case was not reachable through a real cluster (only via programmatically built objects) (source: pr-13714.md, issue-12564).

## Queue-name changes are validated on update

These webhooks did not re-run create-time validation on update, so a suspended job could switch `kueue.x-k8s.io/queue-name` to a valid label value that is not a valid LocalQueue name (for example `Bad_Queue`). The job reconciler then failed on every retry. Since #16221 a changed, non-empty value is validated (shipped in **v0.20.2** via pr-16972 and **v0.19.9** via pr-16973, per raw/kueue/CHANGELOG/CHANGELOG-0.20.md and CHANGELOG-0.19.md). See [[job-framework-interface#Queue-name format is validated on update]] (source: pr-16973.md).

## Related pages

- [[integrations]] — integration mechanics.
- [[workload]] — per-replica-type PodSets.
- [[gang-scheduling]] — WaitForPodsReady.
- [[topology-aware-scheduling]] — placement for bandwidth-sensitive training.
- [[multikueue]] — cross-cluster dispatch.
- [[job-framework-interface]]
