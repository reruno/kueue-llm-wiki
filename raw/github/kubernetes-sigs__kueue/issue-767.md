# Issue #767: Job/MPIJob integration suite recreates the envtest for every test

**Summary**: Job/MPIJob integration suite recreates the envtest for every test

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/767

**Last updated**: 2023-05-31T14:39:47Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-05-12T12:05:30Z
- **Updated**: 2023-05-31T14:39:47Z
- **Closed**: 2023-05-31T14:39:47Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 1

## Description

**What would you like to be cleaned**:

We should recreate the kueue-manager, but not the envtest.

This requires some refactoring in the integration test framework.

Ex: https://github.com/kubernetes-sigs/kueue/blob/main/test/integration/controller/mpijob/mpijob_controller_test.go#L70
And https://github.com/kubernetes-sigs/kueue/blob/main/test/integration/controller/job/job_controller_test.go#L71

**Why is this needed**:

To speed up the run time of the suite

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2023-05-26T09:49:18Z

/assign
