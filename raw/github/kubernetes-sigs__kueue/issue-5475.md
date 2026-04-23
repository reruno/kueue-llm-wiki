# Issue #5475: Populate all flavors available in CQ to cache ClusterQueue's admissionChecks map

**Summary**: Populate all flavors available in CQ to cache ClusterQueue's admissionChecks map

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5475

**Last updated**: 2025-10-14T14:21:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-06-03T13:02:26Z
- **Updated**: 2025-10-14T14:21:37Z
- **Closed**: 2025-10-14T14:21:37Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@ganczak-commits](https://github.com/ganczak-commits)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
In the code of ClusterQueue we assume that if the list of flavors in admissionCheck map is empty this admissionCheck applies to all flavors

https://github.com/kubernetes-sigs/kueue/blob/main/pkg/cache/scheduler/clusterqueue.go#L62-L65

I think this is tricky and we should populate the list with all available flavors in the CQ instead, here:

https://github.com/kubernetes-sigs/kueue/blob/main/pkg/util/admissioncheck/admissioncheck.go#L170


**Why is this needed**:

- Cleaner code
- Will allow to delete the tricky if here: https://github.com/kubernetes-sigs/kueue/pull/5426/files#diff-441da8393964615cf5b020d0afb9199588e157e50718e83b527788eb679391ecR649-R653

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-03T13:04:59Z

> Why is this needed:

I would say it makes reasoning about the code easier. Actually I got caught by this in the initial implemantation of the fix https://github.com/kubernetes-sigs/kueue/pull/5426. Once this task is done we can drop this hacky if: https://github.com/kubernetes-sigs/kueue/blob/be0ec185aa1a365861e9f17b2c29e6cc845267ab/pkg/cache/clusterqueue.go#L649-L653

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-01T13:41:34Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-09-01T14:19:15Z

/remove-lifecycle stale

### Comment by [@ganczak-commits](https://github.com/ganczak-commits) — 2025-09-08T07:19:50Z

/assign
