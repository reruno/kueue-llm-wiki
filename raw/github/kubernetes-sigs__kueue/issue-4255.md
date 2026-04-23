# Issue #4255: [TAS] Remove the TASProfileMostFreeCapacity FG or replace with API configuration

**Summary**: [TAS] Remove the TASProfileMostFreeCapacity FG or replace with API configuration

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4255

**Last updated**: 2026-01-29T15:14:21Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-02-13T16:46:49Z
- **Updated**: 2026-01-29T15:14:21Z
- **Closed**: 2026-01-29T15:14:05Z
- **Labels**: `kind/feature`, `lifecycle/stale`
- **Assignees**: _none_
- **Comments**: 8

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Since we introduced `BestFit` algorithm to TAS, we decided to deprecate `MostFreeCapacity`/`LeastFreeCapacity' algorithms, see (KEP)[https://github.com/kubernetes-sigs/kueue/pull/4542/files]
This involves:
- removing deprecated feature gates,
- cleaning up unit tests in `tas_cache_test.go`
- cleaning up `tas_flavor_snapshot.go`

**Why is this needed**:

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-14T17:32:24Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-05-15T10:55:32Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-28T09:49:25Z

/retitle [TAS] Remove the TASProfileMostFreeCapacity FG or replace with API configuration

Since the mode MostFreeCapacity is gone anyway in 0.13: https://github.com/kubernetes-sigs/kueue/pull/5536

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-26T09:50:33Z

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-10-26T11:05:28Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-24T11:16:39Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-29T15:14:00Z

/close
Lets handle as part of https://github.com/kubernetes-sigs/kueue/issues/8855

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-29T15:14:06Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4255#issuecomment-3818324854):

>/close
>This is part of https://github.com/kubernetes-sigs/kueue/issues/8855


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
