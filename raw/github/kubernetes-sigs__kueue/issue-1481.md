# Issue #1481: Switch to the new event recorder in Kueue

**Summary**: Switch to the new event recorder in Kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1481

**Last updated**: 2025-02-05T13:25:08Z

---

## Metadata

- **State**: open
- **Author**: [@achernevskii](https://github.com/achernevskii)
- **Created**: 2023-12-18T15:19:48Z
- **Updated**: 2025-02-05T13:25:08Z
- **Closed**: —
- **Labels**: `kind/feature`, `lifecycle/frozen`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 10

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

https://github.com/kubernetes-sigs/kueue/issues/1387#issuecomment-1834067535

Switch from `record.EventRecorder` to `events.EventRecorder`, which has extra machine-readable fields.

https://github.com/kubernetes/client-go/blob/84a6fe7e4032ae1b8bc03b5208e771c5f7103549/tools/events/interfaces.go#L29

**Why is this needed**:

It will be useful to distinguish between a "regular"  workload finish (when the job ends) versus another kind of failure, in a machine readable way.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-03-17T15:38:57Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-28T18:37:33Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-06-26T19:26:34Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-07-08T15:05:40Z

/remove-lifecycle stale

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2024-07-18T14:17:22Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-30T13:18:59Z

> It will be useful to distinguish between a "regular" workload finish (when the job ends) versus another kind of failure, in a machine readable way.

It is not clear to me if this motivation is still valid since we have the `reason` field indicating Failed / Succeeded since https://github.com/kubernetes-sigs/kueue/pull/2026. I would suggest to wait for a proper support of the new interface from the controller-runtime, re-opened the discussion in https://github.com/kubernetes-sigs/controller-runtime/issues/2141.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-10-28T13:35:53Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-28T15:59:40Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-01-26T16:55:48Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-05T13:25:04Z

/lifecycle frozen
