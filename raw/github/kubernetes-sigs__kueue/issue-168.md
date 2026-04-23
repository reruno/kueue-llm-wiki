# Issue #168: A summary of Workloads order in queues

**Summary**: A summary of Workloads order in queues

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/168

**Last updated**: 2024-01-26T17:53:48Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-03-31T17:53:44Z
- **Updated**: 2024-01-26T17:53:48Z
- **Closed**: 2024-01-26T17:53:47Z
- **Labels**: `kind/feature`, `priority/backlog`, `lifecycle/frozen`, `kind/ux`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 16

## Description

**What would you like to be added**:

For a pending Workload, I would like to know how many pods are ahead of it.

Of course, this has to be in a best-effort fashion, but it could get pretty accurate in a cluster with lots of long running jobs.

However, this is not trivial to implement, as we use a heap, not a literal queue.

**Why is this needed**:

To provide some level of prediction to end-users for how long their workload will be queued.

## Discussion

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-09T04:52:04Z

Another concern is that for each update to the queue (new Workload added or removed), many Workloads statuses will need to be reconciled. This is expensive and can't be batched since the updates will need to be done for individual objects.

Perhaps we can update the `Queue` status with the order of the workloads, up to a specific limit. The order includes the workload name and its rank in the `ClusterQueue`.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-07-12T03:12:10Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues and PRs.

This bot triages issues and PRs according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue or PR as fresh with `/remove-lifecycle stale`
- Mark this issue or PR as rotten with `/lifecycle rotten`
- Close this issue or PR with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-07-12T13:14:31Z

/lifecycle frozen

### Comment by [@maaft](https://github.com/maaft) — 2023-02-07T10:29:10Z

I'm also very interested in this feature. Has there been any work in this direction? Are there workarounds that I can use **now**?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-07T14:45:20Z

No progress yet. The exact number is hard to calculate or even keep accurate, depending on how fast jobs are being created. It might be easier to give a time estimate based on historical data?

Feel free to add proposals.

cc @mimowo

### Comment by [@maaft](https://github.com/maaft) — 2023-02-08T07:49:38Z

I mean the obvious solution would be to switch out the heap you mentioned for actual (distributed) queue(s). 

Out of curiosity, what were the reasons to use a heap data-structure when implementing a "kueue"? And what kind of heap are you using? Knowing this, I can better start to think about proposals.

But another quick suggestion would be to store:

**Per Queue**:
- current max position int64 `m`
- number of processed elements int64 `p`
- when a workload finishes, increment `p`.

**Per Workload**:
- has an index parameter `i` int64
- on creation: `i = m` ( also update queue's max positon)

Then, a workloads queue position could be evaluated as `pos = i - p`.

In this way, we'd only need to update 2 variables per queue instead of every node.

Of course one have to figure out what happens when a workload is deleted, but I'm optimistic that a solution can be found. E.g.
- store indices that were deleted
- queue position: `pos = i - p - number_of_deleted_items_before_the_node`
- some smart mechanism for housekeeping to decrease storage requirements

### Comment by [@mimowo](https://github.com/mimowo) — 2023-02-08T09:31:34Z

@maaft IIUC the complication with the proposal is that workloads are ordered by priority and creationTimestamp's: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/queue/cluster_queue_strict_fifo.go#L48-L58. So for a newly created workload with the highest priority the position will be `pos=1` (not `i-p`).

Two proposals from me (I suppose the ideas can be combined):
1. extend the kubectl describe command with the computed information. The on-the-fly computation could probably use the cache and would only happen on demand - when `kubectl describe` is invoked.
2. a dedicated CRD, say `WorkloadQueueOrder` which in the `Reconcile` loop would update its status with the workload order within a ClusterQueue, similarly as @ahg-g  suggested with the `Queue` status, but extract the information to a dedicated CRD to avoid conflicts with other BAU updates.

@alculquicondor @ahg-g @maaft WDYT?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-08T15:10:38Z

Correct, a heap allows us to efficiently maintain a head that satisfies the criteria: `O(log(n))` insertion, `O(1)` query. A red-black tree could potentially give us similar performance, but there is no built-in implementation in golang. We probably shouldn't implement our own, but use a well tested implementation.

A linked-list based queue would probably be too slow in clusters with lots of jobs.

Back to proposals from @mimowo:
1. `kubectl describe` can't access information from cache or even trigger an on-the-fly computation, unless it's all client-side. Unless I misunderstood the suggestion.
2. I would not encourage yet another object, for performance reasons of etcd/apiserver. We should probably maintain the status of the Workloads somehow. But ideally it should be best-effort, to avoid consuming valuable QPS.

### Comment by [@mimowo](https://github.com/mimowo) — 2023-02-08T15:21:01Z

> 1. `kubectl describe` can't access information from cache or even trigger an on-the-fly computation, unless it's all client-side. Unless I misunderstood the suggestion.

I was hoping to be able to instantiate a `kubectl describe` handler for workloads, passing it a pointer to cache so that it has access. Once created register it as a handler in the extension point for `kubectl describe`. However, I haven't investigated yet if the API of the extension point actually allows to create such a handler.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2023-02-08T23:20:38Z

@mimowo Which cache are you referring to?

### Comment by [@mimowo](https://github.com/mimowo) — 2023-02-09T07:34:41Z

> @mimowo Which cache are you referring to?

The Kueue's server side cache. There is server-side printing: https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#additional-printer-columns, but apparently it only allows to use `jsonPath` syntax to compute the value, so seems no go. I was hoping the API would allow to run custom code to compute the value.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-11T13:29:42Z

/assign @mimowo

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-08-08T10:11:22Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-08-08T10:11:26Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/168#issuecomment-1669327025):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-26T17:53:43Z

/close

Follow up split in https://github.com/kubernetes-sigs/kueue/issues/1657

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-01-26T17:53:47Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/168#issuecomment-1912456377):

>/close
>
>Follow up split in https://github.com/kubernetes-sigs/kueue/issues/1657


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
