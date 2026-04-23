# Issue #6803: Move AllAtOnce MultiKueue dispatcher to a dedicated controller

**Summary**: Move AllAtOnce MultiKueue dispatcher to a dedicated controller

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6803

**Last updated**: 2026-03-19T09:00:29Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-09-12T09:42:02Z
- **Updated**: 2026-03-19T09:00:29Z
- **Closed**: —
- **Labels**: `kind/cleanup`, `priority/important-longterm`, `area/multikueue`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

To move the code of the AllAtOnce MK dispatcher to a dedicated controller, similarly as done for the incremental dispatcher in https://github.com/kubernetes-sigs/kueue/pull/6601

**Why is this needed**:

To decouple responsibility of MultiKueue dispatcher, and the core MultiKueue controllers.

This is a follow up suggested in https://github.com/kubernetes-sigs/kueue/issues/6179#issuecomment-3283450927

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-11T10:33:34Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-11T10:35:51Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:23:21Z

/area multikueue
/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T08:44:21Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-19T09:00:26Z

/remove-lifecycle stale
