# Issue #467: Handle changing Job parallelism

**Summary**: Handle changing Job parallelism

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/467

**Last updated**: 2023-01-04T16:17:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-12-09T15:59:20Z
- **Updated**: 2023-01-04T16:17:12Z
- **Closed**: 2023-01-04T16:17:11Z
- **Labels**: `kind/feature`
- **Assignees**: [@mwielgus](https://github.com/mwielgus)
- **Comments**: 8

## Description

**What would you like to be added**:

Handle the change in parallelism. Before admission, this is simple: we need to update the workload.

What if the workload is already admitted? If there is enough quota, we could directly update the workload, even though that might violate FIFO semantics. Perhaps we will need to use scheduling gates to hold pods. 

**Why is this needed**:

Parallelism is a mutable field. 

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-12-14T15:52:59Z

We could have a short term solution: handle scale down properly and disallow scale up via webhook.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-12-15T15:30:06Z

Note that in the job controller, if parallelism changes, the job gets suspended and the workload object gets deleted, and so forcing re-queueing the job.

https://github.com/kubernetes-sigs/kueue/blob/705915169f5045c91e033acc1fa59af77bec4e72/pkg/controller/workload/job/job_controller.go#L523

### Comment by [@mwielgus](https://github.com/mwielgus) — 2023-01-04T13:42:56Z

/assign @mwielgus

### Comment by [@ahg-g](https://github.com/ahg-g) — 2023-01-04T15:36:25Z

This is already handled, what else do we want to do with this one?

### Comment by [@ahg-g](https://github.com/ahg-g) — 2023-01-04T15:45:27Z

I think we want to think of this in the context of https://github.com/kubernetes-sigs/kueue/issues/77, not as a separate issue.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-04T16:16:47Z

I had an offline discussion with @mwielgus and we agreed that it's probably not worth doing anything in this space until scheduling readiness gates are GA.

So yes, closing in favor of #77.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-04T16:17:06Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-01-04T16:17:11Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/467#issuecomment-1371133995):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
