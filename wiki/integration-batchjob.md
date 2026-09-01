# Integration: batch/v1 Job

**Summary**: The integration for Kubernetes' built-in `batch/v1.Job`. It's the simplest and most mature — a Job has one PodSet (or one plus a `parallelism`/`completions` count). Kueue suspends the Job at creation and unsuspends on admission.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-09-01

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

## Related pages

- [[workload]] — one PodSet per Job.
- [[elastic-jobs]] — dynamic parallelism.
- [[integrations]] — integration mechanics in general.
