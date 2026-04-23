# Issue #3419: Support ProvisioningRequest v1 API

**Summary**: Support ProvisioningRequest v1 API

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3419

**Last updated**: 2025-08-03T17:14:13Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-11-04T06:27:15Z
- **Updated**: 2025-08-03T17:14:13Z
- **Closed**: 2025-08-03T17:14:12Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 13

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Recently, the autoscaler has been released the v1 ProvisioningRequest API: https://github.com/kubernetes/autoscaler/tree/d06fe04ccd1814ce5ab8c4945432806a9e269bcd/cluster-autoscaler/apis/provisioningrequest/autoscaling.x-k8s.io/v1

So, I believe that we should support both v1beta1 and v1 as well.

**Why is this needed**:
I guess that v1beta1 will be removed in the future.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-04T06:29:43Z

@yaroslava-serdiuk @mwielgus @aleksandra-malinowska Do you have any schedule to remove the v1beta1 ProvisioningRequest?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-05T11:38:33Z

I synced with @yaroslava-serdiuk and 1.31 is the first version of CA supporting ProvReq v1. So, given our policy in Kueue to support all versions which are not EOL the easiest would be to start using v1 when all non-EOL k8s versions support it, which means around 1.34 or 1.35.

### Comment by [@aleksandra-malinowska](https://github.com/aleksandra-malinowska) — 2024-11-05T11:40:06Z

There's currently no schedule for removing v1beta1. We need to verify what are the exact deprecation requirements for SIG-owned APIs such as ProvisioningRequest, but I expect a bare minimum is 1 minor release for deprecation before it disappears. This should give Kueue more than enough time to migrate.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-05T11:43:56Z

Ok, so let's park it for now until we get a deprecation warning in CA or when all non-EOL versions support v1.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-26T13:43:44Z

> Ok, so let's park it for now until we get a deprecation warning in CA or when all non-EOL versions support v1.

Basically, lgtm
But what if the cluster has only v1 ProvisioningRequest CRD?
The Kueue ProvReq creation will fail, isn't it?

### Comment by [@aleksandra-malinowska](https://github.com/aleksandra-malinowska) — 2024-11-26T15:16:44Z

>But what if the cluster has only v1 ProvisioningRequest CRD?

The user can also misconfigure the cluster in other ways, for example not deploy the ProvisioningRequest CRD at all.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-27T13:14:39Z

> > But what if the cluster has only v1 ProvisioningRequest CRD?
> 
> The user can also misconfigure the cluster in other ways, for example not deploy the ProvisioningRequest CRD at all.

I think that there are not issues in the situation since the kueue-controller-manager check if the cluster has ProvReq CRD: https://github.com/kubernetes-sigs/kueue/blob/72e44deaa5565a09f118e841b7f3c22a16ebebc2/cmd/kueue/main.go#L253C64-L253C97

Here is the problem, we can not detect the v1 ProvReq.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-02-25T13:40:15Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-25T15:04:17Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-26T16:01:55Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-26T16:03:18Z

/remove-lifecycle stale

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-03T17:14:08Z

https://github.com/kubernetes-sigs/kueue/pull/4444

This was done in v0.13.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-08-03T17:14:13Z

@kannon92: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3419#issuecomment-3148569291):

>https://github.com/kubernetes-sigs/kueue/pull/4444
>
>This was done in v0.13.
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
