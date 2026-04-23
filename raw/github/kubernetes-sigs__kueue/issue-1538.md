# Issue #1538: Add resource check before dispatching workloads

**Summary**: Add resource check before dispatching workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1538

**Last updated**: 2024-09-29T17:56:29Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@asm582](https://github.com/asm582)
- **Created**: 2024-01-02T14:42:22Z
- **Updated**: 2024-09-29T17:56:29Z
- **Closed**: 2024-09-29T17:56:28Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 16

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

When quotas are not resources it could be the case that the user has enough quota but the cluster does not have enough physical hardware resources to launch the job. This could cause a premature dispatch and lead to the creation of pending pods. In the worst case, this could lead to resource hogging in the cluster.

**Why is this needed**:
This feature is needed to ensure that we have guaranteed workload execution post-workload dispatch.

**Completion requirements**:

This requirement would need modification on Kueue core dispatch logic. 

This enhancement requires the following artifacts:

- [X] Design doc
- [X] API change
- [X] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-02T20:08:39Z

I'm assuming you are asking for Kueue to check the resources in the existing nodes. We don't plan to do this. Kueue's responsibility is quota.

That said, we have a mechanism to extend kueue, called admission checks. We have one admission check that cluster-autoscaler implements. https://kueue.sigs.k8s.io/docs/admission-check-controllers/provisioning/

Then cluster-autoscaler is responsible for checking the nodes or doing a scale up.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-02T20:10:31Z

Btw, in general, quota management is already a good approximation for what is available in a cluster and people are using Kueue in non-autoscaled environments in production just based on that.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-02T20:20:03Z

Since you are coming from DRA, I think we can make this feature request about DRA.
Then, what we would need is a quota model for DRA resources. Not sure if this makes sense at all. But it's definitely not possible without a numeric model.

### Comment by [@asm582](https://github.com/asm582) — 2024-01-02T20:23:22Z

> Btw, in general, quota management is already a good approximation for what is available in a cluster and people are using Kueue in non-autoscaled environments in production just based on that.

ok, so the assumption is that quotas are resources in the cluster

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-02T20:25:10Z

In a fixed sized cluster, yes. In an autoscaled cluster, it's the maximum size that the cluster can reach.

### Comment by [@asm582](https://github.com/asm582) — 2024-01-02T20:30:42Z

> Since you are coming from DRA, I think we can make this feature request about DRA. Then, what we would need is a quota model for DRA resources. Not sure if this makes sense at all. But it's definitely not possible without a numeric model.

With DRA I think quota and physical resources may not be 1:1 and in such a scenario a quota check may pass, for instance user has a quota to acquire a slice of GPU but on the physical hardware such a slice is not realized causing a false positive dispatch if that makes sense. 

I am not sure if the numeric model provides a gaurantee that a user requested slice would be made available on the node.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-02T20:45:34Z

FYI: @asm582

I have a similar situation in the required multiple GPUs per pods. We can imagine the following situation:

- The job has 2 parallelisms and requires the sum of 10 GPUs, which means every pod requires 5 GPUs.
- Every node has only 3 GPUs although the cluster has 10 GPUs.

I'm preparing the new requeueing strategy KEP to prevent infinity re-dispatching the above jobs.

https://github.com/kubernetes-sigs/kueue/pull/1311#issuecomment-1870531528

### Comment by [@asm582](https://github.com/asm582) — 2024-01-03T15:14:53Z

> FYI: @asm582
> 
> I have a similar situation in the required multiple GPUs per pods. We can imagine the following situation:
> 
> * The job has 2 parallelisms and requires the sum of 10 GPUs, which means every pod requires 5 GPUs.
> * Every node has only 3 GPUs although the cluster has 10 GPUs.
> 
> I'm preparing the new requeueing strategy KEP to prevent infinity re-dispatching the above jobs.
> 
> [#1311 (comment)](https://github.com/kubernetes-sigs/kueue/pull/1311#issuecomment-1870531528)

Thanks, I think this still is a case of false positive dispatch because of a lack of resource checks.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-04-02T15:34:07Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-05-02T15:44:44Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-02T16:11:24Z

@asm582 is still fair to say that the request is for Kueue to support DRA?

OTOH, some of these "checks" can be achieved via ProvisioningRequest, once cluster-autoscaler supports DRA.
Or via pod group in kube-scheduler, if the proposal progresses https://github.com/kubernetes/enhancements/pull/3371

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-02T16:11:39Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-07-31T17:02:32Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-08-30T17:12:26Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-09-29T17:56:25Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-09-29T17:56:29Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1538#issuecomment-2381444010):

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


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
