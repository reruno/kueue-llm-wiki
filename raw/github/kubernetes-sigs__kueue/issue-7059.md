# Issue #7059: Create a mechanism for updating comparer function for ClusterQueue's heap

**Summary**: Create a mechanism for updating comparer function for ClusterQueue's heap

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7059

**Last updated**: 2026-02-26T16:52:09Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-09-29T15:25:59Z
- **Updated**: 2026-02-26T16:52:09Z
- **Closed**: 2026-02-26T16:52:08Z
- **Labels**: `kind/cleanup`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
Every ClusterQueue uses a heap structure to order Workloads that are submitted to it. Every heap needs to have a way to compare two Workloads and decide which one is greater. We use `lessFunc` to do so, which we [initiate only once](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/cache/queue/cluster_queue.go#L119) upon creation of a ClusterQueue.

After we introduced AdmissionFairSharing, the heap comparer is not static anymore - it changes and the heap itself requires rebuilding. This happens in two scenarios:
1) When scheduler takes [a head of a CQ that has a pending AFS penalty](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/cache/queue/cluster_queue.go#L341)
2) When LQ controller updates [LQ's resource usage](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/core/localqueue_controller.go#L182-L185)

Right now, less function references those changes in two ways:
Ad 1. It references `afsEntryPenalties` that residues in the `queue.Manager` and is [updated on admitting a Workload by scheduler](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/scheduler.go#L637)
Ad 2. It [fetches](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/workload/workload.go#L325) the information about LQ's resource usage from the controller-runtime informer  

Both of these approach are suboptimal for a couple of reasons (cleanliness/maintenance/algorithm correctness) and I'd like to replace it with something else.

The solution I propose is as following:
1. Store in `queue.ClusterQueue` all the parameters that are necessary to create a lessFunc from scratch. Those are the ones that are currently in the [signature of the function](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/cache/queue/cluster_queue.go#L466), but with a map (could be named something along the lines: `AFSLQUsage`) that maps lqKey to LQ's resource usage, instead of context `ctx` and client `c`.
2. Each time, before rebuilding the heap, update the maps (`AFSPenalty`, `AFSLQUsage`, and potentially other in the future) and update the lessFunc, building it based on parameters that are present in `queue.Manager`   

**Why is this needed**:
Cleanliness, maintenance, algorithm correctness
Related issue: https://github.com/kubernetes-sigs/kueue/issues/6710

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-28T15:52:46Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-27T16:51:42Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-26T16:52:02Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-26T16:52:09Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7059#issuecomment-3967857947):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
