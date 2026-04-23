# Issue #2996: Unexport access to Cohorts and ClusterQueues maps in hierarchy.Manager

**Summary**: Unexport access to Cohorts and ClusterQueues maps in hierarchy.Manager

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2996

**Last updated**: 2025-03-03T12:19:17Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2024-09-05T13:38:16Z
- **Updated**: 2025-03-03T12:19:17Z
- **Closed**: 2025-03-03T12:19:17Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@nasedil](https://github.com/nasedil)
- **Comments**: 6

## Description

**What would you like to be cleaned**:
https://github.com/kubernetes-sigs/kueue/blob/be27bb83d087783d7a227e2068bb874110ac9580/pkg/hierarchy/manager.go#L22-L23

**Why is this needed**:
Current requires callers to avoid modifying this map, outside of using the Manager's add/delete methods. See https://github.com/kubernetes-sigs/kueue/pull/2971#discussion_r1745385475

## Discussion

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-09-05T14:04:29Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-12-04T14:34:17Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-01-03T15:05:03Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-03T18:28:15Z

/remove-lifecycle rotten

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-02-03T14:21:19Z

/unassign

### Comment by [@nasedil](https://github.com/nasedil) — 2025-02-25T13:39:30Z

/assign
