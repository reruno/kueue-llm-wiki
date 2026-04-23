# Issue #533: Support preemption within ClusterQueue while borrowing

**Summary**: Support preemption within ClusterQueue while borrowing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/533

**Last updated**: 2023-03-10T18:54:42Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-01-27T15:58:59Z
- **Updated**: 2023-03-10T18:54:42Z
- **Closed**: 2023-03-10T18:54:42Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 2

## Description

**What would you like to be added**:

Let's assume ClusterQueues A and B in the same cohort, with the following single resource and flavor:

```
A:
  quota: 10
  used: 10
B:
  quota: 10
  used: 9
```

And an incoming workload for A requiring 2 units. The workload could fit by preempting 1 unit from A and borrowing 1 unit from B.

**Why is this needed**:

In #514, borrowing while preempting is not supported. Then, this workload would instead preempt 2 units from A, which is potentially more disruptive.

Supporting this scenario might require:
- updates to the entry sorting logic: workloads that don't require preemption should be admitted first. In the scenario above, if B has an incoming 1 unit Workload, it should be admitted before giving a chance for the workload in A to preempt.
- once preemption with borrowing occurs, do not admit more workloads in the cohort.
- updating `workloadFits` in the `preemption` package to allow borrowing.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc update
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mwielgus](https://github.com/mwielgus) — 2023-03-05T15:20:58Z

After working on this a bit I hit the following problem. Lets imagine that we have 2 queues:

* c1 with cpu min=6 and max=12 (borrowing 6 from c2)
* c2 with cpu min=6 and max=12 (borrowing 6 form c1)

both belonging to the same cohort, and both having reclaim policy set to Any. Lets assume that the content of the queues is:

* c1 - 2 pods requesting 4 cpus  (borrowing 2 cpus from c2).
* c2 - 1 pod requesting 4 cpus 

Now a pod requesting 4 cpus comes to c2. With the previous logic nothing would happen. The new pod needs to borrow 4 and preempt one of the pods from c1 who are borrowing resources from c2. Preemption and borrowing is not allowed.

What if we allow it. The new pod preempts one of c1 pods to get 2 resources back, and for a moment, freeing another 2, just enough to get in.  But now the situation is symmetrical.

* c1 - 1 pod requesting 4 cpus
* c2 - 2 pods requesting 4 cpus  (borrowing 2 cpus from c1).

And the just preempted pod will get back to the queue and start preempting pods c2 in a moment. The possible solutions are:

*  [O1] Don't allow preemptions and borrowing at the same time.
*  [O2] Allow preemptions and borrowing only if reclaim policy is set to LowerPriority.
*  [O3] Allow preempting only lower priority pods on borrowing, even if the reclaim policy is Any.
*  [O4] More sophisticated preemption algorithm that will notice cycles.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-06T13:46:54Z

The scenario you describe is what led me to disallow preemption **with** borrowing. I think the solution is O1.

But note that the issue proposed here is slightly different. It doesn't involve preemption of the other cluster queue.

What I would like to allow is being able to borrow from the other clusterqueue while preempting workloads from the same cluster queue as the incoming workload.

In the example in the description above, a workload is coming to clusterQueue A, preempting a workload from A, but borrowing 1 unused unit from B.
