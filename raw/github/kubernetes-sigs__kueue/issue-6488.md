# Issue #6488: Optimize overlapping preemption problem

**Summary**: Optimize overlapping preemption problem

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6488

**Last updated**: 2026-01-04T17:55:15Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@amy](https://github.com/amy)
- **Created**: 2025-08-06T21:00:19Z
- **Updated**: 2026-01-04T17:55:15Z
- **Closed**: 2026-01-04T17:55:14Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: [@amy](https://github.com/amy)
- **Comments**: 6

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Kueue stalls horizontally across CQs on preemption target overlap within a single `schedule()` invocation. I want to remove preemption targets from being considered by subsequent CQ heads within a single `schedule()` invocation.

**Why is this needed**:
Results in scheduling stalling and an unnecessarily large number of scheduling cycles. (overlapping preemption targets causes `schedule()` to skip the head from being considered for scheduling.)

Also, you could have this:
- pod fails to terminate
- CQ-A has that as a preemption target
- CQ-B also has that as a preemption target, so it skips within the `schedule()`
- We've seen issues where this failing pod termination affects multiple CQ heads instead of just the preemptor CQ. We should isolate this to just affecting the preemptor CQ head.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-08-06T21:48:52Z

/assign

### Comment by [@amy](https://github.com/amy) — 2025-08-07T15:39:58Z

Implementation context:

https://github.com/kubernetes-sigs/kueue/issues/6143#issuecomment-3159958252
drop this block of code:
[kueue/pkg/scheduler/scheduler.go](https://github.com/kubernetes-sigs/kueue/blob/36928e70fc50238b5b10ea2ed9c6391bfd399542/pkg/scheduler/scheduler.go#L278-L283)

Lines 278 to 283 in [36928e7](https://github.com/kubernetes-sigs/kueue/commit/36928e70fc50238b5b10ea2ed9c6391bfd399542)

```
 // We skip multiple-preemptions per cohort if any of the targets are overlapping 
 if preemptedWorkloads.HasAny(e.preemptionTargets) { 
 	setSkipped(e, "Workload has overlapping preemption targets with another workload") 
 	skippedPreemptions[cq.Name]++ 
 	continue 
 } 
```
modify [fits()](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/scheduler.go#L443-L447) function to deduplicate the workloads so that we don't double subtract for the new & overlapping targets
call IssuePreemptions only for newPreemptionTargets (e.preemptionTargets - preemptionTargets)

-----
https://github.com/kubernetes-sigs/kueue/issues/6143#issuecomment-3138204472

change `for iterator.hasNext() {.. here...}`
```
preemptedWorkloads := make(preemption.PreemptedWorkloads)
for iterator.hasNext() {
  ...
  ...
  // Conflict detected, get new assignments
  preemptionTargets := getAssignments(snapshot, preemptedWorkloads)
  // getAssignments removes preemptedWorkloads from snapshot to get new preemption target
  // add new preemption targets to growing list of actually preemptedWorkloads
  ...
  ...
  // complete admission
}
```
- This way, the tournament order is preserved. 
- Potential issue from @mimowo "Potentially, even the previous "Fit" workload may cause the second workload to choose a different flavor" 
  - ❓I'm not quite following the implications of this for either: 
    1.) admissible workloads from nominate -> Do you mean that the admissibility is stale? (I think that's the case for current implementation too. So waiting for the next `schedule()` invocation should be okay? maybe?)
    2.) potentially affecting tournament state or results

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-05T16:34:03Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-05T17:29:29Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-04T17:55:09Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-04T17:55:14Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6488#issuecomment-3708291188):

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
