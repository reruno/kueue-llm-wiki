# Issue #7539: Add Prometheus metrics for Cohort to report resource usage, quota, workload counts

**Summary**: Add Prometheus metrics for Cohort to report resource usage, quota, workload counts

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7539

**Last updated**: 2026-03-30T09:39:27Z

---

## Metadata

- **State**: open
- **Author**: [@varunsyal](https://github.com/varunsyal)
- **Created**: 2025-11-05T09:14:56Z
- **Updated**: 2026-03-30T09:39:27Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-soon`
- **Assignees**: [@mszadkow](https://github.com/mszadkow), [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 26

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Add metrics for cohort similar to clusterqueue:
- kueue_cohort_resource_usage (similar to kueue_cluster_queue_resource_usage)
- kueue_cohort_resource_reservation (similar to kueue_cluster_queue_resource_usage)
- kueue_cohort_nominal_quota (similar to kueue_cluster_queue_nominal_quota)
- kueue_cohort_borrowing_limit (similar to kueue_cluster_queue_borrowing_limit)
- kueue_cohort_admitted_workloads_total (similar to kueue_admitted_workloads_total with clusterqueue label)
- kueue_cohort_admitted_active_workloads (similar to kueue_admitted_active_workloads with clusterqueue label)

**Why is this needed**:
This is needed to report usage, quota and workload counts at the cohort level and not just at the clusterqueue level.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-05T09:17:37Z

cc @mwysokin @amy

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:37:10Z

/priority important-longterm

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-14T16:06:19Z

/priority important-soon
Since we have a user interested in that

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-14T16:09:14Z

/remove-priority important-longterm

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-15T10:27:07Z

@varunsyal the existing metrics, like `cluster_queue_resource_usage` already have a label for "cohort". So IIUC the intention for this proposal is to have the usage aggregated for deeper cohort hierarchies, right?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-15T11:32:56Z

> [@varunsyal](https://github.com/varunsyal) the existing metrics, like `cluster_queue_resource_usage` already have a label for "cohort". So IIUC the intention for this proposal is to have the usage aggregated for deeper cohort hierarchies, right?

As another usecase (problem), we want to track how many Cohort resources (nominalQuota) are consumed.
Currently, we don't have a Cohort resource-specific usage because nominalQuotas defined in the Cohort resource are shared resources for ClusterQueue. Thus, there is no way to determine how many Cohort-defined nominalQuota consumed in child ClusterQueues.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-29T17:03:28Z

> As another usecase (problem), we want to track how many Cohort resources (nominalQuota) are consumed.

For sure, I think this could be answered with `kueue_cohort_resource_usage` which will aggregate the usage for the subtree.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-29T17:12:00Z

/assign @mszadkow 
as we already synced on slack

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-10T12:08:26Z

I think one open question what is the source of the metrics for the aggregated usage: in-memory state of cohort status?

Probably it could be cohort status, but IIUC this information is currently not there. So, to decouple the work we may serve it from the in-memory state (I think). This will allow us more flexibility to for example split by priorty. This refactoring is currently complicating the metrics for ClusterQueue: https://github.com/kubernetes-sigs/kueue/issues/8249.

So, I'm leaning to serve them straight from memory, but let me confirm with @gabesaba

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-02-26T14:55:41Z

In-memory makes sense to me. i wonder what metric we should expose for usage/quota though.. I'd say for sure 1, and i'm on the fence about 2.

1. `SubtreeQuota` and `Usage` defined in node. Do we use this name `SubtreeQuota`? We need to make sure this is well documented as users could miss that this hides usage/quota constrained by lending limit
2. (Optionaly), we can also have quota/usage summed for the entire subtree, ignoring lending limit

For reference:
https://github.com/kubernetes-sigs/kueue/blob/966b88b1a2ceeac7585305573df047c2f6c93c42/pkg/cache/scheduler/resource_node.go#L28-L43

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-03-09T13:13:29Z

I propose adding the following gauge metrics, to expose Cohort hierarchy info in Prometheus. It follows the pattern of [kube_pod_info](https://github.com/kubernetes/kube-state-metrics/blob/2fe9e994ae32de90af10037ea7d093f804ea6431/docs/metrics/workload/pod-metrics.md) or [kube_node_info](https://github.com/kubernetes/kube-state-metrics/blob/2fe9e994ae32de90af10037ea7d093f804ea6431/docs/metrics/cluster/node-metrics.md) in `kube-state-metrics`:

`kueue_cohort_info`, with labels `cohort`, `parent_cohort`, `root_cohort`
`kueue_cluster_queue_info`, with labels `cluster_queue`,  `parent_cohort`, `root_cohort`

These would allow queries like the following (suppose we define this `kueue_cohort_subtree_quota` as well), to see which resource is depleted at various levels in a tree:

```promql
# Available capacity at every hierarchy level within a single tree
(kueue_cohort_subtree_quota - kueue_cohort_resource_usage)
  * on(cohort) group_left(parent_cohort, root_cohort)
kueue_cohort_info{root_cohort="root"}
```

Resulting in something like this (without flavors here, for simplicity):
```
  {cohort="root", parent_cohort="", resource="gpu"}   2 # nearly exhausted
  {cohort="inference",parent_cohort="root", resource="gpu"} 42 # plenty available (post reclamation)
  {cohort="research", parent_cohort="root", resource="gpu"} -40 # borrowing 40 GPUs
  {cohort="nlp", parent_cohort="research", resource="gpu"} -22 # borrowing 22 GPUs
  {cohort="vision", parent_cohort="research", resource="gpu"} -18 # borrowing 18 GPUs
```

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-09T13:52:53Z

Interesting idea @gabesaba , I'm +1 for the new metrics:  `kueue_cohort_info` and `kueue_cluster_queue_info`.
I think we already have PR for `kueue_cohort_subtree_quota` but it is called `kueue_cohort_nominal_quota`, merged as: https://github.com/kubernetes-sigs/kueue/pull/9132

Do you think we should rename the metrics? I think I like the new name better, because what we are measuring is not "nominal quota", but "aggregated nominal quota". We could call it "subtree quota" for short, wdyt?

cc @mszadkow

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-03-09T14:17:16Z

> Do you think we should rename the metrics? I think I like the new name better, because what we are measuring is not "nominal quota", but "aggregated nominal quota". We could call it "subtree quota" for short, wdyt?

Yes, I think it should be renamed, as `nominal` is at the very least ambiguous (since this can be different from nominal quota defined at Cohort level)

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-09T14:34:37Z

sgtm, but following this logic we should also probably rename `kueue_cohort_resource_usage` as `kueue_cohort_subtree_resource_usage`, to also avoid the same ambiguity, right? 

So probably also for all metrics in the Issue description - renaming `cohort` as `cohort_subtree`. This works ok in case of `kueue_cohort_subtree_borrowing_limit`, but it wouldn't probably work of with "cohort_aggregated".

### Comment by [@mszadkow](https://github.com/mszadkow) — 2026-03-12T11:00:15Z

General question, should this be guarded by the config option similar to `EnableClusterQueueResources` ?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-12T11:06:23Z

Which metrics are currently guarded by `EnableClusterQueueResources`  can you list them?

### Comment by [@mszadkow](https://github.com/mszadkow) — 2026-03-12T11:19:57Z

Those are affected metric:
```
ClusterQueueQuotas
ClusterQueueResourceReservations
ClusterQueueResourceUsage
ClusterQueueWeightedShare
```

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-12T11:28:16Z

I see, so what makes them on the list is the presence of the "resource" label? I guess we don't need to guard the cohort metrics by `EnableClusterQueueResources`. I think if needed we should probably have `EnableCohortResources`, but I'm not sure we have a signal this is needed. Is `EnableClusterQueueResources` enabled or disabled by default?

### Comment by [@mszadkow](https://github.com/mszadkow) — 2026-03-12T11:32:28Z

> I see, so what makes them on the list is the presence of the "resource" label? I guess we don't need to guard the cohort metrics by `EnableClusterQueueResources`. I think if needed we should probably have `EnableCohortResources`, but I'm not sure we have a signal this is needed. Is `EnableClusterQueueResources` enabled or disabled by default?

I think so too, I just wanted to clarify.
This flag is set to true in all of the configs and values in helm chart, so I even think it could be cleaned-up (as offtopic).

### Comment by [@ns-sundar](https://github.com/ns-sundar) — 2026-03-12T14:54:54Z

This discussion sounds good to me. 

For my info, why do we need a gate like EnableClusterQueueResources? What is the issue with enabling it by default? 
> This flag is set to true in all of the configs and values in helm chart, so I even think it could be cleaned-up (as offtopic).
I understand this part, b ut was there some rationale why it was introduced earlier?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-13T18:48:30Z

> This discussion sounds good to me.
> 
> For my info, why do we need a gate like EnableClusterQueueResources? What is the issue with enabling it by default?
> 
> > This flag is set to true in all of the configs and values in helm chart, so I even think it could be cleaned-up (as offtopic).
> > I understand this part, b ut was there some rationale why it was introduced earlier?

AFAIK, it is performance. Counting ClusterQueue / Cohort resources consumes additional time. In case of a very large cluster or a highly Job submission throughput environment, this might be a potential scheduling performance issue.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-13T18:52:08Z

@mszadkow @mimowo @gabesaba If we add this Cohort usage to Prometheus, can we also consider storing such usage in Cohort status as well? Or should we open another issue and handle that as out of scope in this issue?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-13T19:30:26Z

> AFAIK, it is performance. Counting ClusterQueue / Cohort resources consumes additional time. In case of a very large cluster or a highly Job submission throughput environment, this might be a potential scheduling performance issue.

Right, but I think this was mostly precautious measures rather than real observation as back then we didn't really support large clusters. Now we support large clusters and I haven't seen any user disabling `EnableClusterQueueResources`. Sure, maybe some super big deployments will need it, but I think we can solve the problem then. Also, there are typically fewer Cohorts than ClusterQueues instances.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-13T19:32:57Z

>  If we add this Cohort usage to Prometheus, can we also consider storing such usage in Cohort status as well? Or should we open another issue and handle that as out of scope in this issue?

I would keep it separate. Indeed we serve ClusterQueue metrics from status, but it does not need to be so. For some improvements this is actually constraining. For example, there is no easy way to split by "priority_class" without refactoring the API for status, or moving to use in-memory cache. For example to track the PendingWorkloads per CLusterQueue per priorty_class. So, I think the coupling actually makes evolution of metrics harder. 

Additionally, we already decided to serve some metrics not from status, for example, guage for finished workloads. There is no reason to spend requests (QPS) updating ClusterQueue status for tracking the number of finished workloads. At the same time it is useful for users to know for example to configure the retention policy, so they were requesting the metric for the number of finished workloads.

Having said that, I totally agree with additional tracking in Cohort status, but I think we may decouple that.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-03-18T11:29:17Z

- [x] https://github.com/kubernetes-sigs/kueue/pull/9833
- [ ] kueue_cohort_resource_reservation (similar to kueue_cluster_queue_resource_usage)
- [x] https://github.com/kubernetes-sigs/kueue/pull/9132
- [ ] https://github.com/kubernetes-sigs/kueue/pull/9347
- [x] https://github.com/kubernetes-sigs/kueue/pull/9999
- [x] https://github.com/kubernetes-sigs/kueue/pull/10013
- [ ] https://github.com/kubernetes-sigs/kueue/pull/10004

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-03-18T11:29:53Z

/assign
