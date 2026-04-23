# Issue #4553: Assert Snapshot Unmodified in scheduler/preemption tests

**Summary**: Assert Snapshot Unmodified in scheduler/preemption tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4553

**Last updated**: 2025-04-25T07:44:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2025-03-11T09:53:43Z
- **Updated**: 2025-04-25T07:44:15Z
- **Closed**: 2025-04-25T07:44:14Z
- **Labels**: `kind/feature`
- **Assignees**: [@Horiodino](https://github.com/Horiodino)
- **Comments**: 2

## Description

**What would you like to be added**:
We have an assertion in TestPreemption to make sure the snapshot was not modified
https://github.com/kubernetes-sigs/kueue/blob/6e8d4143e4969d424597d9a30c7672f6ea1210fc/pkg/scheduler/preemption/preemption_test.go#L1875-L1877

It is broken, as in snapCmpOpts, we are ignoring too much.

**Why is this needed**:
We have complex logic which adds and removes usage and workloads during preemption simulation. Without this assertion, it is possible that a branch misses restoring the snapshot properly, which could lead to wrong preemptions or admissions.

Additionally, these assertions can give us greater confidence that Add/Remove functions are proper inverses.

**Completion requirements**:
- Compare relevant fields in ClusterQueueSnapshot, CohortSnapshot, and potentially Snapshot itself
- Fix assertion in TestPreemption
- Add assertions in TestFairPreemptions

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@Horiodino](https://github.com/Horiodino) — 2025-03-17T03:54:13Z

/assign

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-04-25T07:44:14Z

/close
