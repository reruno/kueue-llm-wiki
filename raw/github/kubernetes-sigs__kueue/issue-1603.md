# Issue #1603: Support Kserve

**Summary**: Support Kserve

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1603

**Last updated**: 2025-11-07T07:42:09Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-01-17T18:08:45Z
- **Updated**: 2025-11-07T07:42:09Z
- **Closed**: 2025-11-07T07:42:08Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 37

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
I would like to support the serverless ML Inference tool, [Kserve](https://kserve.github.io/website/latest/).

**Why is this needed**:
In the hybrid workload (which means training jobs and inference servers and so on) cluster, users often want to manage all cluster capacities by the kueue's flavorQuotas. So, as the first step to support the inference server, supporting Kserve in kueue is nice to have.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.
We will probably implement `suspend` semantics on the Kserve side.
Additionally, we need to move #77 forward together to support the inference server's autoscaling semantics.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-17T18:12:11Z

I think I talked about this with @astefanutti 
Also cc @mwielgus @ahg-g

### Comment by [@ahg-g](https://github.com/ahg-g) — 2024-01-24T05:37:25Z

How do you envision that working? Can you list a couple of CUJs?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-03-06T02:43:12Z

Online inference service is somehow latency sensitive, scalability is highly required, reclaim/preempt the kserve managed services looks not right. I guess Kserve is not that good at offline inference, which in my mind maybe helpful. cc @terrytangyuan

### Comment by [@lizzzcai](https://github.com/lizzzcai) — 2024-03-06T03:16:16Z

I would like to see possible support for this as I am looking for a unified way of managing resources for both model training and serving and Kueue looks like it has this capability. In our case, both training and serving are running in the same cluster. And how it can integrate with the recent `MultiKueue` feature to schedule workload to clusters with available GPU (sometimes there is a shortage of GPU in certain regions). As KServe deployment has min and max replicas, it should be scheduled to cluster that can meet the max replicas.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-06T05:43:11Z

> How do you envision that working? Can you list a couple of CUJs?

I imagined that the similar approach as RayCluster.

So, I would like to add Suspend field to InferenceService resource.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-06T05:46:52Z

> Online inference service is somehow latency sensitive, scalability is highly required, reclaim/preempt the kserve managed services looks not right. I guess Kserve is not that good at offline inference, which in my mind maybe helpful. cc @terrytangyuan

@kerthcet I believe that lending limit would allow us to guarantee capacities for latency sensitive Workloads.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-06T05:48:36Z

> I would like to see possible support for this as I am looking for a unified way of managing resources for both model training and serving and Kueue looks like it has this capability. In our case, both training and serving are running in the same cluster. And how it can integrate with the recent MultiKueue feature to schedule workload to clusters with available GPU (sometimes there is a shortage of GPU in certain regions). As KServe deployment has min and max replicas, it should be scheduled to cluster that can meet the max replicas.

Yes, that's right. Actually, I also deploy Job and Inference Server into a single cluster.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-06T05:49:23Z

Let me try to design this integrations.

/assign

### Comment by [@terrytangyuan](https://github.com/terrytangyuan) — 2024-03-06T17:35:20Z

Thanks! Great to see this. Looking forward to your proposal. @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-06T18:04:43Z

> Thanks! Great to see this. Looking forward to your proposal. @tenzen-y

I will create a dedicated issue later in Kserve side as well.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-06-04T18:58:29Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-05T09:10:59Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-09-03T09:43:30Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-03T11:36:43Z

/remove-lifecycle stale

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-03T11:37:29Z

I do not have enough bandwidth.
So, feel free to take this if anyone is interested in this feature.

/unasign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-03T11:37:36Z

/unassign

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-09-03T15:16:43Z

FYI: we have similar requirements for serving projects but mostly for resource fungibility rather quota managements(although related as a whole).

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-03T17:52:43Z

> FYI: we have similar requirements for serving projects but mostly for resource fungibility rather quota managements(although related as a whole).

Yeah, I fully agree with you. Actually, we wanted to provide the resource fungibility in the mixed type workload clusters.
For example, I want to allocate the free resources to Jobs when a few serving requests come. After serving requests go spike, we want to preempt Jobs and allocate resources to Serving for auto scaling.

But, I found that we can fulfill this motivation by using Kueue Pod integration with a little bit of Knative tuning.
So, maybe before we start natively supporting, we may want to add documentations for the way.

I will try to add Documentation on how to perform Kserve ISVC with Kueue.

### Comment by [@terrytangyuan](https://github.com/terrytangyuan) — 2024-09-03T18:56:26Z

@tenzen-y It would be great if you could share some docs and examples on that!

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-03T19:13:16Z

> @tenzen-y It would be great if you could share some docs and examples on that!

Sure, I will share it in the Kueue documentation.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-12-02T19:21:16Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-12-13T20:01:28Z

/remove-lifecycle stale

### Comment by [@kannon92](https://github.com/kannon92) — 2025-01-22T14:57:57Z

> [@tenzen-y](https://github.com/tenzen-y) It would be great if you could share some docs and examples on that!

We are looking to add a section in the docs to show using pod integration with external frameworks.

https://github.com/kubernetes-sigs/kueue/pull/3898

is an example of using Pod Integration with TektonPipelines.

@varshaprasad96 has done some exploring on how to use kubeflow notebooks with the statefulset integration.

### Comment by [@varshaprasad96](https://github.com/varshaprasad96) — 2025-01-29T12:14:58Z

> @varshaprasad96 has done some exploring on how to use kubeflow notebooks with the statefulset integration.

I'm doing a few tests with the latest version of Kueue for NB integration. Will open an upstream PR to add docs soon.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-04-29T12:19:47Z

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

### Comment by [@varshaprasad96](https://github.com/varshaprasad96) — 2025-04-29T15:51:17Z

In case it helps - I had created this document (https://docs.google.com/document/d/1gJ-LbOG1FWVNLP-M5Wc9p5h2pNTagUzdw2hsII6BFDM/edit?tab=t.0) that goes through the process of using Kueue and integrating KServe through deployment integration. This was done on OpenShift cluster - but it is all open source and can be easily replicated on vanilla K8s too. 

If someone wants to use this doc, and convert it into Kueue docs, please feel free to make use of it :)

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-29T15:53:51Z

> In case it helps - I had created this document (https://docs.google.com/document/d/1gJ-LbOG1FWVNLP-M5Wc9p5h2pNTagUzdw2hsII6BFDM/edit?tab=t.0) that goes through the process of using Kueue and integrating KServe through deployment integration. This was done on OpenShift cluster - but it is all open source and can be easily replicated on vanilla K8s too. 
> 
> If someone wants to use this doc, and convert it into Kueue docs, please feel free to make use of it :) 

Thank you for sharing it. I have serverless mode documentation, internally. We might be able to collaborate to add Kserve support documentation in Kueue.

### Comment by [@doctorpangloss](https://github.com/doctorpangloss) — 2025-04-30T18:44:28Z

Is it already possible to achieve Kueue semantics within Kserve? I.e., to limit the resource usage of "slow" requests to prevent exhausting all resources, allowing "fast" requests to continue to be executed, even when they compete for the same resources? This seems to be the crux of the value prop.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-01T05:46:06Z

> Is it already possible to achieve Kueue semantics within Kserve? I.e., to limit the resource usage of "slow" requests to prevent exhausting all resources, allowing "fast" requests to continue to be executed, even when they compete for the same resources? This seems to be the crux of the value prop.

I might not be able to understand it. What do "slow" requests and "fast" requests mean? Do you indicate replacement like Revision update or auto scaling?

### Comment by [@doctorpangloss](https://github.com/doctorpangloss) — 2025-05-01T15:58:48Z

My goal is to **reduce average delay of "short" requests in exchange for longer delays of "long" requests** when there are limited resources to serve requests, a very common scenario for ML inferencing tasks and fixed GPU quotas. Maybe even the **most** common production issue.

This is a completely orthodox, subjective design choice in the service of user experience that absolutely everyone makes. Developers using Kserve for semi-interactive function calling where the consumer is a real human being, such as with chat and art generative AI tasks: 100% of them will desire this user experience. Why? Because some requests are so much faster than others, that making the longer duration requests wait a little longer is in relative terms a small part of their total execution time.

But if there is only one queue where both long duration and short duration requests are processed, and resources are constrained, over time, short duration requests will be delayed as long as long duration requests take to execute, which means in relative terms, "short" requests become dominating by waiting for queue space.

So there's a simple solution and it's done with Kueue: concurrency limits. I want two flavors (or whatever) and one of them is for concurrency-constrained long queues. I.e., long requests can only use a certain percentage of GPUs in the cluster.

### Example Scenario

Let's say I have two categories of API requests: one that takes duration ~ N(24s, 2s) to complete ("short") and another that takes duration ~ N(15m, 7m) to complete ("long"). Both require exclusive access to a "GPU" resource. I have 8 GPUs.

Suppose users make one or the other request uniformly randomly (i.e., long ~ Uniform[0,1] < 0.5). Short requests tend to arrive in batches of 1-8 (pick a discrete probability dist. with a mean of 4) and long requests tend to arrive in batches of 1 OR 4. The requests tend to arrive once every 15 seconds. 

Under this arrival process things are unstable. We'll say that requests only arrive for the first 30m, and then let's simulate things for 2h.

We're going to measure the average sojourn time (wait + processing time) of the two categories of requests under two scenarios: one is that there is a single FIFO queue for all GPUs, and another is that there are two queues:

 - Long requests are limited to using at most 4 GPUs at a time. If a long request would use a 5th+   - GPU, it will wait in this "Long queue" instead.
 - Short requests can use as many GPUs as needed. This is the "short queue"
 - When a GPU that could service a long request is freed, and there is both a long and a short request waiting to use it, use FIFO (oldest time of arrival) to decide which queue to pop from for the GPU.

### Simulation Results

These are the charts for the sojourn time:

![Image](https://github.com/user-attachments/assets/8b8ba8d8-96e0-40dd-8197-39c97c47dcfa)

![Image](https://github.com/user-attachments/assets/0df85f00-ae14-49ac-95f7-34f3fa0cc7ad)

| Scenario | Mean sojourn at 3 h (short) | Mean sojourn at 3 h (long) | What the curves mean |
|----------|----------------------------|----------------------------|------------------------|
| **Single FIFO queue (8 GPUs)** | **≈ 4 600 s ≈ 77 min** | **≈ 5 100 s ≈ 85 min** | Once arrivals stop (t = 30 min) backlog drains steadily, but both classes finish in roughly the same hour-plus window. |
| **Dual queue (long ≤ 4 GPUs)** | **≈ 55 s** | **≈ 5 300 s ≈ 89 min** | Short jobs stay almost interactive (< 1 min total time) because they never wait behind long ones; long jobs complete in about the same window as FIFO but without congesting the short path. |

So do you see how I added about 200s of processing time for "long" requests in exchange to only slow down "short" requests by 30s? This is a real world example. Everybody wants to do this in Kserve.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-01T19:37:27Z

Thank you for summarizing that. I can understand what you want to say.
I think we have 2 solutions, 1 is handling as a Kueue problem (Pod scheduling), 2 is handling as a traffic scheduling problem.

For the Pod scheduling problem,

I think 2 priorities might resolve your problem, which is priority-long and priority-short.
The long-isvc is queued with priority-long, and the short isvc is queued with priority-short which allows us to prioritize the short request by preemption.

If you are dispatching the training workloads into the same cluster, you might want to prepare dedicated cq for inference.

For the traffic scheduling problem,

I think you might introduce custom filter by envoy or introducing gateway-api-inference-extensions (GIE). However, current Kserve does not support GIE as you can see https://github.com/kserve/kserve/issues/4227
When you consider this problem as a traffic scheduling, both short and long traffic are accommodated by a single isvc, and a single cq.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-31T20:36:00Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-10T05:51:39Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-08T06:29:50Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-08T07:06:24Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-07T07:42:04Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-07T07:42:09Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1603#issuecomment-3501135223):

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
