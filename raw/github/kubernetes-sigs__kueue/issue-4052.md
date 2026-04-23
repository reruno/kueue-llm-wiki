# Issue #4052: Fix kueue-viz frontend error handling

**Summary**: Fix kueue-viz frontend error handling

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4052

**Last updated**: 2025-03-25T12:58:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@akram](https://github.com/akram)
- **Created**: 2025-01-24T07:39:40Z
- **Updated**: 2025-03-25T12:58:35Z
- **Closed**: 2025-03-25T12:58:35Z
- **Labels**: `kind/cleanup`, `area/dashboard`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

When backend is not available or returns incorrect data, the frontend only displays a generic error "Websockets error".

**Why is this needed**:
To have a better user experience and for debuggability purposes, it would be great to have a better error handling.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-24T11:33:01Z

/kind dashboard
