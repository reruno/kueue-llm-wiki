# Issue #6970: Head of CQ Blocking Tracker

**Summary**: Head of CQ Blocking Tracker

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6970

**Last updated**: 2026-03-16T15:58:42Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@amy](https://github.com/amy)
- **Created**: 2025-09-23T18:29:43Z
- **Updated**: 2026-03-16T15:58:42Z
- **Closed**: 2026-03-16T15:58:41Z
- **Labels**: `kind/bug`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**:
This is not created with the intention of solving this overarching problem immediately. Its just one spot to collect scheduling problems we see within this category to assess down the line if we want a more fundamental scheduling algorithm change longer term.

1. Using pod workload type with gracePeriodTermination & prestop lifecycle hook configured. If you submit a bunch of workloads that collectively should all be admitted, and each need preemption, preemption becomes serialized & slow. Requiring manual mitigation. 
  - Scenario 1: CQ is filled with low priority workloads. Submit high priority workloads to preempt them. 
  - Scenario 2: Submit workloads to 1 CQ reclaiming guarantees that all need preemption in burst space. 
  - Issue tracking: https://github.com/kubernetes-sigs/kueue/issues/6143
 
2. There's 2 same priority workloads. 1 inadmissible workload is submitted first. It can block the second admissible workload despite same priority.
  - Issue tracking: https://github.com/kubernetes-sigs/kueue/issues/6929
  - https://github.com/kubernetes-sigs/kueue/issues/7301

**What you expected to happen**:
The head workload shouldn't block admissible workloads from being admitted.

---

If more scheduling problems float up under this category, please link the related issue here.

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-09-23T19:45:11Z

> This is not created with the intention of solving this overarching problem immediately.

FYI @ichekrygin @gabesaba @mwysokin @mimowo

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-15T15:25:45Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-14T15:40:06Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-16T15:58:35Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-16T15:58:42Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6970#issuecomment-4068744898):

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
