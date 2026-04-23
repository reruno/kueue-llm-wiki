# Issue #6480: Allow Pods to identify the workload which admitted them without the "kueue.x-k8s.io/workload" annotation

**Summary**: Allow Pods to identify the workload which admitted them without the "kueue.x-k8s.io/workload" annotation

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6480

**Last updated**: 2026-03-19T09:01:25Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-08-06T11:27:05Z
- **Updated**: 2026-03-19T09:01:25Z
- **Closed**: 2026-03-19T09:01:24Z
- **Labels**: `kind/feature`, `priority/important-soon`, `lifecycle/stale`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 19

## Description

**What would you like to be added**:

Currently we use the "kueue.x-k8s.io/workload" annotation introduced for TopologyUngater to identify the Workload which admitted the Pods. The workload is needed as it contains the TopologyAssignment.

I expect we could use the current indexer for Workloads, we just need to pass the Job GVK and Job name to the pods. So, I propose to have the two annotations instead:
- kueue.x-k8s.io/job-name (example MyJob)
- kueue.x-k8s.io/job-gvk (example batch/v1.Job)

By combining this information TopologyUngater can find the workload by using the current Workload indexing mechanism.

**Why is this needed**:

- as a prerequisite for TAS and ElasticJobs integration, because in ElasticJobs the workload may change during lifetime of the Job, whilst the current approach assumes the "workload" annotation remains not mutated for Pods.
- for ElasticJobs to follow the pattern of ungating in a dedicated controller, offloading the main Job reconciler.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-06T11:27:17Z

cc @tenzen-y @ichekrygin

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-08-06T15:54:32Z

> Currently we use the "kueue.x-k8s.io/workload" annotation introduced for TopologyUngater to identify the Workload which admitted the Pods.

To clarify, which object does the annotation apply to?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-06T16:04:29Z

It is set on the Jobs managed by Kueue in the PodTemplate on admission, as a result it lands on the Pods.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-08-06T16:10:51Z

>It is set on the Jobs managed by Kueue in the PodTemplate on admission, as a result it lands on the Pods.

Sorry if this is a naive question, just want to make sure I fully understand.

Are we saying that the `Job` object is annotated with workload information at the time of admission? If so, that doesn't seem quite right to me.

As I understand it, the `Job` is the *parent* of the `Workload`, and it's created (and admitted) before the corresponding `Workload` exists. That is, unless we're talking about a **MultiKueue** context, where the remote `Job` may be created *after* the workload has already been admitted, effectively reversing the usual order.

Just to clarify, are we specifically discussing the MultiKueue case here?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-06T16:37:14Z

> Are we saying that the Job object is annotated with workload information at the time of admission? If so, that doesn't seem quite right to me.

Yes, we have a generic mechanism in Kueue which modifies the Job on admission (suspend-> false, but also injects nodeSelectors, tolerations, schedulingGates, but also annotations, which is used in this context). 

> As I understand it, the Job is the parent of the Workload, and it's created (and admitted) before the corresponding Workload exists.

Job is created before Workload exists, but is admitted along with the workload. Technically it is workload that is admitted, Job just "follows".

> Just to clarify, are we specifically discussing the MultiKueue case here?

I didn't mean MultiKueue.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-08-06T17:33:20Z


I think I may be conflating two different meanings of "admission", specifically, Kubernetes Job admission during create/update, and Kueue workload admission.

> "Job is created before Workload exists, but is admitted along with the workload."

From a Kubernetes perspective, the Job is considered *admitted* when it is created by the API server. So it might be helpful to disambiguate what’s meant by "admitted along with the workload".

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-06T17:47:32Z

Ah yes, I meant Job admission a bit informally here, meaning the update to unsuspend the Job and inject various Kueue bits, following the admission of the associated Workload. 

Actually, we very rarely in the context Kueue think of admission as creation. Indeed the terminology is also used in core k8s too for object creation. afaik kubełet is using the term of admission for the process of accepting new Pod scheduling. Finally Workload admission could also mean by API server or Kueue. So by default admission to me means by Kueue. On top of that for Jobs it means that the related Workload is admitted.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-08-06T18:02:28Z

> So by default, admission to me means by Kueue.

Thank you for the clarification.

With that out of the way, let me ask the following:
Today, the `Job` is the *parent* object of the `Workload` (or multiple workloads, in the case of ElasticJobs). Kueue already uses the Job’s `controllerOwnerReference` to locate the corresponding workload(s). From what I understand, both the Job's pods and the Job's workload share the same *parent*, the Job itself.

Therefore, it should be possible to associate a workload with its pods by using said owner reference, without needing additional annotations. Do I have that correct?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-06T18:13:11Z

Not really, for many integrations there are multiple layers in between Pods and the Job that owns the Workload: JobSet, AppWrapper, LWS, RayCluster, probably more.

Sometimes the number of owners in the chain may be tricky for example for AppWrapper.

Thus to make the mechanism of ungating pods in TAG generic we relied on the annotation, but this is not compatible with WorkloadSlices.

Actually, this is also partly why I liked the WorkloadResize idea to maintain the 1:1 correspondence. Nowe we need to work carefully to relax it l for the features like TAS or MultiKueue, or use WorkloadResize. I'm trying to make sure it is not a blocker for TAS in case we decide to support many workloads per Job, but this is a conceptaul change.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-06T18:25:00Z

Maybe instead of the proposal as in the issue we can just simply walk up the chain as we already have a helper and index the result, this should work too. I will think it more.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-08-06T19:28:20Z

Perhaps, another alternative could be pushing down the functionality of "finding" or "operating" on workload pods to the Job interface implementation, with some generic helpers for common use cases (i.e., immediate parent, etc.)

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-09T17:09:30Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-08T18:04:31Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-10T09:57:40Z

/remove-lifecycle stale

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2025-12-17T09:36:38Z

/cc

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:23:42Z

/priority important-soon

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T08:44:21Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-19T09:01:18Z

/close
The problem is already solved with the workload-slice-name annotation

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-19T09:01:25Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6480#issuecomment-4088719954):

>/close
>The problem is already solved with the workload-slice-name annotation


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
