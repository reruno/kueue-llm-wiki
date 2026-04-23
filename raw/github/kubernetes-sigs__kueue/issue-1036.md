# Issue #1036: Prevent ClusterQueue with pending workloads to block borrowing in other flavors in the cohort

**Summary**: Prevent ClusterQueue with pending workloads to block borrowing in other flavors in the cohort

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1036

**Last updated**: 2023-08-17T16:25:24Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-08-02T19:02:23Z
- **Updated**: 2023-08-17T16:25:24Z
- **Closed**: 2023-08-17T16:25:24Z
- **Labels**: `kind/feature`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 1

## Description

**What would you like to be added**:

In #475 and #805, we guaranteed the following:
If a ClusterQueue has pending workloads that could fit in the nominalQuota if other workloads finish (regardless of whether preemption is enabled), we don't admit other workloads in the cohort that can fit by borrowing. This allows the pending workloads to be admitted as soon as the quota becomes available without needing to trigger extra preemptions (or waiting for more jobs to finish, if preemption is disabled).

However, the check is too coarse: if the borrowing is happening in a different flavor, we shouldn't block it.

A possible solution is to track not just which cohorts already had workloads admitted in a cycle, but also which combinations of (flavor, resource).

Current check per cohort:

https://github.com/kubernetes-sigs/kueue/blob/913d53674ec0f535b28e37a3e854b29575eecce0/pkg/scheduler/scheduler.go#L145-L160

**Why is this needed**:

As users start setting up complex ClusterQueues, with multiple flavors and multiple CQs per cohort, the current check doesn't match user expectations, specially if low priority pending workloads in a ClusterQueue could end up blocking other ClusterQueue.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-08-02T19:02:30Z

/assign @trasc
