# Issue #1636: Add unit tests for pod group when there are errors on pod cleanup

**Summary**: Add unit tests for pod group when there are errors on pod cleanup

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1636

**Last updated**: 2024-02-16T10:26:54Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-01-24T09:15:47Z
- **Updated**: 2024-02-16T10:26:54Z
- **Closed**: 2024-02-16T10:26:53Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to add unit tests demonstrating the handling of errors works properly in case of errors:
- https://github.com/kubernetes-sigs/kueue/blob/44adc22853fce5daf7f898a6bb3a17ccfb0a37bf/pkg/controller/jobs/pod/pod_controller.go#L757
- https://github.com/kubernetes-sigs/kueue/blob/44adc22853fce5daf7f898a6bb3a17ccfb0a37bf/pkg/controller/jobs/pod/pod_controller.go#L765

**Why is this needed**:

This is a follow up to https://github.com/kubernetes-sigs/kueue/pull/1623, needed to verify the lines for handling errors are needed, and work properly, preventing regressions in case of changes in this code.

More context here: https://github.com/kubernetes-sigs/kueue/pull/1623/files#r1463629651

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-24T09:15:59Z

/cc @alculquicondor

### Comment by [@kaisoz](https://github.com/kaisoz) — 2024-01-25T10:03:35Z

/assign 

I think I can use this to learn more about the project. @alculquicondor please let me know if you don't find this one suitable for me 😊

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-25T15:35:40Z

If @mimowo is willing to assist, yes

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-25T15:36:53Z

> If @mimowo is willing to assist, yes

sure thing, @kaisoz  let stay in touch on slack if you have some questions or get blocked
