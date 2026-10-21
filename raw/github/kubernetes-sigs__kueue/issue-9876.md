# Issue #9876: Support guaranteed minimum runtime before fair sharing preemption

**Summary**: Support guaranteed minimum runtime before fair sharing preemption

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9876

**Last updated**: 2026-10-17T10:54:04Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@mukund-wayve](https://github.com/mukund-wayve)
- **Created**: 2026-03-14T21:31:39Z
- **Updated**: 2026-10-17T10:54:04Z
- **Closed**: 2026-10-17T10:54:04Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

A minAdmitDuration configuration option for fair sharing that prevents recently admitted workloads from being preempted by workloads in other ClusterQueues. Workloads admitted less than minAdmitDuration ago would be excluded from cross-CQ preemption candidates.

**Why is this needed**:

When the owner ClusterQueue wants its nominal quota back, the scheduler may preempt workloads before they have had enough time to make meaningful progress. There is currently no way to guarantee a minimum runtime for workloads against cross-CQ fair sharing preemption.

A configurable minimum admit duration would ensure all workloads make at least some progress before becoming eligible for fair sharing preemption.

This is complementary to [#8522](https://github.com/kubernetes-sigs/kueue/issues/8522), which addresses time-based preemption protection within a single ClusterQueue. This issue covers the cross-ClusterQueue case during fair sharing rebalancing.

User Story

As a cluster administrator, I want to configure a minimum duration that workloads must be admitted before they can be preempted by fair sharing, so that workloads borrowing resources from other ClusterQueues are guaranteed enough time to make meaningful progress.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-06-12T22:20:18Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-07-12T22:49:30Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-10-17T10:53:58Z

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

### Comment by [@kubernetes-prow[bot]](https://github.com/apps/kubernetes-prow) — 2026-10-17T10:54:04Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9876#issuecomment-6233052223):

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
