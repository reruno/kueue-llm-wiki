# Issue #7133: Determine the status of the PrioritySortingWithinCohort feature gate (hopefully drop)

**Summary**: Determine the status of the PrioritySortingWithinCohort feature gate (hopefully drop)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7133

**Last updated**: 2026-03-19T12:51:12Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-02T07:54:50Z
- **Updated**: 2026-03-19T12:51:12Z
- **Closed**: —
- **Labels**: `kind/cleanup`, `priority/important-longterm`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to determine the status of the PrioritySortingWithinCohort feature gate, preferably drop it.

If there are valid use cases for the switch, then it should be moved from feature gate to the global configuration and provided long term.

**Why is this needed**:

Feature gates are only temporary measure. 
This feature gate was introduced to disable priority ordering between CQs before FairSharing was provided. 
It remained alpha for long as it was always designed just a mitigation before FairSharing (which is using DRS for ordering).

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-02T07:55:23Z

cc @amy @mwysokin @tenzen-y 

Opening this up as I noticed it is still in use here: https://github.com/kubernetes-sigs/kueue/issues/7101

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:48:17Z

/priority important-longterm

I would like to drop it in 0.16 or 0.17, let us know @amy if you still need it

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T12:48:21Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-19T12:51:09Z

/remove-lifecycle stale
