# Issue #6491: ElasticJobs: evicted workload slice does not always reset status.

**Summary**: ElasticJobs: evicted workload slice does not always reset status.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6491

**Last updated**: 2025-08-11T16:27:08Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2025-08-07T04:56:56Z
- **Updated**: 2025-08-11T16:27:08Z
- **Closed**: 2025-08-11T16:27:08Z
- **Labels**: `kind/bug`
- **Assignees**: [@ichekrygin](https://github.com/ichekrygin)
- **Comments**: 1

## Description

**What happened**:

In Kueue, evicted or preempted workloads go through a **status reset** phase where their admission status and quota reservation are cleared. This reset logic is handled by the **Job reconciler**, which detects the `Evicted` condition when processing workloads for a given Job.

In the context of **ElasticJobs**, during a scale-up operation, it’s possible for the *old* workload slice to be evicted or preempted *before* the *new* slice is admitted. When this occurs, the old workload may fall **out of scope** for the Job controller (which only processes the current workload). As a result, the eviction finalization step is never executed, leaving the workload in a partially active state, with its admission and quota reservation still set.

This causes the system to treat the preempted workload as if it's still consuming queue resources, until it is eventually marked as `Finished`.

---

**What you expected to happen**:

The status of a preempted workload should be reset, clearing admission and quota reservation, regardless of whether it is part of an ElasticJob or a regular Job.

---

**How to reproduce it (as minimally and precisely as possible)**:

1. Create an ElasticJob and wait for its workload to be admitted.
2. Scale up the Job so that the resulting workload exceeds the nominal queue CPU capacity. This should cause the *new* workload slice to remain pending.
3. Create a second Job with a **higher** priority class to trigger preemption.
4. Observe that the *old* workload from the lower-priority Job is evicted or preempted.
5. Observe that its `admission` and `quotaReservation` fields are **not reset**, leaving the workload in a lingering, resource-claiming state.

--- 

Related to (and discovered by): #6366 and #6478

## Discussion

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-08-07T15:45:11Z

/assign
