# Issue #6248: AFS: add unit tests for scheduling logic with AFS

**Summary**: AFS: add unit tests for scheduling logic with AFS

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6248

**Last updated**: 2025-08-12T07:43:08Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-29T13:22:59Z
- **Updated**: 2025-08-12T07:43:08Z
- **Closed**: 2025-08-12T07:43:08Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 2

## Description

**What would you like to be cleaned**:

Add unit tests for scheduling with AFS which includes entry penalties.

It could be a new test function like "TestScheduleForAFS", by analogy to "TestScheduleForTAS", because the main "TestSchedule" is already enormous. 

**Why is this needed**:

They were not added in the main PR: https://github.com/kubernetes-sigs/kueue/pull/6189

Unit tests are very useful for the ease of debugging. Unit tests are also much faster to run than integration tests, which already take 20min, so they allow to cover many corner cases almost cost free.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-29T13:23:08Z

cc @PBundyra @IrvingMg

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-07-29T13:29:12Z

/assign
