# Issue #208: Add default queue name for not configured workload

**Summary**: Add default queue name for not configured workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/208

**Last updated**: 2022-04-13T12:34:45Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2022-04-12T10:28:22Z
- **Updated**: 2022-04-13T12:34:45Z
- **Closed**: 2022-04-12T19:59:30Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Currently we construct workload in https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/workload/job/job_controller.go#L402-L418, but job's queue name might be empty. we should verify this or add a default one.

**Why is this needed**:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-04-12T13:47:23Z

Queues are namespaced, so there is no "default" queue that would apply to all workloads.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-12T19:59:20Z

Also, if the admin wishes to set defaults, it should happen on object creation via a webhook or policy agent.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-04-12T19:59:30Z

@ahg-g: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/208#issuecomment-1097157581):

>Also, if the admin wishes to set defaults, it should happen on object creation via a webhook or policy agent.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-04-12T23:50:21Z

Currently we enable `ManageJobsWithoutQueueName` to manage the job controller behavior. But if we set queueName in job's annotations, job controller will also take over. I wonder whether this is as you expected. At least to me, `ManageJobsWithoutQueueName` should own the full control whatever we set queueName of not.

https://github.com/kubernetes-sigs/kueue/blob/0e7406aca14d7ec8faeb387cedb2237d36d8f85d/pkg/controller/workload/job/job_controller.go#L136-L139

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-04-13T12:34:45Z

`r.manageJobsWithoutQueueName` is doing what you say. If it's true, the entire conditional is true and the rest of kueue's job controller runs, effectively "taking over".
