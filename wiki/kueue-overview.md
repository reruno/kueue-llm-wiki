# Kueue overview

**Summary**: Kueue is a Kubernetes-native job queueing system that gates when workloads become visible to `kube-scheduler`. It decides when a job should wait, when it should be admitted (its Pods allowed to be created), and when it should be preempted — all without replacing `kube-scheduler` or any existing controller.

**Sources**: `raw/github/kubernetes-sigs__kueue/` — project-level context drawn from the full issue/PR history.

**Last updated**: 2026-04-23

---

## What Kueue is

Kueue is a SIG-Scheduling subproject (home: `kubernetes-sigs/kueue`) that sits between users and existing job APIs. It is a lightweight add-on: rather than re-implementing scheduling, Kueue leaves Pod placement to `kube-scheduler` and instead gates *which* Workloads reach it by toggling `.spec.suspend` on jobs or injecting Pod scheduling gates.

The unit of quota and priority in Kueue is the **job** — not the Pod. Decisions about admission, preemption, and borrowing are made at the [[workload]] level, which is Kueue's wrapper around an underlying job object.

## Problems it solves

- **Batch scheduling on Kubernetes.** `kube-scheduler` is pod-centric; it has no notion of "this is one job of 256 Pods that must all start together." Kueue adds that layer.
- **Multi-tenant quota sharing.** Hierarchical [[cluster-queue]]s, [[local-queue]]s, and [[cohort]]s let multiple teams share a cluster with enforceable fair-shares and borrowing/lending between teams.
- **Heterogeneous workload support.** A single Kueue installation handles `batch/v1` Jobs, JobSet, Kubeflow training jobs (PyTorchJob/TFJob/MPIJob/…), RayJob/RayCluster, Argo Workflows, AppWrapper, LeaderWorkerSet, and plain Pods — see [[integrations]].
- **Gang scheduling.** All-or-nothing admission for jobs that require a minimum Pod count to make progress; see [[gang-scheduling]].
- **Topology-aware placement.** Co-locate Pods within a rack/block/zone for bandwidth-sensitive training — see [[topology-aware-scheduling]].
- **Multi-cluster dispatch.** From a manager cluster, queue a Workload once and let Kueue pick a worker cluster with free capacity — see [[multikueue]].

## Who uses it

Primary users are **platform teams** running shared Kubernetes clusters for ML/AI training, HPC, data processing, or CI. Fair-share quota enforcement across teams on expensive accelerators (GPUs, TPUs) is the most common motivation.

Recurring themes in the issue tracker confirm this audience: RayJob adoption (source: issue-10438.md), PyTorchJob gang-scheduling (source: issue-2796.md), DRA/device support (source: pr-3071.md), and topology-aware placement for ML training (source: issue-2724.md).

## What Kueue is not

- It is **not** a replacement for `kube-scheduler`. It does not make placement decisions (which node a Pod lands on); it only decides *when* a Pod gets to exist.
- It is **not** a job runtime. The actual job execution is handled by `Job`, `JobSet`, `RayJob`, etc. — the upstream controllers Kueue integrates with.
- It is **not** a cluster autoscaler, though it can integrate with one through the [[admission-check]] + ProvisioningRequest mechanism (source: pr-7673.md).

## Related pages

- [[architecture]] — how the pieces fit together.
- [[workload]] — the gated-job object.
- [[cluster-queue]] — the quota pool.
- [[integrations]] — which job APIs are supported.
