# Issue #1762: Cleanup Failed pods once replacement Pods are present

**Summary**: Cleanup Failed pods once replacement Pods are present

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1762

**Last updated**: 2024-03-04T20:30:54Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-02-21T21:08:12Z
- **Updated**: 2024-03-04T20:30:54Z
- **Closed**: 2024-03-04T20:30:54Z
- **Labels**: `kind/feature`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Cleanup Failed pods once there is a level of confidence that replacement Pods exist and the Workload object wouldn't be garbage collected.

We need to be mindful of possible race conditions that could end up finalizing all Pods too early. Integration and E2E tests are a must. 

**Why is this needed**:

Keeping the terminated pods was a conscious design decision for pod groups for a first implementation https://github.com/kubernetes-sigs/kueue/tree/main/keps/976-plain-pods

However, in a busy system where lots of preemptions could happen, the unfinalized pods could cause unnecessary load in the etcd+apiserver.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc: Update KEP with the proposed design
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2024-02-22T15:20:29Z

/assign

### Comment by [@kannon92](https://github.com/kannon92) — 2024-02-22T15:56:51Z

A relevant upstream issue that could be a good long term solution: https://github.com/kubernetes/kubernetes/issues/122187

Not sure if its that related as this would probably not know about replacement pods being present.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-22T16:44:04Z

Not related. Whatever k/k does, it shouldn't get in the way of finalizers, which we are using here.
