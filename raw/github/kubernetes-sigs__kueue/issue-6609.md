# Issue #6609: Remove deprecated QueueAnnotation  from `pkg/constants`  & its usages

**Summary**: Remove deprecated QueueAnnotation  from `pkg/constants`  & its usages

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6609

**Last updated**: 2025-11-16T13:56:54Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@Horiodino](https://github.com/Horiodino)
- **Created**: 2025-08-18T13:13:16Z
- **Updated**: 2025-11-16T13:56:54Z
- **Closed**: 2025-11-16T13:56:53Z
- **Labels**: `lifecycle/stale`, `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 7

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
The constant `constants.QueueAnnotation` is still present and used in the codebase (e.g. in the RayCluster controller test at [https://github.com/kubernetes-sigs/kueue/blob/main/test/integration/singlecluster/controller/jobs/raycluster/raycluster\_controller\_test.go#L262](https://github.com/kubernetes-sigs/kueue/blob/main/test/integration/singlecluster/controller/jobs/raycluster/raycluster_controller_test.go#L262)). This annotation is deprecated and should be removed completely from `pkg/controller/constants/constants.go`.

**Why is this needed**:
Since `QueueAnnotation` is deprecated and `QueueLabel` is already being used in its place, keeping the annotation in the codebase is unnecessary and may cause confusion. It should be removed entirely to ensure only the supported QueueLabel is used  in future.

## Discussion

### Comment by [@Horiodino](https://github.com/Horiodino) — 2025-08-18T13:13:45Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-18T13:21:03Z

We must not remove the annotations. We will remove that when we graduate API version.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-18T13:21:15Z

/unassign @Horiodino

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-16T13:26:11Z

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-16T13:56:41Z

I think we can close it, since it was already removed.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-16T13:56:48Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-16T13:56:54Z

@mbobrovskyi: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6609#issuecomment-3538781031):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
