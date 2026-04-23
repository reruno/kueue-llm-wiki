# Issue #4915: MultiKueue: Support Scheduling of StatefulSet and LWS

**Summary**: MultiKueue: Support Scheduling of StatefulSet and LWS

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4915

**Last updated**: 2026-02-02T10:28:33Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-04-09T08:42:18Z
- **Updated**: 2026-02-02T10:28:33Z
- **Closed**: 2026-02-02T10:28:33Z
- **Labels**: `kind/feature`, `priority/important-soon`, `area/multikueue`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 10

## Description

**What would you like to be added**:

Support for scheduling StatefulSet and LWS with MultiKueue.

Ideally, we don't need to create any Pods on the management cluster, only on the workers. 

**Why is this needed**:

For delegation of serving workloads via MultiKueue.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-09T08:42:45Z

cc @mwielgus @mwysokin @mbobrovskyi @mszadkow

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-04-09T17:44:49Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-08T18:21:45Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-08T18:27:33Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-06T18:46:24Z

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

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-10-27T09:07:24Z

/unassign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-26T09:57:23Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-26T11:57:41Z

/remove-lifecycle rotten

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:27:50Z

/area multikueue
/priority important-soon

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2026-01-14T09:32:00Z

/assign
