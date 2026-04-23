# Issue #630: Add a new page for the troubleshooting to the documentation

**Summary**: Add a new page for the troubleshooting to the documentation

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/630

**Last updated**: 2024-05-21T20:28:43Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2023-03-14T14:21:06Z
- **Updated**: 2024-05-21T20:28:43Z
- **Closed**: 2024-05-21T20:28:41Z
- **Labels**: `kind/feature`, `lifecycle/rotten`, `kind/documentation`
- **Assignees**: _none_
- **Comments**: 11

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Add a "Troubleshooting" page to the documentation.

**Why is this needed**:
We have two different active conditions:

1. `clusterQueueStatus.conditions.type==active` means that all flavors exist in the cluster, and the CQ can admit new workloads. 
2. `localQueueStatus.conditions.type==active`  means that a related CQ exists in the cluster, and the Q can submit new workloads to CQs.

Maybe, those conditions are confusing to users. So it might be better to add a guide about the two different "active" conditions.

Followup: https://github.com/kubernetes-sigs/kueue/pull/623#discussion_r1135563814

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-14T14:21:20Z

/kind documentation

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-14T14:25:43Z

And in general: we need to give some guidance of what to check when a workload is not admitted

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-14T14:27:37Z

> And in general: we need to give some guidance of what to check when a workload is not admitted

agree.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2023-06-12T15:17:59Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-06-13T12:07:19Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-01-22T11:34:00Z

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-22T14:11:55Z

/remove-lifecycle stale

cc @moficodes

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-04-21T15:09:54Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-05-21T15:27:25Z

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-21T20:28:37Z

/close

I implemented most of this in #2185 and #1889

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-05-21T20:28:42Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/630#issuecomment-2123388988):

>/close
>
>I implemented most of this in #2185 and #1889 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
