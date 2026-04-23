# Issue #6595: Remove unused wlKey parameter from evictWorkload in tas node_failure_controller.

**Summary**: Remove unused wlKey parameter from evictWorkload in tas node_failure_controller.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6595

**Last updated**: 2025-08-18T08:05:17Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@Horiodino](https://github.com/Horiodino)
- **Created**: 2025-08-16T13:07:43Z
- **Updated**: 2025-08-18T08:05:17Z
- **Closed**: 2025-08-18T08:05:17Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
Remove the unused parameter `wlKey types.NamespacedName` from the `evictWorkload()` in `pkg/controller/tas/node_failure_controller.go`.

**Why is this needed**:
The `wlKey` parameter is currently not used inside the `evictWorkload` function (see https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/tas/node_failure_controller.go#L223). Removing unused parameters improves code readability and avoids confusion.
