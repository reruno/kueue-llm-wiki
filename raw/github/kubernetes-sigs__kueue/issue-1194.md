# Issue #1194: [dep] Updated `k8s.io/autoscaler/cluster-autoscaler` version to a stable one.

**Summary**: [dep] Updated `k8s.io/autoscaler/cluster-autoscaler` version to a stable one.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1194

**Last updated**: 2024-05-13T13:05:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@trasc](https://github.com/trasc)
- **Created**: 2023-10-11T07:37:52Z
- **Updated**: 2024-05-13T13:05:59Z
- **Closed**: 2024-05-13T13:05:57Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 8

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Use a released version of `k8s.io/autoscaler/cluster-autoscaler` containing https://github.com/kubernetes/autoscaler/commit/5155725a28189cd1b65f001fcdf90699f5cde909

**Why is this needed**:

Have clean dependencies.

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-01-30T03:14:46Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-30T13:00:56Z

/remove-lifecycle stale

@trasc Since released the new cluster-autoscaler with PriviosningRequest API, we can do this, right?

### Comment by [@trasc](https://github.com/trasc) — 2024-02-12T07:03:41Z

@tenzen-y Indeed the the code we need is now part of a github release [1.29.0](https://github.com/kubernetes/autoscaler/releases/tag/cluster-autoscaler-1.29.0) but unfortunately the release is tagged with `cluster-autoscaler-1.29.0` instead of `cluster-autoscaler/v1.29.0` and it cannot be referenced from go.mod.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-02-12T13:20:44Z

> @tenzen-y Indeed the the code we need is now part of a github release [1.29.0](https://github.com/kubernetes/autoscaler/releases/tag/cluster-autoscaler-1.29.0) but unfortunately the release is tagged with `cluster-autoscaler-1.29.0` instead of `cluster-autoscaler/v1.29.0` and it cannot be referenced from go.mod.

@trasc Yea, that makes sense. Indeed, I'm working on new tag format `k8s.io/autoscaler/cluster-autoscaler/apis` in https://github.com/kubernetes/autoscaler/pull/6315#issuecomment-1893441957.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-05-12T14:15:36Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-13T13:04:56Z

/remove-lifecycle stale

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-13T13:05:53Z

This is replaced with #1896 
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-05-13T13:05:58Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1194#issuecomment-2107529221):

>This is replaced with #1896 
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
