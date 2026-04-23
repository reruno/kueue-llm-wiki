# Issue #577: Support for MPIJob scheduling

**Summary**: Support for MPIJob scheduling

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/577

**Last updated**: 2023-02-16T09:18:43Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2023-02-16T08:45:02Z
- **Updated**: 2023-02-16T09:18:43Z
- **Closed**: 2023-02-16T09:18:43Z
- **Labels**: `kind/feature`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Support for scheduling of MPIJob, controller by the MPI-operator (https://github.com/kubeflow/mpi-operator).

The decision for the integration to be part of the Kueue project was discussed here: https://github.com/kubeflow/mpi-operator/issues/505 and here: https://github.com/kubeflow/mpi-operator/pull/521#discussion_r1101481114.

**Why is this needed**:

Users of the MPI operator would like to use Kueue without a need for refactoring. Also, the integration with MPI operator will be the first for Kueue so will pave the way for integrations with other frameworks.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2023-02-16T08:45:17Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-02-16T09:14:10Z

@mimowo Should we use #65?

### Comment by [@mimowo](https://github.com/mimowo) — 2023-02-16T09:18:43Z

Deduplicating as there is already https://github.com/kubernetes-sigs/kueue/issues/65, @tenzen-y thanks for pointing this out.
