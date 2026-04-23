# Issue #266: Add EnableInternalCertManagement to Component Config

**Summary**: Add EnableInternalCertManagement to Component Config

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/266

**Last updated**: 2022-07-15T16:56:19Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2022-05-17T03:29:26Z
- **Updated**: 2022-07-15T16:56:19Z
- **Closed**: 2022-07-15T16:56:19Z
- **Labels**: `kind/feature`
- **Assignees**: [@kerthcet](https://github.com/kerthcet)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Add EnableInternalCertManagement to Component Config as an option for end-users to choose whether to use the internal cert management or a third-party one like cert manager.

**Why is this needed**:
Some users may use cert manager as the default component in their clusters, we should provide the option for them.

**Completion requirements**:
After https://github.com/kubernetes-sigs/kueue/pull/265

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-05-17T03:29:36Z

/assign
