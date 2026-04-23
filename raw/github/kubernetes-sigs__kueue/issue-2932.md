# Issue #2932: Add documentation for the custom AdmissionCheck controllers

**Summary**: Add documentation for the custom AdmissionCheck controllers

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2932

**Last updated**: 2024-09-13T16:17:14Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-08-28T23:37:42Z
- **Updated**: 2024-09-13T16:17:14Z
- **Closed**: 2024-09-13T16:17:14Z
- **Labels**: `kind/feature`, `kind/documentation`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
We want to add documentation on how to implement the custom AdmissionCheck controller, like custom Job framework integration documentation: https://kueue.sigs.k8s.io/docs/tasks/dev/integrate_a_custom_job/

**Why is this needed**:
Currently, we have built-in AdmissionCheck controllers for ProvisioniingRequest and MultiKueuCluster.
In spite of the AdmissionCheck mechanism being extensible, we do not have any documentation on how to implement custom AdmissionCheck controllers.

This was requested here: https://github.com/kubernetes-sigs/kueue/discussions/2699

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-28T23:37:52Z

/kind documentation

### Comment by [@trasc](https://github.com/trasc) — 2024-09-03T09:41:44Z

/assign
