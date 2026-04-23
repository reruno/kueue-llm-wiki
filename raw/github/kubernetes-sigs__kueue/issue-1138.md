# Issue #1138: Skip checking if the cluster queue pending workloads need a change based on the snapshot revision

**Summary**: Skip checking if the cluster queue pending workloads need a change based on the snapshot revision

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1138

**Last updated**: 2024-01-31T15:15:13Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2023-09-19T11:44:49Z
- **Updated**: 2024-01-31T15:15:13Z
- **Closed**: 2024-01-31T15:15:11Z
- **Labels**: `lifecycle/stale`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 9

## Description

The idea is to extend the snapshot used for visibility with its revision (consecutive integers). The clusterQueuePendingWorkloads in the status would also keep the version of the snapshot used.  

Then, we can short-circuit the check of the update of the status, based on comparing revisions. Note that, previously the deep equal check was performed when the lastChangeTime was greater than updateStatusInterval (see https://github.com/kubernetes-sigs/kueue/blob/ee5b6ba29a1bbed1574262e362182573c5f6fa5e/pkg/controller/core/clusterqueue_controller.go#L603), while after https://github.com/kubernetes-sigs/kueue/pull/1135 eliminates this optimization. With the revisions we can do better in both cases.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2023-09-19T11:45:25Z

FYI @tenzen-y @alculquicondor

### Comment by [@mimowo](https://github.com/mimowo) — 2023-09-19T13:04:47Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-09-19T16:30:43Z

> The idea is to extend the snapshot used for visibility with its revision (consecutive integers). The clusterQueuePendingWorkloads in the status would also keep the version of the snapshot used.

@mimowo Does that mean that we will add `revision` field to clusterQueuePendingWorkloads?

https://github.com/kubernetes-sigs/kueue/blob/84ac9527110faf24f165b7966756484a711f3417/apis/kueue/v1beta1/clusterqueue_types.go#L218-L226

If the external other controllers and humans modify the `revision`, what happens? Just reconciliation will be triggered?

### Comment by [@mimowo](https://github.com/mimowo) — 2023-09-19T16:38:05Z

Yes, this is the idea. If a user changes manually to a lower version, then it would safe-heal by overriding with the current revision in the in-memory snapshot counter. If you bump to an arbitrarily high number, then (a) stop updating as this is not supported, or (b) detect that the value is higher than the current max, and override.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-09-19T18:01:05Z

Is this worth? These checks happen in a reconciler, which can have multiple workers. Is the CPU usage relevant, when compared to the latency of the API call?

### Comment by [@mimowo](https://github.com/mimowo) — 2023-09-20T07:03:01Z

> Is this worth? These checks happen in a reconciler, which can have multiple workers. Is the CPU usage relevant, when compared to the latency of the API call?

Yeah, we anyway call `equality.Semantic.DeepEqual(cq.Status, oldStatus)` + send the request if there are differences. In the worst case scenario the DeepEqual for pendingWorkloadStatus needs to compare 4000 items, which seems negligible.

I'm happy to park it for now until we have some experiment, or user feedback that this is an issue.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-01-28T17:59:50Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-31T15:15:07Z

/close 
This is a performance optimization to the feature we deprecate in favor of VisibilityOnDemand, see discussion under: https://github.com/kubernetes-sigs/kueue/issues/1099

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-01-31T15:15:12Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1138#issuecomment-1919309168):

>/close 
>This is a performance optimization to the feature we deprecate in favor of VisibilityOnDemand, see discussion under: https://github.com/kubernetes-sigs/kueue/issues/1099


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
