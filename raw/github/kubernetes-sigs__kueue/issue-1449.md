# Issue #1449: Improve execution of e2e tests by eliminating waiting for 5s for containers to complete

**Summary**: Improve execution of e2e tests by eliminating waiting for 5s for containers to complete

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1449

**Last updated**: 2024-04-17T14:00:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2023-12-13T09:23:21Z
- **Updated**: 2024-04-17T14:00:39Z
- **Closed**: 2024-04-17T14:00:39Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

There are a couple of e2e tests which need long container runtime, like 5s to perform checks, then check that the job / workload finished. Examples:
- "Should unsuspend a job and set nodeSelectors"
- "Should unsuspend a job only after all checks are cleared"

We could do something similar to here: https://github.com/kubernetes-sigs/kueue/blob/e7e232067040f6c602b33b642600a568c944e0a0/test/e2e/e2e_test.go#L175. 

**Why is this needed**:

To optimize the time taken to run e2e tests.

## Discussion

### Comment by [@kaisoz](https://github.com/kaisoz) — 2024-01-31T20:32:53Z

/assign
