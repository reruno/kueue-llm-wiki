# Issue #6621: [Discussion] fairshare dws value issues

**Summary**: [Discussion] fairshare dws value issues

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6621

**Last updated**: 2026-01-14T09:32:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@amy](https://github.com/amy)
- **Created**: 2025-08-20T00:00:36Z
- **Updated**: 2026-01-14T09:32:03Z
- **Closed**: 2026-01-14T09:32:03Z
- **Labels**: `kind/cleanup`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
With this fix #6617...
```
	return max(1, int(dws)) // rounds all fractional dws values up to 1
```

...its opened up a lot of new considerations we should discuss. (Totally understand that this is an initial fix to stop the fairsharing reclamation bug). Let's use this issue to consider a longer term solution:

For a large enough cohort these could be equivalent for fairsharing tournaments:
- borrowing 4, weight 1 | borrowing 100, weight 99
- borrowing 4, weight 1 | borrowing 4, weight 99

How fairshare workload ordering happens today:
```
// candidatesOrdering criteria:
// 0. Workloads already marked for preemption first.
// 1. Workloads from other ClusterQueues in the cohort before the ones in the
// same ClusterQueue as the preemptor.
// 2. Workloads with lower priority first.
// 3. Workloads admitted more recently first. ⭐️ this one deserves discussion
func CandidatesOrdering(
```

Problem 1: For dws values that fall in the same int bucket, what is the tiebreaker? 
- The primary tiebreaker that's relevant to discuss here is timestamp
- Is this enough considering the scenarios above? (maybe it is)
- If its not enough, should CQ weight somehow be intermingled with timestamp for ordering?

Problem 2: How "similar" is similar for dws value precision bucketing? 
- float vs. int probably doesn't matter much, bc we could shift weights
- we should probably use `10K` instead of `1K` for these to accommodate large weights/cohorts:
```
ratio := b * 1000 / lr
dws := drs * 1000 / node.fairWeight().MilliValue()
```
---
Primarily using this github issue to track this discussion. We'll probably need to break this out into other issues if we decide these problems are worth pursuing. 

cc/ @pajakd @tenzen-y @PBundyra @gabesaba

## Discussion

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-08-20T10:52:48Z

Related https://github.com/kubernetes-sigs/kueue/issues/4247

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-09-15T11:49:19Z

For the sake of clarity and completeness, there are two algorithms to order candidates for FS:
1) For preemption there is the one you mentioned which is used to order workloads within a single CQ
2) For ordering workloads that  come from different CQs to determine which one should be handled first within a single scheduling cycle: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/fair_sharing_iterator.go#L167-L188
The criteria there are:
```
1. DRF
2. Priority
3. Timestamp
```


Regrading problems you mentioned:

Ad. 1 I like your proposal with falling back to CQ's weight a lot. Only after the weights are the same I would fall back to to timestamps.

Ad. 2 Please see my proposal here: https://github.com/kubernetes-sigs/kueue/issues/6774#issuecomment-3291706679

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-14T12:14:08Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-13T12:59:42Z

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

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-01-14T09:32:03Z

I think that the concerns are addressed in https://github.com/kubernetes-sigs/kueue/pull/6925
