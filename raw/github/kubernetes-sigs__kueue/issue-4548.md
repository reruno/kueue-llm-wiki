# Issue #4548: TAS: add unit tests for error branches in tas_flavor_assigner

**Summary**: TAS: add unit tests for error branches in tas_flavor_assigner

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4548

**Last updated**: 2025-07-22T12:38:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-11T07:35:08Z
- **Updated**: 2025-07-22T12:38:29Z
- **Closed**: 2025-07-22T12:38:29Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@Horiodino](https://github.com/Horiodino)
- **Comments**: 4

## Description

**What would you like to be cleaned**:

cover the error branches in tas_flavor_assigner:

https://github.com/kubernetes-sigs/kueue/blob/6e8d4143e4969d424597d9a30c7672f6ea1210fc/pkg/scheduler/flavorassigner/tas_flavorassigner.go#L55-L57

https://github.com/kubernetes-sigs/kueue/blob/6e8d4143e4969d424597d9a30c7672f6ea1210fc/pkg/scheduler/flavorassigner/tas_flavorassigner.go#L65-L67

These could be new test cases for `WorkloadsTopologyRequests`. 

**Why is this needed**:

To cover the code with tests, this was suggested in comments  https://github.com/kubernetes-sigs/kueue/pull/4200#discussion_r1951691235 and https://github.com/kubernetes-sigs/kueue/pull/4200#discussion_r1952616625 .

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-11T07:35:19Z

cc @tenzen-y @PBundyra

### Comment by [@Horiodino](https://github.com/Horiodino) — 2025-04-11T16:48:49Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-10T17:45:47Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-10T17:49:44Z

/remove-lifecycle stale
