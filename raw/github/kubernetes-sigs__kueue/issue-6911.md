# Issue #6911: TAS: drop using the "tas" label in indexer

**Summary**: TAS: drop using the "tas" label in indexer

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6911

**Last updated**: 2026-01-27T12:49:53Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-09-18T12:41:50Z
- **Updated**: 2026-01-27T12:49:53Z
- **Closed**: 2026-01-27T12:49:53Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Drop this code: https://github.com/kubernetes-sigs/kueue/pull/6895/files#diff-0a6000cd4794821c10f043f050933b9525918a74538f347966e63ca8ee8a0082R41-R43 
in TAS indexer. 

This code was added to make sure there is no disruptions when upgrading Kueue 0.13 to 0.14. Otherwise TAS workloads which were running in the implicit mode could be treated as non-TAS.

For the newly created workloads now TAS in the implicit mode will inject the "unconstrained" annotation which is used by the indexer to determine if TAS pod or not.

This is needed only in the migration phase. Once all workloads are created with Kueue 0.14+ we can drop it. I think we can drop it in 0.16.

**Why is this needed**:

To cleanup migration code.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-18T12:41:58Z

cc @tenzen-y @PBundyra

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-22T02:48:38Z

> This is needed only in the migration phase. Once all workloads are created with Kueue 0.14+ we can drop it. I think we can drop it in 0.16.

Are you saying that we can only do this issue in 0.16?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-22T07:42:59Z

> Are you saying that we can only do this issue in 0.16?

Yes, at least 0.16.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-21T08:32:06Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-12-22T12:34:48Z

/remove-lifecycle stale
