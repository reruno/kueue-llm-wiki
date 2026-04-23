# Issue #556: Introduce an annotation to ignore a job by Kueue for scheduling

**Summary**: Introduce an annotation to ignore a job by Kueue for scheduling

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/556

**Last updated**: 2023-02-14T17:09:44Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2023-02-07T08:34:48Z
- **Updated**: 2023-02-14T17:09:44Z
- **Closed**: 2023-02-14T17:09:42Z
- **Labels**: `kind/feature`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

An annotation to ignore a workload by Kueue for scheduling. 

**Why is this needed**:

This is needed for [MPI operator](https://github.com/kubeflow/mpi-operator/) to instruct Kueue to do not queue the Launcher Job separately from the main `MPIJob`. The annotation can be added when creating the Launcher `Job`: https://github.com/kubeflow/mpi-operator/blob/31d4575066770756cc8ca347cc6d5ba3113b1e02/pkg/controller/mpi_job_controller.go#L1382.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-02-14T17:05:50Z

/assign @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2023-02-14T17:09:39Z

/close
As https://github.com/kubernetes-sigs/kueue/pull/561 is merged now.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-02-14T17:09:43Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/556#issuecomment-1430091114):

>/close
>As https://github.com/kubernetes-sigs/kueue/pull/561 is merged now.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
