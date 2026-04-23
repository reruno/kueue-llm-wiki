# Issue #170: Replicate ExtendedResourceToleration

**Summary**: Replicate ExtendedResourceToleration

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/170

**Last updated**: 2023-01-08T15:47:23Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-04-01T17:34:21Z
- **Updated**: 2023-01-08T15:47:23Z
- **Closed**: 2023-01-08T15:47:22Z
- **Labels**: `triage/needs-information`, `lifecycle/rotten`, `kind/documentation`
- **Assignees**: _none_
- **Comments**: 11

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Through the [ExtendedResourceToleration admission controller](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#extendedresourcetoleration) kubernetes automatically adds tolerations to pods requesting custom resources.

If a workload uses extended resources that match the ones set by the admission controller and the ClusterQueue has a taint for it, the workloads would be inadmissible.

**Why is this needed**:

Not sure if we actually need it. Maybe it's not a good practice for users to use these taints in their ResourceFlavors?

## Discussion

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-04T21:21:50Z

> If a user sets tolerations for extended resources that match the ones set by the admission controller, the workloads would be inadmissible.

Not sure I understand this, why it will be inadmissible?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-04-05T13:24:39Z

Because the toleration is only added at Pod creation, so it wouldn't be part of the QueuedWorkload. Then kueue wouldn't consider this toleration for flavor assignment.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-04-05T16:00:27Z

It doesn't seem like this would be a valid use case.

We just need to document it.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-07-12T02:12:10Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues and PRs.

This bot triages issues and PRs according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue or PR as fresh with `/remove-lifecycle stale`
- Mark this issue or PR as rotten with `/lifecycle rotten`
- Close this issue or PR with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-08-11T03:11:47Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues and PRs according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue or PR as fresh with `/remove-lifecycle rotten`
- Close this issue or PR with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-11T13:29:41Z

/remove-lifecycle rotten

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-11T13:41:36Z

To clarify why this might not be a valid use case:

A flavor should have taints for a resource model, not the resource itself.

For example, in GKE, Pods can have the following nodeSelector to match a particular GPU model:

```yaml
cloud.google.com/gke-accelerator: nvidia-tesla-k80
```

Whereas the name of the resource itself is `nvidia.com/gpu`. Flavors shouldn't have a taint against this label.

But if someone has a use-case that I'm missing, we can probably add this feature as an option.

/triage needs-information

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-11-09T14:28:29Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues and PRs.

This bot triages issues and PRs according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue or PR as fresh with `/remove-lifecycle stale`
- Mark this issue or PR as rotten with `/lifecycle rotten`
- Close this issue or PR with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-12-09T15:01:21Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues and PRs according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue or PR as fresh with `/remove-lifecycle rotten`
- Close this issue or PR with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2023-01-08T15:47:20Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-01-08T15:47:23Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/170#issuecomment-1374866265):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
