# Issue #8653: Requeue relevant inadmissible workloads after a non-TAS workload finishes

**Summary**: Requeue relevant inadmissible workloads after a non-TAS workload finishes

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8653

**Last updated**: 2026-04-20T21:52:37Z

---

## Metadata

- **State**: open
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2026-01-19T09:50:57Z
- **Updated**: 2026-04-20T21:52:37Z
- **Closed**: —
- **Labels**: `kind/bug`, `lifecycle/stale`, `priority/important-longterm`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 3

## Description

**What happened**:
After a non-TAS workload finishes, we don't trigger workloads to be moved from unscheduable queue. This can result in starvation of workload.

**What you expected to happen**:

**How to reproduce it (as minimally and precisely as possible)**:
See integration tests defined in #8484. When QueueInadmissibleWorkloads is removed, the tests fail

**Anything else we need to know?**:
We decided not to fix in #8484 - see comments https://github.com/kubernetes-sigs/kueue/pull/8484#discussion_r2698841024 and https://github.com/kubernetes-sigs/kueue/pull/8484#discussion_r2698987153

**Environment**:
- Kueue version: 0.15.2

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T16:24:12Z

/priority important-longterm

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-20T20:53:58Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-20T21:52:35Z

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
