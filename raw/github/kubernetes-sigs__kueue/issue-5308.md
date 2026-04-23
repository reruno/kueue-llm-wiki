# Issue #5308: Documentation for ProvisioningRequestConfig PodSetMergePolicy

**Summary**: Documentation for ProvisioningRequestConfig PodSetMergePolicy

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5308

**Last updated**: 2025-05-29T06:56:21Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-05-22T07:56:46Z
- **Updated**: 2025-05-29T06:56:21Z
- **Closed**: 2025-05-29T06:56:21Z
- **Labels**: `kind/documentation`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 2

## Description

/kind documentation

As a follow up to https://github.com/kubernetes-sigs/kueue/issues/5266

Probably an extention to https://kueue.sigs.k8s.io/docs/admission-check-controllers/provisioning/#provisioningrequestconfig is enough.

I would like to emphasize that using IdenticalWorkloadSchedulingRequirements is available in >=0.12.0, and how to use it. Maybe we could also provide example PyTorchJob spec, or refer https://kueue.sigs.k8s.io/docs/tasks/run/kubeflow/pytorchjobs/#sample-pytorchjob, which exactly demonstrates the use case.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-22T07:57:27Z

/assign @mszadkow 
tentatively as the feature author

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-22T07:57:36Z

cc @mwysokin @mwielgus
