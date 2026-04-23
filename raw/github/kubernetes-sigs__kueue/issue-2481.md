# Issue #2481: Allow usage of plain Pod owned by integrations that are disabled

**Summary**: Allow usage of plain Pod owned by integrations that are disabled

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2481

**Last updated**: 2024-07-12T15:32:44Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-06-26T13:31:22Z
- **Updated**: 2024-07-12T15:32:44Z
- **Closed**: 2024-07-12T15:32:44Z
- **Labels**: `kind/feature`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Allow Pods to be managed by the pod integration if they are owned by a job integration that is disabled.

The current check is only for whether an integration exists, regardless of whether it's enabled.

**Why is this needed**:

Use cases of elastic jobs (such as RayCluster) that don't require atomicity can be served via pod integration.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-26T13:31:29Z

/assign @trasc
