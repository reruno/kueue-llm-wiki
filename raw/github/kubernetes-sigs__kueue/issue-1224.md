# Issue #1224: Support guaranteed resources in kueue

**Summary**: Support guaranteed resources in kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1224

**Last updated**: 2024-05-20T05:57:49Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2023-10-19T10:27:08Z
- **Updated**: 2024-05-20T05:57:49Z
- **Closed**: 2024-05-20T05:57:47Z
- **Labels**: `kind/feature`, `lifecycle/stale`
- **Assignees**: [@B1F030](https://github.com/B1F030)
- **Comments**: 18

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Based on the current implementation, one clusterQueue's resources can be consumed totally by another clusterQueue(within the same cohort), we have the borrowingLimit, but as a consumer, I hope I can use as much resources as possible and it's hard to decide how much I want to borrow. On the contrary, as a provider, I hope I have some resources not shard with others, so I need a guaranteed resource pool. 



**Why is this needed**:

Better resource management among different teams.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-19T15:24:36Z

Are you suggesting the opposite of BorrowingLimit? That is, a ClusterQueue can say: I only want others to borrow up to x of my nominalQuota?

Otherwise.... guaranteed resources are already possible in kueue, like:
- Do not put the CQ in a cohort :)
- Enable preemption (reclaimWithinCohort: Any)

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-10-20T01:55:36Z

> Are you suggesting the opposite of BorrowingLimit? That is, a ClusterQueue can say: I only want others to borrow up to x of my nominalQuota?

No, what I mean is I hope I can reserve resource and no other clusterQueues can borrow.

> Do not put the CQ in a cohort :)

I do want the resource sharing for improving resource utilization.

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-10-20T07:29:48Z

Workloads in CQs can reclaim the resources that be borrowed by others by preemption.
Is there any problems if the resources were reclaimed?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-10-20T08:26:36Z

What I mean is I want to reserve some resources that can't be borrowed.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-10-20T11:08:55Z

You mean that CQ with guaranteed mode can borrow resources from other CQs, and that CQ isn't stolen resources from other CQs?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-10-20T11:13:27Z

It might be useful for serving model use cases.
I think serving needs to have more resources to scale out to prepare spiking requests. So we should guarantee resources.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-20T14:16:17Z

> > Are you suggesting the opposite of BorrowingLimit? That is, a ClusterQueue can say: I only want others to borrow up to x of my nominalQuota?
> 
> No, what I mean is I hope I can reserve resource and no other clusterQueues can borrow.

Then you would set x=0. I'm trying to generalize.
Is that what you want?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-11-07T09:12:11Z

> Then you would set x=0. I'm trying to generalize.

Set borrow to zero means I won't borrow any resource from other clusterQueues, but what I want is I hope to reserve x resources that won't be borrowed by other clusterQueues, it generally looks like:
```
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 9
        BorrowingLimit: 5
        guaranteedQuota: 8
```
Then it means the clusterQueue has at least 9 cpus, and can borrow up to 5 then we have 14 cpus at the most, but when being borrowed by other clusterQueues, only 9-8 = 1 cpu is allowed.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-11-07T15:00:11Z

We are suggesting the same thing but with different names :)
Lending limit means how much you allow others to borrow from you.

### Comment by [@B1F030](https://github.com/B1F030) — 2023-11-13T02:29:44Z

/assign
I'm working on this, writing a KEP based on LendingLimit.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-11-15T07:51:01Z

By the way, with lendingLimit introduced, do we need the borrowingLimit anymore? ClusterQueue can claim the guaranteed resources and all the neighbors can borrowing as much as possible.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-11-15T13:27:37Z

For backwards compatibility, yes.

I think both knobs are useful anyways.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-02-13T14:14:20Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-02-13T14:36:50Z

/remove-lifecycle stale

@B1F030 Could you add documentation?

### Comment by [@B1F030](https://github.com/B1F030) — 2024-02-18T01:25:10Z

> @B1F030 Could you add documentation?

Sure.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-05-18T01:43:20Z

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

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-05-20T05:57:43Z

/close
As completed.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-05-20T05:57:48Z

@kerthcet: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1224#issuecomment-2119723266):

>/close
>As completed.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
