# Issue #434: Make ClusterQueue.spec.queuingStrategy immutable

**Summary**: Make ClusterQueue.spec.queuingStrategy immutable

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/434

**Last updated**: 2022-12-07T13:19:09Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-11-23T19:02:49Z
- **Updated**: 2022-12-07T13:19:09Z
- **Closed**: 2022-12-07T13:17:20Z
- **Labels**: `kind/feature`
- **Assignees**: [@nayihz](https://github.com/nayihz)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Make the field immutable in the webhook.

**Why is this needed**:

The current implementation doesn't support changing the strategy. Since requeing everything might be costly, it's better to explicitly require the user to recreate the ClusterQueue if that's the desired behavior.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@nayihz](https://github.com/nayihz) — 2022-12-01T10:29:45Z

In k8s 1.25, we can do this by add 
```
--- a/apis/kueue/v1alpha2/clusterqueue_types.go
+++ b/apis/kueue/v1alpha2/clusterqueue_types.go
@@ -134,6 +134,7 @@ type ClusterQueueSpec struct {
        // admitting newer workloads that fit existing quota.
        //
        // +kubebuilder:default=BestEffortFIFO
+       // +kubebuilder:validation:XValidation:rule="self == oldSelf",message="Value is immutable"
        // +kubebuilder:validation:Enum=StrictFIFO;BestEffortFIFO
        QueueingStrategy QueueingStrategy `json:"queueingStrategy,omitempty"`
```
refs: https://kubernetes.io/blog/2022/09/29/enforce-immutability-using-cel/

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-12-01T14:12:48Z

That's awesome!
For now, we want to support 1.23+ though.

### Comment by [@nayihz](https://github.com/nayihz) — 2022-12-01T14:25:33Z

/assign

### Comment by [@kannon92](https://github.com/kannon92) — 2022-12-07T13:17:15Z

I think we can close due to https://github.com/kubernetes-sigs/kueue/pull/456

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-12-07T13:17:21Z

@kannon92: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/434#issuecomment-1340955447):

>I leave we can close due to https://github.com/kubernetes-sigs/kueue/pull/456
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
