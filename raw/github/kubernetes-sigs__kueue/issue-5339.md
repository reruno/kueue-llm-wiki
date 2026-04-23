# Issue #5339: [AFS] Add entrance penalty for admitted Workloads

**Summary**: [AFS] Add entrance penalty for admitted Workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5339

**Last updated**: 2025-07-25T15:04:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-05-26T09:02:56Z
- **Updated**: 2025-07-25T15:04:30Z
- **Closed**: 2025-07-25T15:04:30Z
- **Labels**: `kind/feature`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
When a Workload gets admitted, we should increase the resource usage in LQ's FairSharing status. The penalty should be equivalent to the period of one `.usageSamplingInterval`

**Why is this needed**:
In case there are 2 LQs with the same (without the loss of generality, let's say 0) resource usage in FairSharing status, Kueue admits all Workloads with the respect of the priorities/creation timestamp until the status is recomputed (the worst case scenario, after the `.usageSamplingInterval` time).

We'd like to provide better support for such a case, so the admission of a Workload increases its LQ's FairSharing resource usage right away, and it's more fair

**Completion requirements**:

This feature doesn't require any API changes. It requires code changes in the code of Kueue's scheduler. During admission cycle we should update the LQ's usage by the entrance penalty. At the beginning of each scheduling cycle we should recreate heap to make sure the entrance penalty from the previous cycle is respected

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-06-27T13:03:49Z

/cc @mbobrovskyi

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-27T13:27:18Z

> This feature doesn't require any API changes.

Yes, but it changes the semantics of the mode, so @PBundyra I think we need to reflect this in the kEP first.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-27T13:32:24Z

IIUC the penalty should not be accounted on the restart of Kueue, right? So, maybe it is a good idea to account it during assumption into cache (which would happen on regular admission), but not on Kueue restart, IIRC.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-06-27T15:06:41Z

Related PR that populates snapshot with `AdmissionScope` field 
https://github.com/kubernetes-sigs/kueue/pull/5632

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-07-04T09:39:01Z

/assign
