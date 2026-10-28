# Kueue overview

**Summary**: Kueue is a Kubernetes-native job queueing system that gates when workloads become visible to `kube-scheduler`. It decides when a job should wait, when it should be admitted (its Pods allowed to be created), and when it should be preempted — all without replacing `kube-scheduler` or any existing controller.

**Sources**: `raw/github/kubernetes-sigs__kueue/` — project-level context drawn from the full issue/PR history; `raw/kueue/site/data/adopters.yaml`; pr-17456.md; 2026-10-28 batch: pr-17718.md, pr-17543.md, pr-17807.md, pr-17842.md, pr-17766.md, pr-17770.md, `raw/kueue/README.md`, `raw/kueue/site/content/en/docs/getting-started/installation.md`, `raw/kueue/site/content/en/docs/tasks/troubleshooting/troubleshooting_delete_clusterqueue.md`.

**Last updated**: 2026-10-28

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

Recurring themes in the issue tracker confirm this audience: RayJob adoption ([[issue-10438]]), PyTorchJob gang-scheduling ([[issue-2796]]), DRA/device support ([[pr-3071]]), and topology-aware placement for ML training ([[issue-2724]]).

### Public adopters list

The website's adopters page renders `site/data/adopters.yaml` as text cards (name, URL, type, description, integrations, contact; no logo needed). At kueue@3bbb8cce4 it lists: Canva, CyberAgent, DaoCloud, WattIQ, Horizon, FAR AI, Shopee, Mondoo, Google Cloud, Onna Technologies, IBM Research, Innovatrics, Red Hat, Octue, LY Corporation, Preferred Networks, Wayve, Krea AI, Parasail, Netflix, the NYCU Office of AI Affairs, CoreWeave and Etsy. Etsy, added by pr-17456, runs Kueue on GKE as the admission layer of its ML platform with the RayCluster and RayJob integrations (source: raw/kueue/site/data/adopters.yaml, pr-17456.md). To add an organisation, append an entry to that file in a PR with `/area website`.

## Supported Kubernetes versions

Kubernetes **1.35 or newer** is recommended. Only those versions are officially supported and tested; older ones may work. Kueue drops a Kubernetes minor when it reaches end of life: 1.34 was removed from the e2e matrix and the docs on its EOL date, 2026-10-27 (source: pr-17807.md; raw/kueue/README.md, installation.md). The tested set and how it changes: [[release-process#Kubernetes version support]].

## The landing README

pr-17718 (merged 2026-10-27, by mimowo) turned `README.md` into a short landing page:

- capabilities at a glance;
- a **Get started** section with the support statement, one `kubectl apply --server-side` of the latest `manifests.yaml`, and a link to the quick start;
- collapsible sections for integrations, roadmap, configuration and operations guides, production readiness, and testing and compatibility, which includes the TestGrid dashboards per Kubernetes version.

The PR says every earlier link was kept (146 unique links); only the badge images were dropped. pr-17543 added **Help Kueue grow**: star the repository, add your organisation to `site/data/adopters.yaml`, or share an experience on Medium with the `kueue` tag (source: pr-17718.md, pr-17543.md). On release branches, `make prepare-release-branch` rewrites the README's doc links to the branch's versioned docs (`/v0.X/docs/`) (source: pr-17842.md; see [[release-process]]).

## Uninstalling: delete Kueue objects first

Kueue puts the `kueue.x-k8s.io/resource-in-use` finalizer on Workloads, ClusterQueues, ResourceFlavors, AdmissionChecks and Topologies, and `kueue.x-k8s.io/managed` on the Pods it manages. **Only the Kueue controller removes them.** Deleting the release manifests or the Helm release while such objects exist removes the controller together with the CRDs, and the objects and CRDs stay `Terminating`. The installation guide (pr-17766, published to the website by pr-17770) now says to delete, while the controller still runs, in this order:

1. Jobs submitted to Kueue (Jobs, JobSets, Pods and so on).
2. Leftover Workloads, for example a prebuilt Workload that no job adopted.
3. LocalQueues and ClusterQueues.
4. Cohorts, ResourceFlavors and AdmissionChecks.
5. Topologies.

LocalQueues and Cohorts carry no finalizer and are in the list only because of what references them. If Kueue was already uninstalled, the troubleshooting page ("What if Kueue was uninstalled first?") says to remove **only** Kueue's finalizer entry from each stuck object and keep other controllers' finalizers. Never do that while the controller runs, because it bypasses checks such as deleting a ClusterQueue whose quota is still in use (source: pr-17766.md; raw/kueue/site/content/en/docs/getting-started/installation.md, troubleshooting_delete_clusterqueue.md). See [[cluster-queue]], [[workload]].

## What Kueue is not

- It is **not** a replacement for `kube-scheduler`. It does not make placement decisions (which node a Pod lands on); it only decides *when* a Pod gets to exist.
- It is **not** a job runtime. The actual job execution is handled by `Job`, `JobSet`, `RayJob`, etc. — the upstream controllers Kueue integrates with.
- It is **not** a cluster autoscaler, though it can integrate with one through the [[admission-check]] + ProvisioningRequest mechanism ([[pr-7673]]).

## Related pages

- [[architecture]] — how the pieces fit together.
- [[workload]] — the gated-job object.
- [[cluster-queue]] — the quota pool.
- [[integrations]] — which job APIs are supported.
- [[release-process]] — releases, supported Kubernetes versions.
- [[kueuectl]], [[dashboard]] — the CLI and the KueueViz UI.
