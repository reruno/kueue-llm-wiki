# Integration: JobSet

**Summary**: JobSet is a SIG-Apps API for running a set of related Jobs as one unit — leader + workers, multi-replica training, etc. It's the recommended primitive for complex training workloads because it's a Kueue-native match (explicit PodSet-per-replicated-job, built-in suspend semantics).

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

---

## Shape

A JobSet has `replicatedJobs[]`, each with a `template` (Job spec) and a `replicas` count. Total Pods = sum over `replicatedJobs` of (replicas × job-parallelism).

The integration produces one Workload PodSet per `replicatedJobs[]` entry, with `count = replicas × parallelism`. This gives Kueue per-template quota accounting — the leader and workers can have different resource requirements and different [[resource-flavor]] assignments.

## Edge cases

- **`replicas: 0`** was not handled initially; creating a JobSet with a zero-replica template used to fail (source: issue-2227.md, source: issue-2532.md — flaky integration for zero-replica replicatedJob).
- **Section naming in docs.** "JobSet is not mentioned in section on batch users" (source: issue-1522.md) is a doc-gap marker, not a functional one.
- **Suspend semantics.** Suspending a JobSet-typed Workload (source: issue-2096.md) flows down to child Jobs.

## MultiKueue with JobSet

JobSet is well-supported under [[multikueue]] (source: issue-2320.md — a deletion-lag issue between manager and worker). When a JobSet is created on the manager with MultiKueue enabled but no matching ClusterQueue exists, early versions failed at creation (source: issue-2416.md).

## TAS

JobSets are a natural consumer of [[topology-aware-scheduling]]: ML training JobSets benefit from placing all replicas in one rack. "TAS: Add sanity e2e test for JobSet" (source: issue-3388.md) and related flaky-test noise reflect the breadth of integration testing.

## Related pages

- [[integrations]] — integration mechanics.
- [[workload]] — multi-PodSet decomposition.
- [[topology-aware-scheduling]] — gang-placement in topology domains.
- [[multikueue]] — multi-cluster dispatch.
