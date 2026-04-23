# Issue #316: Default requests to limits in Workload

**Summary**: Default requests to limits in Workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/316

**Last updated**: 2022-08-10T02:44:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-08-09T17:55:02Z
- **Updated**: 2022-08-10T02:44:31Z
- **Closed**: 2022-08-10T02:44:31Z
- **Labels**: `kind/feature`
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

If limit is specified, but the corresponding request is not, set request equal to limit.

**Why is this needed**:

This is the defaulting that k8s API does for Pods, but that wouldn't apply until the Pods are created.

https://github.com/kubernetes/kubernetes/blob/42a5eb48184547465ef4be962af2a07422311f82/pkg/apis/core/v1/defaults.go#L149-L177

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-09T17:55:10Z

/assign
