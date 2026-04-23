# Issue #251: Getting heads of queues can be more efficient by checking clusterQueue status

**Summary**: Getting heads of queues can be more efficient by checking clusterQueue status

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/251

**Last updated**: 2022-05-13T16:03:50Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2022-05-06T06:30:02Z
- **Updated**: 2022-05-13T16:03:50Z
- **Closed**: 2022-05-13T16:03:49Z
- **Labels**: `kind/feature`
- **Assignees**: [@kerthcet](https://github.com/kerthcet)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
As @ahg-g mentioned here: https://github.com/kubernetes-sigs/kueue/pull/230#discussion_r862511992, we'd like to add status check in `Heads()` to reduce the waste of calculating.

**Why is this needed**:
More efficient.

**Completion requirements**:
After https://github.com/kubernetes-sigs/kueue/pull/230 merged.

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-05-06T06:31:13Z

/assign
