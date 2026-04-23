# Issue #231: maintain the same type of passed in parameters in clusterQueueImpl

**Summary**: maintain the same type of passed in parameters in clusterQueueImpl

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/231

**Last updated**: 2022-05-04T14:06:24Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2022-04-26T14:10:08Z
- **Updated**: 2022-05-04T14:06:24Z
- **Closed**: 2022-05-04T14:06:23Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 8

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
currently the type of enqueue elements in clusterQueueImpl are different as belows., some are `*kueue.Workload`, and the others are `*workload.Info`, should we change to the same type for connsistency?
```
func (c *ClusterQueueImpl) PushOrUpdate(w *kueue.Workload) {
	info := workload.NewInfo(w)
	c.heap.PushOrUpdate(info)
}

func (c *ClusterQueueImpl) Delete(w *kueue.Workload) {
	c.heap.Delete(workload.Key(w))
}

func (c *ClusterQueueImpl) RequeueIfNotPresent(wInfo *workload.Info, _ bool) bool {
	return c.pushIfNotPresent(wInfo)
}
```
**Why is this needed**:

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-04-26T14:10:40Z

cc @ahg-g @alculquicondor

### Comment by [@Shivansh2407](https://github.com/Shivansh2407) — 2022-05-03T04:07:02Z

Hey @kerthcet, would like to take up this issue. Let me know if this has been fixed or is being worked upon, else I'll fix it up and raise a PR.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-05-03T04:11:03Z

Thanks @Shivansh2407 , but it's still in discussion, if this is accepted, you can take it as you can. cc @alculquicondor as the first author.

### Comment by [@Shivansh2407](https://github.com/Shivansh2407) — 2022-05-03T04:41:09Z

Cool ok, do keep me updated on this. Also, if there is some public discussion on this, I would like to be a part of that as well. Thanks!

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-05-03T13:20:14Z

This is kind of intentional. When inserting an element for the first time, it seemed appropriate to handle the creation of workload.Info within the function.

But when trying to re-queue, you might want to keep the same object, as it might carry number of retries, last scheduling attempt or other metadata that we don't want to override.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-05-04T14:05:57Z

#162 has more details of a complete solution

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-05-04T14:06:14Z

/close

Let's move the discussion there.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-05-04T14:06:24Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/231#issuecomment-1117356767):

>/close
>
>Let's move the discussion there.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
