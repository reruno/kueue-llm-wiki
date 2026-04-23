# Issue #6006: Controller pods reediness check succeed while there is no leader

**Summary**: Controller pods reediness check succeed while there is no leader

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6006

**Last updated**: 2026-04-13T17:09:54Z

---

## Metadata

- **State**: open
- **Author**: [@gbenhaim](https://github.com/gbenhaim)
- **Created**: 2025-07-17T07:26:04Z
- **Updated**: 2026-04-13T17:09:54Z
- **Closed**: —
- **Labels**: `kind/bug`, `lifecycle/stale`
- **Assignees**: _none_
- **Comments**: 7

## Description

Not sure if it's a bug, just wanted to hear other people opinions.

**What happened**:

When leader election is enabled, as long as the controllers haven't decided on a leader, resource are not being reconciled. 

**What you expected to happen**:

On one hand, controllers are eventually consistent and delays in reconciling resources are expected.
On the other hand, if for some reason the controllers can't agree on a leader because of  a bug (and it's not something that will get resolved in a timely manner), it is valid to consider the controller as not ready.

**How to reproduce it (as minimally and precisely as possible)**:

Deploy the kueue controller with leader election enabled with high values for `LeaseDuration`, `RenewDeadline`, `RetryPeriod`, such as:

```go
LeaseDuration: v1.Duration{Duration: 137 * time.Second},
RenewDeadline: v1.Duration{Duration: 107 * time.Second},
RetryPeriod:   v1.Duration{Duration: 26 * time.Second},
```
* Those high values are required for gracefully handle API unavailability for at most minute, something that can happen in large cluster while ETCD is performing fragmentation.

## Discussion

### Comment by [@gbenhaim](https://github.com/gbenhaim) — 2025-07-17T07:26:18Z

cc @kannon92

### Comment by [@kannon92](https://github.com/kannon92) — 2025-07-17T11:41:50Z

ref: https://github.com/openshift/kueue-operator/pull/441#discussion_r2207285597

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-15T12:03:49Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-15T13:04:22Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-13T14:01:43Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-13T16:55:04Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-13T17:09:51Z

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
