# Integration: batch/v1 Job

**Summary**: The integration for Kubernetes' built-in `batch/v1.Job`. It's the simplest and most mature — a Job has one PodSet (or one plus a `parallelism`/`completions` count). Kueue suspends the Job at creation and unsuspends on admission.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

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

## Related pages

- [[workload]] — one PodSet per Job.
- [[elastic-jobs]] — dynamic parallelism.
- [[integrations]] — integration mechanics in general.
