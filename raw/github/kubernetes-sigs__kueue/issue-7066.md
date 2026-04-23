# Issue #7066: Additional metadata label for Kueue metrics

**Summary**: Additional metadata label for Kueue metrics

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7066

**Last updated**: 2026-03-16T08:45:00Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@varunsyal](https://github.com/varunsyal)
- **Created**: 2025-09-29T22:11:31Z
- **Updated**: 2026-03-16T08:45:00Z
- **Closed**: 2026-03-13T15:51:37Z
- **Labels**: `kind/feature`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 17

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Add ability to add metadata based on Clusterqueue labels/annotations for prometheus metrics like: `kueue_cluster_queue_resource_usage`. These can be added for any `kueue_cluster_queue_*` or even extended to other metrics if useful.


**Why is this needed**:

It is useful to get custom metadata into the Clusterqueue metrics as labels which could make filtering easier for a variety of use cases. 

As an example, let us say I want to calculate sum of usage for clusterqueues aggregated over some custom label, example all clusterqueues by parentCohort, or clusterqueues belonging to one team/organization that is available as a label in Clusterqueue metadata.

**Completion requirements**:
`kueue_cluster_queue_*` metrics including `kueue_cluster_queue_resource_usage` have a label which could have values injected from clusterqueue metadata.

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-09-29T22:33:58Z

/cc

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-30T08:07:49Z

Let me check 2 things:

1. Do you assume propagate ClusterQueue labels to existing metrics like [`cluster_queue_resource_usage`](https://github.com/kubernetes-sigs/kueue/blob/a0289bc948ff1d26edf2247f3b3c159d68386636/pkg/metrics/metrics.go#L424-L430)?

2. Is the below requirement satisfied by adding parentName (for Cohort) and cohortName (for ClusterQueue) to existing metrics? Instead of propagating all Cohort / ClusterQueue labels, I'm wondering if we can propagate those Kueue-associated labels.

> clusterqueues by parentCohort, or clusterqueues belonging to one team/organization that is available as a label in Clusterqueue metadata.

### Comment by [@varunsyal](https://github.com/varunsyal) — 2025-10-01T07:06:54Z

> Do you assume propagate ClusterQueue labels to existing metrics like [cluster_queue_resource_usage](https://github.com/kubernetes-sigs/kueue/blob/a0289bc948ff1d26edf2247f3b3c159d68386636/pkg/metrics/metrics.go#L424-L430)?

I am not sure if it makes sense to add all ClusterQueue labels but if there is a way to add a limited number of labels eg. those with some special pre-defined prefixes, to the metrics. That could be useful. 

Only adding the cohort or parentName may not suffice, but could still be something that may be good to add.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-01T12:52:26Z

I'm wondering how generic we want to be here. Opening the API to all labels, or even prefixes is tricky and maybe not necessary. It is tricky because the metrics have in k8s a predefined and static set of labels, see example: https://github.com/kubernetes-sigs/kueue/blob/81113ca514a6b20dce3e0b3fecc6d6fe14b75109/pkg/metrics/metrics.go#L118

Sure, maybe we can hack this during Kueue startup time, but it is not "idiomatic" (I think).

So, I'm wondering if your @varunsyal use case could be covered by a dedicated label recognized by Kueue to categorized ClusterQueues, for example: `kueue.x-k8s.io/metrics-category-label`. Then the value could be "BestEffort", or "Guaranteed", and the value would go into the metrics as a value for the label: `category`.

This way we could easily extend the existing metrics.

### Comment by [@ecdatadog](https://github.com/ecdatadog) — 2025-11-28T10:43:12Z

I am also interested by this feature. To dig a bit more to https://github.com/kubernetes-sigs/kueue/issues/7066#issuecomment-3355024393, I was thinking to inject some labels/annotations presents in CQ/LQ/Cohort based on configuration at Kueue level (https://kueue.sigs.k8s.io/docs/reference/kueue-config.v1beta1/#ControllerMetrics) . Something like : 
```
 metrics:
   bindAddress: :8080
   enableClusterQueueResources: true
   customMetricTags:
      clusterQueue:
        - resourceTag: team
        - resourceTag: user
        - resourceTag: gpu_type
          overrideMetricTag: my_gpu_type
```
My usage is to do some further aggregation of usage per ClusterQueue bases on some tags that I inject.

### Comment by [@ecdatadog](https://github.com/ecdatadog) — 2025-12-08T14:00:44Z

@varunsyal, Thanks for opening the issue. I am also interested by this feature. In order to discuss a bit more, I choose to made a draft [PR](https://github.com/kubernetes-sigs/kueue/pull/8099) (the PR is clearly not production ready but can be a basis to discuss)  adds some configuration items to fetch some labels in the kueue objects (ClusterQueue currently) and adds them as labels to the prometheus metrics 

It would rely on a configuration on 
```
 metrics:
   bindAddress: :8080
   enableClusterQueueResources: true
   customMetricTags:
      clusterQueue:
        - resourceTag: team
        - resourceTag: user
        - resourceTag: gpu_type
          overrideMetricTag: my_gpu_type
```
Where the resourceTag is on k8s side and overrideMetricTag is on prometheus side. 
overrideMetricTag would be optional allow people to either shorten/transform k8s level for their observability stack

@mimowo, I would be interested by our opinion about my proposal to solve this issue

### Comment by [@yashnib](https://github.com/yashnib) — 2026-01-23T05:40:48Z

Hi! I noticed there’s a draft PR up for this from about a month ago.

Just checking whether this is still being worked on, or if help would be welcome. I’d be happy to pick it up or assist with pushing it forward.

### Comment by [@yashnib](https://github.com/yashnib) — 2026-02-03T04:04:56Z

@miwowo I’m leaning toward the single-label approach you suggested: add one fixed Prometheus label (e.g. category) to ClusterQueue metrics, whose value is read from a well-known ClusterQueue label such as kueue.x-k8s.io/metrics-category-label.

This keeps the metric label set static and avoids introducing a fully generic “export arbitrary labels” API. Cardinality would be managed via documentation, with the expectation that this label is used for a small, bounded set of values.

### Comment by [@varunsyal](https://github.com/varunsyal) — 2026-02-05T19:49:25Z

A single label may be too limited, and will need to be overloaded if we need to add more than one detail. Currently we need to join the metric with some other metrics to filter by multiple custom categories which makes the dashboard queries very slow.
I like @ecdatadog's idea or any similar approach, and maybe we can put some limits on the number of `resourceTags` that can be added.

### Comment by [@yashnib](https://github.com/yashnib) — 2026-02-06T00:50:41Z

I was looking at other projects' approach to this. Argo Workflows allows arbitrary user-defined metric labels with no hard limit and relies on documentation to avoid high cardinality; given Kueue’s always-on, high-volume metrics, I think a bounded approach (e.g. 2–3 configurable labels) strikes a safer balance while still covering common team/env/class use cases.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-06T10:11:47Z

Sure, I'm positive about the feature in principle, but we need to clarify the design in a KEP, because there are non-obvious design questions, and it inevitably extends the API surface. 

I'm rather cautious about the arbitrary tag names as proposed in the PR: https://github.com/kubernetes-sigs/kueue/pull/8099, because it may result in name conflicts or even breaking changes for users if Kueue starts to introduce natively some new labels like "team". Also:
- supporting custom labels will not be discoverable via our metrics documentation https://kueue.sigs.k8s.io/docs/reference/metrics/
- the metrics page is currently auto-generated from the tags. To avoid extra maintance on our side, then adjusting the generation scripts needs to be part of the solution, see https://github.com/kubernetes-sigs/kueue/blob/main/hack/internal/tools/metricsdoc/main.go
- sure some projects can do that, but I'm not aware of this practice in the core k8s, which is an indication to me that it is not a good practice to open the set of labels for runtime.

So, I'm trying to make sure first that the "static" approach with pre-defined, and documented metrics inside Kueue like `kueue.x-k8s.io/metrics-category-label` with the corresponding label `category`,could cover the use-cases people have.

Sure, single additional metrics label can be too constraining, so I would like to hear from interested parties how many is typically needed in practice. I also think we could have predefined labels like `kueue.x-k8s.io/metrics-category2-label` or `kueue.x-k8s.io/metrics-category3-label`. Not the prettiest, but it will work fine without opening up the set of labels for runtime.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-06T10:13:29Z

I would also love this topic to be discussed at the wg-batch.

Let me also cc other maintainers, @gabesaba and @tenzen-y if they have some other view.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-09T13:14:30Z

Actually, I synced with @varunsyal and apparently something like 4-5 extra catergories is needed. At this point, I think it is worth to re-consider the configurable extension similarly as @ecdatadog started in comment https://github.com/kubernetes-sigs/kueue/issues/7066#issuecomment-3627082197. To mitigate my concern about future collisions we could say that the custom label metrics always start with "custom_".

@ecdatadog are you willing to continue the draft PR, and also open some KEP PR for discussing the details?

### Comment by [@yashnib](https://github.com/yashnib) — 2026-02-09T17:51:32Z

Sounds good to me. I’d be happy to help with tests, or to review the KEP / PR changes if that’s useful.

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2026-02-10T12:18:15Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-16T11:16:00Z

@varunsyal @yashnib @ecdatadog would you like to give a review pass to the design proposal https://github.com/kubernetes-sigs/kueue/pull/9225?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-16T08:45:00Z

@varunsyal @yashnib as https://github.com/kubernetes-sigs/kueue/pull/9774 is merged the task is ready for testing. Would you like to give it a pass using the main branch? Alternatively we could prepare a release candidate.
