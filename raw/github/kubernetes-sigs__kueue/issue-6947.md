# Issue #6947: Inadmissible Workload Blocks ClusterQueue

**Summary**: Inadmissible Workload Blocks ClusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6947

**Last updated**: 2025-09-23T07:32:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2025-09-22T13:41:23Z
- **Updated**: 2025-09-23T07:32:28Z
- **Closed**: 2025-09-23T07:32:27Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 5

## Description

**What happened**:
Consider the following structure:
- Cohort
  - ClusterQueueA(Nominal=3, ReclaimWithinCohort=any, QueueingStrategy=BestEffortFifo)
  - ClusterQueueB(Nominal=0)

Submit the following workloads, in order:
- workload(1) -> ClusterQueueB
- workload(4) -> ClusterQueueA
- workload(3) -> ClusterQueueA

Workload(3) yields to Workload(4) for a single cycle, triggering preemption of Workload(1). However, the next cycle we try to schedule Workload(4) and Workload(1). This cycle repeats, resulting in Workload(1) being preempted indefinitely, and even worse, Workload(3) failing to schedule.

**What you expected to happen**:
Workload(3) should schedule after reclaming quota, despite pathological Workload(4)

**How to reproduce it (as minimally and precisely as possible)**:
See integration test: https://github.com/kubernetes-sigs/kueue/commit/6883dcca570536fe3c506b2fae6e4a565144891a

**Anything else we need to know?**:

**Environment**:
- Kueue version (use `git describe --tags --dirty --always`): v0.14.0-rc.0-5-g6883dcca5 (main at commit efc4a1bc10eacdd8a86129ccae34eadf3dd75424)

## Discussion

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-09-22T13:47:25Z

Two paths worth considering:

1) exponential backoff workloads which failed to schedule for certain reasons e.g. `NoFit` assigned by FlavorAssigner, as in the case of Workload(4) in this issue
2) exponential backoff for preempted workloads (related to https://github.com/kubernetes-sigs/kueue/issues/6861, if we wanted to have a mechanism to stop preemption loops/frequent preemptions)

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-22T16:03:16Z

It looks like this could be related to: https://github.com/kubernetes-sigs/kueue/issues/6929

### Comment by [@amy](https://github.com/amy) — 2025-09-22T16:12:42Z

If its the same, I prefer to close this one to continue the discussion on https://github.com/kubernetes-sigs/kueue/issues/6929

Just in case its there's some nuanced difference. I dont like exponential backoff bc it introduces the possibility that during the backoff a lower priority workload could slip in while the head is backing off, violating CQ priority ordering.

This could mean that p1 inadmissible blocks p2 admissible forever / a really long time. For which... maybe there's a way to provide metrics insight on when a head is blocking admissible candidates. (Thinking about the algorithm though, this seems really hard.)

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-09-23T07:32:22Z

Yes, it is the same. Will close in favor of #6929 

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-23T07:32:28Z

@gabesaba: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6947#issuecomment-3322767967):

>Yes, it is the same. Will close in favor of #6929 
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
