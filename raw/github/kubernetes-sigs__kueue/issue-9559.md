# Issue #9559: Add TASBalancedPlacement as a workload-level setting

**Summary**: Add TASBalancedPlacement as a workload-level setting

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9559

**Last updated**: 2026-05-28T09:59:07Z

---

## Metadata

- **State**: open
- **Author**: [@varunsyal](https://github.com/varunsyal)
- **Created**: 2026-02-27T09:37:21Z
- **Updated**: 2026-05-28T09:59:07Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Today, we can use the `TASBalancedPlacement` feature gate to set a global cluster-wide placement strategy. Can we add this at the workload-level as well? If it makes sense, the same could be done for other placement strategies supported by Kueue like `BestFit`.

**Why is this needed**:

This could enable use cases, where we can set  one global policy regarding the placement at the cluster level, but allow workloads to specify and override this through an annotation.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x ] API change
- [x ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-05-28T09:57:45Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-05-28T09:59:04Z

/remove-lifecycle stale
cc @mwysokin
