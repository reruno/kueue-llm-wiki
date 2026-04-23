# Issue #285: Add the finalizer via webhook when creating clusterQueue

**Summary**: Add the finalizer via webhook when creating clusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/285

**Last updated**: 2022-07-19T17:58:07Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2022-06-21T10:26:45Z
- **Updated**: 2022-07-19T17:58:07Z
- **Closed**: 2022-07-19T17:58:07Z
- **Labels**: `kind/feature`
- **Assignees**: [@kerthcet](https://github.com/kerthcet)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

**Why is this needed**:
Same to https://github.com/kubernetes-sigs/kueue/issues/283, In https://github.com/kubernetes-sigs/kueue/pull/284, we add the finalizer in Reconcile, there's still a time clusterQueue doesn't have the finalizer, we'd like to avoid this by webhook mutation.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-07-13T19:25:59Z

this also needed now

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-07-15T10:10:08Z

/assign
