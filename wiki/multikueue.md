# MultiKueue

**Summary**: MultiKueue dispatches [[workload]]s from a **manager cluster** to one of several **worker clusters**. Users submit jobs on the manager as usual; MultiKueue (implemented as an [[admission-check]]) picks a worker cluster with capacity, forwards the job, and mirrors status back. It's how one Kueue installation governs a fleet of clusters.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

---

## Topology

- **Manager cluster** — runs Kueue with MultiKueue configured. Has ClusterQueues, LocalQueues, Workloads, but no actual worker Pods.
- **Worker clusters** — run their own Kueue. They are registered on the manager via `MultiKueueCluster` (a connection config) and `MultiKueueConfig` (which worker clusters to use for a given AdmissionCheck).
- **AdmissionCheck** — a `MultiKueue`-typed AdmissionCheck on the manager's ClusterQueue gates admission on a worker cluster accepting the job.

## Flow

1. User creates a Job on the manager cluster, labeled with a [[local-queue]].
2. Manager's integration controller creates a suspended Workload with QuotaReserved.
3. MultiKueue check kicks in: it picks a worker cluster (preferring clusters with capacity per the Workload's requirements) and creates a mirror Job there.
4. Worker cluster's Kueue admits the mirror Workload through its own pipeline.
5. Once the worker Workload is Admitted, the MultiKueue check on the manager returns Ready.
6. The manager Workload is Admitted; the integration unsuspends the manager Job (cosmetically — Pods don't exist on the manager).
7. Status (conditions, active Pods, completion) is mirrored from the worker Workload back to the manager Workload on a reconcile loop.

## Why a check rather than a scheduler plugin

Using the [[admission-check]] extension point kept MultiKueue out of Kueue's core scheduler. Any number of dispatch policies can be implemented as checks; MultiKueue is one such implementation. This is why there's no dedicated "MultiKueue controller" in the core — it reuses the existing check mechanism.

## Which integrations are supported

Not every job integration trivially mirrors. MultiKueue has specific integration work per job type:

- batch/v1 Job, JobSet — early and stable.
- Kubeflow jobs (PyTorchJob, MPIJob, TFJob, etc.) — rolled out later.
- RayJob, RayCluster — worker-side reconciliation is complex because Ray's state is non-trivial.
- Plain Pods and PodGroups — added with caveats ([[issue-2341]], [[issue-4719]]).
- Priority class mutation on managed workloads ([[issue-7429]] — support mutating the priority class for workloads managed by MultiKueue).

A general tracking theme: "Fair Share Preemption with MultiKueue + Plain Pods - Preempted Pod not Terminated in the Manager Cluster" ([[issue-5979]]) captures the cross-cluster preemption mirroring problem.

## Worker cluster selection

Worker choice is per-Workload: when the MultiKueue check evaluates, it queries each candidate worker cluster for free capacity (via a lightweight RPC reading the worker's ClusterQueue status), chooses one, and dispatches. There's no cross-worker global optimization — each admission cycle picks independently.

## KEP tracker and graduation

MultiKueue was built under its own KEP; graduation work is tracked in recurring issues (representative: [[issue-10626]], [[pr-10684]], [[pr-10656]]). Priority-class mutation ([[issue-7429]]) is indicative of the feature area still being shaped.

## Operational considerations

- **Kubeconfigs.** The manager needs credentials to each worker. These live in a Secret referenced by `MultiKueueCluster`.
- **Version skew.** Worker clusters must run a Kueue version compatible with the manager — cross-version mirror-Workload fields can drift.
- **Observability.** Metrics expose both manager-side admission and mirror-side dispatch; both should be scraped for end-to-end visibility. See [[metrics]].
- **Plain Pods caveat.** Because plain Pods aren't owned by a controller the manager can suspend, enabling MultiKueue for plain Pods required extra glue ([[issue-2341]]).

## Related pages

- [[admission-check]] — MultiKueue is one.
- [[workload]] — mirror workloads exist on each worker.
- [[integrations]] — which job types can be dispatched.
- [[multikueue-orchestrated-preemption]] — **[Alpha]** serializes preemption across worker clusters to avoid duplicate disruption.
