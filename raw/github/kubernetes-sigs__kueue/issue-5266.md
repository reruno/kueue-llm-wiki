# Issue #5266: Allow to merge equivalent PodSets when creating ProvisioningRequest

**Summary**: Allow to merge equivalent PodSets when creating ProvisioningRequest

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5266

**Last updated**: 2025-05-22T07:06:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-05-16T07:55:24Z
- **Updated**: 2025-05-22T07:06:40Z
- **Closed**: 2025-05-22T07:06:40Z
- **Labels**: `kind/feature`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Ability to merge similar to identical PodSets into one PodTemplate in ProvisioningRequest.

So the API we could add a new API in ProvisiongRequestConfig, for example
MergePodSets: Equivalent / Identical

Equivalent would allow for small differences in fields which are not impacticting ClusterAutoscaler decisions (like args and commends), but would require identical resources requests>

Identical means that the pod sets are strictly identical.


**Why is this needed**:

To overcome the limitation that some cloud-providers may only allow for provisioning one PodTemplate at the time. In that case we want to allow running PyTorch with two PodTemplates which often use same resources, leader and worker using GPUs.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-16T07:55:46Z

cc @mwielgus @mwysokin @tenzen-y @mszadkow

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-05-16T12:23:14Z

/assign
