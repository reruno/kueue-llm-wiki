# Issue #3637: Provide the validation enhancements for all Jobs without queue-name as alternative of manageJobsWithoutQueueName

**Summary**: Provide the validation enhancements for all Jobs without queue-name as alternative of manageJobsWithoutQueueName

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3637

**Last updated**: 2025-06-26T16:21:46Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-11-25T15:41:36Z
- **Updated**: 2025-06-26T16:21:46Z
- **Closed**: 2025-06-26T16:21:45Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 8

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
I would like to provide the validation feature for all Jobs without queue-name (`requiredJobsWithQueueName`), which rejects the Jobs without queue-name. 
However, the validations will be implemented as VAPs, and we never implement the custom validation mechanism as webhook and other APIs.

If the cluster administrator enables the `requiredJobsWithQueueName` in the Kueue Configuration API, the kueue-controller-manager will create the VAPs for all enabled Jobs.

**Why is this needed**:
The manageJobsWithoutQueueName automatically suspends all Jobs without queue-name to avoid the quota violation.
But the feature does not have good UX since it's challenging for batch users to find the reason why their Jobs are not runnable.

So, I would like to provide a way that they can easily find the reason when they submit Jobs.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-25T15:41:51Z

This is under discussion. So, anyone can not take this one.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-02-23T16:32:13Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-23T16:36:04Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-24T16:51:54Z

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

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-05-27T14:52:50Z

I think LocalQueueDefaulting provides an alternate approach to solving the UX issue.  And properly dealing with child/ancestor jobs is more complex than we realized and probably beyond the scope of a VAP.  Therefore I'd suggest closing this issue as a path we are no longer planning to pursue.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-26T15:23:49Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-26T16:21:40Z

> I think LocalQueueDefaulting provides an alternate approach to solving the UX issue. And properly dealing with child/ancestor jobs is more complex than we realized and probably beyond the scope of a VAP. Therefore I'd suggest closing this issue as a path we are no longer planning to pursue.

@dgrove-oss Good point. I wanted to remove validation and enforcing mechanisms from Kueue code base to avoid violating the Kueue principle (Kueue does not implement the overwrapping features with Kube core features and famous defact OSS tools like OPA/Gatekeeper, cluster-autoscaler).

However, as you mentioned, today's Kueue manages the nested ancestors across Jobs. So, I guess that VAP can not resolve this problem. Hence, I'm closing this one for now.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-06-26T16:21:46Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3637#issuecomment-3009048382):

>> I think LocalQueueDefaulting provides an alternate approach to solving the UX issue. And properly dealing with child/ancestor jobs is more complex than we realized and probably beyond the scope of a VAP. Therefore I'd suggest closing this issue as a path we are no longer planning to pursue.
>
>@dgrove-oss Good point. I wanted to remove validation and enforcing mechanisms from Kueue code base to avoid violating the Kueue principle (Kueue does not implement the overwrapping features with Kube core features and famous defact OSS tools like OPA/Gatekeeper, cluster-autoscaler).
>
>However, as you mentioned, today's Kueue manages the nested ancestors across Jobs. So, I guess that VAP can not resolve this problem. Hence, I'm closing this one for now.
>
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
