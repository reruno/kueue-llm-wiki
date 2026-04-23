# Issue #752: Support Weight in localQueue for better resource partitioning

**Summary**: Support Weight in localQueue for better resource partitioning

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/752

**Last updated**: 2024-02-09T18:15:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2023-05-09T02:41:44Z
- **Updated**: 2024-02-09T18:15:34Z
- **Closed**: 2024-02-09T18:15:32Z
- **Labels**: `kind/feature`
- **Assignees**: [@KunWuLuan](https://github.com/KunWuLuan)
- **Comments**: 12

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Currently, for queues inside one CQ, we can submit queues as much as we want until the bottleneck of CQ, and one queue can occupy the whole resources with higher priorities, considering localQueue represents the tenant, this is not reasonable. We should have hard restrictions on how much resources each tenant can have. Instead of defining the resources requests inconveniently, we can have a weight field.

One think for better resource utilization consideration is when resources are sufficient, how to breakthrough the hard restriction of weight and also preemption when resources are not enough.

**Why is this needed**:

Multi-tenant requirement and better resource utilization.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-06-13T10:17:37Z

If no one working on this, I will try to create a kep to track this issue and work on this
/assign

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-06-13T11:19:33Z

Due to the fact that each cluster queue can borrow resources from other cluster queues, the total amount of resources for each queue is uncertain. So it is not easy to design with weight.

I think we can use 'max and min' or 'nominal and borrowingLimit' to define the limit for local queue.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-13T13:31:20Z

Ideally we should be using just weight so that new LocalQueues can be easily added without changing the configuration for other queues.

In system that use weights, the calculations of fair sharing are always dynamic and depend on how many queues have running or pending jobs and the total resources from the parent queue. 
https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/FairScheduler.html
https://karthiksharma1227.medium.com/deep-dive-into-yarn-scheduler-options-cf3f29e1d20d

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-06-13T16:04:03Z

The weight is a relative value, unlike max or min, it's an absolute value. So as Aldo shares, fair sharing is dynamic. Like queueA's weight is a, queueB's weight is b, then queueA can get a/(a+b) of the resources. One concern is if a queue get the resources, then another queue joined with a hight weight, then will the original queue be preempted?

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-06-14T02:36:30Z

If we just use weight, how this weight work with borrow? Should we use `nominal+borrowing limit` as total resources?  Or we can just calculate the proportion of each queue's admitted workloads and only pop workloads from those queues whose proportion is under theirs weights. 
If this is not enough, we can add min and max to guarantee min resources for each queue, this can be another question.

We can achieve the goals by two steps.
In first step, we add an interface in kueue scheduler to determine whether a queue has used too much resources and reject the next workload if yes. In this way we can make each queue get their desired resources when queues don't change.
In second step, we add a controller in kueue to preempt workload if a queue used too much resources. In this way we can make each queue get their desired resources when queues change.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-14T18:33:06Z

> Or we can just calculate the proportion of each queue's admitted workloads and only pop workloads from those queues whose proportion is under theirs weights.

This sounds like a better idea, and closer to what I've seen other systems do. Another thing to consider is that if a queue is 100% empty and has no running workloads, there is no need to consider it in the calculations.

> One concern is if a queue get the resources, then another queue joined with a high weight, then will the original queue be preempted?

That is a very important question. Maybe it should be configurable whether or not to preempt.

I think the best step at this point is to do a review of existing systems. Then we can start collaborating in a google doc or KEP PR.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-15T14:50:43Z

cc @mwielgus

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-07-10T04:11:05Z

@alculquicondor Hi, I have submit a new kep for this, we can discuss details there.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-01-24T02:57:05Z

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

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-01-24T02:58:55Z

/remove-lifecycle stale

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-09T18:15:29Z

/close
in favor of https://github.com/kubernetes-sigs/kueue/issues/1714

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-02-09T18:15:33Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/752#issuecomment-1936395019):

>/close
>in favor of https://github.com/kubernetes-sigs/kueue/issues/1714


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
