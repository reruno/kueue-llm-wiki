# Issue #3469: Remove our custom defaulter when controller-runtime fix is released

**Summary**: Remove our custom defaulter when controller-runtime fix is released

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3469

**Last updated**: 2025-03-25T15:02:43Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-11-06T08:45:00Z
- **Updated**: 2025-03-25T15:02:43Z
- **Closed**: 2025-03-25T15:02:43Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 4

## Description

**What would you like to be cleaned**:

We have a custom defaulter in Kueue registered via `pkg/controller/jobframework/webhook/builder.go ` to workaround a bug in controller-runtime which was dropping unknown fields in webhooks.

For that we need to await until the fix https://github.com/kubernetes-sigs/controller-runtime/pull/2982 is released in controller-runtime, probably 0.20.

**Why is this needed**:

To cleanup Kueue code, and use a fix which allows to also remove fields in Kueue's webhooks (if we need it).

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-06T08:45:13Z

cc @tenzen-y @mbobrovskyi

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-02-04T08:56:06Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-04T23:03:05Z

/remove-lifecycle stale

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-25T09:38:34Z

/assign
