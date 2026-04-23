# Integration: RayJob and RayCluster

**Summary**: KubeRay's RayJob and RayCluster each have their own Kueue integration. RayCluster is a long-lived cluster you submit Ray jobs into; RayJob bundles a cluster with a job entrypoint. Kueue accounts for the head pod, the worker groups, and (for RayJob) a short-lived submitter Pod.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

---

## Shape

A RayCluster has `spec.headGroupSpec` and `spec.workerGroupSpecs[]`. A RayJob additionally has `spec.submitterPodTemplate`.

Kueue's RayCluster integration produces:

- One PodSet for the head.
- One PodSet per worker group (where each PodSet's `count = replicas × minReplicas`).

The RayJob integration further accounts for the **submitter Pod** — a transient Pod that drives the job via the Ray client. "PodSets for RayJobs should account for submitter Job Pod" (source: issue-1434.md) tracked making that accounting explicit so the cluster's quota picture doesn't omit it.

## Adding RayCluster support

RayCluster came later than RayJob ("Add support for RayCluster" — source: issue-1272.md). The integration posed questions about longer-lived Workloads whose underlying object doesn't naturally have a "finished" state.

## Suspend vs scheduling gates

RayCluster's native `spec.suspend` flag controls whether the Ray head and workers are created. Kueue toggles it. Dynamic scaling (adding worker replicas after admission) uses Pod scheduling gates per [[elastic-jobs]]; "Kueue sometimes does not inject scheduling gates for elastic jobs" (source: issue-10167.md) and "RayCluster with elastic jobs via workload-slices support should support scheduling pending workload after freeing capacity on scale-down" (source: issue-10170.md) are the canonical elastic+Ray issues.

## Operational quirks

- **Status timeliness.** RayJob status updates lagged (source: issue-1164.md). Admitted RayJobs sometimes stayed pending when `manageJobsWithoutQueueName: true` was enabled (source: issue-1568.md).
- **Preempted RayJob resume.** "Preempted RayJob will not resume when resource reclaimed" (source: issue-1146.md) was an earlier bug; resuming Ray state after preemption is not trivial.
- **In-tree autoscaling.** "Flaky E2E: Kuberay Should run a rayjob with InTreeAutoscaling" (source: issue-10438.md, source: issue-10642.md) — interaction with Ray's internal autoscaler is complex because it changes replica counts outside Kueue's direct control.
- **redis-cleanup Pods.** "Kueue does not remove the scheduling gate from Ray's redis-cleanup jobs" (source: issue-8443.md) — a post-termination Pod got left gated.

## MultiKueue

RayJob and RayCluster have MultiKueue adapters; cross-cluster status mirroring is nontrivial because Ray's state space is large.

## TAS

Rank-based ordering within TAS for Ray worker groups is tracked (source: issue-3716.md — TAS: Implement e2e tests for RayJob with TAS).

## Related pages

- [[integrations]] — integration mechanics.
- [[workload]] — head + workers + submitter decomposition.
- [[elastic-jobs]] — Ray is the biggest consumer.
- [[multikueue]] — Ray + multi-cluster.
- [[topology-aware-scheduling]] — Ray + topology.
