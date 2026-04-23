# Issue #4286: Revisit the documentation with respect to the concepts of Job and Workload

**Summary**: Revisit the documentation with respect to the concepts of Job and Workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4286

**Last updated**: 2026-04-09T04:51:07Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-02-17T12:04:18Z
- **Updated**: 2026-04-09T04:51:07Z
- **Closed**: —
- **Labels**: `kind/feature`, `kind/documentation`
- **Assignees**: _none_
- **Comments**: 16

## Description

/kind documentation

**What would you like to be added**:

Historically Kueue was only for "Jobs", so there was a clear 1:1 mapping between user's Job (and thus user's workload) and Kueue Workload API. This is no longer the case since:
- we support serving workloads too (Deployments, StatefulSets, LWS)
- for some user workloads Kueue creates multiple Workload API objects (like for Deployment or LWS), this is by design to allow scaling which is very important for serving workloads.

To reflect that I would like to revisit the documentation, specifically:
- change Jobs to Workload in most places of the documentation
- add a note to the documentation that historically Kueue supported Jobs but we not support serving workloads too, so we say Workload
- when we want to refer to the internal Kueue Workload API object in the documentation, to make it non-ambigous I would suggest consistent naming like "Kueue's Workload API", "Kueue's Workload API object" or "internal Workload API object" (we can decide during review about the specific term.

**Why is this needed**:

To avoid confusions which has already been encountered a couple of times. 

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-17T12:09:58Z

I guess that we want to consider what is appropriate name instead of Jobs something like Task? Workload (this conflict with Workload API)? Application?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-17T12:50:37Z

cc @dgrove-oss

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-17T12:51:19Z

> I guess that we want to consider what is appropriate name instead of Jobs something like Task? Workload (this conflict with Workload API)? Application?

I'm ok with Task, but would need to see how this presents itself in the docs.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-17T20:20:11Z

> > I guess that we want to consider what is appropriate name instead of Jobs something like Task? Workload (this conflict with Workload API)? Application?
> 
> I'm ok with Task, but would need to see how this presents itself in the docs.

SGTM

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-19T07:36:50Z

cc @PBundyra who is also looking into improvements for docs

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-02-19T18:35:44Z

I agree that using something other than Job in the documentation as the generic name for the user-level "thing Kueue manages" is desirable.  Job has a strong connotation of "batch job" and there is also the confusion between a generic `Job` and a `batch/v1 Job`. 

I wish I could come up with a good synonym for workload that we weren't already using.  Failing that, I do still think that overloading workload to mean both the user's notion of a workload and Kueue's Workload API object would still be an improvement.   If we consistently said "Kueue Workload" for the later, that might be enough.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-07T21:52:02Z

> I agree that using something other than Job in the documentation as the generic name for the user-level "thing Kueue manages" is desirable. Job has a strong connotation of "batch job" and there is also the confusion between a generic `Job` and a `batch/v1 Job`.
> 
> I wish I could come up with a good synonym for workload that we weren't already using. Failing that, I do still think that overloading workload to mean both the user's notion of a workload and Kueue's Workload API object would still be an improvement. If we consistently said "Kueue Workload" for the later, that might be enough.

Actually, in Kubernetes, we call all application level APIs like Job, ReplicaSet, StatefulSet and so on... as "Workload" resources as you can see in https://kubernetes.io/docs/concepts/workloads/.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-05T22:21:05Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-06T06:06:27Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-04T06:59:36Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-04T07:40:21Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-06T05:07:19Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-04T05:12:09Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2026-01-08T10:29:56Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-08T11:05:23Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-04-09T04:51:03Z

/remove-lifecycle stale
