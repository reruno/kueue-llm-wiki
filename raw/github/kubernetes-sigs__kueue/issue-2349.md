# Issue #2349: Provide a way to implement a MultiKueue support for the custom Jobs

**Summary**: Provide a way to implement a MultiKueue support for the custom Jobs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2349

**Last updated**: 2025-09-19T13:57:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-06-03T16:54:15Z
- **Updated**: 2025-09-19T13:57:29Z
- **Closed**: 2025-09-19T13:57:28Z
- **Labels**: `kind/feature`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 43

## Description

<!-- Please only use this template for submitting enhancement requests -->
This is blocked by 

- [x] #2331 
- [x] #2350.

**What would you like to be added**:
I would like to support the extension mechanism so that we can implement the MultiKueue controller for the custom / in-house Jobs. I'm thinking of exposing the `jobAdapter` interface and implementing a mechanism to add arbitrary objects to the `adapters` similar to the jobframework integration manager:

`adapters`: https://github.com/kubernetes-sigs/kueue/blob/e461fe0827786e5cd6f45ff6739ebeed9a700b05/pkg/controller/admissionchecks/multikueue/workload.go#L48-L51
`jobAdapters` interface: https://github.com/kubernetes-sigs/kueue/blob/e461fe0827786e5cd6f45ff6739ebeed9a700b05/pkg/controller/admissionchecks/multikueue/workload.go#L66-L81

`jobframework integration manager`: https://github.com/kubernetes-sigs/kueue/blob/e461fe0827786e5cd6f45ff6739ebeed9a700b05/pkg/controller/jobframework/integrationmanager.go

**Why is this needed**:
In many company, they have company specific CustomResources, and we should give a possibility to manage such CustomResources across multiple clusters.

**Completion requirements**:


This enhancement requires the following artifacts:

- [x] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-03T16:54:41Z

cc: @trasc @mimowo @alculquicondor

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-03T17:01:09Z

+1
Is this something you want to give a first try to?

We've had requests to support kubeflow TFJobs

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-03T17:36:32Z

> Is this something you want to give a first try to?

I will try this issue after I finish #2175.
So, feel free to assign this issue to anyone.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-06-03T18:03:54Z

We should design this to support external integrations as well.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-03T18:45:28Z

> We should design this to support external integrations as well.

Yes, we can do it. But I think starting things as a minimum required is better. So, I want to take the external integrations as a separate issue.

### Comment by [@trasc](https://github.com/trasc) — 2024-06-04T05:35:05Z

For other jobs with built-in support in kueue it is fairly easy to do.

For fully external implementation it might be a bit harder, the multikueue admission check controller is composed of 3 object controllers (reconcilers for workload, admissionchecks and multikueue clusters)  and some long lived clients with watchers connected to the worker clusters. It's likely that the MulikueueCluster API needs to be modified to ensure that one multikueue cluster is only managed by one admission check controller.

For now I wold suggest to do the builtin jobs support and create a follow-up  for the external usage.

### Comment by [@trasc](https://github.com/trasc) — 2024-06-04T05:35:28Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-04T05:38:52Z

> For other jobs with built-in support in kueue it is fairly easy to do.
> 
> For fully external implementation it might be a bit harder, the multikueue admission check controller is composed of 3 object controllers (reconcilers for workload, admissionchecks and multikueue clusters) and some long lived clients with watchers connected to the worker clusters. It's likely that the MulikueueCluster API needs to be modified to ensure that one multikueue cluster is only managed by one admission check controller.
> 
> For now I wold suggest to do the builtin jobs support and create a follow-up for the external usage.

@trasc This issue motivation is supporting in-house/external jobs. So, if you work only on built-in jobs like TFJob, could you open another issue?

### Comment by [@trasc](https://github.com/trasc) — 2024-06-04T05:55:15Z

> @trasc This issue motivation is supporting in-house/external jobs. So, if you work only on built-in jobs like TFJob, could you open another issue?

Done #2350

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-04T05:57:07Z

> > @trasc This issue motivation is supporting in-house/external jobs. So, if you work only on built-in jobs like TFJob, could you open another issue?
> 
> Done #2350

@trasc Thank you. I'm guessing that we can work on this after #2350 is done because we will implement a mechanism to support more bilt-in Jobs in #2350, right?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-04T06:56:20Z

I synced supporting MultiKueue for the custom Jobs with @trasc.
In conclusion, we need to have 2 phases to support it in the following:

1. Move JobAdapters to JobFramework, and then expose the interface to other Go packages.
2. Implement a mechanism to specify AdmissionCheck ControllerName for the MultiKueue via JobFramwork.

In #2350, @trasc tries the first phase, and then he will try the second phase in this issue.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-06-10T12:12:19Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-12T17:38:11Z

> Implement a mechanism to specify AdmissionCheck ControllerName for the MultiKueue via JobFramwork.

That sounds odd. External controllers shouldn't have to re-implement the admission check. They should only implement how to sync jobs.

If those two things are tightly coupled, they should be decoupled.

@trasc can you actually write a short description of the components involved in MultiKueue and put it in https://github.com/kubernetes-sigs/kueue/tree/main/keps/693-multikueue

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-13T20:27:22Z

@alculquicondor @trasc TBH, as an external contributor (non Googler), I'm feeling that the MultiKueue specifications is not clearing.
Because even though the current MultuKueue is significantly evolving different from the design phase, the KEP is too outdated (actually, we don't have the `MultiKueueConfig` resource in the implementations level): https://github.com/kubernetes-sigs/kueue/tree/main/keps/693-multikueue#design-details.

So, before we apply the something enhancements into the MultiKueue, shouldn't we update the KEP to align with the actual implementations and behavior?

After that, can we add new enhancements to the MultiKueue?

### Comment by [@trasc](https://github.com/trasc) — 2024-06-14T05:36:26Z

Hi @tenzen-y , indeed the KEP does not contain all the implementation details, but I don't think it should,  and I don't see any significant deviations from the design. 

To be specific  `MultiKueueConfig` is defined here: 
https://github.com/kubernetes-sigs/kueue/blob/8b217c67c6cfb2a588a90107a63d3cf19182b191/apis/kueue/v1alpha1/multikueue_types.go#L112-L118

and used:

https://github.com/search?q=repo%3Akubernetes-sigs%2Fkueue+%22MultiKueueConfig%22+language%3AGo&type=code

`<site>/docs/concepts/multikueue` and `<site>/docs/tasks/manage/setup_multikueue` are also providing additional information about MultiKueue.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-14T15:48:36Z

> To be specific MultiKueueConfig is defined here:

I meant the MultiKueueCluster.

> <site>/docs/concepts/multikueue and <site>/docs/tasks/manage/setup_multikueue are also providing additional information about MultiKueue.

That is user documentation, so I still think updating the MultiKueue proposal would be worth it since clarifying the internal mechanism would be worth it. Even if some maintainers step down from this project, this Kueue project continue to be the journey. Actually, I have some experience in the unclear internal specifications brought OSS projects bugs and challenging maintenance.

Additionally, the latest KEP (not outdated) allows us to clear the place where the rabbit hole is and could reduce the risks of generating traps by being reviewed by multiple contributors.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-14T16:40:08Z

Personally, I think this is a distinguished feature which justifies a dedicated KEP (even though I would be acceptive of MultiKueue KEP update). I would like to see the chosen approach outlined, and indicated alternatives, along with pros and cons. Additionally, the KEP process creates space for early feedback from users who are not code reviewers.

My ask is motivated by difficulty understanding design choices taken in the pending PRs (https://github.com/kubernetes-sigs/kueue/pull/2373 and https://github.com/kubernetes-sigs/kueue/pull/2405). Getting the decisions discussed and agreed early on could avoid the confusion, and potentially dropping a significant amount of code in case we decide to change the approach.

### Comment by [@trasc](https://github.com/trasc) — 2024-06-14T16:54:46Z

> I meant the MultiKueueCluster.

https://github.com/kubernetes-sigs/kueue/blob/8b217c67c6cfb2a588a90107a63d3cf19182b191/apis/kueue/v1alpha1/multikueue_types.go#L57-L85

### Comment by [@trasc](https://github.com/trasc) — 2024-06-14T16:58:37Z

> Additionally, the latest KEP (not outdated) allows us to clear the place where the rabbit hole is and could reduce the risks of generating traps by being reviewed by multiple contributors.

The KEP cannot cover all the implementation details, The details in all the KEPs are limited, take the provisioning admission check controller , a very similar component, there is no mentioning of it's internal components.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-17T19:00:08Z

I synced with @trasc offline.

We agreed that there are quite a few mini-components in MultiKueue that it is a bit hard to keep track of as an outsider. Traian will update the KEP with those design elements, spending about 1 paragraph for each mini-component.

I agree that most features don't require such level of detail, but the complexity in MultiKueue is a bit higher.

### Comment by [@trasc](https://github.com/trasc) — 2024-06-18T11:57:15Z

#2436 opened, but on hold pending the merge of #2373

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-18T21:50:13Z

#2373 looks like a simple refactoring overall to me. I'm ok merging it and have the documentation match those changes.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-20T06:26:43Z

> > Additionally, the latest KEP (not outdated) allows us to clear the place where the rabbit hole is and could reduce the risks of generating traps by being reviewed by multiple contributors.
> 
> The KEP cannot cover all the implementation details, The details in all the KEPs are limited, take the provisioning admission check controller , a very similar component, there is no mentioning of it's internal components.

Actually, I synced with @trasc regarding to MultiKueue previous KEP, In conclusion, I agree with the current proposal, basically.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-20T15:01:42Z

> Actually, I synced with @trasc regarding to MultiKueue previous KEP, In conclusion, I agree with the current proposal, basically.

I'm sorry in advance if I ask stupid questions, but I still have some difficulty understanding the approach which I see continues to be implemented in https://github.com/kubernetes-sigs/kueue/pull/2458. 

Specifically:
- is it going to be a single AdmissionCheck per Job? In that case how a user can configure a single ClusterQueue to run multiple types of built-in jobs?
- will the new AdmissionChecks also run the built-in jobs, or the admins are expected to configure different admission checks for custom and built-in jobs?
- do we really need the new zoo of MultiKueue Admission checks? 

Can we at least consider a design where we still have a single MultiKueue admission check, but the custom jobs adapters are registered to it. I think it will make life on OnCall easier to have a single MutliKueue admission check that can be quickly identified by its name rather than a zoo of AdmissionChecks. It would also make admin users life easier to have a global configuration for the MK AC plugins, rather than doing this per ClusterQueue.

### Comment by [@trasc](https://github.com/trasc) — 2024-06-20T15:04:15Z

We are preparing a KEP for that.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-20T15:35:54Z

Ok great!

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-28T13:59:14Z

> We are preparing a KEP for that.

That sounds great to me. I will review the submitted design soon.
Thank you.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-09-26T14:33:22Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-26T15:22:30Z

/remove-lifecycle stale

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-26T15:22:50Z

@mszadkow Is there any progressing on your KEP?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-26T15:38:39Z

We will probably postpone the KEP effort until after MK goes beta

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-26T15:44:27Z

> We will probably postpone the KEP effort until after MK goes beta

That makes sense. The KEP could move forward during the MK beta graduation if @mszadkow has time.
But, we can prioritize the MK beta beta graduation rather than this feature.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-12-25T16:15:56Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-12-28T19:45:18Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-28T20:14:15Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-04-27T20:57:45Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-28T00:35:20Z

/remove-lifecycle rotten

### Comment by [@pramodbindal](https://github.com/pramodbindal) — 2025-07-07T09:11:48Z

Hi,
We at RedHat are adding MultiKueue feature in Tekton Pipelines.

This feature will allow PipelineRuns to be distributed across cluster. But PipelineRun being external framework we are not able to admit PipelineRun jobs in MultiKueue.

```
status:
  admission:
    clusterQueue: cluster-queue
    podSetAssignments:
    - count: 1
      flavors:
        tekton.dev/pipelineruns: default-flavor
      name: pod-set-1
      resourceUsage:
        tekton.dev/pipelineruns: "1"
  admissionChecks:
  - lastTransitionTime: "2025-07-04T13:44:14Z"
    message: No multikueue adapter found for owner kind "tekton.dev/v1, Kind=PipelineRun"
    name: sample-multikueue
    state: Rejected
```

Please let me know the process I need to follow to be able to admit my PipelineRun Workloads to MultiKueue.

> _FYI: I am able to admit PipelineRun workloads to single cluster setup._

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-08T15:14:08Z

IIRC, this is pending at https://github.com/kubernetes-sigs/kueue/pull/2458 due to deprioritization.
However, I think this is still a valid feature request.

/remove-lifecycle rotten

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-08T07:27:37Z

FYI we have decided to go with the design merged in: https://github.com/kubernetes-sigs/kueue/pull/5981

~cc @Khurram~

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-08T07:28:02Z

@khrm

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-19T13:57:23Z

With https://github.com/kubernetes-sigs/kueue/pull/6760, I think we can mark this as done.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-19T13:57:29Z

@kannon92: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2349#issuecomment-3312309161):

>With https://github.com/kubernetes-sigs/kueue/pull/6760, I think we can mark this as done.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
