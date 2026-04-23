# Issue #5258: Implement PyTorchJob E2E tests

**Summary**: Implement PyTorchJob E2E tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5258

**Last updated**: 2025-06-24T12:56:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-05-15T15:34:09Z
- **Updated**: 2025-06-24T12:56:30Z
- **Closed**: 2025-06-24T12:56:30Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

We would like to implement PyTorchJob E2E tests.

**Why is this needed**:

As we discussed in the below PR thread, we want to cover all KF integration test cases by PyTorchJob. The PyTorchJob integration has actually all verification checks in UTs and integration test levels.

https://github.com/kubernetes-sigs/kueue/pull/4613#discussion_r2086671836

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-15T15:34:48Z

cc @mimowo @vladikkuzn

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-15T15:48:07Z

/retitle Implement PyTorchJob E2E tests

Reading this I think we already have integration tests for PyTorch and you want e2e tests now.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-15T15:48:50Z

At least I see https://github.com/kubernetes-sigs/kueue/tree/main/test/integration/singlecluster/controller/jobs/pytorchjob?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-15T15:52:49Z

> /retitle Implement PyTorchJob E2E tests
> 
> Reading this I think we already have integration tests for PyTorch and you want e2e tests now.

Ah, right. I wanted to say about E2E test, thanks

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-15T17:20:53Z

/assign @vladikkuzn 
tentatively as this is a follow up
