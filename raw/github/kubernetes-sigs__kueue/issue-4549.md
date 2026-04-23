# Issue #4549: TAS: add test cases for multiple podsets to TestFindTopologyAssignment

**Summary**: TAS: add test cases for multiple podsets to TestFindTopologyAssignment

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4549

**Last updated**: 2025-08-13T13:27:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-11T07:41:24Z
- **Updated**: 2025-08-13T13:27:12Z
- **Closed**: 2025-08-13T13:27:12Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@Horiodino](https://github.com/Horiodino)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Extend the tests in TestFindTopologyAssignment (in pkg/cache/tas_cache_test.go) with multiple pod sets.

**Why is this needed**:

To cover full logic of the exposed function `FindTopologyAssignment` at this level of tests. The case of multiple podsets is currently covered by scheduler_test.go, but it is a higher level test. 

This was discussed in the thread: https://github.com/kubernetes-sigs/kueue/pull/4200#discussion_r1950941580

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-11T07:42:05Z

cc @tenzen-y @PBundyra

### Comment by [@Horiodino](https://github.com/Horiodino) — 2025-03-17T12:33:20Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-15T12:39:20Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-06-16T13:35:57Z

/remove-lifecycle stale
