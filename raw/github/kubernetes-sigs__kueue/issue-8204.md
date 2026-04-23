# Issue #8204: Add integration test to make sure finished workloads are not considered by scheduler after restart

**Summary**: Add integration test to make sure finished workloads are not considered by scheduler after restart

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8204

**Last updated**: 2025-12-12T11:12:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-12T10:41:06Z
- **Updated**: 2025-12-12T11:12:12Z
- **Closed**: 2025-12-12T11:12:12Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Add an integration test for the restart scenario fixed in https://github.com/kubernetes-sigs/kueue/pull/8186

**Why is this needed**:

To make sure we don't have regression in the future.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-12T10:41:35Z

/assign @mbobrovskyi 
as I know synced with Mike and he is already looking into it

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-12T10:42:57Z

/assign
