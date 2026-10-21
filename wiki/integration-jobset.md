# Integration: JobSet

**Summary**: JobSet is a SIG-Apps API for running a set of related Jobs as one unit — leader + workers, multi-replica training, etc. It's the recommended primitive for complex training workloads because it's a Kueue-native match (explicit PodSet-per-replicated-job, built-in suspend semantics).

**Sources**: `raw/github/kubernetes-sigs__kueue/`., pr-16370.md, pr-16436.md

**Last updated**: 2026-10-21

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

## Restore guard on pod set count mismatch

`RestorePodSetsInfo` returns false and skips the restore when the JobSet's pod set count differs from its admitted Workload; it now logs the mismatch at V(2) with expected and actual counts (source: pr-13114.md; see [[job-framework-interface#`RestorePodSetsInfo` takes a context]]). Open: stale `reclaimablePods` after a JobSet restart can under-count usage and over-admit ([[issue-14609]]).

## Child Jobs and `SkipChildJobSuspension`

A JobSet's child `batch/v1` Jobs are *non-top-level* jobs for the generic reconciler. By default Kueue still suspends a running child Job when no unfinished JobSet Workload can be found. With the Alpha gate `SkipChildJobSuspension` (off by default) Kueue leaves that to the JobSet controller, which already suspends its children when the JobSet is suspended. Review noted that the old code was originally added as a workaround for JobSet–Kueue integration issues (source: pr-16370.md). See [[job-framework-interface#Child jobs: `SkipChildJobSuspension`]].

## Related pages

- [[integrations]] — integration mechanics.
- [[workload]] — multi-PodSet decomposition.
- [[topology-aware-scheduling]] — gang-placement in topology domains.
- [[multikueue]] — multi-cluster dispatch.
- [[job-framework-interface]]
