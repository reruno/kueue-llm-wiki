# Issue #9852: KEP-8303: Add an explicit opt-in API for MultiKueue single-cluster preemptions

**Summary**: KEP-8303: Add an explicit opt-in API for MultiKueue single-cluster preemptions

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9852

**Last updated**: 2026-06-11T11:54:20Z

---

## Metadata

- **State**: open
- **Author**: [@kshalot](https://github.com/kshalot)
- **Created**: 2026-03-13T11:14:53Z
- **Updated**: 2026-06-11T11:54:20Z
- **Closed**: —
- **Labels**: `kind/feature`, `lifecycle/stale`, `area/multikueue`
- **Assignees**: _none_
- **Comments**: 2

## Description

**What would you like to be added**:
Extend the MultiKueue `Configuration` API with fields serving as opt-in for the `MultiKueueOrchestratedPreemption` feature gate.

For example `PreemptionsMode: Concurrent|AtMostOne`.

**Why is this needed**:
https://github.com/kubernetes-sigs/kueue/pull/9721 implements the `MultiKueueOrchestratedPreemption` feature gate which serves as the opt-in mechanism for the single-cluster preemption guarantee in MultiKueue. When this feature graduates to beta without an explicit opt-in mechanism from the user, the default behavior of MultiKueue deployments would change.

We should add an API that allows the users to control the behavior of the preemptions in MultiKueue.

See https://github.com/kubernetes-sigs/kueue/pull/9721#issuecomment-4054172653 for context.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kshalot](https://github.com/kshalot) — 2026-03-13T11:15:02Z

/area multikueue

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-06-11T11:54:18Z

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
