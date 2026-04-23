# Issue #4429: Create an e2e customconfig test that tests WaitForPodsReady

**Summary**: Create an e2e customconfig test that tests WaitForPodsReady

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4429

**Last updated**: 2025-04-17T09:27:11Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-02-27T10:23:55Z
- **Updated**: 2025-04-17T09:27:11Z
- **Closed**: 2025-04-17T09:27:11Z
- **Labels**: `kind/feature`
- **Assignees**: [@mykysha](https://github.com/mykysha)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
An e2e tests with falls under the `customconfigs/` directory that would test `WaitForPodsReady` feature. We already have integration tests for WaitForPodsReady but they don't run job controller, so it would be nice to have some scenarios with job controller covered. 

Scenarios:
- `.timeout` is surpassed before all pods reach readiness - the workload is evicted, and requeued
- during runtime a pod fails, and `.recoveryTimeout` is surpassed - the workload is evicted and requeued
- during runtime a pod fails, and the recovery pod is scheduled before `.recoveryTimeout` is surpassed - the workload continues to run 

**Why is this needed**:

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Code changes

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-27T10:24:59Z

+1, waitForPodsReady is quite an important feature for our users for failure recovery. I think it deserves at least a baseline e2e test

### Comment by [@mykysha](https://github.com/mykysha) — 2025-03-05T11:25:42Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-07T20:21:14Z

+1
