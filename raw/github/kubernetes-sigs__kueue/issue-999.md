# Issue #999: Integrate with cluster-autoscaler's ProvisioningRequest

**Summary**: Integrate with cluster-autoscaler's ProvisioningRequest

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/999

**Last updated**: 2024-01-25T16:24:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-07-18T16:59:20Z
- **Updated**: 2024-01-25T16:24:32Z
- **Closed**: 2024-01-25T16:24:30Z
- **Labels**: `kind/feature`, `lifecycle/stale`
- **Assignees**: _none_
- **Comments**: 4

## Description

**What would you like to be added**:

Use #993 to integrate with the ProvisioningRequest API by cluster autoscaler https://github.com/kubernetes/autoscaler/pull/5848

**Why is this needed**:

This will allow atomic scale ups (depending on the provider implementation of cluster-autoscaler).

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-01-24T19:06:06Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-25T16:12:57Z

@alculquicondor Is this still needed? I think this already done.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-25T16:24:26Z

oh yes, the PR is #1154

I guess we duplicated this issue here #1136

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-01-25T16:24:31Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/999#issuecomment-1910549641):

>oh yes, the PR is #1154
>
>I guess we duplicated this issue here #1136
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
