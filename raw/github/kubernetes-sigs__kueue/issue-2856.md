# Issue #2856: Add a label to PodTemplates created by Kueue

**Summary**: Add a label to PodTemplates created by Kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2856

**Last updated**: 2024-08-22T16:32:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-08-19T12:13:55Z
- **Updated**: 2024-08-22T16:32:32Z
- **Closed**: 2024-08-22T16:32:32Z
- **Labels**: `kind/feature`
- **Assignees**: [@PBundyra](https://github.com/PBundyra)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

A label or set of labels that are added to every PodTemplate created by Kueue (for the ProvReq mechanism). This should be configurable via the Kueue Configuration API.

**Why is this needed**:

To easily identify Workloads created by Kueue.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-08-20T12:06:29Z

/assign @PBundyra

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-08-20T12:07:35Z

and maybe it can just be a fixed label on both PodTemplates and ProvisioningRequests. Maybe just `kueue.x-k8s.io/managed=true`
