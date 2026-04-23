# Integration: JobSet

**Summary**: JobSet is a SIG-Apps API for running a set of related Jobs as one unit — leader + workers, multi-replica training, etc. It's the recommended primitive for complex training workloads because it's a Kueue-native match (explicit PodSet-per-replicated-job, built-in suspend semantics).

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

---

## Shape

A JobSet has `replicatedJobs[]`, each with a `template` (Job spec) and a `replicas` count. Total Pods = sum over `replicatedJobs` of (replicas × job-parallelism).

The integration produces one Workload PodSet per `replicatedJobs[]` entry, with `count = replicas × parallelism`. This gives Kueue per-template quota accounting — the leader and workers can have different resource requirements and different [[resource-flavor]] assignments.

## Edge cases

- **`replicas: 0`** was not handled initially; creating a JobSet with a zero-replica template used to fail ([[issue-2227]], [[issue-2532]] — flaky integration for zero-replica replicatedJob).
- **Section naming in docs.** "JobSet is not mentioned in section on batch users" ([[issue-1522]]) is a doc-gap marker, not a functional one.
- **Suspend semantics.** Suspending a JobSet-typed Workload ([[issue-2096]]) flows down to child Jobs.

## MultiKueue with JobSet

JobSet is well-supported under [[multikueue]] ([[issue-2320]] — a deletion-lag issue between manager and worker). When a JobSet is created on the manager with MultiKueue enabled but no matching ClusterQueue exists, early versions failed at creation ([[issue-2416]]).

## TAS

JobSets are a natural consumer of [[topology-aware-scheduling]]: ML training JobSets benefit from placing all replicas in one rack. "TAS: Add sanity e2e test for JobSet" ([[issue-3388]]) and related flaky-test noise reflect the breadth of integration testing.

## Related pages

- [[integrations]] — integration mechanics.
- [[workload]] — multi-PodSet decomposition.
- [[topology-aware-scheduling]] — gang-placement in topology domains.
- [[multikueue]] — multi-cluster dispatch.
