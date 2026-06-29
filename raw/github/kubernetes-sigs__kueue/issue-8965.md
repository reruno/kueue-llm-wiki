# Issue #8965: Add label filters for TAS e2e tests

**Summary**: Add label filters for TAS e2e tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8965

**Last updated**: 2026-06-12T11:09:21Z

---

## Metadata

- **State**: open
- **Author**: [@j-skiba](https://github.com/j-skiba)
- **Created**: 2026-02-03T14:55:47Z
- **Updated**: 2026-06-12T11:09:21Z
- **Closed**: —
- **Labels**: `lifecycle/stale`, `kind/cleanup`
- **Assignees**: [@laxmi-333](https://github.com/laxmi-333)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

It would be nice to have label filters for tas e2e tests like here - https://github.com/kubernetes-sigs/kueue/pull/8005 too. It takes a lot of time to setup the cluster for these tests.

**Why is this needed**:

Quicker cluster setup time when running specific suites of TAS e2e tests

## Discussion

### Comment by [@laxmi-333](https://github.com/laxmi-333) — 2026-03-14T11:03:47Z

Hi @j-skiba, I would like to work on this issue.

### Comment by [@laxmi-333](https://github.com/laxmi-333) — 2026-03-14T11:07:10Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-06-12T11:09:18Z

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
