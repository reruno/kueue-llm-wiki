# Issue #1100: Do not export `DefaultOptions` is not needed

**Summary**: Do not export `DefaultOptions` is not needed

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1100

**Last updated**: 2023-09-14T15:20:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2023-09-08T09:13:46Z
- **Updated**: 2023-09-14T15:20:15Z
- **Closed**: 2023-09-14T15:20:15Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@lowang-bh](https://github.com/lowang-bh)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

This is a follow up to address: https://github.com/kubernetes-sigs/kueue/pull/1069#discussion_r1319089505

**What would you like to be cleaned**:

The `DefaultOptions` is not used externally so does not need to be exported.

**Why is this needed**:

To improve readability by allowing to deduce about the scope of variables quickly.

## Discussion

### Comment by [@lowang-bh](https://github.com/lowang-bh) — 2023-09-14T14:48:54Z

/assign
