# Issue #7252: Introduce a scheduling category for workloads with more permanent failures

**Summary**: Introduce a scheduling category for workloads with more permanent failures

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7252

**Last updated**: 2026-02-18T06:11:36Z

---

## Metadata

- **State**: open
- **Author**: [@amy](https://github.com/amy)
- **Created**: 2025-10-13T22:42:55Z
- **Updated**: 2026-02-18T06:11:36Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: [@amy](https://github.com/amy)
- **Comments**: 6

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Kueue currently has 2 categories of workloads: admissible, inadmissible
Similar to the k8s scheduler, we should introduce 3 categories of workloads: admissible, backoff, inadmissible

Where the 3rd category of failure handles workloads with more permanent failure categories. Ex: capacity exceeds cohort size, resource doesn't exist. This category should not be retried unless there's config change. 

Context:
- https://github.com/kubernetes-sigs/kueue/pull/7157#issuecomment-3367116538
- https://github.com/kubernetes-sigs/kueue/pull/7157#issuecomment-3376286386

**Why is this needed**:
Scheduling optimization to prevent retries of workloads that won't be admissible anytime soon.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-10-13T22:44:19Z

cc/ @gabesaba @hiboyang

### Comment by [@amy](https://github.com/amy) — 2025-10-28T18:00:15Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-26T18:45:41Z

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

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-01-27T08:23:51Z

/remove-lifecycle stale

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-02-17T10:21:20Z

@amy are you still working on this? We may also take inspiration from k8s core scheduler's queueing-hint: https://kubernetes.io/blog/2024/12/12/scheduler-queueinghint/

### Comment by [@amy](https://github.com/amy) — 2026-02-18T06:11:36Z

@gabesaba yeah I'll have some time in the upcoming weeks. But if someone else wanted to pick it up, feel free. Will take a look at the link.
