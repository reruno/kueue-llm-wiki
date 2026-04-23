# Issue #5779: Write a unit test to make sure `sliceState` is set to 0 between TAS fitting consecutive PodSets in a single Workload

**Summary**: Write a unit test to make sure `sliceState` is set to 0 between TAS fitting consecutive PodSets in a single Workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5779

**Last updated**: 2025-09-08T10:59:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@lchrzaszcz](https://github.com/lchrzaszcz)
- **Created**: 2025-06-26T09:53:37Z
- **Updated**: 2025-09-08T10:59:29Z
- **Closed**: 2025-09-08T10:59:29Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi), [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
Slice-level topology in Kueue TAS has been added recently:
- https://github.com/kubernetes-sigs/kueue/pull/5596 - new API 
- https://github.com/kubernetes-sigs/kueue/pull/5353 - TAS algorithm change
- https://github.com/kubernetes-sigs/kueue/pull/5582 - validation of the annotations

As suggested in a [comment](https://github.com/kubernetes-sigs/kueue/pull/5353#discussion_r2142290756) we should add unit test with two or more PodSets that check if we actually reset the `sliceState` between trying to fit consecutive PodSets from the same Workload.

It would be best to tackle [this](https://github.com/kubernetes-sigs/kueue/issues/5373) task first to add a new test in already consolidated suite.

**Why is this needed**:
As far as I know we had a hard to track bug connected with not resetting `state`, which is similar to `sliceState`. Given that, we should write a test for this as it is easy to break in the future.

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-07-10T11:06:22Z

/assign

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-08-11T08:41:11Z

/assign
