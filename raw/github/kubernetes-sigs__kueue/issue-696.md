# Issue #696: Consider ResourceQuota when admitting workloads

**Summary**: Consider ResourceQuota when admitting workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/696

**Last updated**: 2025-05-31T18:14:08Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2023-04-14T20:06:01Z
- **Updated**: 2025-05-31T18:14:08Z
- **Closed**: 2025-05-31T18:14:05Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 28

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Batch administrators can install [ResourceQuota](https://kubernetes.io/docs/concepts/policy/resource-quotas/) to set constraints for total requests in the namespace.

We should consider ResourceQuotas when admitting Workloads.

**Why is this needed**:
~~For now, we may sometime face the following problems:~~

~~1. if we use `Sequential Admission with Ready Pods` and ResourceQuotas together, we may face deadlocks.~~
~~2. Many unschedulable pods (with pending status) could be created.~~

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-14T22:23:47Z

I like this idea and I don't think we will face the problems you mention.
When ResourceQuotas are hit, the effect is that the pod can't even be created. The scheduler doesn't even get to see those pods. And because we will only allow jobs that satisfy the resource quota to be created, they won't hit the limit.
However, the open question is what to do with flavors. For it's simplest form, probably there would only be one flavor for which all resources are defined. And I guess we would create a ClusterQueue for each ResourceFlavor. It could be an optional mode of operation.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-04-18T11:44:58Z

> When ResourceQuotas are hit, the effect is that the pod can't even be created. The scheduler doesn't even get to see those pods. And because we will only allow jobs that satisfy the resource quota to be created, they won't hit the limit.

Ah, I see. Thank you for clarifying.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-04-18T13:09:46Z

> However, the open question is what to do with flavors. For it's simplest form, probably there would only be one flavor for which all resources are defined. And I guess we would create a ClusterQueue for each ResourceFlavor.

Uhm. In that case, we can not create ClusterQueues with multiple ResourceFlavors if batch admins select the optional mode of operation, right?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-20T09:17:44Z

Unless there are some annotations in the ResoureQuota, but that could be a later extension

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-04-23T18:27:21Z

> Unless there are some annotations in the ResoureQuota, but that could be a later extension

Sounds good.

### Comment by [@samzong](https://github.com/samzong) — 2023-12-05T06:34:35Z

> Unless there are some annotations in the ResoureQuota, but that could be a later extension

Could you explain this design in more detail? Sorry to bother you after such a long time.

How to balance clusterqueue quota vs. namespace ResourceQuota is a bit complicated, especially when clusterqueue is a cluster-level resource.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-12-05T06:36:15Z

Would NS ResourceQuota be another admission check?

### Comment by [@panpan0000](https://github.com/panpan0000) — 2023-12-07T02:48:57Z

Hi, @tenzen-y 

One of the import use case as below:

In a namespace, there may be different types of workloads(I call it "hybrid-workload") consuming hardware accelerators:

- Batch Jobs
- interactive notebook
- model serving deployments


So below situation happens:

- `kueue` can management the batch jobs, to limit them under quota of the ClusterQueue's FlavorQuotas.
- But the other workloads are still controlled by native kubernetes namespaced [resourceQuota](https://kubernetes.io/docs/concepts/policy/resource-quotas/)


The challenges are :

- The two quota-systems are in different dimension, FlavorQuota are not under namespace granularity, it's not suitable for multi-tenant scenarios (maybe I'm wrong..)
- The two kinds of workloads actually compete for same hardware resources. But they are not aware of the other. 
- For example
      - case 1: CluterQueue quota >= namespaced resourceQuota, and namespace quota meet its limit :  batch  jobs eat up all physical GPU, and later a notebook fails to launch. At this case, namespaced resourceQuota takes the ground control.
      - case 2:  But CluterQueue is not aware of namespaced resourceQuota, so maybe some notebook pods have used some GPU, and new batch job fails because namespace limit hit, but there's plenty of room in CluterQueue Quota.



In short, I think it's valuable to address the challenges , so that user can leverage `kueue` in multi-tenant circumstance with  
"hybrid-workload" :-)

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-07T06:08:40Z

> Would NS ResourceQuota be another admission check?

@kerthcet I think so too. Additional admission checks would resolve this issue.
@alculquicondor Any concerns?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-07T06:18:57Z

@panpan0000 I agree with issues by multi-dimensions quota management.

However, I think that your use cases might be sufficient once you can create CluserQueue against each namespaces (tenants). Then, you can construct cohorts against multiple ClusterQueue.

> interactive notebook
model serving deployments

Since we support [naked pods](https://kueue.sigs.k8s.io/docs/tasks/run_plain_pods/), you can manage those workloads by kueue. Ideally, I would suggest implementing CutomJob controllers to manage those workloads, then you can implement [the kueue workload controllers](https://kueue.sigs.k8s.io/docs/tasks/integrate_a_custom_job/) to manage those CustomJobs by kueue.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-07T06:25:50Z

I'm not against supporting ResourceQuota by admission checks, and I agree with the ResourceQuota support. I'm sure there are use cases in which we want to manage workloads by kueue + ResourceQuota, although, in an ideal world, all workloads are managed by the kueue's flavorQuotas.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-07T06:30:46Z

Also, we need to support elastic jobs to support model serving deployment with autoscaling semantics.

https://github.com/kubernetes-sigs/kueue/issues/77

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-12-07T06:48:09Z

What we hope to mitigate here is make job scheduling more smoothly, rather than admitted by kueue but rejected the resourceQuota admission plugin. But the tricky thing here is resourceQuota is too flexible, it has a bunch of policies and kueue can not simply sync with. So admission check might be the simplest thing we can boot with.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-27T17:48:54Z

> So admission check might be the simplest thing we can boot with.

I agree. An additional admission check would be better.
As another use case, existing resources managed by ResourceQuotas could easily adapt to the kueue.

In the adaption to the existing environments, I think that the ResourceQuota support has an advantage in terms of using all kueue features over using naked pod integration since our naked pod integration doesn't support all kueue features.

However, I'm on the fence about whether we should support ResourceQuota by AdmissionCheck since using ResourceQuota is a temporary measure since as I mentioned above, ideally, all resources are managed by Kueue's flavorQuotas.

@alculquicondor What do you think about supporting ResourceQuota by AdmissionCheck for easy adaptation to the existing environment?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-27T17:53:18Z

I don't think we should implement it.

As explained, it will be possible for someone to implement it using AdmissionChecks, but I don't think we should support it  in core Kueue. I would accept a controller in the cmd/experimental package though.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-27T17:58:02Z

> I don't think we should implement it.
> 
> As explained, it will be possible for someone to implement it using AdmissionChecks, but I don't think we should support it in core Kueue. I would accept a controller in the cmd/experimental package though.

The `cmd/experimental` sounds much more reasonable. SGTM

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-03-26T18:17:33Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-04-25T19:14:44Z

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

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-04-26T06:46:52Z

/remove-lifecycle rotten
Still valid I think

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-07-25T07:33:33Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-08-24T08:15:32Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-09-23T09:09:23Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-09-23T09:09:29Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/696#issuecomment-2367632889):

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

### Comment by [@yuvipanda](https://github.com/yuvipanda) — 2024-10-25T20:40:52Z

This would still be very helpful for multitenant scenarios, where there are multiple users of interactive computing on the same cluster and need access to individual queues.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-01T17:24:14Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-01T17:24:19Z

@kannon92: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/696#issuecomment-2845308996):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-31T18:14:00Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-31T18:14:06Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/696#issuecomment-2925528669):

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
