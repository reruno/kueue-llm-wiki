# Issue #92: Make sure assumed workloads are deleted when the object is deleted

**Summary**: Make sure assumed workloads are deleted when the object is deleted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/92

**Last updated**: 2022-03-09T14:47:13Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-03-03T19:16:04Z
- **Updated**: 2022-03-09T14:47:13Z
- **Closed**: 2022-03-09T14:47:12Z
- **Labels**: `kind/bug`
- **Assignees**: [@denkensk](https://github.com/denkensk)
- **Comments**: 4

## Description

Since the scheduler works on a snapshot, it's possible that a workload is deleted between the time we get it from a queue and when we assume it.

We should check the client cache before Assuming a workload to make sure it still exists.

Also, when a workload is deleted, we should clear the cache even if the workload API object is not assigned (regardless of DeleteStateUnknown). This is because the workload could be deleted between the time the scheduler Assumes a workload and it updates the assignment in the API.

/kind bug

## Discussion

### Comment by [@denkensk](https://github.com/denkensk) — 2022-03-08T03:18:28Z

/assign

### Comment by [@denkensk](https://github.com/denkensk) — 2022-03-09T02:44:10Z

Is it still needed ?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-09T14:47:02Z

I think I'm convinced now that there is no bug, because we Forget the assumption if the API update fails.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-03-09T14:47:13Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/92#issuecomment-1062996735):

>I think I'm convinced now that there is no bug, because we Forget the assumption if the API update fails.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
