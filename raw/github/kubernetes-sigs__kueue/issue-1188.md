# Issue #1188: AdmissionCheck: Add Active condition to AdmissionCheck object

**Summary**: AdmissionCheck: Add Active condition to AdmissionCheck object

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1188

**Last updated**: 2023-10-10T18:27:10Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@trasc](https://github.com/trasc)
- **Created**: 2023-10-09T14:09:02Z
- **Updated**: 2023-10-10T18:27:10Z
- **Closed**: 2023-10-10T18:27:10Z
- **Labels**: `kind/feature`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Add a new `Active` condition for the admission check, This condition should be managed by  the AdmissionCheck controller (eg. `ProvisioningAdmissionCheckController`) and considered false by default.

This status condition should be taken into account when the `Active` state of the Cluster Queues using it is evaluated.

**Why is this needed**:

Without this , having a miss-configured AdmissionCheck  (eg, the parameter object is no properly referenced ) can be hard to debug, the workloads can get quota reservation but cannot be fully admitted.

**Completion requirements**:

A workload having at least one inactive AdmissionCheck configured should be marked as inactive.

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2023-10-09T14:09:12Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-10T15:00:13Z

/retitle AdmissionCheck: Add Active condition to AdmissionCheck object
