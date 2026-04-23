# Issue #3759: Support Hierarchical Cohorts with FairSharing

**Summary**: Support Hierarchical Cohorts with FairSharing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3759

**Last updated**: 2025-03-21T09:36:33Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-12-06T15:56:12Z
- **Updated**: 2025-03-21T09:36:33Z
- **Closed**: 2025-03-21T09:36:33Z
- **Labels**: `kind/feature`
- **Assignees**: [@gabesaba](https://github.com/gabesaba)
- **Comments**: 3

## Description

**What would you like to be added**:

Proper support for Hierarchical Cohorts with Fair Sharing. Determine what are the gaps to make it officially supported and implement the support.

**Why is this needed**:

Currently the behavior for combining Hierarchical Cohorts with FairSharing is undefined. See: https://github.com/kubernetes-sigs/kueue/blob/3edad2589255cb14a8ce3d69424f38edd8319876/apis/kueue/v1alpha1/cohort_types.go#L68-L70

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] Implementation
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-06T15:56:38Z

/assign @gabesaba 
tentatively
cc @mwielgus @mwysokin @tenzen-y

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-06T16:01:59Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-06T16:09:41Z

/remove-lifecycle stale
