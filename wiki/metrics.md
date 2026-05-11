# Metrics

**Summary**: The `kueue-controller-manager` binary exposes Prometheus metrics on `/metrics`. Metrics cover per-[[cluster-queue]] usage and reservation, [[workload]] admission/preemption counters, [[admission-check]] outcomes, and scheduling-loop latency. Labels include `cluster_queue`, `flavor`, `priority_class`, and recently `priority_class_source`.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-05-08

---

## Core families

- `kueue_pending_workloads` (gauge, per CQ) — head-of-queue and active pending counts.
- `kueue_reserving_active_workloads`, `kueue_admitted_active_workloads` — currently reserving/admitted.
- `kueue_admitted_workloads_total`, `kueue_evicted_workloads_total` — admissions and preemptions, labeled by reason (see [[preemption]]).
- `kueue_cluster_queue_nominal_quota`, `kueue_cluster_queue_borrowing_limit`, `kueue_cluster_queue_lending_limit`, `kueue_cluster_queue_resource_usage` — per-CQ quota shape.
- `kueue_cohort_*` — equivalent gauges at the [[cohort]] level.
- `kueue_admission_attempts_total`, `kueue_admission_attempt_duration_seconds` — scheduling loop instrumentation.

## Labels

Labels are expanded incrementally. Relevant issues:

- "Add priority_class label to Kueue metrics" ([[issue-5989]]).
- "Add priority_class_source label to Kueue metrics" ([[issue-7291]]).

The `priority_class_source` label distinguishes stock `PriorityClass` from `WorkloadPriorityClass` so dashboards can separate the two. See [[workload-priority]].

## Cohort metrics reliability

Cohort-level metrics have had flakes as the hierarchical-cohort accounting matured:

- "[Flaky] Cohorts follows reporting correct metrics" ([[issue-10195]]).
- "flaky test: Cohorts when creating, modifying and removing follows reporting correct metrics" ([[issue-10417]]).
- "Cohorts when creating, modifying and removing correctly handles cohort metrics when workload admitted with admission check" ([[issue-10057]]).

These are test flakes, not always reliability issues in production; still, dashboards that sum across cohort levels should be checked for double-counting under hierarchical setups.

### Cohort CPU unit fix (v0.16.7 / v0.17.2 / v0.18.0)

Until v0.16.6, `kueue_cohort_subtree_quota` and `kueue_cohort_subtree_resource_reservations` reported raw **milliCPU** values (e.g. `30000`) for CPU resources, while the equivalent ClusterQueue metrics correctly reported **CPU units** (e.g. `30.0`). The cohort variant did not call `resourceFloat()`. Dashboards that summed CQ + cohort metrics or compared them side-by-side would get wildly inconsistent numbers. [[pr-10747]] aligns the cohort path: `applyCohortMetricPoint` now applies the same conversion and the metric function signatures take `float64`. Fixes [[issue-10746]].

### Stale cohort metrics after subtree change

`kueue_cohort_subtree_admitted_workloads_total` and `kueue_cohort_subtree_admitted_active_workloads` could include results for an implicit root Cohort after a child Cohort or ClusterQueue was deleted. Fixed via #10080 (in v0.18.0 changelog). See also `SubtreeQuota` invalidation under [[fair-sharing]].

## v0.18.0 metric changes

- **`workload_eviction_latency_seconds`** — new histogram recording the time from when an eviction is started to when it is finalized (#10323). Useful as a SLO metric for preemption efficiency.
- **`evicted_workloads_once_total`** — the `detailed_reason` label was **renamed** to `underlying_cause` for consistency with other metrics (#10637). **Action required**: dashboards/alerts using `detailed_reason` must migrate to `underlying_cause`.

## What to alert on

Common alert patterns:

- Sustained pending count growth → saturated CQ.
- Admission attempt duration p99 spike → scheduler loop overload (see [[performance-and-scale]]).
- Eviction rate by reason — per-reason deltas indicate policy misconfiguration (e.g. too much reclaim-within-cohort implies lending limits are too aggressive).
- AdmissionCheck Ready time — high p99 signals ProvisioningRequest or MultiKueue backpressure.

## Related pages

- [[cluster-queue]] — where per-CQ labels come from.
- [[performance-and-scale]] — interpreting scheduling-loop metrics.
- [[visibility-api]] — complementary view.
- [[dashboard]] — KueueViz, the UI-layer consumer of the same data.
- [[workload-priority]] — `priority_class*` labels.
- [[debugging-guide]] — which metrics to check when triaging stuck workloads.
