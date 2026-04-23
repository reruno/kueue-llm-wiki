# Issue #6244: Generalize the updateSliceCountsToMinimum and updateCountsToMinimum code

**Summary**: Generalize the updateSliceCountsToMinimum and updateCountsToMinimum code

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6244

**Last updated**: 2025-09-24T08:10:18Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@lchrzaszcz](https://github.com/lchrzaszcz)
- **Created**: 2025-07-29T13:11:00Z
- **Updated**: 2025-09-24T08:10:18Z
- **Closed**: 2025-09-24T08:10:18Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
After introducing [PodSet grouping](https://github.com/kubernetes-sigs/kueue/pull/5845) in one of the [comments](https://github.com/kubernetes-sigs/kueue/pull/5845#discussion_r2228484296) it has been suggested that we have a duplicated logic on two functions:
- `updateSliceCountsToMinimum`
- `updateCountsToMinimum`

Both functions contain conditional logic depending on the remaining leader pods, however, logic on both branches is quite similar. In this issue we would like to explore possibilities to deduplicate that logic.

**Why is this needed**:
TAS algorithm grew in complexity due to the number of recently added features. This issue will potentially remove a lot of code and make code more generic and easy to understand.

## Discussion

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-09-01T08:42:32Z

/assign
