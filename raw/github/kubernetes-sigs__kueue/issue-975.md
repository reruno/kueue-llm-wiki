# Issue #975: Partial preemption of workloads

**Summary**: Partial preemption of workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/975

**Last updated**: 2026-02-05T22:11:28Z

---

## Metadata

- **State**: open
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2023-07-11T17:25:03Z
- **Updated**: 2026-02-05T22:11:28Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 21

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Partial preemption of workloads. Currently preemption is performed for the whole workload, for example when giving back borrowed capacity. This is too aggressive for workloads that tolerate downscaling (e.g., a Ray cluster).

We can come up with a heuristic to select which podset to downscale, could be as simple as going by their order in addition to having a flag indicating which ones can downscale and which can't (and so at the extreme just preempt the whole workload).

**Why is this needed**:
To limit disruptions caused by preemption.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-07-19T02:54:50Z

/cc

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-01-24T20:07:03Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-25T16:57:09Z

/remove-lifecycle stale

### Comment by [@gu-san](https://github.com/gu-san) — 2024-02-21T23:26:19Z

Thanks for the great project.  We have a very similar requirement to what @ahg-g outlines.
We are keen to learn if there have been any design discussions on this topic, and if we could help contribute to the implementation/discussion?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-02-22T02:57:45Z

> Thanks for the great project. We have a very similar requirement to what @ahg-g outlines. We are keen to learn if there have been any design discussions on this topic, and if we could help contribute to the implementation/discussion?

We have yet to discuss this feature, but we're open to discussion.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-05-22T03:38:24Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-22T03:43:21Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-08-20T04:29:21Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-20T15:33:33Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-11-18T16:31:54Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-27T13:16:37Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-06T16:29:08Z

A related, but more specialized issue: https://github.com/kubernetes-sigs/kueue/issues/3762

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-06T17:01:56Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-06T23:40:57Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-05T00:10:04Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-05T11:07:21Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-03T11:54:35Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-03T12:29:20Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-03T14:13:52Z

/remove-lifecycle rotten

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2025-12-17T13:20:45Z

/cc

### Comment by [@mukund-wayve](https://github.com/mukund-wayve) — 2026-02-05T22:11:28Z

We've been running Kueue in production. It's been working pretty well and are now enabling it for our RayJobs. Our main concern is that preemption today is all-or-nothing -- when reclaiming borrowed capacity, a running RayJob gets fully preempted even if only a fraction of its resources need to be freed. We plan to run several RayJobs concurrently on shared clusters, and downscaling a running job would be far less disruptive than killing it entirely.

There's related discussion on the WorkloadResize approach (#5897) and the ElasticJobsViaWorkloadSlices beta path (#8651). I'm new to the Kueue contributor community but happy to help with testing, prototyping, or whatever else would be useful to move this forward.
