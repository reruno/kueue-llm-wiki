# Issue #3884: Support Kubeflow TrainJob (v2)

**Summary**: Support Kubeflow TrainJob (v2)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3884

**Last updated**: 2025-09-16T19:50:38Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-12-18T15:28:30Z
- **Updated**: 2025-09-16T19:50:38Z
- **Closed**: 2025-09-16T19:50:28Z
- **Labels**: `kind/feature`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 16

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
I would like to support the Kubeflow [TrainJob](https://github.com/kubeflow/training-operator/tree/69094e16309382d929606f8c5ce9a9d8c00308b1/docs/proposals/2170-kubeflow-training-v2), which is Kubeflow TrainingOperator v2.

The new TrainJob AP relies on the JobSet API, but we should not enqueue the entire TrainJob or JobSet since the TrainJob uses the JobSet `DependOn` feature, which has some Kueue collaboration problems, as we mentioned [there](https://github.com/andreyvelich/jobset/blob/ea622a6d6ba8cfd876a7d662da2e141c977ecddc/keps/672-serial-job-execution/README.md#risks-and-mitigations)

Hence, in the short term, the TrainJob queueing should rely on the Kueue batch/v1 Job integration to mitigate and avoid the problems once the TrainJob is submitted. This concept is similar to Deployment integration, which depends on the Pod integration. 

Additionally, we might be able to extend the JobSet integration so that the JobSet with dependsOn will be enqueued by batch/v1 Job integration to avoid the long-term unused computing resources lock.

**Why is this needed**:
Currently, we are supporting the Kubeflow v1 APIs, but the v1 APIs will be stopped support within the next year.
We will probably completely stop the v1 support in the next 2 or 3 Training Operator releases.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-12-18T15:29:06Z

cc: @andreyvelich @mimowo @kannon92

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-18T15:35:52Z

@mwielgus @mwysokin

### Comment by [@kannon92](https://github.com/kannon92) — 2024-12-19T16:59:28Z

> Hence, in the short term, the TrainJob queueing should rely on the Kueue batch/v1 Job integration to mitigate and avoid the problems once the TrainJob is submitted. This concept is similar to Deployment integration, which depends on the Pod integration.

TrainJob -> JobSet -> (Job A + JobB)

I think you'd want to explore integration with JobSet before you started with jobs.

What exactly is the end state of integration? Do we want DependsOn or are we fine with support via JobSet? 

If we want to support DependsOn I think Kubeflow community should focus on implementing that in JobSet. Whatever we add we will have to support. So "Short Term" features would end up being long term features as we can't really drop support once customers use it.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-12-21T00:37:50Z

> If we want to support DependsOn I think Kubeflow community should focus on implementing that in JobSet. Whatever we add we will have to support. So "Short Term" features would end up being long term features as we can't really drop support once customers use it.

I did not indicate that we aim to implement `DependsOn` in the Kubeflow repository, we will implement the `DependsOn` in the JobSet side, first.
The motivation for using batch/v1 Job Kueue integration is https://github.com/andreyvelich/jobset/blob/ea622a6d6ba8cfd876a7d662da2e141c977ecddc/keps/672-serial-job-execution/README.md#risks-and-mitigations.

Even if Kubeflow uses the JobSet `DependsOn`, we should implement the TrainJob integration as the Kueue batch/v1 Job depending integration in the 1st step since there is no way to enqueue the JobSet step by step.
In the long term, we need to consider how we can separately enqueue each ReplicatedJob as we mentioned in the JobSet `DependsOn` KEP.

After Kueue supports the separate admission Job, the TrainJob Kueue integration will be implemented as JobSet depending integration.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-21T00:59:07Z

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

### Comment by [@andreyvelich](https://github.com/andreyvelich) — 2025-03-21T11:49:29Z

/remove-lifecycle stale

### Comment by [@kannon92](https://github.com/kannon92) — 2025-06-03T13:34:57Z

@andreyvelich @tenzen-y is there any idea of timeline when this can be implemented?

I know of some people that are interested in using the finetuning functionality with Kueue so it would be worth prioritizing this effort if possible.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-04T05:38:18Z

> [@andreyvelich](https://github.com/andreyvelich) [@tenzen-y](https://github.com/tenzen-y) is there any idea of timeline when this can be implemented?
> 
> I know of some people that are interested in using the finetuning functionality with Kueue so it would be worth prioritizing this effort if possible.

Before we start natively supporting TrainJob in Kueue, we want to bump JobSet API version to Beta or GA to avoid multi API versions supporting.
Additionally, users can now enqueue TrainJob via Kueue JobSet integration, as Kueue supports limited integration.

@kannon92 Do you see any lack of Kueue features for TrainJob via JobSet Kueue integration?

### Comment by [@andreyvelich](https://github.com/andreyvelich) — 2025-06-04T17:34:22Z

>Additionally, users can now enqueue TrainJob via Kueue JobSet integration, as Kueue supports limited integration.

@tenzen-y Given that we have `suspend` and `managedBy` API on the TrainJob side, we still require integration with Kueue Job framework, isn't?
Also, TrainJob handles some custom orchestration of Kubernetes resources (e.g. MPI Plugin).

Additionally, TrainJob might introduce different state machine compare to JobSet, which needs to be integrated with Kueue and MultiKueue.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-09T11:17:32Z

> > Additionally, users can now enqueue TrainJob via Kueue JobSet integration, as Kueue supports limited integration.
> 
> [@tenzen-y](https://github.com/tenzen-y) Given that we have `suspend` and `managedBy` API on the TrainJob side, we still require integration with Kueue Job framework, isn't? Also, TrainJob handles some custom orchestration of Kubernetes resources (e.g. MPI Plugin).
> 
> Additionally, TrainJob might introduce different state machine compare to JobSet, which needs to be integrated with Kueue and MultiKueue.

Yes, we are still eager to natively support TrainJob in Kueue since the JobSet integration is not able to MPI TrainJob, as you said. However, before doing that, KF and JobSet community should mature the APIs.

### Comment by [@andreyvelich](https://github.com/andreyvelich) — 2025-06-09T13:20:01Z

Shall we search for contributors to support TrainJob within Kueue after we make the 2.0 release ?
Given that many customers will migrate from Training Operator V1 to V2, I feel like the integration with Kueue is a high priority.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-23T11:01:21Z

As we discussed with @tenzen-y, @andreyvelich, and @mimowo in KubeCon Tokyo, we decided to support TrainJob v1alpha1, which means we will just drop older API versions from Kueue once a more mature API like v1alpha2 / v1beta1 API.

Additionally, the better management of the `dependsOn` feature is out of scope for this initial TrainJob support. We should appropriately handle it in the future Kueue release.

### Comment by [@amy](https://github.com/amy) — 2025-08-10T03:04:04Z

/assign kaisoz

(Just correlating the issues. I see that @kaisoz has volunteered here: https://github.com/kubernetes-sigs/kueue/issues/5719#issuecomment-3035560865
And this issue is 0.14.0 release candidate.)

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-16T19:50:24Z

With https://github.com/kubernetes-sigs/kueue/pull/6597 merging, I think we can call this done.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-16T19:50:29Z

@kannon92: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3884#issuecomment-3300139379):

>With https://github.com/kubernetes-sigs/kueue/pull/6597 merging, I think we can call this done.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-16T19:50:38Z

Please feel free to reopen if you want to track the follows up here.
