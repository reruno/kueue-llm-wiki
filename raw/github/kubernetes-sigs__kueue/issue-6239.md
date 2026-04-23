# Issue #6239: AFS: avoid heapifying ClusterQueus which don't require it

**Summary**: AFS: avoid heapifying ClusterQueus which don't require it

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6239

**Last updated**: 2025-07-30T18:21:10Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-29T12:27:56Z
- **Updated**: 2025-07-30T18:21:10Z
- **Closed**: 2025-07-30T18:21:09Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 6

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Currently we call inside Scheduler this https://github.com/kubernetes-sigs/kueue/blob/2b55cef4a8e57f7fa4c2dd07394ee42150905b88/pkg/scheduler/scheduler.go#L199

However, heapifying cluster queues is costly so we should scope it to only doing this for CQs which use AFS, and have pending entry penalties.

**Why is this needed**:

To optimize performance of scheduling since performance of scheduling is quite important.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-29T12:28:17Z

cc @IrvingMg @PBundyra 
/remove-kind feature
/kind cleanup

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-07-29T13:10:39Z

Currently, heapifying happens if AFS is enabled and there are pending entry penalties:
https://github.com/kubernetes-sigs/kueue/blob/2c0cb71c6d49a2066b9c4dbf99a908cd3f247c0d/pkg/scheduler/scheduler.go#L198-L199

But  I think we can still add a third condition to check whether the ClusterQueue uses AFS, based on the presence of AdmissionScope:
https://github.com/kubernetes-sigs/kueue/blob/2c0cb71c6d49a2066b9c4dbf99a908cd3f247c0d/pkg/queue/cluster_queue.go#L88

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-29T13:27:42Z

Yes, exactly.

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-07-29T13:28:49Z

/assign

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-07-30T18:21:04Z

/close

Fixed it in #6258

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-30T18:21:09Z

@IrvingMg: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6239#issuecomment-3137393153):

>/close
>
>Fixed it in #6258 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
