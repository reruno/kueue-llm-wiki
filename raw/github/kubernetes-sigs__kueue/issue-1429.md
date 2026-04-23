# Issue #1429: Stop supporting kubeflow/mxjob integration

**Summary**: Stop supporting kubeflow/mxjob integration

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1429

**Last updated**: 2025-03-17T16:26:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2023-12-08T15:40:24Z
- **Updated**: 2025-03-17T16:26:23Z
- **Closed**: 2025-03-17T16:26:21Z
- **Labels**: `kind/cleanup`, `lifecycle/frozen`
- **Assignees**: _none_
- **Comments**: 8

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
We should stop supporting the kubeflow/mxjob integration.

**Why is this needed**:
Due to Apache MXNet having been archived, the kubeflow community plans to remove MXJob from the training-operator.

https://github.com/kubeflow/training-operator/pull/1953

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-08T15:41:33Z

We need to watch #1953, and then we can decide when we stop supporting this integration.

### Comment by [@terrytangyuan](https://github.com/terrytangyuan) — 2023-12-21T02:24:08Z

Yes, I don't have any concerns about dropping Apache MXNet support.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-03-20T03:04:00Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-20T16:32:28Z

/lifecycle frozen.

Kubeflow Community decided to remove MXJob after 1 minor release.
So, we can remove the kubefow/mxjob integration after it.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-20T16:32:39Z

/lifecycle frozen

### Comment by [@kannon92](https://github.com/kannon92) — 2025-03-17T16:22:03Z

@tenzen-y 

With https://github.com/kubernetes-sigs/kueue/pull/4077, is there any reason to keep this doc open?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T16:26:17Z

>  doc open?

i assume "issue" open, I don't think there is, closing
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-17T16:26:22Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1429#issuecomment-2730136805):

>>  doc open?
>
>i assume "issue" open, I don't think there is, closing
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
