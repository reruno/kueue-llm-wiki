# Issue #283: Add the finalizer via webhook when creating resourceFlavor

**Summary**: Add the finalizer via webhook when creating resourceFlavor

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/283

**Last updated**: 2022-07-19T15:04:07Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2022-06-21T02:25:01Z
- **Updated**: 2022-07-19T15:04:07Z
- **Closed**: 2022-07-19T15:04:07Z
- **Labels**: `kind/feature`
- **Assignees**: [@kerthcet](https://github.com/kerthcet)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
In https://github.com/kubernetes-sigs/kueue/pull/263, we add the finalizer in `Reconcile`, there's still a time resourceFlavor doesn't have the finalizer, we'd like to avoid this by webhook mutation.

**Why is this needed**:

**Completion requirements**:
It's a follow up after https://github.com/kubernetes-sigs/kueue/pull/263

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-06-21T02:25:14Z

/assign

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-07-13T19:25:43Z

I guess this is due now

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-07-15T03:48:24Z

I'll follow this ASAP.
