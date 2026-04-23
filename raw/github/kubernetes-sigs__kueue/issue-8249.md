# Issue #8249: Add priority class label to resource-usage and workload metrics

**Summary**: Add priority class label to resource-usage and workload metrics

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8249

**Last updated**: 2026-04-20T17:52:01Z

---

## Metadata

- **State**: open
- **Author**: [@dominikgrewe](https://github.com/dominikgrewe)
- **Created**: 2025-12-15T17:16:19Z
- **Updated**: 2026-04-20T17:52:01Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-soon`
- **Assignees**: _none_
- **Comments**: 13

## Description

**What would you like to be added**:

I would like have an additional label for some metrics that specifies the priority class. In particular I would like the following metrics to have the additional priority class label:

- kueue_local_queue_resource_reservation
- kueue_local_queue_resource_usage
- kueue_local_queue_pending_workloads
- kueue_cluster_queue_resource_reservation
- kueue_cluster_queue_resource_usage

**Why is this needed**:

This helps us understand how resources are used across priority classes. For example, when looking into fair sharing, we would like to understand how fairly resources are distributed within a priority class. Or when trying to understand how busy the queues are it's helpful to know what priorities pending and active workloads have.

**Completion requirements**:

The metrics listed above have an additional label indicating the priority class.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-15T17:21:30Z

Have you checked recent releases of Kueue?

We did have https://github.com/kubernetes-sigs/kueue/issues/5989 and I believe we addressed most of these asks.

### Comment by [@dominikgrewe](https://github.com/dominikgrewe) — 2025-12-15T17:26:28Z

Yes, the ask is very similar but none of the metrics above were included in #5989 from what I can see.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-15T17:42:34Z

cc @mbobrovskyi

### Comment by [@mukund-murali](https://github.com/mukund-murali) — 2025-12-18T15:41:27Z

For the reason described in the PR, adding `priority_class` to the below metrics would also be super helpful:
```
kueue_pending_workloads
kueue_reserving_active_workloads
kueue_admitted_active_workloads

kueue_local_queue_pending_workloads
kueue_local_queue_reserving_active_workloads
kueue_local_queue_admitted_active_workloads
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:35:53Z

/priority important-soon

### Comment by [@andrewseif](https://github.com/andrewseif) — 2025-12-27T17:40:37Z

I would like to work on this feature/task 😃

### Comment by [@andrewseif](https://github.com/andrewseif) — 2025-12-29T11:55:50Z

**LocalQueue Status Metrics:**

- [ ] #8426

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-29T15:23:59Z

This doesn’t look easy to implement. We are currently using the LocalQueue status as the source of metrics:

https://github.com/kubernetes-sigs/kueue/blob/1d5cae5e227e117dd331993f22b3d961afae6458/pkg/controller/core/localqueue_controller.go#L369-L380

We’ll probably need to make additional changes to implement this. We need to carefully consider the approach, as changes to the API are not easy.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-21T07:48:22Z

Hi folks @andrewseif @mbobrovskyi what is the status here? Can we make some progress with some of the metrics? It is not clear to me which are hard and which are easy.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-21T07:53:56Z

Actually, I would like to generalize the issue, and include the priority_class for all workload-related metrics.

Looking at https://github.com/kubernetes-sigs/kueue/blob/main/pkg/metrics/metrics.go we are missing on `admission_attempts_total` or `admission_attempt_duration_seconds`, but also many more.

### Comment by [@andrewseif](https://github.com/andrewseif) — 2026-01-22T08:52:18Z

As far as I understand we can add the priority_class for all these metrics, but as @mbobrovskyi showed, the function (e.g. recordLocalQueueUsageMetrics) calling the Report* functions contains aggregates of the LQ/CQ, not the priority_class  of the workloads themselves. 

I remember agreeing with @mbobrovskyi to put it on hold, since the change might be big, and we were not sure what direction to take.

This issue applies to all these metrics:

- kueue_local_queue_resource_reservation
- kueue_local_queue_resource_usage
- kueue_local_queue_pending_workloads
- kueue_cluster_queue_resource_reservation
- kueue_cluster_queue_resource_usage

### Comment by [@andrewseif](https://github.com/andrewseif) — 2026-01-22T08:55:53Z

For admission_attempts_total or admission_attempt_duration_seconds, I'll have to investigate as they were not in the initial issue.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-20T17:52:01Z

Re as we hit the complication of adding the priority_class to some of the metrics, see https://github.com/kubernetes-sigs/kueue/issues/8249#issuecomment-3670904854, due to required re-org of the structures to support quick computation of the metrics.

We recently hit similar performance issue for the pending_workloads_wait_seconds, see https://github.com/kubernetes-sigs/kueue/issues/10124, and I'm cosidering the use of async computation for some of the metrics in the thread https://github.com/kubernetes-sigs/kueue/pull/10323#discussion_r310887334, that would allow us to have routine running every 15s or so to update the metrics.
