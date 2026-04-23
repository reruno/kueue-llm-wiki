# Issue #3257: Support MPIJob managedBy feature for the MultiKueue

**Summary**: Support MPIJob managedBy feature for the MultiKueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3257

**Last updated**: 2024-10-29T10:56:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-10-17T14:15:31Z
- **Updated**: 2024-10-29T10:56:04Z
- **Closed**: 2024-10-29T10:56:01Z
- **Labels**: `kind/feature`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 7

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
If we want to use the current MPIJob MultiKueue feature, we need to uninstall the mpi-operator from the management cluster.
But, since the [mpi-operator v0.6.0](https://github.com/kubeflow/mpi-operator/releases/tag/v0.6.0), we started to support the managedBy feature similar to the batch/v1 Job.

Hence, we want to support it by implementing in the following:

1. Implement the `IsJobManagedByKueue`: https://github.com/kubernetes-sigs/kueue/blob/4199c9dd9ce89636eb4e72f5cebb3c9adfba3f0c/pkg/controller/jobs/mpijob/mpijob_multikueue_adapter.go#L89-L91
2. Implement the defaulting webhoooks similar to [Job](https://github.com/kubernetes-sigs/kueue/blob/4199c9dd9ce89636eb4e72f5cebb3c9adfba3f0c/pkg/controller/jobs/job/job_webhook.go#L84-L102) and [JobSet](https://github.com/kubernetes-sigs/kueue/blob/4199c9dd9ce89636eb4e72f5cebb3c9adfba3f0c/pkg/controller/jobs/jobset/jobset_webhook.go#L72-L91): 

And other needed implementations to support it if it exists.

**Why is this needed**:
The MPIJob with managed feature allows us to install the mpi-operator to management and worker clusters so that we can easily introduce multi-cluster MPIJob dispatching and give the possibility of running the MPIJob in the management cluster as well.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-17T14:15:54Z

cc: @mimowo @mszadkow

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-10-17T14:21:24Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-10-21T10:25:28Z

https://github.com/kubernetes-sigs/kueue/pull/3274

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-24T21:03:33Z

/reopen 
For documentation.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-10-24T21:03:38Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3257#issuecomment-2436334135):

>/reopen 
>For documentation.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-29T10:55:56Z

Closed by https://github.com/kubernetes-sigs/kueue/pull/3316
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-10-29T10:56:02Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3257#issuecomment-2443889117):

>Closed by https://github.com/kubernetes-sigs/kueue/pull/3316
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
