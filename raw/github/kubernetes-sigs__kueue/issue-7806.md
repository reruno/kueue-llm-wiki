# Issue #7806: Better test coverage for scheduler handling of failed preemptions

**Summary**: Better test coverage for scheduler handling of failed preemptions

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7806

**Last updated**: 2026-04-20T05:33:17Z

---

## Metadata

- **State**: open
- **Author**: [@olekzabl](https://github.com/olekzabl)
- **Created**: 2025-11-21T10:32:50Z
- **Updated**: 2026-04-20T05:33:17Z
- **Closed**: —
- **Labels**: `kind/cleanup`, `priority/important-longterm`
- **Assignees**: _none_
- **Comments**: 4

## Description

**What would you like to be cleaned**:

I'd like to have more tests for #7665, including:

- some unit tests
- some test (unit or integration) verifying that workloads with `RequeueReasonPreemptionFailed` don't get sticky (in the sense of #7157)

**Why is this needed**:

For a good coverage; also discussed in review of #7665, [here](https://github.com/kubernetes-sigs/kueue/pull/7665#discussion_r2549061842).

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:04:32Z

/priority important-longterm
/help-wanted
maybe some community members want to help

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T10:46:23Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-18T11:15:55Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-04-20T05:33:15Z

/remove-lifecycle rotten
