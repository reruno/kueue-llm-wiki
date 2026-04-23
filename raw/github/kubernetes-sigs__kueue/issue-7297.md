# Issue #7297: Simplify TAS-related validation based on the pattern in Kubeflow

**Summary**: Simplify TAS-related validation based on the pattern in Kubeflow

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7297

**Last updated**: 2026-04-14T14:21:53Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-16T13:00:00Z
- **Updated**: 2026-04-14T14:21:53Z
- **Closed**: —
- **Labels**: `lifecycle/stale`, `kind/cleanup`, `priority/important-longterm`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

We have rather complex validation steps for TAS, see here: https://github.com/kubernetes-sigs/kueue/blob/a02abfed9173e74dcf5fc074e68d8d0cb7e6a09f/pkg/controller/jobs/jobset/jobset_webhook.go#L142-L168

I think the major issue was to know the validation path per PodSet, but with the recent changes in https://github.com/kubernetes-sigs/kueue/pull/7061 we can now follow this much simpler pattern:
https://github.com/kubernetes-sigs/kueue/pull/7249/files#diff-5e480b6f7a8d2f0786c69430f298412c1045bdda45790b865c7be63e55b1441cR145-R162

or at least investigate that deeper.

**Why is this needed**:

To simplify the validation code.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-16T13:00:23Z

cc @kshalot , @kaisoz

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-14T13:12:45Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-14T13:29:44Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-14T13:29:52Z

/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-14T14:21:50Z

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
