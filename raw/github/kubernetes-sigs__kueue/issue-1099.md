# Issue #1099: Decouple the ClusterQueue snapshots queue from the CQ reconciler

**Summary**: Decouple the ClusterQueue snapshots queue from the CQ reconciler

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1099

**Last updated**: 2024-01-30T22:46:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2023-09-08T09:06:23Z
- **Updated**: 2024-01-30T22:46:51Z
- **Closed**: 2024-01-30T22:46:49Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@lowang-bh](https://github.com/lowang-bh)
- **Comments**: 14

## Description

<!-- Please only use this template for submitting clean up requests -->

This is a follow up for the comment: https://github.com/kubernetes-sigs/kueue/pull/1069#discussion_r1319096989

**What would you like to be cleaned**:

Decouple the `snaphotsQueue` from the CQ reconciler.

**Why is this needed**:

To improve readability by not overloading the reconciler with responsibilities.

## Discussion

### Comment by [@lowang-bh](https://github.com/lowang-bh) — 2023-09-15T11:05:51Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2023-09-19T16:12:05Z

@lowang-bh FYI: https://github.com/kubernetes-sigs/kueue/pull/1135 makes the coupling somewhat stronger. I'm wondering if this is still feasible.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-01-28T16:59:49Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-30T13:18:01Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-30T13:27:34Z

I think it is fair to close it, we probably prefer to have the visibility server anyway, and we could drop the workloads in status entirely in the future releases. It is Alpha level anyway at this point.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-30T13:34:15Z

> we probably prefer to have the visibility server 

I'd also prefer to use the visibility server. However, we can not remove ClusterQueueVisibility without visibility-server since the ClusterQueueVisibility without visibility-server is under the beta stage, and we already expose pending workloads via beta API, ClusterQueue.

So, I think that some refactoring would still be effective.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-30T13:45:54Z

Hm, even though the feature itself is Alpha-level: https://github.com/kubernetes-sigs/kueue/blob/38cedb172e42cbbeb8c12225baab827583db6c3b/pkg/features/kube_features.go#L40? 

I would prefer to deprecate it and drop entirely.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-30T13:52:20Z

> Hm, even though the feature itself is Alpha-level:
> 
> https://github.com/kubernetes-sigs/kueue/blob/38cedb172e42cbbeb8c12225baab827583db6c3b/pkg/features/kube_features.go#L40
> 
> ?
> I would prefer to deprecate it and drop entirely.

Oh, I see. I thought this is in beta stage due to: https://github.com/kubernetes-sigs/kueue/blob/f2cba29c80349181773183bc053a0510ea399a5e/keps/168-pending-workloads-visibility/kep.yaml#L20

However, I think that we can not change APIs without backward compatibility since the ClusterQueue API is beta.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-30T14:00:38Z

Can we just keep dummy API and remove the code to support it, is there any procedure to remove beta apis?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-30T14:20:49Z

> Can we just keep dummy API and remove the code to support it

I'm not sure that it follows the Kubernetes deprecation policy. 
@alculquicondor Let us know what we should do in this case.

> is there any procedure to remove beta apis?

You mean that introducing a new API version, v1beta2 or v1?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-30T14:55:26Z

> You mean that introducing a new API version, v1beta2 or v1?

I meant to remove an API field, possibly going to v1beta2 without the fields.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-30T14:58:05Z

> I meant to remove an API field

This way has breaking backward compatibility... So I think that we can not take this way.

> possibly going to v1beta2 without the fields.

If so, we probably need to provide conversion webhooks.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-30T22:46:45Z

Yes, we should remove it once we are ready to go to v1beta2 or v1.

Let's close this for now.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-01-30T22:46:49Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1099#issuecomment-1918040409):

>Yes, we should remove it once we are ready to go to v1beta2 or v1.
>
>Let's close this for now.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
