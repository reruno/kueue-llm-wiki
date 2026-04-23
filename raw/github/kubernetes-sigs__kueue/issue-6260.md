# Issue #6260: Optimize 2 phase scheduling approach to 1 phase

**Summary**: Optimize 2 phase scheduling approach to 1 phase

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6260

**Last updated**: 2025-12-27T17:30:51Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@amy](https://github.com/amy)
- **Created**: 2025-07-29T21:27:40Z
- **Updated**: 2025-12-27T17:30:51Z
- **Closed**: 2025-12-27T17:30:50Z
- **Labels**: `kind/cleanup`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
@ichekrygin proposal:
```
In the current two-phase approach: for-all-candidates(nominate) followed by for-all-candidates(process),
In the proposed one-phase inline approach: for-each-candidate(nominate + schedule)
```

**Why is this needed**: reduces runtime complexity which is important to ramp up throughput of scheduling. 

**Context**: No, really, you actually do need to catch up on this thread https://github.com/kubernetes-sigs/kueue/issues/6143#issuecomment-3114656497

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-07-29T21:28:18Z

> https://github.com/kubernetes-sigs/kueue/issues/6143#issuecomment-3133810305
> @ichekrygin 
> I believe the number of operations per scheduling cycle is the same in both models:
> 
> In the current two-phase approach: for-all-candidates(nominate) followed by for-all-candidates(process),
> In the proposed one-phase inline approach: for-each-candidate(nominate + schedule)
> Similarly, the time required to preempt an individual workload should remain unchanged between the two.
> 
> The key difference is in execution flow,
> In the one-phase model, we eliminate preemption target collisions by performing flavor assignment, preemption evaluation, and scheduling inline, per workload. This removes the need to track or deduplicate preemption targets across workloads and avoids retrying skipped workloads in a subsequent scheduling cycle.
> 
> While the cost per workload for flavor assignment and preemption evaluation is the same, the difference lies in how those evaluations are sequenced and isolated, which could result in a runtime complexity reduction in some cases.

Ah its clicking! Going to restate what you've already said @ichekrygin, but do you mean this?

```
Today:
schedule()
- get heads
- snapshot
- nominate() // find admissible workloads from heads, in my approach need to remove list of preemption targets within snapshot to prevent overlap within nominate. 
- process() // process all admissible heads, simulate preemption again, check "fitness" after previous workload was admitted
```

```
@ichekrygin proposal:
schedule()
- get heads
- snapshot
- foreach head:
  - check admissibility
  - if admissible, admit()
  - update snapshot with preempted & admitted workloads
    - probably need to track admissions to block them from being preempted within the same schedule(). 
      Perhaps this doesn't matter, depending on how workload heads are sorted. (ie, subsequent heads probably 
      wouldn't preempt the current head within a single schedule())
```

If my understanding is correct... I think here's what I'll do:
- implement what I proposed first in https://github.com/kubernetes-sigs/kueue/issues/6143 because it doesn't branch off too much from existing implementation
- interested to also take a stab at @ichekrygin your proposal as a follow up. I'm sure the concern is that any large divergence from existing implementation would need a lot of guidance/consideration for testing. By doing both, I can make sure I have a fix, and something to revert back to with the 1 phase approach.

cc/ @mimowo @tenzen-y

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-28T17:10:02Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-27T17:10:22Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-27T17:30:46Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-27T17:30:51Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6260#issuecomment-3694112645):

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
