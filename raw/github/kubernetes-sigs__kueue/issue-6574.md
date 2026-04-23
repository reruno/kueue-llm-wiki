# Issue #6574: HC x LendingLimit: Add scheduler test case

**Summary**: HC x LendingLimit: Add scheduler test case

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6574

**Last updated**: 2026-02-16T15:20:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-08-13T15:14:50Z
- **Updated**: 2026-02-16T15:20:03Z
- **Closed**: 2026-02-16T15:20:03Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@ikchifo](https://github.com/ikchifo)
- **Comments**: 6

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
I would like to add a scheduler UnitTest cases (https://github.com/kubernetes-sigs/kueue/blob/37e444fcf4d27834436077123552112018a287fb/pkg/scheduler/scheduler_test.go#L78) to verify if a Cohort (HC) lendingLimit could be effective when a Cohort borrows resources from other Cohorts.

**Why is this needed**:

The HC lendingLimit (`.resourceGroups[*].lendingLimit`) will be considered when cohort borrow resources from other cohorts. However, at first glance, we don't have a case to verify the behavior.

We should guarantee and check the HC x LendingLimit behaviors in tests.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-13T15:15:44Z

@mimowo @gabesaba Please let me know if you remember already implementing those test cases.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-11T15:39:07Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-11T19:58:13Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-09T20:41:01Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-09T20:43:03Z

/remove-lifecycle stale

### Comment by [@ikchifo](https://github.com/ikchifo) — 2026-02-12T02:54:59Z

/assign
