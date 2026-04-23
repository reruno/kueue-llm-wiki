# Issue #6591: Remove unused ctx parameter in  core: initializeAdmissionFsStatus

**Summary**: Remove unused ctx parameter in  core: initializeAdmissionFsStatus

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6591

**Last updated**: 2025-08-15T11:35:08Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@Horiodino](https://github.com/Horiodino)
- **Created**: 2025-08-15T09:32:19Z
- **Updated**: 2025-08-15T11:35:08Z
- **Closed**: 2025-08-15T11:35:08Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

The `ctx` parameter in `localqueue_controller.go` (around line 262) appears to be unused and should be removed.

**Why is this needed**:

helps keep the codebase clean and maintainable.

Reference: [https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/core/localqueue\_controller.go#L262](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/core/localqueue_controller.go#L262)
