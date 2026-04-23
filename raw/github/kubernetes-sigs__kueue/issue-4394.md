# Issue #4394: Allow to specify image version for kueue-viz in helm charts

**Summary**: Allow to specify image version for kueue-viz in helm charts

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4394

**Last updated**: 2025-02-26T10:06:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@akram](https://github.com/akram)
- **Created**: 2025-02-25T14:28:17Z
- **Updated**: 2025-02-26T10:06:39Z
- **Closed**: 2025-02-26T10:06:39Z
- **Labels**: `kind/feature`, `area/dashboard`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Allow to specify image version for kueue-viz in helm charts
**Why is this needed**:
Right now images are hardcoded. To allow users to install any version, that could be good to allow at least setting the version or the full image url.
**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.


/kind dashboard

## Discussion

### Comment by [@akram](https://github.com/akram) — 2025-02-25T14:29:30Z

/kind dashboard

### Comment by [@kannon92](https://github.com/kannon92) — 2025-02-25T15:51:27Z

Yea this is important! The staging repos we link in the charts are not persistent I believe.
