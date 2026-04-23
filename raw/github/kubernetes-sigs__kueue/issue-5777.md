# Issue #5777: Validate upper-bound of slice size

**Summary**: Validate upper-bound of slice size

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5777

**Last updated**: 2025-07-28T10:06:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@lchrzaszcz](https://github.com/lchrzaszcz)
- **Created**: 2025-06-26T09:25:15Z
- **Updated**: 2025-07-28T10:06:31Z
- **Closed**: 2025-07-28T10:06:31Z
- **Labels**: `kind/feature`
- **Assignees**: [@mykysha](https://github.com/mykysha)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
Slice-level topology in Kueue TAS has been added recently:
- https://github.com/kubernetes-sigs/kueue/pull/5596 - new API 
- https://github.com/kubernetes-sigs/kueue/pull/5353 - TAS algorithm change
- https://github.com/kubernetes-sigs/kueue/pull/5582 - validation of the annotations

In the last PR we validate that slice size is greater than 0, however we should also validate that it is lower than the number of pods in PodSet.

**Why is this needed**:
Values greater than the number of pods in a PodSet make no sense. In edge cases, setting that number to a high value might result in calculating number of slices as 0.

## Discussion

### Comment by [@lchrzaszcz](https://github.com/lchrzaszcz) — 2025-06-26T09:25:59Z

There is a draft PR with my experiment how to tackle that problem: https://github.com/kubernetes-sigs/kueue/pull/5618

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-26T16:24:19Z

/remove-kind cleanup
/kind feature

Actually, this is an enhancement to improve UX so that users can avoid accidental errors.

### Comment by [@mykysha](https://github.com/mykysha) — 2025-07-04T08:41:23Z

/assign
