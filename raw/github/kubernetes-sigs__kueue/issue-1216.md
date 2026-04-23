# Issue #1216: Add integration test for resuming a partially completed job

**Summary**: Add integration test for resuming a partially completed job

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1216

**Last updated**: 2023-10-28T03:40:17Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-10-17T13:23:23Z
- **Updated**: 2023-10-28T03:40:17Z
- **Closed**: 2023-10-28T03:40:17Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@stuton](https://github.com/stuton)
- **Comments**: 2

## Description

**What would you like to be cleaned**:

Add an integration test that:
1. Create a CQ with quota 3
2. Creates a workload A of size 3, which gets admitted.
2. Reclaim 1 from workload A
3. Create a workload B of size 3, with higher priority, which preempts workload A.
4. Reclaim 2 from workload B
5. Verify that workload A gets readmitted (only has 2 pods left, instead of 3).

This test can replace the existing tests `Should admit workloads when resources are dynamically reclaimed` and `Should admit workloads with 0 count for podSets due to reclaim` (in `test/integration/scheduler_test.go`), as it is more comprehensive.

**Why is this needed**:

To increase coverage of the dynamic reclaiming behavior

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-17T13:24:15Z

I got this idea from #1215

### Comment by [@stuton](https://github.com/stuton) — 2023-10-18T15:51:50Z

/assign
