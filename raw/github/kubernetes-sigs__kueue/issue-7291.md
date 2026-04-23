# Issue #7291: Add priority_class_source label to Kueue metrics

**Summary**: Add priority_class_source label to Kueue metrics

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7291

**Last updated**: 2026-04-14T11:21:52Z

---

## Metadata

- **State**: open
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-10-16T09:55:40Z
- **Updated**: 2026-04-14T11:21:52Z
- **Closed**: —
- **Labels**: `kind/feature`, `lifecycle/stale`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

As we discussed [here](https://github.com/kubernetes-sigs/kueue/issues/5989#issuecomment-3323638229) we should add priority_class_source label to workload-related metrics in Kueue.

**Why is this needed**:

To distinguish between WorkloadPriorityClass and Pod PriorityClass.

**Completion requirements**:

The following existing metrics should be enhanced with the priority_class_source label:

ClusterQueue Status Metrics:

- [ ] kueue_admitted_workloads_total (Counter)
- [ ] kueue_evicted_workloads_total (Counter)
- [ ] kueue_evicted_workloads_once_total (Counter)
- [ ] kueue_quota_reserved_workloads_total (Counter)
- [ ] kueue_admission_wait_time_seconds (Histogram)
- [ ] kueue_quota_reserved_wait_time_seconds (Histogram)
- [ ] kueue_admission_checks_wait_time_seconds (Histogram)

LocalQueue Status Metrics (alpha):

- [ ] kueue_local_queue_admitted_workloads_total (Counter)
- [ ] kueue_local_queue_evicted_workloads_total (Counter)
- [ ] kueue_local_queue_quota_reserved_workloads_total (Counter)
- [ ] kueue_local_queue_admission_wait_time_seconds (Histogram)
- [ ] kueue_local_queue_quota_reserved_wait_time_seconds (Histogram)
- [ ] kueue_local_queue_admission_checks_wait_time_seconds (Histogram)

Optional Metrics (if waitForPodsReady is enabled):

- [ ] kueue_ready_wait_time_seconds (Histogram)
- [ ] kueue_admitted_until_ready_wait_time_seconds (Histogram)
- [ ] kueue_local_queue_ready_wait_time_seconds (Histogram)
- [ ] kueue_local_queue_admitted_until_ready_wait_time_seconds (Histogram)

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-10-16T09:56:08Z

cc: @vladikkuzn @IrvingMg

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-16T10:05:25Z

Before doing I would like to hear from the community if we have use cases for that. It seems like the right think to do, but adding a new label may require extra aggregation for users, so let's see if we have valid use cases.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-14T10:09:44Z

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-14T10:30:04Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-14T11:21:49Z

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
