# Issue #5989: Add priority_class label to Kueue metrics

**Summary**: Add priority_class label to Kueue metrics

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5989

**Last updated**: 2025-12-11T15:30:45Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gbenhaim](https://github.com/gbenhaim)
- **Created**: 2025-07-16T06:11:15Z
- **Updated**: 2025-12-11T15:30:45Z
- **Closed**: 2025-09-26T19:04:19Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 21

## Description

**What would you like to be added**:

Add `workload_priority_class` label to workload-related metrics in Kueue to enable monitoring and analysis of workload performance by priority class.

The following existing metrics should be enhanced with the `workload_priority_class` label:

**ClusterQueue Status Metrics:**
- `kueue_admitted_workloads_total` (Counter)
- `kueue_evicted_workloads_total` (Counter)
- `kueue_evicted_workloads_once_total` (Counter)
- `kueue_quota_reserved_workloads_total` (Counter)
- `kueue_admission_wait_time_seconds` (Histogram)
- `kueue_quota_reserved_wait_time_seconds` (Histogram)
- `kueue_admission_checks_wait_time_seconds` (Histogram)

**LocalQueue Status Metrics (alpha):**
- `kueue_local_queue_admitted_workloads_total` (Counter)
- `kueue_local_queue_evicted_workloads_total` (Counter)
- `kueue_local_queue_quota_reserved_workloads_total` (Counter)
- `kueue_local_queue_admission_wait_time_seconds` (Histogram)
- `kueue_local_queue_quota_reserved_wait_time_seconds` (Histogram)
- `kueue_local_queue_admission_checks_wait_time_seconds` (Histogram)

**Optional Metrics (if waitForPodsReady is enabled):**
- `kueue_ready_wait_time_seconds` (Histogram)
- `kueue_admitted_until_ready_wait_time_seconds` (Histogram)
- `kueue_local_queue_ready_wait_time_seconds` (Histogram)
- `kueue_local_queue_admitted_until_ready_wait_time_seconds` (Histogram)

**Why is this needed**:

Priority classes are a fundamental concept in Kueue for workload scheduling and resource allocation. Currently, Kueue metrics don't provide visibility into how different priority classes are performing, making it difficult to:

1. **Monitor SLA compliance**: Different priority classes often have different SLA requirements (e.g., high-priority workloads should have lower admission wait times)

2. **Identify resource contention patterns**: Understanding which priority classes are experiencing evictions or long wait times helps with capacity planning and resource allocation

3. **Optimize scheduling policies**: Data-driven insights into priority class performance can inform adjustments to ClusterQueue configurations and resource quotas

4. **Troubleshoot performance issues**: When workloads are experiencing delays, being able to filter metrics by priority class helps identify whether the issue affects all workloads or specific priority tiers

5. **Implement proper alerting**: Operations teams need to set up different alert thresholds for different priority classes (e.g., alert immediately if high-priority workloads wait >1 minute, but only alert if low-priority workloads wait >10 minutes)

This enhancement aligns with Kueue's existing support for WorkloadPriorityClass and would provide the observability needed for production workload management.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-16T08:24:37Z

+1, I can very well understand that motivation, and I prefer that over a new set of metrics adding just this label.  Actually, we may also revisit if we want a separate set of metrics for LocalQueues, maybe there could be just a new optional "local_queue" label.

Since different users have different requirement for the set of labels I think this would be a good option to make it configurable. For example, we could have API configuration under [ControllerMetrics](https://github.com/kubernetes-sigs/kueue/blob/f4a78e032c0d116860d7dff15d445952a65e6904/apis/config/v1beta1/configuration_types.go#L169C6-L180) options like `IncludeWorkloadPriority` or `IncludeLocalQueue`. 

I prefer to keep it out-of-scope changes to the [LocalQueue metrics](https://github.com/kubernetes-sigs/kueue/issues/1833) design, but use it as another example demonstrating that a more customizable approach to metrics might be prefer.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-16T08:28:50Z

wdyt @tenzen-y @gabesaba @KPostOffice @kannon92

### Comment by [@kannon92](https://github.com/kannon92) — 2025-07-16T19:49:22Z

Makes sense to me!

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-23T06:46:20Z

I have another use-case, which might be an issue on its own, but seems like a good case for the approach described in https://github.com/kubernetes-sigs/kueue/issues/5989#issuecomment-3077519391, to have a new label "rootCohort". 

It is useful for users to aggregate metrics within cohort this way.

### Comment by [@gbenhaim](https://github.com/gbenhaim) — 2025-08-22T12:55:58Z

> +1, I can very well understand that motivation, and I prefer that over a new set of metrics adding just this label. Actually, we may also revisit if we want a separate set of metrics for LocalQueues, maybe there could be just a new optional "local_queue" label.
> 
> Since different users have different requirement for the set of labels I think this would be a good option to make it configurable. For example, we could have API configuration under [ControllerMetrics](https://github.com/kubernetes-sigs/kueue/blob/f4a78e032c0d116860d7dff15d445952a65e6904/apis/config/v1beta1/configuration_types.go#L169C6-L180) options like `IncludeWorkloadPriority` or `IncludeLocalQueue`.
> 
> I prefer to keep it out-of-scope changes to the [LocalQueue metrics](https://github.com/kubernetes-sigs/kueue/issues/1833) design, but use it as another example demonstrating that a more customizable approach to metrics might be prefer.

@mimowo I didn't fully understand the configuration you suggested. Do you mean have a configuration option for the inclusion of the priority_class label in the metrics? If so why it should be configurable? I'm afraid it would make the code complex.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-09T14:31:08Z

> @mimowo I didn't fully understand the configuration you suggested. Do you mean have a configuration option for the inclusion of the priority_class label in the metrics? 

Yes, that was my idea, to have the metrics extensible by a configuration. Say "metrics.includeWorkloadPriority".

> If so why it should be configurable? 

I foresee more use-cases for the granular metrics, like reporting LocalQueue one of them.

At some point multiplying LocalQueue, workload priorities and other things may increase the cardinality of a metric beyond acceptable. 

>  I'm afraid it would make the code complex.

Yes, me too. OTOH we have some users using Kueue at large scale, so I'm cautious that increasing metric cardinality can backfire at some point. 

My assumption is that it would just be a check like `if cfg.metrics.IncludeWorkloadPriority {  add label }` - otherwise report "N/A". 

To keep things simple I'm also ok to have it behind a feature gate like "MetricsIncludeWorkloadPriority", and "MetricsIncludeLocalQueue".  Then we keep the feature gates for a couple of releases, and no one reports then we graduate. Then, we can have "negative" configuration if needed one day say. Wdyt?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-11T12:48:12Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-11T13:13:44Z

### ClusterQueue Status Metrics:
- [x] https://github.com/kubernetes-sigs/kueue/pull/6795
- [x] https://github.com/kubernetes-sigs/kueue/pull/6860
- [x] https://github.com/kubernetes-sigs/kueue/pull/6876
- [x] https://github.com/kubernetes-sigs/kueue/pull/6882
- [x] https://github.com/kubernetes-sigs/kueue/pull/6885
- [x] https://github.com/kubernetes-sigs/kueue/pull/6887
- [x] https://github.com/kubernetes-sigs/kueue/pull/6886
- [x] https://github.com/kubernetes-sigs/kueue/pull/6951

### LocalQueue Status Metrics (alpha):
- [x] https://github.com/kubernetes-sigs/kueue/pull/6845
- [x] https://github.com/kubernetes-sigs/kueue/pull/6898
- [x] https://github.com/kubernetes-sigs/kueue/pull/6897
- [x] https://github.com/kubernetes-sigs/kueue/pull/6899
- [x] https://github.com/kubernetes-sigs/kueue/pull/6900
- [x] https://github.com/kubernetes-sigs/kueue/pull/6902

### Optional Metrics (if waitForPodsReady is enabled):
- [x] https://github.com/kubernetes-sigs/kueue/pull/6944

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-11T17:07:18Z

I'm also wondering if you need specifically the workload_priority_class, or just the priority_class would be better. 

This is a subtle distinction, but some integrations, like MPIJob or KubeflowJobs can derive the effective priority_class from the PodTemplate: https://github.com/kubernetes-sigs/kueue/blob/16fca759336f241cdeecd0a0bde4f17903c2f39c/pkg/controller/jobframework/reconciler.go#L1254-L1270

see also: https://github.com/kubernetes-sigs/kueue/blob/16fca759336f241cdeecd0a0bde4f17903c2f39c/pkg/controller/jobs/mpijob/mpijob_controller.go#L183-L192

OTOH, these checks were introduced prior to WorkloadPriorityClass, and they are hacky. Maybe we should now promote the WorkloadPriorityClass only, so I'm ok either way. 

wdyt @gbenhaim @tenzen-y @gabesaba ?

### Comment by [@gbenhaim](https://github.com/gbenhaim) — 2025-09-12T04:53:45Z

@mimowo I agree. We should promote the workload_priority_class. For my use case (tetkon pipelines) I need the workload_priority_class.

I don't think kueue should report the priorit_class in its metrics since this can be set for pods outside the context of kueue. I would expect kube_state_metrics to report the priority_class for pods.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-12T06:00:06Z

sgtm

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-17T06:56:23Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-17T06:56:29Z

@mbobrovskyi: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5989#issuecomment-3301573094):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-22T14:34:17Z

cc @tenzen-y 
Linking the discussion with the question from Yuki under one of the PRs: https://github.com/kubernetes-sigs/kueue/pull/6944#discussion_r2368383130

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-23T09:47:21Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-23T09:47:27Z

@mbobrovskyi: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5989#issuecomment-3323194061):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-23T11:40:59Z

> cc [@tenzen-y](https://github.com/tenzen-y) Linking the discussion with the question from Yuki under one of the PRs: [#6944 (comment)](https://github.com/kubernetes-sigs/kueue/pull/6944#discussion_r2368383130)

As we discussed in the above comment, the Pod PriorityClass is still a center of our Kueue scheduling mechanism, and it is not tricky way. So, we decided to introduce `priority_class` label instead of `workload_priority_class` label.

After this issue, we might to introduce the `priority_class_source` separate from it to distinguish between WorkloadPriorityClass and Pod PriorityClass.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-23T11:41:13Z

/retitle Add priority_class label to Kueue metrics

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-25T10:54:05Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-25T10:54:11Z

@mbobrovskyi: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5989#issuecomment-3333390539):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mukund-murali](https://github.com/mukund-murali) — 2025-12-11T15:30:45Z

I see we now have priority_class in most Histogram and Counter metrics. It would be very useful to have `priority_class` splits for these gauge metrics as well:
```
kueue_pending_workloads
kueue_reserving_active_workloads
kueue_admitted_active_workloads
```

This helps understand priority-based demand and admissions over time. Combined with the eviction metrics, it also helps see what is driving them.

I understand there may be a high-cardinality risk for the local-queue versions, but I expect this shouldn’t be a problem for the cluster-level metrics. I’m happy to raise a PR if this sounds useful.
