# Issue #1234: Avoid use of Consistently in Kubeflow tests

**Summary**: Avoid use of Consistently in Kubeflow tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1234

**Last updated**: 2023-10-30T10:48:10Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-10-20T20:09:30Z
- **Updated**: 2023-10-30T10:48:10Z
- **Closed**: 2023-10-30T10:48:10Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@stuton](https://github.com/stuton)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

The Kubeflow tests (MPI and others) have 5 uses of `Consistently`. We should remove them if they don't provide much value.

**Why is this needed**:

A somewhat busy wait in integration tests can increase the runtime of the tests and usually add meaningful coverage. We should avoid them as much as possible.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-20T20:10:18Z

@stuton can you take this one?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-10-20T20:16:04Z

And also, we should strictly verify conditions. Please see details: https://github.com/kubernetes-sigs/kueue/pull/1191#discussion_r1367415961

### Comment by [@stuton](https://github.com/stuton) — 2023-10-23T09:55:29Z

/assign
