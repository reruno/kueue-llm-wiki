# Issue #993: Introduce a plugin mechanism for arbitrary checks during workload admission.

**Summary**: Introduce a plugin mechanism for arbitrary checks during workload admission.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/993

**Last updated**: 2024-01-31T17:48:36Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mwielgus](https://github.com/mwielgus)
- **Created**: 2023-07-17T22:13:20Z
- **Updated**: 2024-01-31T17:48:36Z
- **Closed**: 2024-01-30T23:37:41Z
- **Labels**: `kind/feature`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 9

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

A mechanism to admit workloads based on both ClusterQueue quota and checks made by an external controller. 

**Why is this needed**:

The current admission process only checks queue resources and doesn't allow to use some cloud provider API or prometheus database query.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-08-25T13:34:19Z

/reopen
Implementation is still ongoing

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-08-25T13:34:23Z

@alculquicondor: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/993#issuecomment-1693371355):

>/reopen
>Implementation is still ongoing


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@trasc](https://github.com/trasc) — 2023-09-13T14:52:54Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-01-28T06:59:53Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-29T13:16:01Z

/remove-lifecycle stale

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-30T23:37:36Z

/close

This was implemented in 0.5

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-01-30T23:37:42Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/993#issuecomment-1918094726):

>/close
>
>This was implemented in 0.5


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-31T07:15:18Z

@alculquicondor IIRC, we're still working on #1178. Or, we should open a separate issue?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-31T17:48:35Z

Good point, opened #1677.
