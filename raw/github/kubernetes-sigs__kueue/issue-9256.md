# Issue #9256: doc: Add missing labels and annotations documentations

**Summary**: doc: Add missing labels and annotations documentations

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9256

**Last updated**: 2026-03-23T18:16:20Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2026-02-15T14:12:21Z
- **Updated**: 2026-03-23T18:16:20Z
- **Closed**: 2026-03-23T18:16:20Z
- **Labels**: `kind/documentation`
- **Assignees**: [@nerdeveloper](https://github.com/nerdeveloper)
- **Comments**: 1

## Description

<!-- Please use this template for documentation-related issues -->

**What would you like to be documented or improved**:
The site/content/en/docs/reference/labels-and-annotations.md reference page is missing 13 labels/annotations with the kueue.x-k8s.io domain that are defined in the codebase.

Missing entries:

TAS (Topology Aware Scheduling):
- kueue.x-k8s.io/podset-required-topology (Annotation, apis/kueue/v1beta1/topology_types.go)
- kueue.x-k8s.io/podset-preferred-topology (Annotation, apis/kueue/v1beta1/topology_types.go)
- kueue.x-k8s.io/podset-unconstrained-topology (Annotation, apis/kueue/v1beta1/topology_types.go)
- kueue.x-k8s.io/podset-slice-required-topology (Annotation, apis/kueue/v1beta1/topology_types.go)
- kueue.x-k8s.io/podset-slice-size (Annotation, apis/kueue/v1beta1/topology_types.go)
- kueue.x-k8s.io/workload (Annotation, apis/kueue/v1beta1/topology_types.go)
- kueue.x-k8s.io/podset-group-name (Annotation, apis/kueue/v1beta1/topology_types.go)

Workload Slicing:
- kueue.x-k8s.io/workload-slice-name (Annotation, apis/kueue/v1beta1/topology_types.go)
- kueue.x-k8s.io/elastic-job (Annotation, pkg/workloadslicing/workloadslicing.go)
- kueue.x-k8s.io/workload-slice-replacement-for (Annotation, pkg/workloadslicing/workloadslicing.go)

Job Controller:
- kueue.x-k8s.io/stopping (Annotation, pkg/controller/jobs/job/job_controller.go)
- kueue.x-k8s.io/safe-to-forcefully-terminate (Annotation, pkg/controller/constants/constants.go)

ProvisioningRequest:
- provreq.kueue.x-k8s.io/ (Annotation prefix, pkg/controller/constants/constants.go)

These should be added to the reference page in alphabetical order following the existing format.

**Location** (URL, file path, or section if applicable):

[site/content/en/docs/reference/labels-and-annotations.md](https://kueue.sigs.k8s.io/docs/reference/labels-and-annotations/)

## Discussion

### Comment by [@nerdeveloper](https://github.com/nerdeveloper) — 2026-02-16T03:31:42Z

/assign
