# Issue #3716: TAS: Implement e2e tests for RayJob with TAS

**Summary**: TAS: Implement e2e tests for RayJob with TAS

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3716

**Last updated**: 2025-03-04T18:21:46Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-12-03T09:32:27Z
- **Updated**: 2025-03-04T18:21:46Z
- **Closed**: 2025-03-04T18:21:46Z
- **Labels**: `kind/feature`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
E2e tests for RayJob with TAS

**Why is this needed**:

Discussed here as well: https://github.com/kubernetes-sigs/kueue/pull/3704#discussion_r1866116694

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-12-03T09:32:48Z

/cc @mbobrovskyi

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-12-04T07:23:52Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-04T07:38:14Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-04T07:45:00Z

/remove-lifecycle stale
It is being done as part of https://github.com/kubernetes-sigs/kueue/pull/4341
