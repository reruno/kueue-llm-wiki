# Issue #9375: Clean up workaround for the MPI Operator installation in E2E

**Summary**: Clean up workaround for the MPI Operator installation in E2E

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9375

**Last updated**: 2026-02-27T05:09:56Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2026-02-19T17:31:45Z
- **Updated**: 2026-02-27T05:09:56Z
- **Closed**: 2026-02-27T05:09:56Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
I'd like to the following workaround:

https://github.com/kubernetes-sigs/kueue/blob/419b31ca89318879f3e8ca5168d2a835a346a732/hack/testing/e2e-common.sh#L753-L762

**Why is this needed**:
We released the new MPI Operator version, which has the fix for the above problem.

Context: https://github.com/kubernetes-sigs/kueue/pull/8805#issuecomment-3831022121

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-19T17:32:05Z

@vladikkuzn could you take a look if you can?

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-02-20T14:10:29Z

/assign
