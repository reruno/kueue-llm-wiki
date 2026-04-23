# Issue #2801: Make kueue statically linked

**Summary**: Make kueue statically linked

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2801

**Last updated**: 2024-08-09T20:41:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@pspurlock](https://github.com/pspurlock)
- **Created**: 2024-08-08T16:02:54Z
- **Updated**: 2024-08-09T20:41:23Z
- **Closed**: 2024-08-09T20:41:23Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Make kueue binary statically linked

**Why is this needed**:

This ensures that no other dependencies would be needed when using on different OS like RHEL.

**Completion requirements**:

Currently this can be done building from source with `CGO_ENABLED=0 make kueuectl`

## Discussion

### Comment by [@pspurlock](https://github.com/pspurlock) — 2024-08-08T16:03:50Z

@ktarplee

### Comment by [@kannon92](https://github.com/kannon92) — 2024-08-08T20:34:49Z

Are you asking that just kueuectl be made static?
