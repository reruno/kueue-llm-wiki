# Issue #6938: [Fair Sharing] Surface more precise WeightedShare

**Summary**: [Fair Sharing] Surface more precise WeightedShare

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6938

**Last updated**: 2026-04-15T13:40:32Z

---

## Metadata

- **State**: open
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2025-09-22T09:53:06Z
- **Updated**: 2026-04-15T13:40:32Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 33

## Description

**What would you like to be added**:
After https://github.com/kubernetes-sigs/kueue/pull/6925, we internally differentiate between fractional [WeightedShares](https://github.com/kubernetes-sigs/kueue/blob/8c0c1a68bb232871177bb1c57cc1d8c380e6c5d7/apis/kueue/v1beta1/fairsharing_types.go#L55). We should surface this granularity to the user in status (and metrics?)

In this scope of this issue, we should also decide:
1) whether we change the scale of the number surfaced (e.g. scale the WeightedShare by 1,000 or 1,000,000)
2) whether we should surface a float

**Why is this needed**:

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-09-22T09:53:14Z

cc @amy

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-22T12:20:57Z

This will be considered as v1beta2 API.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-22T12:50:34Z

> whether we change the scale of the number surfaced (e.g. scale the WeightedShare by 1,000 or 1,000,000)
> whether we should surface a float

I'm ok with both approaches. Maybe (1.) does not need require v1beta2?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-22T13:25:13Z

> > whether we change the scale of the number surfaced (e.g. scale the WeightedShare by 1,000 or 1,000,000)
> > whether we should surface a float
> 
> I'm ok with both approaches. Maybe (1.) does not need require v1beta2?

I think so too

### Comment by [@amy](https://github.com/amy) — 2025-09-24T01:48:52Z

Yeah... if this needs CQ migration from CRD API upgrade, let's change the scale of the number.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-09-24T08:13:05Z

Changing the scale of the number could break users too (if they were consuming these numbers in alerting/dashboards for example). Perhaps we introduce a new field, with whichever option we think is best long term, and then rename this field to WeightedShare in v1beta2?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-24T08:32:17Z

 > Changing the scale of the number could break users too (if they were consuming these numbers in alerting/dashboards for example).

Yeah, but I don't think this type of change warrants v1beta2 generally. I think we could mitigate by a warning in the release notes, as we typically do with "ACTION REQUIRED" in similar cases.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-24T13:25:43Z

> > Changing the scale of the number could break users too (if they were consuming these numbers in alerting/dashboards for example).
> 
> Yeah, but I don't think this type of change warrants v1beta2 generally. I think we could mitigate by a warning in the release notes, as we typically do with "ACTION REQUIRED" in similar cases.

I'm ok with changing scale with/ ACTION REQUIRED since the change will not break CRD, which means the Kueue system will keep healthy, but their third-party tool might affect the problem as @gabesaba mentioned.

So, we have no commitment to guarantee third-party tools.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-24T13:28:00Z

> whether we should surface a float

However, I'm hesitant about introducing floating point to our API since that is obviously an anti-pattern. Could we use `resource.Quantity`?

https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#primitive-types

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-24T13:52:15Z

AFAIK, floating point have some problems. This is just one example: https://github.com/kubernetes-sigs/controller-tools/issues/245

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-24T14:19:32Z

> Could we use resource.Quantity?

This might be complication for API clients outside of golang, like in Python etc? I'm not saying this is a problem for now, but it also makes me sceptial about using float or resource.Quantity at the API level.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-24T14:27:07Z

> > Could we use resource.Quantity?
> 
> This might be complication for API clients outside of golang, like in Python etc? I'm not saying this is a problem for now, but it also makes me sceptial about using float or resource.Quantity at the API level.

I think so too. As much as possible, we should not use those.
If we really need floating representations, we should select resource.Quantity.

### Comment by [@amy](https://github.com/amy) — 2025-10-01T14:23:11Z

Given current efforts to upgrade Kueue to v1beta2 anyways.

Let's just make the CRD representation a float.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-01T14:29:50Z

As we discussed in this issue, the float should be avoided as much as possible, which is obviously not recommended, and API debt.
As an alternative, we can use `resource.Quantity` instead of flaot64.

### Comment by [@amy](https://github.com/amy) — 2025-10-01T15:21:24Z

Yeah my bad. I meant a more precise number on the CRD rather than the proposal to scale the number up by 1K / 1M. `resource.Quantity` LGTM too.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-01T16:11:39Z

> Yeah my bad. I meant a more precise number on the CRD rather than the proposal to scale the number up by 1K / 1M. `resource.Quantity` LGTM too.

No worries :)
Thank you for checking that 👍

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-06T19:30:15Z

cc @JoelSpeed @everettraven

### Comment by [@everettraven](https://github.com/everettraven) — 2025-10-07T12:32:34Z

At a high level, don't use floats because of round-tripping and the varying precision and representations across different languages and architectures.

I also don't know that `resource.Quantity` necessarily makes sense for a static value (i.e not consuming some amount of a compute-like resource).

I don't have much background context here, but reading https://github.com/kubernetes-sigs/kueue/blob/8c0c1a68bb232871177bb1c57cc1d8c380e6c5d7/apis/kueue/v1beta1/fairsharing_types.go#L48-L55 I'm also not sure I really understand what this calculation is for/does. That makes it a bit difficult for me to provide any tangible feedback as to what a reasonable type to use here is.

What is a "fractional" WeightedShare? Why do you need the additional precision here? Why is this information useful to an end user?

### Comment by [@JoelSpeed](https://github.com/JoelSpeed) — 2025-10-07T15:48:34Z

For some context on similar APIs, other "weights" I've seen in Kube APIs have generally been bounded as int32 with a value in the range 0-100 inclusive. 

I have similar questions to @everettraven  about what this feature is and how it works, and reading various docs [A](https://kueue.sigs.k8s.io/docs/reference/kueue.v1beta1/#kueue-x-k8s-io-v1beta1-FairSharing), [B](https://kueue.sigs.k8s.io/docs/concepts/admission_fair_sharing/), [C](https://kueue.sigs.k8s.io/docs/concepts/fair_sharing/), I haven't really worked out the exact use case for this API or how it works/how an end user is supposed to use this, so it's hard to advise on the shape of an API until we better understand the actual end user expected behaviour.

Can someone provide an example of a scenario where the current model (whatever that is) doesn't work and results in unpredictable behaviour that a user would like more predictability over?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-08T14:40:23Z

@JoelSpeed @everettraven thank you a lot for looking into this. Let me share the context.

Kueue allows setting quota at the level of ClusterQueues which may belong to a "Cohort" (see [here](https://kueue.sigs.k8s.io/docs/tasks/manage/administer_cluster_quotas/#multiple-clusterqueues-and-borrowing-cohorts).
Fair sharing allows to share the quota among multiple ClusterQueues within a cohort, and the "Weight" specifies priority of each ClusterQueue. 

Assume you have a shareable pool of 100GPUs (shared by multiple teams above the teams' nominal quotas). You may want to say "team A" can use twice more than "team B" (above their nominal quota). Then you can set ClusterQueueA weight as 2, and ClusterQueueB weight as 1.

For each ClusterQueue Kueue computes the [DRS](https://github.com/kubernetes-sigs/kueue/blob/1ea074de47d0f5c4a751cc8f62764bfbf117c3e0/pkg/cache/scheduler/fair_sharing.go#L41-L47) (DominantResourceShare value) which determines how much above the "NominalQuota" a ClusterQueue is.  For the correctness of the fair sharing it is essential that we have a precise value of DRS for each ClusterQueue. Otherwise "infinite" preemption loops are possible.

The "WeightedShare" in status exposes the DRS values for each CQ. Its role is informational to the admin to understand the state of the system wrt Fair sharing. 

The idea is to expose to the admins as precise data as is needed for decision making by "Fair Sharing" in Kueue. 

Let me know if you would like me to expand the explanation in some parts.

In my view, I wouldn't change the int, or use resource.Quantity as mentioned above. I don't think an admin would be comparing values at the 6th position. Also, the update to the ClusterQueue status might be delayed in time, vs the scheduling decision, so it will not be precise anyway, for other reasons (ClusterQueue status lagging behind the value of DRS in scheduling cache). The role of the field is to just provide "rough idea". IMO int plays this role great. I would prefer to revisit extending the range of the values used to 10^6 (point one in the issue description, if really needed).

### Comment by [@JoelSpeed](https://github.com/JoelSpeed) — 2025-10-08T16:50:42Z

> The idea is to expose to the admins as precise data as is needed for decision making by "Fair Sharing" in Kueue.

In the real world, what resolution do you expect to actually need on this weighted share for the system to be effective and prevent the infinite preemptions? Are there alternatives that can be used as a tie break in the case that (at a certain resolution) the weighted shares are equal?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-09T06:46:14Z

We have [prooven](https://kueue.sigs.k8s.io/docs/concepts/fair_sharing/) that having the precise DRS prevents the infinite preemption loops. I think the main assumption in the proof is that the `DRS_without_workload < DRS_with_workload`. This may not hold true for rounded DRS, say you have DRS with precision 1000, but workload size is 1GPU, while the quota in CQ is 10k GPU, then admitting the workload will not shift DRSs.

Maybe it is possible to ensure this condition using some tiebreaking, like `DRS=(rounded DRS, number of preemptions within CQ)` , but it becomes even trickier to reason about correctness, and trickier for an admin to reason about the decisions. Also, it may create "unfair" decisions when CQ with higher DRS is preempting CQ with lower (just slightly).

So, talking about practice, let's assume the Workload is small, say 1GPU, while the quota in a really huge cluster of the future we have 1mln GPU (10^6), then we can use scaling factor of the WeightedShare reported in status, so that  `DRS_without_workload < DRS_with_workload` holds true for an API observer. 
On top of that, as mentioned in the previous comment, the DRS (WeightedShare) exposed in CQ status is not reflecting the DRS used the at the moment of admission by Kueue due to the distributed nature of controllers. 

I think the idea (1.) is enough for all practical purposes.

### Comment by [@JoelSpeed](https://github.com/JoelSpeed) — 2025-10-10T13:07:52Z

> This may not hold true for rounded DRS

Computers are always rounded to some degree, that's why I was curious to what resolution does the current system work? Is it based on the precision of a 64 bit float?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-10T13:17:06Z

Ah, I see what you mean. Yes, indeed, we assume that the "precise" calculation of DRS, based on float64, precision is enough to say  `DRS(CQ with workload) > DRS(CQ without workload)`. So thus currently we have 2 functions on the DRS struct: 
- [PreciseWeightedShare](https://github.com/kubernetes-sigs/kueue/blob/63a568161e862f98a264b264faf7fabe2035bea1/pkg/cache/scheduler/fair_sharing.go#L65) for internal computations based on the state of the cache
- [roundedWeightedShare](https://github.com/kubernetes-sigs/kueue/blob/63a568161e862f98a264b264faf7fabe2035bea1/pkg/cache/scheduler/fair_sharing.go#L102) for API for admins to know the state of the system

Technically speaking we could even have more precise [DRS Compare](https://github.com/kubernetes-sigs/kueue/blob/63a568161e862f98a264b264faf7fabe2035bea1/pkg/cache/scheduler/fair_sharing.go#L81) if we didn't use division (to float64), but then we would need to multiply 3 int32 numbers, and so we would need to use math.Big.

### Comment by [@amy](https://github.com/amy) — 2025-10-11T00:32:27Z

Hm...

> On top of that, as mentioned in the previous comment, the DRS (WeightedShare) exposed in CQ status is not reflecting the DRS used the at the moment of admission by Kueue due to the distributed nature of controllers.

Yeah... and the DRS values don't matter unless they're contextualized with the values it's being compared against since they change so fast.

Okay. Happy to drop surfacing precise DRS values to the CRD. We can probably just focus on contextualizing the values within the tournament tree better in logs or metrics like you mentioned above.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-13T06:45:30Z

Indeed, so we have two sources which make the floats imprecise anyway:
1. delay due to distributed updates (vs cached value used for scheduling)
2. for tournament the values are only comparable if two CQs have the same parent

Addressing (2.) for metrics is a good idea. While k8s discourages using float in API, it seems perfectly ok in metrics, for example many usage metrics count float, see [here](https://github.com/kubernetes/kubernetes/blob/42ee6dafd55e411a258f6e5d947b1fb95f38a6b5/pkg/kubelet/metrics/collectors/resource_metrics.go#L193-L218). To contextualize them more we could have a label "parentCohort". So, this could be a new guage metric:

name: cluster_queue_weighted_share (guage)
labels:  cluster_queue, cohort, value (we may also include rounded_value to match the API)

I expect metrics propagate faster than API requests (as this is just a local memory update vs request to API server), so the latency for (1.) would also be smaller, making the values more precise.

> Okay. Happy to drop surfacing precise DRS values to the CRD. 

I'm totally ok to increase the precision by scaling DRS to 10^6. I think this will be precise for all practical purposes (assuming immediate propagation of requests) for long. 

EDIT: I open a dedicated issue to track adding the metrics: https://github.com/kubernetes-sigs/kueue/issues/7244

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-16T14:58:42Z

> Indeed, so we have two sources which make the floats imprecise anyway:
> 
> 1. delay due to distributed updates (vs cached value used for scheduling)
> 2. for tournament the values are only comparable if two CQs have the same parent
> 
> Addressing (2.) for metrics is a good idea. While k8s discourages using float in API, it seems perfectly ok in metrics, for example many usage metrics count float, see [here](https://github.com/kubernetes/kubernetes/blob/42ee6dafd55e411a258f6e5d947b1fb95f38a6b5/pkg/kubelet/metrics/collectors/resource_metrics.go#L193-L218). To contextualize them more we could have a label "parentCohort". So, this could be a new guage metric:
> 
> name: cluster_queue_weighted_share (guage) labels: cluster_queue, cohort, value (we may also include rounded_value to match the API)
> 
> I expect metrics propagate faster than API requests (as this is just a local memory update vs request to API server), so the latency for (1.) would also be smaller, making the values more precise.
> 
> > Okay. Happy to drop surfacing precise DRS values to the CRD.
> 
> I'm totally ok to increase the precision by scaling DRS to 10^6. I think this will be precise for all practical purposes (assuming immediate propagation of requests) for long.
> 
> EDIT: I open a dedicated issue to track adding the metrics: [#7244](https://github.com/kubernetes-sigs/kueue/issues/7244)

I totally agree with this. Thanks.

### Comment by [@pajakd](https://github.com/pajakd) — 2025-10-17T11:40:45Z

I see that we [already have](https://github.com/kubernetes-sigs/kueue/blob/bb2b22ff2e83246ab0d3b0f3f29fede4c5512ac2/pkg/metrics/metrics.go#L472-L483) a metric with name `cluster_queue_weighted_share` -- it holds the rounded values. Should we change the existing metric to hold the precise values or introduce a new one? 

I would lean towards changing the existing metric.

Do you see any use cases of having both of them @amy @mimowo ?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-17T11:43:43Z

When posting the comment I didn't check we already have the metric with the proposed name. I'm also leaning to change the existing one.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-15T12:23:44Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-15T12:40:10Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-15T13:36:50Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-15T13:40:29Z

/remove-lifecycle stale
