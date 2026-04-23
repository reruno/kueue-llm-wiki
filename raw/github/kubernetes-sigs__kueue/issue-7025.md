# Issue #7025: [Hierarchical Cohorts] Consider Borrowing Level during scheduling after assignments

**Summary**: [Hierarchical Cohorts] Consider Borrowing Level during scheduling after assignments

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7025

**Last updated**: 2026-01-07T23:17:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2025-09-26T15:45:41Z
- **Updated**: 2026-01-07T23:17:35Z
- **Closed**: 2026-01-07T23:17:34Z
- **Labels**: `lifecycle/stale`, `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 4

## Description

**What would you like to be cleaned**:
Follow-up to https://github.com/kubernetes-sigs/kueue/pull/7024. This number should be used during sorting in scheduling cycle, in addition to by FlavorAssignment

**Why is this needed**:
Better sorting of workloads (for non-FairSharing?)

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-09-26T19:16:15Z

/cc

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-25T19:24:10Z

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

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-01-07T23:17:28Z

We already do this: https://github.com/kubernetes-sigs/kueue/blob/f0b9b15eb437e2c8e9c2919e19e259f01152e142/pkg/scheduler/scheduler.go#L733-L738

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-07T23:17:35Z

@gabesaba: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7025#issuecomment-3721235063):

>We already do this: https://github.com/kubernetes-sigs/kueue/blob/f0b9b15eb437e2c8e9c2919e19e259f01152e142/pkg/scheduler/scheduler.go#L733-L738
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
