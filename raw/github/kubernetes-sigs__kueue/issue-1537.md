# Issue #1537: respect Pod/Job  PriorityClass

**Summary**: respect Pod/Job  PriorityClass

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1537

**Last updated**: 2024-01-10T01:07:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@panpan0000](https://github.com/panpan0000)
- **Created**: 2024-01-02T08:05:29Z
- **Updated**: 2024-01-10T01:07:15Z
- **Closed**: 2024-01-10T01:07:14Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Among a ClusterQueue, workloads may carry with different PriorityClass, but it doesn't help for preemption.

Assuming case below:
1. a big workload with lower priority has been admitted and running,
2. then another workload created, but insufficient  resource and hit clusterQueue quota
3. the new workload will be pending( not admitted) by Kueue
4. no chance for new workloads' pods generation, even with higher priorityClass, they can not preempt the old workload pods with in-tree kubernetes PriorityClass mechanism . 

For underlaying solution ,I guess it's similar with issue https://github.com/kubernetes-sigs/kueue/issues/1530
But I'm stating a exact use case here.

**Why is this needed**:

Priority Preemption inside a Queue. for example, inside one namespace/tenant, offline batching job should be lower priority than real-time serving job.

**Completion requirements**:


This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@panpan0000](https://github.com/panpan0000) — 2024-01-10T01:07:14Z

I found there is `priority` field for `Workload` CR , and it will derive from the pod priority and priorityClass.
so the workload will be prioritized in kueue perspective .
I will close this .
