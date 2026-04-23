# Issue #5516: Consolidate kueueviz backend Go module to root one

**Summary**: Consolidate kueueviz backend Go module to root one

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5516

**Last updated**: 2026-04-08T03:58:25Z

---

## Metadata

- **State**: open
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-06-05T11:06:28Z
- **Updated**: 2026-04-08T03:58:25Z
- **Closed**: —
- **Labels**: `lifecycle/stale`, `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 9

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to consolidate kueueviz backend Go module (https://github.com/kubernetes-sigs/kueue/blob/main/cmd/kueueviz/backend/go.mod) into the root one (https://github.com/kubernetes-sigs/kueue/blob/main/go.mod).

**Why is this needed**:

Historically, kueueviz started as an experimental project. So, we have dedicated Go module separate from the root one. However, it was promoted to non-experimental project recently.

So we should consolidate it to the root one to enforce the same library version across all components.

xref: https://github.com/kubernetes-sigs/kueue/pull/5242#discussion_r2126353917

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-05T11:06:38Z

cc @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-05T11:14:22Z

is this a well established practice in projects?

when someone wants to import kueue as a dependency at compile time, and does not use KueueViz, does it mean importing a bigger blob of dependencies?

Maybe, we should consider then exposing kueue API package separately, similarly as k8s exposes k8s-api.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-09T11:25:57Z

> is this a well established practice in projects?
> 
> when someone wants to import kueue as a dependency at compile time, and does not use KueueViz, does it mean importing a bigger blob of dependencies?
> 
> Maybe, we should consider then exposing kueue API package separately, similarly as k8s exposes k8s-api.

That makes sense. I can support the idea.
However, I would like to handle it as a separate one since that's a downstream issue.

The current problem for this issue is double management dependencies version between the root module and kueueviz. 
Actually we have kube related libraries in 2 places (`go.mod` and `cmd/kueueviz/backend/go.mod)`)

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-07T12:24:49Z

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-07T13:55:47Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-06T14:43:29Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-05T15:24:11Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-08T03:52:11Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-08T03:58:22Z

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
