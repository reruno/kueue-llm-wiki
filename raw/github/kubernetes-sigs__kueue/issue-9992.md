# Issue #9992: Allow TAS to ignore pods that have lower priority than workload trying to be scheduled

**Summary**: Allow TAS to ignore pods that have lower priority than workload trying to be scheduled

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9992

**Last updated**: 2026-05-01T22:25:54Z

---

## Metadata

- **State**: open
- **Author**: [@SeungjinYang](https://github.com/SeungjinYang)
- **Created**: 2026-03-19T00:48:47Z
- **Updated**: 2026-05-01T22:25:54Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: [@amy](https://github.com/amy)
- **Comments**: 16

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Currently, when TAS [calculates capacity](https://kueue.sigs.k8s.io/docs/concepts/topology_aware_scheduling/#capacity-calculation), the calculation "subtracts the usage coming from all other non-TAS Pods (owned mainly by DaemonSets, but also including static Pods, Deployments, etc.)"

It'd be nice if the usage of non-TAS pods were not considered if the k8s priority of these pods are lower than the k8s priority of the workload trying to be scheduled.

**Why is this needed**:

The specific motivation stems from Kueue's interaction with [Coreweave's HPC verification pods](https://docs.coreweave.com/platform/fleet-management/hpc-verification). From their documentation:

> You may briefly see a Job named hpc-verification-* in kubectl get pods -A while the test runs. The test uses a Kubernetes PriorityClass of cw-hpc-verification with a value of -1, meaning it always runs at a lower priority than customer workloads.

The idea here is that Coreweave may run static pods on the k8s cluster, but this pod is meant to be preempted when user pod needs the resource. However, I've observed this empirically does not work with TAS. What I believe is happening is some sort of a chicken and egg problem:
- For the HPC pod to be preempted, a pod requesting the resource being used by HPC pod needs to be scheduled.
- The pod (in this case a Kueue workload) is in SchedulingGated state. TAS blocks the pod's admission because does not see enough free resource on the node. TAS doesn't seem to be aware of the fact that the HPC pod would be preempted once the pod is scheduled, freeing up necessary resource for the pod to run.

Aside: I am using plain pods integration, if that matters.

Edit: I'm using [scenario 2 ](https://kueue.sigs.k8s.io/docs/concepts/workload_priority_class/#the-relationship-between-pods-priority-and-workloads-priority) of the priority configuration:
> A job specifies only WorkloadPriorityClass
WorkloadPriorityClass is used for the workload’s priority.
WorkloadPriorityClass is not used for pod’s priority.

and therefore any workload pod's priority is 0.

**Completion requirements**:

TAS should check the workload pod's priority, and ignore usage of already scheduled pods that have lower priority than the pod trying to be scheduled.

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-23T07:17:33Z

@SeungjinYang this sounds to me like a valid approach. I think this does not even require a new API, and we could introduce it as a bugfix for the integration with the core scheduler. We didn't do that in the original implementation as we were not aware of the usage pattern, most of the time TAS is responsible for accelerators while non-TAS pods are only DaemonSets / static Pods, but this looks like a legit use case for "fixing" the support.

On the technical level in nonTasUsageCache we already keep the information about the Pods' usage, so we could extend the information with their priority, and compare the priority with the priority in PodTemplate. I think the priority of the Workload is not relevant in this case. Certainly we will need a feature gate for safety.

As a workaround you may try to inject TAS annotation `kueue.x-k8s.io/podset-unconstrained-topology` to recognize the Coreweave's pods as TAS. 

cc @Huang-Wei @amy

### Comment by [@Huang-Wei](https://github.com/Huang-Wei) — 2026-03-23T20:49:06Z

> As a workaround you may try to inject TAS annotation kueue.x-k8s.io/podset-unconstrained-topology to recognize the Coreweave's pods as TAS.

I tried a similar approach to enroll those pods into Kueue TAS (I used `LocalQueueDefaulting` after talking to @tenzen-y offline), but it caused unknown ungating issue (maybe due to ungater's scalability) - we observed a lot of pods stay in SchedulingGated state.

For some context, CoreWeave's hcp-verfiication Job is cron-based (backed by argocd's [cron-workflow](https://argo-workflows.readthedocs.io/en/latest/cron-workflows/)) and hence will use plain Pod integration, and will spawn N `workload` simultaneously (`N` = number of nodes).

So to work around the issue, what I did internally is to build a custom Kueue image that ensure Kueue TAS simply bypass negative-priority Pods (configurable) - the code is at https://github.com/Huang-Wei/kueue/commit/bb27afed0383f3db21c406ff07fd0fe631e6eba6 (based off v0.16.2).

If needed, I can rework this commit as a PR onto `main`. Overall, I think Kueue TAS to have a knob to bypass certain pods is more efficient and sustainable.

### Comment by [@islewis](https://github.com/islewis) — 2026-04-28T03:11:30Z

+1 on this feature request, this would be incredibly nice to have

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-28T05:29:41Z

@Huang-Wei @islewis thank you for the proposal and bringing the issue to my attention - sorry I somehow missed the recent update / proposal notification.

I can totally see the need to fix this issue for non-TAS pods. I'm ok with the proposal, but it seems to me that the global priority threshold may not play well if the TAS workload is also of a low priority.

Let me put forward two alternatives I see for discussion:
1. add a custom annotation to the non-TAS pods like `kueue.x-k8s.io/tas-ignore`
2. when scheduling a TAS workload and accounting for non-TAS Pods, then only account for those which have >= priority than the preempting Pod

I think:
- (1.) would be very simple to implement too, but requires changing the pre-existing non-TAS workloads. 
- (2.) is generally better but requires more coding

Let me know if I'm missing something. If we agree that (2.) is the best option long term, but hard to implement (maybe not so much), then I'm ok with a short-term workaround like in the proposal or (1.) here, but would I would like to make sure we are on the same page with the pros & cons.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-28T05:29:55Z

cc @tenzen-y in case you have some opinion here

### Comment by [@islewis](https://github.com/islewis) — 2026-04-28T16:44:21Z

Thanks for the quick response @mimowo  I agree with your points.

I do not love (1). This shifts the scheduling responsibility from the workload in question to all other workloads. While this would be acceptable for my specific use case, this is somewhat messy, especially for anyone with more complicated multi-tenant clusters.

(2) is a cleaner separation of concerns, as well as allowing more nuanced behavior with multiple layers of prioritization. “only account for those which have >= priority than the preempting Pod” makes sense, but this would need to also be conditional on the workloads `preemptionPolicy`- without this a workload would run the risk of being admitted but then then failing to place once at kube-scheduler if it had `preemptionPolicy: Never` and could not evict compute that Kueue ignored

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-28T17:34:36Z

@islewis  - thanks for the summary. In particular (2.) is tricky as it requires non-trivial lookup into the Pod's preemptionPolicy - I missed that detail initially. 

So, I'm ok with the priority-based cutoff approach as this is very simple, much simpler than (2.).

One remaining question I have, do we need the configuration via ConfigMap, or a feature gate like `TASIgnoreNonTASPodsWithNegativePriority` would be enough for your use cases. 

The benefits of FG rather than ConfigMap:
1. we do not commit to maintaining the knob long term, as maybe we can implement (2.) eventually
2. we could cherrypick the FG, but we tend not to CP APIs

### Comment by [@islewis](https://github.com/islewis) — 2026-04-28T19:11:33Z

understood that the original (2) is more complicated than initially expected.

> or a feature gate like TASIgnoreNonTASPodsWithNegativePriority would be enough for your use cases.

More context about my setup given I different from OP's despite having similar needs. We run what we call "background compute", which are various non-kueue workloads on our cluster. These workloads are evictable, running at a low PC, and will scale up to use as much compute as possible in order for us to maximize our compute. All other higher priority workloads will scheduled on top of them, evicting background compute to find space.

We have a Kueue TAS workload that we've had to isolate from the rest of the cluster in order to block background compute from running there, or else it would not schedule. 

Unlike OP, a more generalizable solution that would allow for an ignoring anything below an arbitrary Priority level would be ideal as our PC values are non negative and non zero. I dont believe this is doable with a FG.

How much complexity would it be to make this config non-global, configured at the `ClusterQueue` level? Having multiple configs is a good workaround for not being able to check the incoming workloads `preemptionPolicy`- users could route workloads with different preemption expectations through different queues, each with its own threshold. This is not critical to my specific usecase but I could imagine this being helpful for others

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-28T19:26:51Z

> Unlike OP, a more generalizable solution that would allow for an ignoring anything below an arbitrary Priority level would be ideal as our PC values are non negative and non zero. I dont believe this is doable with a FG.

Got it, in that case, maybe let's have a quick KEP towards the approach as proposed in https://github.com/kubernetes-sigs/kueue/issues/9992#issuecomment-4113617458, wdyt?  It seems like the sweetspot between complexity of full scheduler preemptionPolicy awareness, and simplicity. It covers all the use cases known to date.

> How much complexity would it be to make this config non-global, configured at the ClusterQueue level? 

This is actually less trivial than it seems, because the TASCache is at the level of ResourceFlavor, rather than a particular ClusterQueue. So that there can be two CQs referencing the same ResourceFlavor, and thus they would have the shared tasCache - which already includes aggregated usage coming from Nodes in the flavor. 

So, we would need to somehow put another layer of cache which allows to use the CQ-context, because currently the non-TAS usage is already aggregated at the snapshot building time, and does not have the context of CQ here. I'm thinking about [this](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/cache/scheduler/tas_flavor.go#L69-L92) cache. Maybe other options are availble, but nothing obvious and simple to me.

Using the global threshold makes it much simpler because then we can filter out the Pods at the snaphshot building stage (in the context of Flavor).

EDIT" At this level of complication I would be leaning to implement the fully support of the kube-scheduler's preemptionPolicy.

### Comment by [@Huang-Wei](https://github.com/Huang-Wei) — 2026-04-28T21:37:40Z

> Let me put forward two alternatives I see for discussion:
> 
> 1. add a custom annotation to the non-TAS pods like `kueue.x-k8s.io/tas-ignore`
> 2. when scheduling a TAS workload and accounting for non-TAS Pods, then only account for those which have >= priority than the preempting Pod

(2) is definitely better b/c it's aware of the low-priority non-TAS pods, and hence can achieve optimal preemption strategy (least or none preemption disruption for non-TAS pods). However, I felt the same about its complexity and potential unknown side effects.

For (1), I have run it for a while in a prod cluster, it's straightforward and works well (a bit rigid though :))

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-29T04:32:18Z

Thank you for the input. So by (1.) do you mean still a custom commit to exclude a custom annotation? 

Thinking about this more, annotation seems morr flexible that a global priority threshold. 

Im also thinking that there is another no-code workaround which is to add the kueue.x-k8s.io/podset-topology-unconstrained annotation to the nonTas Pods. This will make Kueue skip them as NonTas pods, at the same time they will be skipped from TAS because they dont have a TAS workload.

If this works it would probably be my short term recommendation. For the long term seems we all agree (2.) is the way to go.

### Comment by [@islewis](https://github.com/islewis) — 2026-04-29T15:52:24Z

> add the kueue.x-k8s.io/podset-topology-unconstrained annotation to the nonTas Pods ... If this works it would probably be my short term recommendation. For the long term seems we all agree (2.) is the way to go.

This works well to get us unblocked, thank you both. I am going to close the linked KEP as it sounds like its no longer needed. Very much appreciate the willingness to bounce ideas around.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-29T16:13:11Z

> This works well to get us unblocked, thank you both. I am going to close the linked KEP as it sounds like its no longer needed. Very much appreciate the willingness to bounce ideas around.

Awesome that the workaround works for you, this avoids any work on API we would need to maintain otherwise, even if simple.

### Comment by [@Huang-Wei](https://github.com/Huang-Wei) — 2026-05-01T19:16:44Z

> So by (1.) do you mean still a custom commit to exclude a custom annotation?

Sorry for the late response. I meant my custom commit.

> Im also thinking that there is another no-code workaround which is to add the kueue.x-k8s.io/podset-topology-unconstrained annotation to the nonTas Pods.

Yup, I think it works - similar like the idea of "a custom annotation" in (1), but just reusing an existing annotation in another way :)

cc @jzhaojieh

### Comment by [@amy](https://github.com/amy) — 2026-05-01T21:33:32Z

Happy to pick option 2 up for 0.19: `when scheduling a TAS workload and accounting for non-TAS Pods, then only account for those which have >= priority than the preempting Pod`

if we decide that we want this longer term even with the workaround. Let me know @Huang-Wei @islewis

### Comment by [@amy](https://github.com/amy) — 2026-05-01T22:25:52Z

/assign
