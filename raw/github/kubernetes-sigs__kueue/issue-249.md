# Issue #249: resourceFlavor can't be deleted unless no clusterQueue references it

**Summary**: resourceFlavor can't be deleted unless no clusterQueue references it

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/249

**Last updated**: 2022-07-06T13:34:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2022-05-06T02:27:46Z
- **Updated**: 2022-07-06T13:34:51Z
- **Closed**: 2022-07-06T13:34:51Z
- **Labels**: `kind/feature`
- **Assignees**: [@kerthcet](https://github.com/kerthcet)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
When we deleting resourceFlavor, we should make sure there's no cluster queue references it.

Refer to discussion here: https://github.com/kubernetes-sigs/kueue/pull/230#discussion_r862497340

**Why is this needed**:
Prevent potential bug.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-05-06T02:28:11Z

/assign

### Comment by [@nayihz](https://github.com/nayihz) — 2022-05-09T13:18:46Z

When we deleting resourceFlavor and find that there is a `ClusterQueue` referencing it, we should add a `finalizer` to it and then watch clusterqueue `Delete Event` until we can delete this `resourceFlavor` completely, is it right?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-05-10T03:48:51Z

> When we deleting resourceFlavor and find that there is a `ClusterQueue` referencing it, we should add a `finalizer` to it and then watch clusterqueue `Delete Event` until we can delete this `resourceFlavor` completely, is it right?

yes and more details:
- [ ] add `finalizer` to resourceFlavor controller, flavors can only be deleted when there's no `ClusterQueue` referencing it
- [ ] only a ClusterQueue which references the flavor has no admitted workloads, then we can delete the flavor.

### Comment by [@nayihz](https://github.com/nayihz) — 2022-05-10T12:14:31Z

Thanks for your detailed explanation.
If you haven't started doing it, would you mind letting me try to work on it?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-05-10T14:19:08Z

emm, actually, I have finished most part of the work already.
