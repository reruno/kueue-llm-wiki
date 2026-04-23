# Issue #68: Add integration tests for core controllers independent of the scheduler

**Summary**: Add integration tests for core controllers independent of the scheduler

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/68

**Last updated**: 2022-03-15T20:21:56Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-02-24T22:01:50Z
- **Updated**: 2022-03-15T20:21:56Z
- **Closed**: 2022-03-15T20:21:56Z
- **Labels**: `kind/cleanup`, `priority/important-longterm`
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor)
- **Comments**: 3

## Description

Just to focus on the event handlers and status updates.
Keeping them independent of the scheduler should allow us to not depend on a specific queuing policy.
The test itself can do the assignments.

/kind cleanup

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-24T22:01:59Z

/priority important-longterm

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-25T21:24:43Z

/assign

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-15T20:21:56Z

I assume this is done as a high-level issue to create integration test suites for each controller. If we want more tests, we should have specific issues describing what is missing to test.
