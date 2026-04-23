# Issue #4940: Consider dropping IsManagingObjectsOwner as it seems redundant

**Summary**: Consider dropping IsManagingObjectsOwner as it seems redundant

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4940

**Last updated**: 2025-04-16T15:27:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-04-11T17:42:28Z
- **Updated**: 2025-04-16T15:27:12Z
- **Closed**: 2025-04-16T15:27:12Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Consider dropping IsManagingObjectsOwner as it seems redundant. 

**Why is this needed**:

To simplify code. All Jobs implement it just by checking GVK.

It was discussed a little bit on https://github.com/kubernetes-sigs/kueue/pull/4808#discussion_r2039537827

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-11T17:42:36Z

cc @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-04-16T14:59:34Z

/assign
