# MultiKueue

**Summary**: MultiKueue dispatches [[workload]]s from a **manager cluster** to one of several **worker clusters**. Users submit jobs on the manager as usual; MultiKueue (implemented as an [[admission-check]]) picks a worker cluster with capacity, forwards the job, and mirrors status back. It's how one Kueue installation governs a fleet of clusters.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-05-06

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

## MultiKueueCluster reconnect mechanics

When a worker cluster's apiserver becomes unreachable, the manager's `clustersReconciler` retries on an exponential backoff (`pkg/controller/admissionchecks/multikueue/multikueuecluster.go`).

**Backoff formula.** `retryAfter(n) = 2^(min(n, 7) - 1) * 5s`, where `n = failedConnAttempts`. Sequence: `5s, 10s, 20s, 40s, 80s, 160s, 320s`, capped at ~5m20s. `retryIncrement = 5s`, `retryMaxSteps = 7`.

**State.** `failedConnAttempts` is held on the `remoteClient`. It's incremented on each watch failure inside `setConfig` and reset to `0` only when the watch is successfully (re)established or when the kubeconfig itself changes. The `connecting` atomic flag stays `true` across failures, so subsequent reconciles re-enter the connect path even if the config is unchanged.

**Trigger sources for a reconcile.** A retry can be queued by any of:
- The `RequeueAfter` returned from the previous failed reconcile (this is the throttled path).
- A `watch-ended` event when a previously running watch goroutine exits.
- A change to the `MultiKueueCluster` object — **including the controller's own status patch**.

**Why two consecutive failures appear in the same second.** When a healthy cluster first goes down, the `MultiKueueClusterActive` condition flips `True/Connected → False/ClientConnectionFailed`. That status write produces an object-change event that immediately enqueues a second reconcile (before the `RequeueAfter` from the first one fires). The second reconcile increments `failedConnAttempts` to 2 and logs `retryAfter: 10s`; its status update is a no-op because `cmpConditionState` sees the same condition, so the cascade stops there. From that point on, retries are paced strictly by `RequeueAfter`.

This is an artifact of condition-flip + reconcile-on-status-update, not two real connection attempts being deliberately scheduled in the same second.

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
