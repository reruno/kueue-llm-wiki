# Issue #6473: Replace t.Context() with utiltesting.ContextWithLog(t)

**Summary**: Replace t.Context() with utiltesting.ContextWithLog(t)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6473

**Last updated**: 2025-08-25T14:13:11Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-08-05T14:27:06Z
- **Updated**: 2025-08-25T14:13:11Z
- **Closed**: 2025-08-25T14:13:11Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@Horiodino](https://github.com/Horiodino)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to replace `t.Context()` usage with `utiltesting.ContextWithLog(t)` in UTs.

https://github.com/kubernetes-sigs/kueue/blob/083c7ff7e88cc41fef25756932cf7c239e88962c/pkg/util/testing/context.go#L38-L43

**Why is this needed**:

The usage of `utiltesting.ContextWithLog(t)` allows us logging when we specify `TEST_LOG_LEVEL=8` environment variable.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-05T14:27:16Z

cc @mimowo @gabesaba

### Comment by [@Horiodino](https://github.com/Horiodino) — 2025-08-22T15:39:18Z

/assign
