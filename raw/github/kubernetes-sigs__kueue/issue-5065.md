# Issue #5065: Add resource flavor usage to exposed metrics to improve observability

**Summary**: Add resource flavor usage to exposed metrics to improve observability

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5065

**Last updated**: 2025-05-06T12:37:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mwysokin](https://github.com/mwysokin)
- **Created**: 2025-04-22T10:13:18Z
- **Updated**: 2025-05-06T12:37:35Z
- **Closed**: 2025-05-06T12:37:34Z
- **Labels**: `kind/feature`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 11

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

I'd like to request adding a new metric which would allow to track resource flavor usage in the system. Something similar to what Kueue has for Cluster Queues but in a form that's easily consumable by analytics and visualization tools such as grafana.

**Why is this needed**:

Adding this metrics will improve general observability and give a good overview of the state of the system especially at scale.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-04-22T10:14:37Z

This could be potentially but not necessarily tackled as part of the same work as https://github.com/kubernetes-sigs/kueue/issues/5064.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-22T10:49:35Z

This sounds like already exposed by the metrics: https://github.com/kubernetes-sigs/kueue/blob/3279d9c05817e465229fac6bdc64250c890ea7dd/pkg/metrics/metrics.go#L304-L318

EDIT: I believe grafana allows to aggregate the metrics by cluster_queue and cohort (sum over them).

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-05-02T08:52:02Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-05-02T08:52:30Z

Checking the Grafana approach that @mimowo suggested.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-02T18:32:17Z

@mszadkow could you check if @mimowo solutions works fine? If yes, we can close this one.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-05-05T07:19:45Z

Yes, that's what I am working on

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-05-05T12:26:41Z

IIUC I think this is possible.

Flavor X usage by cq:

![Image](https://github.com/user-attachments/assets/6e3aa13f-fe40-46d5-a56a-4b571bca6106)

Flavor X usage by cohort:

![Image](https://github.com/user-attachments/assets/27b1d1ff-7134-4839-b1e0-774bd7e60a7d)

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-05T12:39:29Z

iiuc the original description we would like to get the flavor usage aggregated across all cqs. Iiuc your functions aggregate over flavors to get aggregated results per CQ. I guess we would like to actually get a curve per flavor, and resource name.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-05-05T15:00:28Z

ptal
sum(kueue_cluster_queue_resource_reservation) by (flavor, resource)
![Image](https://github.com/user-attachments/assets/39a74f89-3dc8-45ae-918b-8382b888a2d7)

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-05T16:08:06Z

> sum(kueue_cluster_queue_resource_reservation) by (flavor, resource)

Exactly, this is what I had in mind - aggregating across CQs and cohorts is easy formula and grafana, and so I'm not convinced we need another dedicated metric. wdyt @mwysokin ?

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-05-06T12:37:34Z

I think that's exactly what I was looking for. Let's close the issue for now and if I come up with something that's not supported I'll either re-open or create a new issue. Thank you!
