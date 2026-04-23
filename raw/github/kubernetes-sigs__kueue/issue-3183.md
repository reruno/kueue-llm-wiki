# Issue #3183: Support automatic quota detection in ClusterQueue based on available nodes

**Summary**: Support automatic quota detection in ClusterQueue based on available nodes

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3183

**Last updated**: 2025-06-06T19:05:13Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@andrewsykim](https://github.com/andrewsykim)
- **Created**: 2024-10-02T20:19:21Z
- **Updated**: 2025-06-06T19:05:13Z
- **Closed**: 2025-06-06T19:05:11Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 12

## Description

**What would you like to be added**:

I would like to create a ClusterQueue resource that automatically contains quotas based on available node capacity in my Kubernetes cluster. I have configured my Kubernetes cluster with autoscaling and specify max nodes. 

**Why is this needed**:

Caculating and adjusting quotas manually for ClusterQueue is toilsome. Often the total quota of a cluster is managed in the form of max nodes in a node pool. It would be great if the quota for a ClusterQueue can automatically detect total available capacity and dynamically set quotas for resources. 

**Completion requirements**:

This enhancement requires the following artifacts:

- [X] Design doc
- [X] API change
- [X] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2024-10-02T20:19:56Z

This would only work for clusters wtih a single ClusterQueue, but I think it would still be useful. 

An alternative approach is allowing quotas to specify percentages instead of strict resource quantites

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-03T06:52:06Z

Thank you for opening the discussion; this is definitely on our radar.

For autoscaled environments, Kueue would need to learn about the max-nodes configuration and understand the node resources to automatically adjust ClusterQueue quotas. I'm not sure we have a readily available API (like CA CRDs) to read this information from so it may require preparatory work in CA. It requires some exploration. 

For non-autoscaling environments, we're working on [Topology-Aware Scheduling](https://github.com/kubernetes-sigs/kueue/issues/2724). Part of this feature involves scraping node capacities, effectively limiting the quota based on the currently available nodes. We are not planning to support CA in the first iteration of TAS, but may revisit in the future iterations.

Expressing quotas as percentages within a cohort sounds useful to reduce the manual toil, and could be done as an independent feature. This concept is similar to the P&F (Priority and Fairness) configuration, with parameters like [lendablePercent and borrowingLimitPercent](https://github.com/kubernetes/api/blob/5c8e0b9613978ddec6e4ddbe732bd2f13ec70f82/flowcontrol/v1beta1/types.go#L488-L515). 

/cc @mwielgus

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2024-10-03T15:10:44Z

Thanks for the reply!

> Kueue would need to learn about the max-nodes configuration and understand the node resources to automatically adjust ClusterQueue quotas.

Do we need to the max-nodes configuration from CA? Could we instead just watch for new nodes and dynamically adjust the quotas? I guess the challenge with either approach is there will be Pods on every ndoe (DaemonSets), that won't necessarily consume quotas from ClusterQueue, we would need user input to know how much resources from each node can be allocated to the quota. This would be not that different from supporting quotas as percentages

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-03T15:35:26Z

> Could we instead just watch for new nodes and dynamically adjust the quotas?

This is pretty much the approach we take in Topology Aware Scheduling (TAS), but in autoscaling environments you don't have the nodes until the workload is admitted (so kind of a chicken and egg problem?).

> I guess the challenge with either approach is there will be Pods on every ndoe (DaemonSets), that won't necessarily consume quotas from ClusterQueue, we would need user input to know how much resources from each node can be allocated to the quota

Yeah, for TAS we plan to scrape the information about the Pod usage from DaemonSets. Either by watching DaemonSets or Pods directly.

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2024-10-03T17:13:33Z

Thanks @mimowo, great to hear you're already thinking about this

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-11T09:19:34Z

> An alternative approach is allowing quotas to specify percentages instead of strict resource quantites

For this idea, you can achieve something very close to it with fair sharing. You can basically have a cohort, and assign fair sharing weights to the ClusterQueues within the cohort. The weights denote for priorities, and would translate for "percentages". For example, if you have 3 CQs, and you want them to share load in roughly 10%,20%,70% proportions you can assign the fair sharing weights as: 10, 20, 70. One reason these are weights rather than percenates is that it allows to mutating the values and the set of CQs without violating the sum to 100.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-11T12:53:40Z

As alternatively, I'm wondering if we can obtain the simulation result from the CA. Because AFAIK, the CA has Pod scheduling simulation mechanism, and the CA will resize the cluster based on the simulation result, right?

So, I'm curious if we can obtain the Pod Scheduling simulation result and auto-adjust the CQ configuration.

But, for the solution, we may need to pay massive development costs, I guess...

### Comment by [@CecileRobertMichon](https://github.com/CecileRobertMichon) — 2025-01-07T16:37:38Z

> For this idea, you can achieve something very close to it with fair sharing

@mimowo wouldn't you still need to assign total nominal quota to match the available capacity somewhere so Kueue knows what quota is available to borrow in the cohort? If nominal quota is higher than capacity, pods risk getting admitted but staying stuck in unschedulable, but it quota is lower than capacity Kueue won't admit workloads to make use of the full available capacity. Wonder if I'm missing something here.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-04-07T17:24:23Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-07T18:21:19Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-06T19:05:06Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-06-06T19:05:11Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3183#issuecomment-2950279410):

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
