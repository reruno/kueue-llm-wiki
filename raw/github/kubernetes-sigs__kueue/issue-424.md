# Issue #424: Add roadmaps to README.md

**Summary**: Add roadmaps to README.md

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/424

**Last updated**: 2023-02-16T17:09:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2022-10-27T11:18:40Z
- **Updated**: 2023-02-16T17:09:41Z
- **Closed**: 2023-02-16T17:09:41Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 11

## Description

We should provide the roadmap for users who has some interests with this project and let them known where we're heading. 
Here's what I know:

1. Integration with cluster autoscaler.
2. More advanced scheduling strategies for better resource sharing.
3. Job preemption.
4. Integration with common custom workloads, Spark, Kubeflow, Tekton, etc..
5. Budget support.
6. Multi-cluster support.
7. Better observability.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-10-27T13:37:01Z

I think this is a good idea.

6. Not so sure about this one. While it is in our roadmap, it's probably too far for it to be meaningful to be in the page.
7. What else would you like to see, other than the metrics and statuses we already have? I don't think there is anything major missing.

cc @ahg-g

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-10-28T01:13:43Z

> Not so sure about this one. While it is in our roadmap, it's probably too far for it to be meaningful to be in the page.

Yes, it's a long term plan, multi-cloud and multi-cluster is common nowadays, I think people will show some interests in this feature. But I'm ok to get rid of it.

> Better observability

I hope we can have an overview about the capacity, resource utilization and information about resource sharing in kueue, it could be a dashboard. I think this is meaningful to manager.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-10-28T13:01:55Z

Yeah, most of the information is already available as status or metrics. So maybe it makes more sense to consolidate them in a UI, rather than adding more information in statuses.

### Comment by [@dmatch01](https://github.com/dmatch01) — 2022-10-31T13:02:28Z

> > Not so sure about this one. While it is in our roadmap, it's probably too far for it to be meaningful to be in the page.
> 
> Yes, it's a long term plan, multi-cloud and multi-cluster is common nowadays, I think people will show some interests in this feature. But I'm ok to get rid of it.

I would like to see multi-cluster on the roadmap as we have use cases for queuing across multiple clusters.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-10-31T13:52:23Z

I'm just saying that it's unrealistic that we will have a multi-cluster story in the next year, so it would be deceiving to say that it's in our roadmap.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-10-31T17:32:12Z

May be we can add a list of "aspirational goals" to cover major long term features like multi-cluster

### Comment by [@dmatch01](https://github.com/dmatch01) — 2022-11-01T14:56:48Z

> I'm just saying that it's unrealistic that we will have a multi-cluster story in the next year, so it would be deceiving to say that it's in our roadmap.

I see, although I do like the suggestion from @ahg-g to have a section for long term features.   

I have another question/comment: should support for elastic batch jobs be called out as an explicit work item in the road map list or is the thought that it will be added as part of support for item `4.` above?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-11-01T15:00:06Z

It can be separate. For example, the job controller supports changing parallelism, but we don't react to that in kueue.

### Comment by [@dmatch01](https://github.com/dmatch01) — 2022-11-01T15:03:44Z

> It can be separate. For example, the job controller supports changing parallelism, but we don't react to that in kueue.

Ok great.  Thanks!

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-12-21T18:32:18Z

FYI: Tomorrow at the WG batch meeting we will discuss the roadmap. Meeting notes https://docs.google.com/document/d/1XOeUN-K0aKmJJNq7H07r74n-mGgSFyiEDQ3ecwsGhec/edit#heading=h.xrdsqqbtp4xq

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-12-22T01:28:24Z

> FYI: Tomorrow at the WG batch meeting we will discuss the roadmap. Meeting notes https://docs.google.com/document/d/1XOeUN-K0aKmJJNq7H07r74n-mGgSFyiEDQ3ecwsGhec/edit#heading=h.xrdsqqbtp4xq

Thanks for reminding!
