# Issue #4173: FairSharing Preemption Configuration

**Summary**: FairSharing Preemption Configuration

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4173

**Last updated**: 2026-04-08T03:58:24Z

---

## Metadata

- **State**: open
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2025-02-07T16:42:24Z
- **Updated**: 2026-04-08T03:58:24Z
- **Closed**: —
- **Labels**: `kind/feature`, `lifecycle/stale`
- **Assignees**: _none_
- **Comments**: 13

## Description

**What would you like to be added**:
The semantics of ClusterQueue.preemption are underspecified and potentially misleading for FairSharing. As of `v0.10.1`, we are using `borrowWithinCohort` in a counter-intuitive way: rather than it limiting preemptions to a certain threshold, it guarantees that workloads below that threshold are always preempted while ignoring the fair sharing value. See https://github.com/kubernetes-sigs/kueue/pull/4165

Updating how FairSharing uses `borrowWithinCohort` to limit preemptions to a threshold results in additional complexity (see https://github.com/kubernetes-sigs/kueue/pull/4165#issuecomment-2642662029), and confusing semantics compared to Classical Preemption. While enabling `borrowWithinCohort` (versus only `reclaimWithinCohort`) in Classical Preemption results in more targets, this proposal would result in fewer targets in FairSharing.

I propose the following changes:

1) `preemption.borrowWithinCohort` is made incompatible with FairSharing. As currently stated in the documentation, only `preemption.reclaimWithinCohort` and `preemption.withinClusterQueue` are compatible with `FairSharing`.
2) `preemption.reclaimWithinCohort` and `preemption.withinClusterQueue` are extended to have a threshold priority, similarly to `preemption.borrowWithinCohort`
3) FairSharing, in addition to Classical Preemption, will respect these new thresholds. This allows FairSharing users to limit preemption of important workloads with priorities above some threshold.


**Why is this needed**:
Make configuration more user friendly, and more powerful for FairSharing.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-10T10:31:48Z

+1, the issue with extending `reclaimWithinCohort` is that it is a string field so it would be a breaking change to make it a struct. We could introduce something like `reclaimWithinCohortConfig`, and re-design the API when upgrading to v1beta2.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-10T10:53:39Z

Basically, lgtm
In that case, what is the value of the `preemption.borrowWithinCohort`? IIUC, fairSharing completely covers and overlaps the `preemption.borrowWithinCohort` feature. So, we might be able to deprecate `preemption.borrowWithinCohort` then remove it in the v1beta2.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-10T11:07:29Z

I'm happy to consider dropping `preemption.borrowWithinCohort` (and I'm pretty sure @gabesaba would be happy to do so :)), but consider what we do with users who are already using it without fair sharing.

One potential obstacle is that fair sharing is global while `preemption.borrowWithinCohort` is per CQ. Maybe we could make fair sharing cohort-scoped, then I think this one goes away.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-11T12:06:21Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-12T12:50:21Z

/remove-lifecycle stale

We are still discussing for this one.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-10T12:50:45Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-09T12:55:52Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-09T12:57:27Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-09T12:57:34Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-08T12:59:32Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-07T13:50:02Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-08T03:48:12Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-08T03:58:21Z

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
