# Issue #3405: Workload above nominal of CQ prioritized over workload within nominal quota of other CQ

**Summary**: Workload above nominal of CQ prioritized over workload within nominal quota of other CQ

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3405

**Last updated**: 2024-11-15T16:22:54Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2024-10-31T18:47:24Z
- **Updated**: 2024-11-15T16:22:54Z
- **Closed**: 2024-11-15T16:22:54Z
- **Labels**: `kind/bug`
- **Assignees**: [@gabesaba](https://github.com/gabesaba), [@PBundyra](https://github.com/PBundyra)
- **Comments**: 3

## Description

**What happened**:
Suppose system has CQs sharing a Cohort. Two CQs are trying to admit a workload. These CQs are lending capacity and configure `reclaimWithinCohort=any`.

Suppose WL1 requests fit within nominal capacity of CQ1, but the sum of the running workloads' plus new workload's requests surpass the nominal + borrowing limit of CQ1.

Suppose WL2 fits within the nominal capacity of CQ2, even considering other running workloads in CQ2. Suppose that excess capacity of CQ2 is being lend out to, and used by other ClusterQueues in the Cohort, so that CQ2 needs to issue preemptions to reclaim its nominal quota.

WL1 will be considered not borrowing ([code](https://github.com/kubernetes-sigs/kueue/blob/d9ade1b2c879601d7d626a425278243f9ff73cc6/pkg/scheduler/flavorassigner/flavorassigner.go#L623-L626)). If WL1 was created before WL2 - and priority sorting/fair sharing are disabled - it will be processed first in a scheduling cycle ([code](https://github.com/kubernetes-sigs/kueue/blob/d9ade1b2c879601d7d626a425278243f9ff73cc6/pkg/scheduler/scheduler.go#L646-L679)).

It may end up reserving capacity in the Cohort ([code](https://github.com/kubernetes-sigs/kueue/blob/d9ade1b2c879601d7d626a425278243f9ff73cc6/pkg/scheduler/scheduler.go#L250-L257)), which WL2 is depending on to be able to schedule ([code](https://github.com/kubernetes-sigs/kueue/blob/d9ade1b2c879601d7d626a425278243f9ff73cc6/pkg/scheduler/scheduler.go#L271-L277)). WL2 is blocked indefinitely, unable to issue preemptions until WL1 successfully schedules.

**What you expected to happen**:
Even without FairSharing enabled, WL2 should be sorted before WL1 and able to issue preemptions immediately, since it fits within nominal capacity without borrowing required.

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:
FairSharing should solve this problem, as CL1+WL1 will have a higher DominantResourceShare than CL2+WL2

**Environment**:
- Kueue version: 0.8.1

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-06T10:30:54Z

/assign @PBundyra 
tentatively

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-08T11:03:21Z

We have investigated the issue with @PBundyra and in our opinion the root cause is in this [line](https://github.com/kubernetes-sigs/kueue/blob/d9ade1b2c879601d7d626a425278243f9ff73cc6/pkg/scheduler/flavorassigner/flavorassigner.go#L620), which will return `borrow=false` (meaning  "does not need borrowing") in the issue description.

This is problematic because the workload does not have any preemption targets and so will need to borrow to get admitted. And, in fact, it is entitled to borrow due to `borrowWithinCohort` enabled.

The bug is for historical reasons - the flavorassigner didn't have access to the list of workloads to determine if borrowing is actually needed or not, so we implemented this line which is just a heuristic. Since this [PR](https://github.com/kubernetes-sigs/kueue/pull/2811)  the flavorassigner has access to the list of workloads, so such a check is possible.

So, I think the proper solution is to simulate the preemption algorithm (similarly as the PR mentioned above, using `getTargets` like [here](https://github.com/kubernetes-sigs/kueue/blob/0f54466b991a7d198eeca306dc75f2aee518c482/pkg/scheduler/preemption/preemption_oracle.go#L45)) and see if, given the set of preemption targets, the workload needs to borrow or not. So, the problematic line will be replaced with `borrow = oracle.NeedsBorrowWhilePreempting(...)`. There are two possibilities to implement that function:
1. by analyzing the list of returned preemption targets and seeing if borrowing is still needed
2. by extending the returned value by `getTargets` to include this information as this is known during the algorithm

I'm leaning towards (2.) as more performant (avoid re-doing the snapshot manipulations). 

Given that the [PR](https://github.com/kubernetes-sigs/kueue/pull/2811) has put the ground work I think this fix is not going to be too complex, but for safety we may consider a feature-gate (TBD).

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-11-14T14:22:53Z

/assign
