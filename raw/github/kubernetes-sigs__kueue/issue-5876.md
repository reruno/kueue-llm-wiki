# Issue #5876: [AFS] Extend integration tests for sorting candidates for preemption based on LQ's usage

**Summary**: [AFS] Extend integration tests for sorting candidates for preemption based on LQ's usage

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5876

**Last updated**: 2026-04-08T11:05:25Z

---

## Metadata

- **State**: open
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-07-04T13:37:25Z
- **Updated**: 2026-04-08T11:05:25Z
- **Closed**: —
- **Labels**: `lifecycle/stale`, `kind/cleanup`
- **Assignees**: [@PBundyra](https://github.com/PBundyra)
- **Comments**: 9

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
Add more tests for sorting candidates for preemption based on LQ's usage, with AFS

**Why is this needed**:

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-07-04T13:37:31Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-04T13:43:43Z

This is a follow up to https://github.com/kubernetes-sigs/kueue/pull/5632.

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-07-09T10:01:36Z

@mimowo @PBundyra Since you merged the PR last week shall we close the issue?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-09T10:32:01Z

This issue was opened because the merged implementation didn't contain the expected tests. We merged without them as Patryk was starting.vacation

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-07T10:48:24Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-07T10:52:13Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-05T11:24:12Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2026-01-08T10:27:51Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-08T11:05:22Z

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
