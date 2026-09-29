# Integration: batch/v1 Job

**Summary**: The integration for Kubernetes' built-in `batch/v1.Job`. It's the simplest and most mature — a Job has one PodSet (or one plus a `parallelism`/`completions` count). Kueue suspends the Job at creation and unsuspends on admission.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-09-29

---

## Mechanics

- **Trigger**: a Job carries `kueue.x-k8s.io/queue-name: <lq>`.
- **Suspend**: `.spec.suspend: true` is set before any Pods are created. The `batch/v1` controller respects the field natively — no Pod objects exist while suspended.
- **PodSet**: one PodSet, with `count = max(parallelism, completions)`.
- **Admit**: Kueue flips `.spec.suspend: false`. `kube-controller-manager`'s Job controller creates the Pods.
- **Finish**: Job's `Complete` or `Failed` condition triggers Workload's `Finished`.

## Elastic parallelism

With the `ElasticJobsViaWorkloadSlices` feature gate (see [[elastic-jobs]]), `parallelism` can be changed on an admitted Job. The integration observes the change and adjusts the Workload via WorkloadSlices. Flaky tests around this path are tracked ([[issue-6161]] — elastic Job scale-down/up flakes).

## MultiKueue

The batch/v1 Job adapter is the canonical MultiKueue adapter: the manager creates a mirror Job on the worker; status is mirrored back. See [[multikueue]].

## MultiKueue does not copy `spec.ttlSecondsAfterFinished`

When a `batch/v1` Job is dispatched through [[multikueue]], the remote worker Job is created **without** `spec.ttlSecondsAfterFinished`, so the worker's TTL controller cannot delete the completed remote Job before its terminal status has been synced back to the manager. The manager Job keeps its own TTL and remains authoritative for cleanup. Behind `MultiKueueBatchJobClearingTTLSecondsAfterFinishedOnWorkerCluster` — Beta/on in v0.20, Alpha/off in the 0.18 and 0.19 backports. See [[multikueue#Worker Job TTL]] ([[pr-14734]], [[pr-14827]], [[pr-14828]]).

## Reclaimable pods when `parallelism > completions`

Correction to the PodSet count above: the Workload PodSet reserves `min(parallelism, completions)` pods (`podsCount()`). `ReclaimablePods` used to measure the reclaimable count against `parallelism`, so with `parallelism: 10`, `completions: 5` and one succeeded Pod it reported 6, clamped to the PodSet count of 5, and the 4 still-running Pods no longer held quota (ClusterQueue could over-admit). It now measures against `podsCount()` for both Indexed and NonIndexed Jobs (source: pr-16111.md; backports pr-16132.md, pr-16138.md).

## Zero-parallelism elastic Jobs

A Job created at `parallelism: 0` used to be admitted on whichever flavor came first, and its `nodeLabels` were stamped into the pod template; see [[elastic-jobs#Zero-count PodSets and flavor selection]] (source: pr-15444.md).

## Related pages

- [[workload]] — one PodSet per Job.
- [[elastic-jobs]] — dynamic parallelism.
- [[integrations]] — integration mechanics in general.
