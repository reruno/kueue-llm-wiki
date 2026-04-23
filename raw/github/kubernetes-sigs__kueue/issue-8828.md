# Issue #8828: TAS: evict workloads which are running on nodes which become tainted

**Summary**: TAS: evict workloads which are running on nodes which become tainted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8828

**Last updated**: 2026-01-28T18:48:50Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-27T15:50:20Z
- **Updated**: 2026-01-28T18:48:50Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: [@j-skiba](https://github.com/j-skiba)
- **Comments**: 10

## Description

**What would you like to be added**:

Support for evicting workloads which are running on Nodes which become tainted.

One use case for tainting nodes is to allow running another high priority workload on a dedicated set of nodes.

We could probably make it part of the Node Hot Swap, so that when a single node is tainted we may quickly find a replacement. 

Part of the task is to determine the scope:
- are we handling NoExecute, or NoSchedule taint too?
- do we have some delay?
- do we use NodeHotSwap

Despite the open questions, we should certainly improve the setup.

**Why is this needed**:

Currently, pods of such a workload get deleted (evicted) by kubernetes core, but the workload continues to "run", and Kueue's TAS cache still keeps space for the workload. 

This prevents starting the new high priority workload quickly.

Currently, we need to wait a couple of minutes for the waitForPodsReady.recoveryTimeout to evict such a workload.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-27T15:50:36Z

/assign @j-skiba

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-27T15:50:39Z

@mimowo: GitHub didn't allow me to assign the following users: j-skiba.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8828#issuecomment-3805980500):

>/assign @j-skiba 
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-27T15:50:44Z

cc @tenzen-y @gabesaba

### Comment by [@j-skiba](https://github.com/j-skiba) — 2026-01-28T07:04:01Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-28T07:43:22Z

> Currently, pods of such a workload get deleted (evicted) by kubernetes core, but the workload continues to "run", and Kueue's TAS cache still keeps space for the workload.

IIUC, even if a node gets taints with NoSchedule, running workloads have never been evicted. 
Only when the cluster admins call `kubectl drain` command, the pods will be evicted which internally calls eviction API.

What does "kubernetes core" mean? Any cloud provider-specific extension you say?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-28T08:04:03Z

Yes, k8s core evicts pods running only to the NoExecute taint, and the code is in [TaintEviction controller](pkg/controller/tainteviction/taint_eviction.go).

For the NoSchedule taints the pods continue. So, here we can only evict the workload if we observe the Pods are not yet scheduled, or are evicted by some user tooling. Basically, if user deleted the pods manually or with tooling we know the pods will not get re-scheduled on the same nodes.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-28T17:11:15Z

> Yes, k8s core evicts pods running only to the NoExecute taint, and the code is in [TaintEviction controller](pkg/controller/tainteviction/taint_eviction.go).
> 
> For the NoSchedule taints the pods continue. So, here we can only evict the workload if we observe the Pods are not yet scheduled, or are evicted by some user tooling. Basically, if user deleted the pods manually or with tooling we know the pods will not get re-scheduled on the same nodes.

Yes, exactly. I was wondering which `effect` (NoSchedule, NoExecute) will you handle in this mechanism? If we are assuming only `NoExecute`, I'm fine with that. If you think handle NoSchedule as well, I think that we should avoid that to align with K8s scheduler mechanism.

Additionally, we probably need to consider how to handle `tolerationSeconds` in Pod which probably could be "delay" semantic or we might be able to introduce another Kueue specific delay mechanism.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-28T18:38:41Z

surely we handle both. 

We may need a prototype, but I think we dont even code specific to differentiate them. We can just react to terminatibg pods (or absent pods) on node which have taints which are not tolerated. 

Then in case of NoExecute it will trigger workload eviction, because NodeHotSwap will see multiple nodes like this. 

Similarly, in case of untolerated NoSchedule this will trigger workload eviction by NodeHotSwap if user evicts the Pods manually. If user does not evict the Pods manually, they will continue to run undisturbed.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-28T18:44:02Z

> Similarly, in case of untolerated NoSchedule this will trigger workload eviction by NodeHotSwap if user evicts the Pods manually. If user does not evict the Pods manually, they will continue to run undisturbed.

Basically LGTM. But how to block scheduling Pods by kube-scheduler after users issue eviction manually?
Do you assume to implement webhook mechanism for manually evicted pods which will inject a TAS scheduling gate?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-28T18:48:14Z

I might be missing something, but I think we dont need any special mechanism. If the new NoSchedule taint is untolerated kube-scheduler will not schedule the pods on the newly tainted nodes. It will also not schedule them on other pods due to the NodeSelector injected by TopologyUngater.
