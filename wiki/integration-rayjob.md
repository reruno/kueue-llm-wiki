# Integration: RayJob and RayCluster

**Summary**: KubeRay's RayJob and RayCluster each have their own Kueue integration. RayCluster is a long-lived cluster you submit Ray jobs into; RayJob bundles a cluster with a job entrypoint. Kueue accounts for the head pod, the worker groups, and (for RayJob) a short-lived submitter Pod.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-06-29

---

## Shape

A RayCluster has `spec.headGroupSpec` and `spec.workerGroupSpecs[]`. A RayJob additionally has `spec.submitterPodTemplate`.

Kueue's RayCluster integration produces:

- One PodSet for the head.
- One PodSet per worker group (where each PodSet's `count = replicas × minReplicas`).

The RayJob integration further accounts for the **submitter Pod** — a transient Pod that drives the job via the Ray client. "PodSets for RayJobs should account for submitter Job Pod" ([[issue-1434]]) tracked making that accounting explicit so the cluster's quota picture doesn't omit it.

**Worker-group cap.** Because each worker group becomes its own PodSet and the head reserves one PodSet, the number of worker groups is bounded by the [[workload]] `spec.podSets` length limit. [[pr-11388]] raised that limit from 8 to **10**, so a RayCluster/RayJob/RayService can now declare up to **9 worker groups** (was 7).

## Adding RayCluster support

RayCluster came later than RayJob ("Add support for RayCluster" — [[issue-1272]]). The integration posed questions about longer-lived Workloads whose underlying object doesn't naturally have a "finished" state.

## Suspend vs scheduling gates

RayCluster's native `spec.suspend` flag controls whether the Ray head and workers are created. Kueue toggles it. Dynamic scaling (adding worker replicas after admission) uses Pod scheduling gates per [[elastic-jobs]]; "Kueue sometimes does not inject scheduling gates for elastic jobs" ([[issue-10167]]) and "RayCluster with elastic jobs via workload-slices support should support scheduling pending workload after freeing capacity on scale-down" ([[issue-10170]]) are the canonical elastic+Ray issues.

## Operational quirks

- **Status timeliness.** RayJob status updates lagged ([[issue-1164]]). Admitted RayJobs sometimes stayed pending when `manageJobsWithoutQueueName: true` was enabled ([[issue-1568]]).
- **Preempted RayJob resume.** "Preempted RayJob will not resume when resource reclaimed" ([[issue-1146]]) was an earlier bug; resuming Ray state after preemption is not trivial.
- **In-tree autoscaling.** "Flaky E2E: Kuberay Should run a rayjob with InTreeAutoscaling" ([[issue-10438]], [[issue-10642]]) — interaction with Ray's internal autoscaler is complex because it changes replica counts outside Kueue's direct control.
- **redis-cleanup Pods.** "Kueue does not remove the scheduling gate from Ray's redis-cleanup jobs" ([[issue-8443]]) — a post-termination Pod got left gated.

## Ray version pin (v0.18.0)

Kueue's e2e fixtures and the RayJob submitter image were bumped from **Ray 2.41.0 → 2.53.0** in [[pr-10707]] (cherry-picks [[pr-10958]] and [[pr-10959]]). The 2.41.0 line had a SIGABRT in the opencensus dependency (`ray-project/kuberay#4760`) that destabilized the Ray submitter Pod. 2.53.0 also requires that Kueue's TAS RayJob e2e bumps the head CPU and CQ quota — see the test bump in PR #10970. Operators upgrading to v0.18 should plan for this Ray version's resource baseline.

## Redis cleanup Job accounting (GCS fault tolerance, v0.19)

When KubeRay **GCS fault tolerance** is enabled, KubeRay spawns a short-lived **Redis cleanup Job** during RayCluster teardown (to clear the cluster's data from the external Redis). Kueue built PodSets only from the head + worker groups, so the cleanup Job's requests were never reserved → quota **under**-accounting ([[pr-11260]], fixes [[issue-10946]]).

The fix **folds** the cleanup Job's requests into the **Ray head PodSet** using max-accounting, rather than adding a separate PodSet (which would have eaten one of the 8 `MaxPodSets` slots). Details:

- The cleanup Job's requests are **hardcoded in KubeRay** at **200m CPU / 256Mi memory**; `accountForRedisCleanupInHeadPodSet` merges them into the head container via `MergeResourceListKeepMax` (so the head's reservation is `max(head, cleanup)`, not a sum).
- Gated by the **`KubeRayAccountForRedisCleanup`** feature gate (Beta, default on; introduced v0.19, GA targeted v0.21) — a bailout for clusters running the KubeRay operator with `ENABLE_GCS_FT_REDIS_CLEANUP=false`. The accounting only applies when GCS fault tolerance is actually detected (`GcsFaultToleranceOptions != nil` or the annotation).
- `ExpectedPodSetsCount = len(workerGroupSpecs) + 1`; the PodSet count is **unchanged** because the cleanup is folded into the head. Applies to all three controllers — **RayCluster, RayJob, and RayService**.

## MultiKueue

RayJob and RayCluster have MultiKueue adapters; cross-cluster status mirroring is nontrivial because Ray's state space is large.

**RayService worker RBAC.** RayService has been MultiKueue-managed since v0.17.0, but the worker-cluster ClusterRole generated by `create-multikueue-kubeconfig.sh` originally omitted `rayservices` / `rayservices/status`, so a dispatched RayService failed at the API level on the worker. [[pr-11400]] adds those rules; hand-written worker ClusterRoles must include them. See [[multikueue#RBAC: RayService on worker clusters]].

## TAS

Rank-based ordering within TAS for Ray worker groups is tracked ([[issue-3716]] — TAS: Implement e2e tests for RayJob with TAS).

## Related pages

- [[integrations]] — integration mechanics.
- [[workload]] — head + workers + submitter decomposition.
- [[elastic-jobs]] — Ray is the biggest consumer.
- [[multikueue]] — Ray + multi-cluster.
- [[topology-aware-scheduling]] — Ray + topology.
