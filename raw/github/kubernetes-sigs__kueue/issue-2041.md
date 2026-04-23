# Issue #2041: Support all ProvisioningRequest's conditions

**Summary**: Support all ProvisioningRequest's conditions

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2041

**Last updated**: 2024-07-10T09:50:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-04-23T12:28:38Z
- **Updated**: 2024-07-10T09:50:02Z
- **Closed**: 2024-07-10T09:50:02Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Support for recently introduced new ProvisioningRequest's [conditions](https://github.com/kubernetes/autoscaler/blob/349559c32f496900ccd643172c7e4f87a8fecc02/cluster-autoscaler/apis/provisioningrequest/autoscaling.x-k8s.io/v1beta1/types.go#L183) - `BookingExpired` and `CapacityRevoked`

**Why is this needed**:
Improve Kueue's integration with ProvisioningRequest

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] KEP update
- [ ] Codebase update
- [ ] Docs update

The artifacts should be linked in subsequent comments.
