# Issue #6551: TAS: Filter Node Reconcile events

**Summary**: TAS: Filter Node Reconcile events

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6551

**Last updated**: 2025-08-21T19:41:08Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@utam0k](https://github.com/utam0k)
- **Created**: 2025-08-11T23:40:48Z
- **Updated**: 2025-08-21T19:41:08Z
- **Closed**: 2025-08-21T19:41:07Z
- **Labels**: _none_
- **Assignees**: [@Ladicle](https://github.com/Ladicle), [@utam0k](https://github.com/utam0k)
- **Comments**: 9

## Description

The node reconciler used in TAS does not filter events. QueueInadmissibleWorkloads is called each time a reconciliation occurs.
https://github.com/kubernetes-sigs/kueue/blob/3ff67d04883d1e091400acfba120a02a348d3e66/pkg/controller/tas/resource_flavor.go#L151-L157

As a result, in large clusters, InadmissibleWorkloads may return to the heap before scanning the entire heap.

How about adding a filter to node events to avoid this issue? The kube-scheduler implementation may be helpful.
https://github.com/kubernetes/kubernetes/blob/ee065dfc80b5762d53c5d9d896a8cc4b1d9c6bd2/pkg/scheduler/framework/events.go#L161-L169

// I wasn't sure which issue template would be appropriate, so I created one from blank.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-12T07:04:54Z

To mitigate the "too often reconciles" we implement [batching by 1s](https://github.com/kubernetes-sigs/kueue/blob/3ff67d04883d1e091400acfba120a02a348d3e66/pkg/controller/tas/resource_flavor.go#L133). 

Still, this sounds like a useful optimization. I think we can use the same list of Node properties: nodeChangeExtracters as in kube-scheduler (node labels which are primarily used by TAS are already included).

### Comment by [@Ladicle](https://github.com/Ladicle) — 2025-08-12T08:04:59Z

Let me add something about this optimization (@utam0k and I work in the same team). 
We've tested this behavior in our environment, and most of this reconciliation is triggered by the node's `LastHeartbeatTime` condition updates.  We use the kubelet default `node-status-update-frequency`,  so at least one unnecessary reconciliation will run every 10 seconds.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-12T08:19:25Z

This seems to be a common starvation problem due to inadmissible workload updating regardless of TAS.
We have mitigation ways to resolve that `requeuingStrategy`. Did you optimize those (https://kueue.sigs.k8s.io/docs/tasks/manage/setup_wait_for_pods_ready/#enabling-waitforpodsready)? Especially `requeuingStrategy.timestamp`

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-12T08:24:20Z

> We've tested this behavior in our environment, and most of this reconciliation is triggered by the node's LastHeartbeatTime condition updates. 

+1, these would be helpful to skip reconciles triggered just by heartbeat.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-12T08:26:39Z

> > We've tested this behavior in our environment, and most of this reconciliation is triggered by the node's LastHeartbeatTime condition updates.
> 
> +1, these would be helpful to skip reconciles triggered just by heartbeat.

SGTM as well.

### Comment by [@utam0k](https://github.com/utam0k) — 2025-08-12T12:03:32Z

/assign utam0k ladicle

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-12T12:07:07Z

To clarify, I would like to start introducing a predicate or an event handler to filter out only `LastHeartbeatTime` updates for now.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-21T19:41:02Z

/close 
by #6570

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-08-21T19:41:08Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6551#issuecomment-3211855328):

>/close 
>by #6570 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
