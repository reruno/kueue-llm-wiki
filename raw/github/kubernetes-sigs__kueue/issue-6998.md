# Issue #6998: Workload condition shows finished and quota reserved. And the CQ still exists.

**Summary**: Workload condition shows finished and quota reserved. And the CQ still exists.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6998

**Last updated**: 2026-02-22T18:59:20Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@amy](https://github.com/amy)
- **Created**: 2025-09-24T22:06:01Z
- **Updated**: 2026-02-22T18:59:20Z
- **Closed**: 2026-02-22T18:59:20Z
- **Labels**: `kind/cleanup`, `lifecycle/rotten`
- **Assignees**: [@amy](https://github.com/amy)
- **Comments**: 18

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
I think there's something wrong with how QuotaReservation condition is marked for finished workloads. The good thing is that I don't see the reservation counted within the CQ. 

Workload conditions:
```
  conditions:
  - lastTransitionTime: "2025-09-24T21:21:48Z"
    message: All pods reached readiness and the workload is running
    observedGeneration: 1
    reason: Started
    status: "True"
    type: PodsReady
  - lastTransitionTime: "2025-09-24T21:21:44Z"
    message: Quota reserved in ClusterQueue foo-cq
    observedGeneration: 1
    reason: QuotaReserved
    status: "True"
    type: QuotaReserved
  - lastTransitionTime: "2025-09-24T21:21:44Z"
    message: The workload is admitted
    observedGeneration: 1
    reason: Admitted
    status: "True"
    type: Admitted
  - lastTransitionTime: "2025-09-24T21:26:48Z"
    message: 'Pods succeeded: 1/1.'
    observedGeneration: 1
    reason: Succeeded
    status: "True"
    type: Finished
```

foo-cq still exists. Luckily it doesn't show this workload is reserving anything in the CQ, given its finished because of this: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/cache/scheduler/cache.go#L418. But for finished workloads, the QuotaReserved condition should be correctly set to false to avoid confusion.

**Why is this needed**:
Workload should accurately reflect QuotaReservation condition.

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-09-24T22:13:11Z

/assign

Just want confirmation that we expect workload condition `QuotaReserved` to be `false` for `Finished` workloads when the CQ still exists.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-24T23:20:27Z

> Just want confirmation that we expect workload condition QuotaReserved to be false for Finished workloads when the CQ still exists.

IIUC, the "Finished" condition takes precedence over all others, though I could be wrong.

In this context, I see `QuotaReserved:True` as a historical condition rather than a current one. A good analogy is a Pod with `Scheduled:True` after it has completed: it reflects that the Pod *was* scheduled in the past, not that it is scheduled now.

That’s my interpretation, I’ll defer to maintainers to confirm or correct it.

### Comment by [@amy](https://github.com/amy) — 2025-09-24T23:45:37Z

I think that's inconsistent with this comment: https://github.com/kubernetes-sigs/kueue/pull/6819#issuecomment-3292434085

Ie, the condition needs to reflect a transition of its current state. (The context for that is that I wanted to keep the old reason, and just mark Evicted to false)

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-25T00:18:41Z

I think there is a difference. The **Finished** condition is a terminal, non-reentrant state, and once it becomes true it cannot be deactivated. Other conditions,for example **Evicted**, **Preempted**, **QuotaReserved**, are reentrant and can transition from `Active=True` to `Active=False` and back.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-25T02:49:29Z

This is the expected state transition.
@ichekrygin 's description is completely right. The `Finished` state is terminal, and Kueue does not perform any action (like unsetting QuotaReservation).

### Comment by [@amy](https://github.com/amy) — 2025-09-25T02:58:55Z

@tenzen-y Thanks! For learning purposes, what is `Deactivated`. Is that terminal or reentrant?

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-25T04:36:41Z

AFAICT, most (if not all) workload conditions are "re-entrant" except "Finished".

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-25T04:39:32Z

> AFAICT, most (if not all) workload conditions are "re-entrant" except "Finished".

Yes, that's right. But, if the `Deactivated` was triggered by `.spec.active=false` in Workload, they need to manually re-enter Workload, which means the Deactivated workloads are not automatically re-entered to the queue.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-25T04:40:55Z

@Amy brings up a good point. It would be super helpful to document all condition types, explicitly calling out which ones are terminal states. Something similar to [this example](https://github.com/kubernetes-sigs/kueue/blob/main/apis/kueue/v1beta1/workload_types.go#L366), but expanded into an exhaustive list.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-25T04:44:32Z

Just a quick chime-in on the Deactivated condition, which is a special case that effectively acts like spec. IIRC, it describes the desired state for a workload to be Evicted. This isn’t obvious (or visible) from the API today, and documenting it would be really helpful.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-25T05:02:03Z

> Just a quick chime-in on the Deactivated condition, which is a special case that effectively acts like spec. IIRC, it describes the desired state for a workload to be Evicted. This isn’t obvious (or visible) from the API today, and documenting it would be really helpful.

Just FYI: we have a small guide in https://kueue.sigs.k8s.io/docs/concepts/workload/#active
But, I totally agree with documenting the state machine, although it might be harder to explain all cases 😓

### Comment by [@amy](https://github.com/amy) — 2025-09-25T15:16:29Z

@tenzen-y so to clarify. Deactivated is effectively terminal from the QuotaReservation condition perspective. (Given it requires manual user intervention to unsuspend a workload)

As in: you can have deactivated true and quota reservation true?

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-25T16:28:33Z

As a follow up I opened the issue ^ to improve workload status docs.

### Comment by [@amy](https://github.com/amy) — 2025-09-25T17:08:35Z

Nice. The reason I'm asking all these questions is because I'm getting around to this: https://github.com/kubernetes-sigs/kueue/pull/6477

And wanted to understand when I should / shouldnt trust QuotaReserved condition. Or which condition takes precedence.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-24T17:10:10Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-23T17:58:40Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-22T18:59:16Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-22T18:59:20Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6998#issuecomment-3941531754):

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
