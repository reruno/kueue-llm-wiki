# Issue #8038: [TAS] Add documentation for two-level scheduling TAS with examples of JobSet

**Summary**: [TAS] Add documentation for two-level scheduling TAS with examples of JobSet

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8038

**Last updated**: 2026-03-19T10:50:14Z

---

## Metadata

- **State**: open
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-12-02T11:35:53Z
- **Updated**: 2026-03-19T10:50:14Z
- **Closed**: —
- **Labels**: `priority/important-soon`, `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
Test manually how two-level scheduling for JobSet works and add documentation. Particularly cover 3 scenarios, when Jobset uses:
- just `podset` TAS annotations
- just `podset-slice` TAS annotations
- both `podset` and `podset-slice` annotations

**Why is this needed**:

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-12-11T10:07:15Z

cc @kshalot

### Comment by [@kshalot](https://github.com/kshalot) — 2025-12-11T10:47:34Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:42:02Z

/priority important-soon

### Comment by [@kshalot](https://github.com/kshalot) — 2025-12-19T09:46:19Z

/unassign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T10:46:20Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-19T10:50:11Z

/remove-lifecycle stale
