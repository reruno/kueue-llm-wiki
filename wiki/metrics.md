# Metrics

**Summary**: The `kueue-controller-manager` binary exposes Prometheus metrics on `/metrics`. Metrics cover per-[[cluster-queue]] usage and reservation, [[workload]] admission/preemption counters, [[admission-check]] outcomes, and scheduling-loop latency. Labels include `cluster_queue`, `flavor`, `priority_class`, and recently `priority_class_source`.

**Sources**: `raw/github/kubernetes-sigs__kueue/`, pr-15288.md, pr-15026.md, pr-16208.md, raw/kueue/pkg/metrics/metrics.go, raw/kueue/site/content/en/docs/reference/metrics.md

**Last updated**: 2026-09-29

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

## Changes in v0.18.6 / v0.19.2 / v0.20

### New: workload recovery wait time

[[pr-14766]] (fixes [[issue-14636]]) adds two histograms measured only when `WaitForPodsReady` with `recoveryTimeout` is enabled:

| Metric | Scope |
|---|---|
| `kueue_workload_recovery_wait_time_seconds` | per ClusterQueue |
| `kueue_local_queue_workload_recovery_wait_time_seconds` | per LocalQueue |

Both measure from the Workload entering recovery (`PodsReady=False`, `Reason=WaitForRecovery`) until it becomes ready again (`PodsReady=True`, `Reason=Recovered`). Observations are clamped to `>= 0` ([[pr-14800]], fixes [[issue-14797]]).

### Readiness metrics are no longer emitted after a recovery

`kueue_ready_wait_time_seconds`, `kueue_admitted_until_ready_wait_time`, `kueue_local_queue_ready_wait_time_seconds` and `kueue_local_queue_admitted_until_ready_wait_time_seconds` were being emitted again when a Workload *recovered*, not only when it first became ready — which skewed every one of them toward longer waits. [[pr-14626]] (fixes #14623) records them only on the initial readiness transition; use the recovery histograms above for the recovery path.

### `kueue_pod_scheduling_gate_removal_seconds`

Two independent fixes to the same metric:

- **Negative observations are clamped to zero** ([[pr-14474]] / [[pr-14731]], fixes [[issue-14456]]). `pkg/util/pod.RecordPodSchedulingGateRemovalSeconds` computes `cl.Now().Sub(cond.LastTransitionTime.Time)`. `LastTransitionTime` is stamped by the **apiserver** while `Now()` reads the **controller's** clock, so skew, a leader transition, or a wall-clock adjustment can make the duration negative. A negative observation makes the classic histogram's `_sum` *decrease*, Prometheus reads the drop as a counter reset, and `rate()` over that series returns garbage. This matches the guard `ReportWorkloadEvictionLatency` already had. The timestamp-source comment was corrected in [[pr-14740]] / [[pr-14750]] ([[issue-14730]]).
- **`replica_role` label added** ([[pr-14488]] / [[pr-14530]], fixes [[issue-14457]]). It was the only metric in the health group without it, so leader / follower / standalone observations were indistinguishable. The `RoleTracker` is threaded through the shared recording helper and all three emit paths (Pod controller via a new `WithRoleTracker` PodOption; the TAS topology ungater and the elastic-job ungater already carried a tracker); `roletracker.GetRole` yields `standalone` when the tracker is nil. The label is placed **before** the configured ClusterQueue custom labels, matching every other role-labeled metric. **Adding a label changes series identity** — existing queries on this metric must be updated.

Related: the "Job controller with CustomMetricLabels" integration block widened the shared metric vectors and panicked later specs ([[issue-14744]], fixed by [[pr-14745]] / [[pr-14751]]).

### New in v0.20

- **`kueue_unadmitted_workloads`** (gauge; `cluster_queue`, `reason`, `underlying_cause`, `replica_role`) and **`kueue_local_queue_unadmitted_workloads`** (`name`, `namespace`, `cluster_queue`, `reason`, `underlying_cause`, ...): counts Workloads without quota reservation per tiered reason. Emitted only with `UnadmittedWorkloadsObservability` (Beta/on in v0.20). Unlike `kueue_pending_workloads` (`active`/`inadmissible`), it also counts Workloads that referenced a missing queue ([[unadmitted-workloads-observability]]).
- **`multikueue_workloads_evicted_total`** (counter; `cluster_queue`, `cluster`, `reason`, `replica_role`, pr-15288): remote Workload evictions on a worker cluster, next to `multikueue_workloads_dispatched_total`, `multikueue_workloads_admitted_total` and the `multikueue_cluster_status` gauge (one series per manager ClusterQueue referencing a worker, so use `max by (cluster)` not `sum` to count distinct workers). See [[multikueue]].
- **Preemption `reason` label value `ConfigurablePreemption`** on `kueue_preempted_workloads_total` and the eviction metrics when a `PreemptionConfig` rule selected the victim (Alpha, [[configurable-preemptions]]); eviction metrics that carry an `underlying_cause` label use the PreemptionConfig name.
- **`kueue_preemption_target_recomputations_total`** (label `result`) and **`kueue_admission_cycle_preemption_skips`** (gauge per ClusterQueue: Workloads that had candidates but were skipped because another ClusterQueue needed the same resources in the cycle) describe overlap handling in the scheduling cycle ([[scheduler-internals#Recompute an assignment when preemption targets overlap]]).
- **`kueue_pending_scheduling_hashes`** (gauge; `cluster_queue`, `status`): unique pending scheduling-equivalence hashes, reported only with `SchedulingEquivalenceHashing`.
- **`replica_role`** is a label on all of these; custom metric labels are appended to ClusterQueue and LocalQueue series.

### Exact quota amounts and `+Inf`

pr-15026 changed how large quota and usage are reported: an amount at or past `math.MaxInt64` is `+Inf` as before, but for CPU the boundary moved from `MaxInt64/1000` cores to `MaxInt64` milli (0.807 cores apart), and amounts between are now exact rather than saturated ([[cache-architecture#Quota amounts are exact past int64 (pr-15026)]]).

### Integer overflow and unlimited quota

Kueue metrics could silently report incorrect quota and usage for very large resource quantities because of `int64` overflow. Large values are now preserved, and an **unlimited quota is reported as `+Inf`** ([[pr-14050]], original #13585). See [[scheduler-internals#Quota arithmetic and integer-overflow safety]].

## Related pages

- [[cluster-queue]] — where per-CQ labels come from.
- [[performance-and-scale]] — interpreting scheduling-loop metrics.
- [[visibility-api]] — complementary view.
- [[dashboard]] — KueueViz, the UI-layer consumer of the same data.
- [[workload-priority]] — `priority_class*` labels.
- [[debugging-guide]] — which metrics to check when triaging stuck workloads.
