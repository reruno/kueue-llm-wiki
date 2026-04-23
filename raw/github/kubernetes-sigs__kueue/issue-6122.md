# Issue #6122: Metric that measures time between eviction and actual preemption

**Summary**: Metric that measures time between eviction and actual preemption

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6122

**Last updated**: 2026-04-21T12:32:03Z

---

## Metadata

- **State**: open
- **Author**: [@amy](https://github.com/amy)
- **Created**: 2025-07-21T16:26:32Z
- **Updated**: 2026-04-21T12:32:03Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: [@amy](https://github.com/amy)
- **Comments**: 17

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Metric that measures time between eviction and actual preemption

**Why is this needed**:
We notice long time periods between when a workload is marked for eviction, and when preemption actually occurs (either by workload completion or by the pod hitting its set grace period).

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-07-21T16:26:56Z

/assign

### Comment by [@amy](https://github.com/amy) — 2025-07-21T16:31:20Z

Probably call it... `pods_evicted_to_preemption_time_seconds`

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-21T16:33:14Z

`eviction_duration_seconds` maybe? 

yes, we await for pods to terminate, but we don't observe them directly, but via the "IsActive" field which is watching for CRD Job specific field, eg. status.active.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-07-22T00:13:26Z

Will this metric apply across all frameworks, or is it only relevant to the pod-integration framework?

### Comment by [@amy](https://github.com/amy) — 2025-07-22T04:03:17Z

@ichekrygin probably just pod integration? But not sure how other frameworks work. 

Specifically for pod framework, Kueue propogates the preemption down to the k8s scheduler level. This means that it waits for k8s scheduler to fully preempt the pod (respecting termination grace period and prestop lifecycle hooks). This results in a long time between Kueue eviction and actual pod preemption. I didn't notice this happening for Job framework as an example. Relevant PR where I delved into this and created an E2E: https://github.com/kubernetes-sigs/kueue/pull/6125

(Coordinating with another user to submit an issue from slack discussion: https://kubernetes.slack.com/archives/C032ZE66A2X/p1752770229994679)

If this metric is interesting to you for other frameworks, happy to look into it! It would be helpful to provide a sample of the diff between eviction and actual pod preemption for other frameworks. Ie if you see production examples where there's a long time between & in what scenarios.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-07-22T05:14:58Z

AFAIK, Kueue doesn’t currently track actual pod preemption events for frameworks other than `pod-integration`.
If that’s correct, is there any concern about exposing metrics like `pods_evicted_to_preemption_time_seconds` (or similar), which might not be relevant or populated for other frameworks?

Additionally, is it already a standard practice in Kueue to include framework-specific metrics, or would this be a new direction?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-22T05:30:38Z

I would prefer all integrations, similarly as we do for other Eviction related metrics.

Indeed Kueue does not track pods directly but determines if pods are terminated by the CRD starus fields. For k8s batch job this is status.active field, but more generally check the GenericJob.IsActive.

I think we could measure the time between: Evicted=True & PodsReady=True and Evicted=True & (QuitaReserved=False || Finished || Deactivated).

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-07-22T05:42:14Z

>when a workload is marked for eviction, and when preemption actually occurs

Just to make sure I’m understanding correctly, when we say “when preemption actually occurs,” are we referring to the point at which pods are actually preempted (i.e., deleted)? In other words, are we talking about the time between the workload receiving the `Evicted` condition and the actual pod removal?

If so, that can be tricky to determine without directly inspecting the pods or their events. For example, `GenericJob.IsActive = false` doesn’t necessarily imply that pods were immediately removed; it could just mean the job is no longer managing active pods, even if they’re still terminating.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-22T05:48:27Z

Indeed, we can get more accurate results with status.active + status.terminating

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-07-22T05:49:45Z

On a related note, will this metric track "preemption seconds" per pod instance (e.g., using a pod name or UID label)? That approach makes sense to me, tracking it at the pod level rather than the workload level, since for workloads with multiple pods, it’s not clear how we'd define a single "cut-off" point. Would it be the max, min, average, or something else?

Curious to hear your thoughts!

### Comment by [@amy](https://github.com/amy) — 2025-07-22T17:54:17Z

@ichekrygin @mimowo I think on our end... we'd primarily like to measure the areas where slow eviction/preemption affects Kueue admission. 

So if this does that at the workload level: `Evicted=True & PodsReady=True and Evicted=True & (QuotaReserved=False || Finished || Deactivated)`, I will go with this approach!

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-20T19:58:54Z

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

### Comment by [@amy](https://github.com/amy) — 2025-10-22T17:51:30Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-20T18:26:34Z

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-21T03:52:14Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-21T03:55:35Z

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

### Comment by [@amy](https://github.com/amy) — 2026-04-21T12:32:01Z

/remove-lifecycle stale
/important-long-term
