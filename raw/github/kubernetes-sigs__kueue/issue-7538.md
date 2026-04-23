# Issue #7538: Add more details to the status of Cohort

**Summary**: Add more details to the status of Cohort

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7538

**Last updated**: 2026-04-20T05:37:23Z

---

## Metadata

- **State**: open
- **Author**: [@varunsyal](https://github.com/varunsyal)
- **Created**: 2025-11-05T08:58:40Z
- **Updated**: 2026-04-20T05:37:23Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-longterm`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

When we describe a "cohort" object, add details under the Status section of the cohort similar to a clusterqueue:
- Flavor Usage
- Flavor Reservation
- Admitted workloads
- Pending Workloads
- Reserving workloads

**Why is this needed**:
This is to determine at a cohort level, what is the total resource usage and how much is a cohort borrowing and using its own guarantees. This information is only available at the lowest Clusterqueue level.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:37:19Z

/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T11:47:19Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-18T12:16:54Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-04-20T05:36:37Z

/remove-lifecycle rotten

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-04-20T05:37:23Z

In https://github.com/kubernetes-sigs/kueue/issues/7539, we had some progress for Cohort metrics.
So, in the next step, I think that we can consider this Observability enhancement.
