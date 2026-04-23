# Issue #4655: Replace context.Background() with testing.TB.Context() in tests

**Summary**: Replace context.Background() with testing.TB.Context() in tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4655

**Last updated**: 2025-03-24T07:08:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-03-17T14:45:10Z
- **Updated**: 2025-03-24T07:08:34Z
- **Closed**: 2025-03-24T07:08:34Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@Horiodino](https://github.com/Horiodino)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
Since Go 1.24, it supports `testing.TB.Context()`. We can replace all `context.Background()` usage in tests.

**Why is this needed**:

For better testing and stable context usage.

## Discussion

### Comment by [@Horiodino](https://github.com/Horiodino) — 2025-03-21T14:03:06Z

/assign
