# Issue #6581: Consider allowing 1 preemption target to be attributed to multiple preemptors

**Summary**: Consider allowing 1 preemption target to be attributed to multiple preemptors

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6581

**Last updated**: 2026-01-11T22:20:27Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@amy](https://github.com/amy)
- **Created**: 2025-08-14T15:29:42Z
- **Updated**: 2026-01-11T22:20:27Z
- **Closed**: 2026-01-11T22:20:26Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: [@amy](https://github.com/amy)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
This is moreso an early idea what I'd like to explore down the line. We should consider allowing 1 preemption target to be attributed to multiple preemptors. 

So lets say you have this:

Schedule 1:
Borrow-CQ: borrows 8CPU from cohort
Preemptor-CQ1: has 4CPU nominal
Preemptor-CQ2: has 4CPU nominal

Schedule 2: 
Preemptor-CQ1: submits 4CPU 
Preemptor-CQ2: submits 4CPU
- Preemptor-CQ1 gets Requeue pending preemption of target. 
- Borrow-CQ: starts eviction/preemption
- Preemptor-CQ2 gets skipped despite being able to fit within the previous preemption target

Today, the second workload would be skipped despite being able to fit. To improve this logic, its more than just refreshing assignments on target overlap seen here:
- https://github.com/kubernetes-sigs/kueue/issues/6488
- https://github.com/kubernetes-sigs/kueue/pull/6541

This is because, once a workload is marked as a preemption target, the entire workload and its resources is removed from consideration by following heads.

It would involve changes probably in `preempted_workloads.go` where you track what portion of the preemption target gets claimed by the preemptor. And in next iterations within 1 `schedule` invocation, other preemptors can check if there's enough GPUs left to fit. 

Allowing multiple preemptors to set a single target within`entry{...preemptionTargets    []*preemption.Target}` is important especially in the case for pod workload type, because we need to requeue until eviction of the preemption target completes.

**Why is this needed**:
Optimization in scheduling algorithm. Generally... I feel like we shouldn't skip within 1 schedule invocation if something can clearly fit. Also theoretically... this behavior could cause overpreemption despite fit if 2 head workloads by happenstance target 2 different preemption targets. Despite the second workload being able to fit within the preemption target triggered by the first preemptor. 

**Completion requirements**:
Will fill this out later....

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-08-14T15:36:36Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-12T21:50:08Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-12T21:53:23Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-11T22:20:21Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-11T22:20:27Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6581#issuecomment-3736097166):

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
