# Issue #7139: Time-based safety scheduling cycle to check if there are schedulable workloads

**Summary**: Time-based safety scheduling cycle to check if there are schedulable workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7139

**Last updated**: 2026-04-18T13:17:56Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-02T12:31:51Z
- **Updated**: 2026-04-18T13:17:56Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-longterm`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 6

## Description

**What would you like to be added**:

A time-based safety mechanism in scheduler to trigger a scheduling cycle after a while, even if using "BestEffortFIFO".

Before doing I would like to consult community if they hit such issues, so that we can assess the importance.

**Why is this needed**:

To have a safety mechanism in case of bugs, for example:
- scheduler stops retrying https://github.com/kubernetes-sigs/kueue/issues/5590
- moving workloads from the inadmissibleworkloads list to the queue is event-driven. If there is a missing event 

Sure, ideally we have no bugs like this, but in practice a safety measure like "recheck every 1min or so.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-02T12:31:59Z

cc @mwysokin @mwielgus

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-15T00:15:29Z

Does this issue mean that you want to trigger the scheduling cycle even if there are no events (no object updating, creation, etc)?
Do you assume that we want to define the fixed time for triggering?
Do you assume that introducing backoff mechanism to the fixed time to avoid too busy?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-17T08:00:46Z

I was thinking about the mechanism similar to periodicResync in controllers based on informers, as the go-clients provides this functionality. However, periodic resync is not available in scheduler, because it does not maintain an informer on its own. I think something like once in 5min should be enough, and would not generate too much load on scheduler, wdyt?

I think it could be triggered either 5min from the last scheduling cycle only if not triggered otherwise.

EDIT: in any case this is not for 0.15 for sure

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:47:37Z

/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T12:48:20Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-18T13:17:53Z

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
