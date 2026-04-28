# Metrics

**Summary**: The `kueue-controller-manager` binary exposes Prometheus metrics on `/metrics`. Metrics cover per-[[cluster-queue]] usage and reservation, [[workload]] admission/preemption counters, [[admission-check]] outcomes, and scheduling-loop latency. Labels include `cluster_queue`, `flavor`, `priority_class`, and recently `priority_class_source`.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

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
