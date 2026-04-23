# Issue #582: Preemption based on resource flavor order

**Summary**: Preemption based on resource flavor order

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/582

**Last updated**: 2023-10-11T06:29:20Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2023-02-17T17:18:38Z
- **Updated**: 2023-10-11T06:29:20Z
- **Closed**: 2023-10-09T08:42:39Z
- **Labels**: `kind/feature`
- **Assignees**: [@KunWuLuan](https://github.com/KunWuLuan)
- **Comments**: 8

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

The order of ResourceFlavors within a ClusterQueue represents preference of consumption.

Consider the case where a CQ has two RFs, standard then spot; and consider a group of low priority jobs coming in first consuming all standard quota, then a higher priority job is submitted; although the high priority job could start using the spot quota, I would like it to preempt the lower priority jobs so it can consume resources from the preferred RF (standard).

A similar scenario happens with borrowing: if CQ2 is borrowing resources from CQ1 from higher order RF, I want new jobs submitted to CQ1 to reclaim borrowed resources to fit in the preferred RF.

This behavior can be added as a knob on the CQ.

**Why is this needed**:

Allows setting up CQs in way that ensures stronger guarantees on their nominal quota.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-17T18:30:20Z

Related to #312

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-04-20T10:06:29Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2023-07-19T10:13:02Z

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

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-07-19T11:10:09Z

/remove-lifecycle stale

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-09-08T14:35:37Z

/reopen
Implementation is still under review.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-09-08T14:35:42Z

@alculquicondor: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/582#issuecomment-1711775056):

>/reopen
>Implementation is still under review.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-10T15:26:06Z

@KunWuLuan can you work on the documentation for this feature?

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-10-11T06:29:19Z

sure
