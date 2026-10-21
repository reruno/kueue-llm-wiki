# Metrics

**Summary**: The `kueue-controller-manager` binary exposes Prometheus metrics on `/metrics`. Metrics cover per-[[cluster-queue]] usage and reservation, [[workload]] admission/preemption counters, [[admission-check]] outcomes, and scheduling-loop latency. Labels include `cluster_queue`, `flavor`, `priority_class`, `priority_class_source`, `replica_role`, and (Alpha, `CustomMetricLabels`) operator-defined `custom_*` labels sourced from ClusterQueues, LocalQueues, Cohorts or Workloads.

**Sources**: `raw/github/kubernetes-sigs__kueue/`, pr-15288.md, pr-15026.md, pr-16208.md, raw/kueue/pkg/metrics/metrics.go, raw/kueue/site/content/en/docs/reference/metrics.md, pr-13420.md, pr-13469.md, pr-13635.md, pr-16730.md, pr-16670.md, pr-16372.md, pr-16379.md, pr-16398.md, pr-16762.md, pr-16833.md, pr-16890.md, pr-16888.md, pr-16493.md, pr-16581.md, pr-17057.md, issue-16530.md, pr-16743.md, issue-16623.md, pr-15391.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, raw/kueue/CHANGELOG/CHANGELOG-0.19.md, raw/kueue/site/content/en/docs/tasks/manage/observability/configure_custom_metric_labels.md, raw/kueue/apis/config/v1beta2/configuration_types.go

**Last updated**: 2026-10-21

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

## New in v0.20: execution-time histograms (pr-13420)

`kueue_execution_time_seconds{cluster_queue, priority_class, replica_role, ...CQ custom labels}` and `kueue_local_queue_execution_time_seconds{name, namespace, priority_class, replica_role, ...}` are histograms observed once, when a Workload finishes (source: pr-13420.md, CHANGELOG-0.20.md v0.20.0).

- **Value** = `status.accumulatedPastExecutionTimeSeconds` + (`Finished.LastTransitionTime` − `Admitted.LastTransitionTime`), computed by `workload.TotalExecutionTime` and recorded from `WorkloadReconciler.reportFinishedWorkload` (source: raw/kueue/pkg/workload/workload.go). It therefore spans every admission, including readmissions after eviction — the same accumulator [[workload-max-execution-time]] uses.
- **Not observed** when the Workload finishes without `Admitted=True` (returns `nil`, review asked for `nil` rather than a `-1` sentinel) (source: pr-13420.md).
- The LocalQueue variant obeys the LocalQueue-metrics selector (`ShouldExposeLocalQueueMetricsForWorkload`).
- **Buckets**: `generateExponentialBuckets(16)` = `1, 2.5, 5, … 40960` s (about 11.4 h); longer runs land only in `+Inf`, so quantiles above ~11 h are not meaningful (source: raw/kueue/pkg/metrics/metrics.go).

## `MetricForWorkloadCreationLatency` is GA (main, v0.21 dev)

pr-16493 locks the gate on (`0.21 GA`, `LockToDefault`); `kueue_workload_creation_latency_seconds{job_kind, replica_role}` is registered and recorded without checking the gate. Recording is still limited to job objects with `metadata.generation <= 1`, so a Workload recreated for an already-edited job is not sampled (source: pr-16493.md, raw/kueue/pkg/features/kube_features.go). See [[feature-gates]].

## Custom metric labels (`CustomMetricLabels`, Alpha, off)

Configured under `metrics.customLabels` in the Configuration (source: configuration_types.go, configure_custom_metric_labels.md):

| Field | Rule |
|---|---|
| `name` | Prometheus suffix; label is `custom_<name>`; `[a-zA-Z][a-zA-Z0-9_]*`, unique |
| `sourceKind` | `ClusterQueue` (default), `LocalQueue`, `Cohort`, `Workload` |
| `sourceLabelKey` / `sourceAnnotationKey` | mutually exclusive; default `sourceLabelKey = name` |
| `trackedValues` | **required for `Workload`** (1-12 values); 0-16 for other kinds (empty = any value). Out-of-list values are reported as `kueue.x-k8s.io/_UNTRACKED_VALUE_` |
| limits | at most **2** Workload-sourced labels, **6** per other kind, **20** total; validated at startup (invalid config = manager does not start) |

A Workload-sourced value is read from the Workload; the job framework copies the configured key from the job onto the Workload it creates. Kueue's internal labels/annotations (`kueue.x-k8s.io/job-uid`, `multikueue-origin`, `workload-slice-name`, `priority-boost`, …) are never copied even if a custom label names them (v0.20.1 / v0.19.8, #16773/#16774); StatefulSet did not copy these sources at all until v0.20.1 / v0.19.8 (#16751/#16770) (source: CHANGELOG-0.20.md, CHANGELOG-0.19.md).

**Which metrics take Workload-sourced labels** (each a separate PR, all require the gate):

| Metric | Since |
|---|---|
| `kueue_admitted_active_workloads` (CQ) | earlier (the only one the user guide still lists — the doc is stale) |
| `kueue_pending_workloads` | v0.20.0 (pr-13469) |
| `kueue_local_queue_pending_workloads` | v0.20.0 (#14167) |
| `kueue_local_queue_admitted_active_workloads`, `kueue_local_queue_admitted_workloads_total`, `kueue_local_queue_admission_wait_time_seconds` | v0.20.0 (pr-13635) |
| `kueue_cohort_subtree_admitted_workloads_total` | main only, v0.21 dev (pr-16730) |

Implementation notes for contributors (source: pr-13469.md, pr-16670.md):

- `ClusterQueue.Pending(cl)` in `pkg/cache/queue` now returns two `metrics.LabelValsTracker`s (active, inadmissible) instead of two ints; without Workload labels it records one entry under `metrics.Empty()`. The inflight Workload counts as active.
- When a ClusterQueue is **stopped**, `reportCQPendingWorkloads` merges the active tracker into the inadmissible one — all pending Workloads of an inactive CQ are reported as `status="inadmissible"`.
- **Stale-series bug (fixed in v0.20.1, pr-16670 / #16871):** the old code deleted only label sets present in a tracker with a zero count. On stop the active tracker was replaced by an empty one, so the old `status="active"` series never got deleted; on resume the merge-only `inadmissible` series were never deleted. `sum(kueue_pending_workloads)` double-counted after a stop/resume. The fix takes the union of active and inadmissible label sets (trackers retain zero-count sets), then for each set and both statuses sets the series if positive or calls `DeleteLabelValues` otherwise — only the CQ's own series, no metric scan, no transient disappearance of valid series. `LabelValsTracker.PopZeroCounts` was removed; `Count` added. Not backported to 0.19 because Workload labels on pending metrics are 0.20+ only.
- Panic fixed in v0.20.0 (#14419, backported as pr-15391): `kueue_pod_scheduling_gate_removal_seconds` with a ClusterQueue-sourced custom label could crash the manager; the metric is now recorded with the CQ's custom labels (source: pr-15391.md).

## Pending-workload gauges: refresh on queue lifecycle events

The pending gauges are pushed from the queue manager, not computed at scrape time, so every event that changes what a queue counts must trigger a report:

- **ClusterQueue stop/resume** (pr-16833, v0.20.1 / v0.19.8): `UpdateClusterQueue` now refreshes pending-workload metrics after every successful CQ update, including updates that do not change readiness; it only *broadcasts* (wakes the scheduler) on an inactive→active transition. Before, stopping a CQ that moved no inadmissible Workloads published nothing until the next Workload update (issue-16825 flake) (source: pr-16833.md).
- **LocalQueue create / resume / internal move / stop / delete** (#15576, backported as pr-16890 to 0.20 and pr-16888 to 0.19; in v0.20.1 / v0.19.8): metrics are refreshed on each event, and the LocalQueue's custom labels are stored *before* the create handler reports, so Workloads observed before their LocalQueue are counted under the right labels (source: pr-16890.md, pr-16888.md).
- v0.20.0 also fixed `kueue_cluster_queue_resource_pending` being permanently inflated when a LocalQueue resync pushed a Workload already tracked as inadmissible (#13660), and stale LocalQueue admitted/reserving counts after the referenced ClusterQueue was deleted (#13708) (source: CHANGELOG-0.20.md).

Testing note: the requeuer is asynchronous with a 100 ms batch period in integration tests, so tests that hand-craft an inadmissible state race with it; such coverage moved to table-driven unit tests with the synchronous requeuer (pr-16372, closes issue-16559).

## Invalid `localQueueSelector` now fails startup (v0.20.0, ACTION REQUIRED)

`NewLocalQueueMetricsConfig` used to discard the selector-parse error and return `nil`, and `nil` means "no filtering", so with `metrics.localQueueMetrics.enable: true` an invalid `localQueueSelector` (e.g. `operator: InvalidOp`) silently exposed metrics for **every** LocalQueue — higher cardinality and a wider monitoring scope than intended. The error is now propagated and the manager refuses to start. Fix invalid selectors before upgrading (source: pr-16379.md; backported to release-0.19 as pr-16977 after v0.19.8). General rule: a failed parse must never be represented by the same value as "no restriction" (see [[security-code-patterns]]).

## Cohort metrics after hierarchy changes

- **`kueue_cohort_subtree_admitted_active_workloads`** (v0.20.0, v0.19.7, v0.18.11; pr-16398): a Cohort's `admittedWorkloadsCount` was maintained incrementally on Workload events but not rebuilt when the Cohort tree changed, so the gauge could go stale, zero or **negative** (e.g. reconciling a Cohort with an unchanged parent recreated its implicit root with a zero count; reparenting or deleting a Cohort with children did the same). Now the count is rebuilt from children together with the rest of the tree, and the gauge is re-reported for both the old and new trees *during the cache's tree rebuild* (old trees and implicit Cohorts may never be reconciled again). Semantics: the gauge follows the **current** subtree (moving `ch1` with 3 admitted under `root2` with 2 makes `root2` = 5), whereas `kueue_cohort_subtree_admitted_workloads_total` is a counter of admissions and is not moved. Deleting an explicit Cohort that still has children leaves it as an implicit Cohort, so its gauge is kept (its counter is cleared) (source: pr-16398.md).
- **ClusterQueue deletion** (pr-16762, main; backported to 0.20 as pr-16941, after v0.20.1): the CQ delete handler called `ClearCohortMetrics`, which computes subtree metrics as if the whole Cohort were removed, and nothing re-recorded them. A Cohort that still had other CQs or child Cohorts lost its `kueue_cohort_subtree_quota` and `kueue_cohort_subtree_resource_reservations` series (for a root Cohort until another member CQ reconciled). The delete path now re-records from the updated cache, like the cohort-change path in `Update` (source: pr-16762.md).

## Weighted-share gauges: `NaN` for a zero-weight borrower

Both `kueue_cluster_queue_weighted_share` and `kueue_cohort_weighted_share` are documented to return `NaN` when weight is 0 and the node is borrowing. #7338 added the `+Inf → NaN` conversion only to the ClusterQueue controller; `CohortReconciler.updateCohortStatusIfChanged` and `Cache.ResyncCohortGaugeMetrics` passed `+Inf` through (issue-16530). pr-16581 fixed both Cohort paths (v0.20.1 #16818, v0.19.8 #16864); `status.fairSharing.weightedShare` still stores `math.MaxInt64` because the status is an `int64` and cannot hold `NaN`/`+Inf` (source: pr-16581.md, issue-16530.md). pr-17057 (main, no user-visible change) makes all four reporting sites test `ZeroWeightBorrows()` carried on the usage stats instead of `share == +Inf` — with any non-zero weight (the webhook requires ≥ 1n) the share overflows to `+Inf` only after borrowing more than ~1e296, so the old check worked only by accident; tests also assert the gauge returns to 0 when borrowing stops (source: pr-17057.md). Related v0.20.1 fix: a borrowing node with a huge weight (e.g. 1e308) now reports the smallest positive float64 instead of 0 (#16584, source: CHANGELOG-0.20.md). See [[fair-sharing]].

## `kueue_replaced_workload_slices_total` was never registered

The counter (`cluster_queue`, `replica_role`) was defined, incremented on slice replacement and documented since v0.13 (#5510, KEP-77 Beta criterion), but missing from `Register()`, so it never appeared on `/metrics` while `kueue_admitted_workloads_total` counted both slices. Registered by pr-16743 (fixes issue-16623; v0.20.1 #16763, v0.19.8 #16856). Lesson for reviewers: a new metric needs a test that it is exposed, not only that it is incremented (source: issue-16623.md, pr-16743.md). See [[elastic-jobs]].

## Release map for this batch

| Fix | main PR | First release(s) |
|---|---|---|
| Execution-time histograms | pr-13420 | v0.20.0 |
| Workload labels on pending / LQ pending / LQ admitted metrics | pr-13469, #14167, pr-13635 | v0.20.0 |
| Invalid LQ selector fails startup | pr-16379 | v0.20.0 (0.19 backport merged later) |
| Cohort subtree gauge after hierarchy change | pr-16398 | v0.20.0, v0.19.7, v0.18.11 |
| Stale custom-label pending series on CQ stop/resume | pr-16670 | v0.20.1 |
| Pending refresh on CQ stop/resume and LQ lifecycle | pr-16833, #15576 | v0.20.1, v0.19.8 |
| `kueue_cohort_weighted_share` NaN | pr-16581 | v0.20.1, v0.19.8 |
| `kueue_replaced_workload_slices_total` registered | pr-16743 | v0.20.1, v0.19.8 |
| Cohort subtree quota series kept after CQ delete | pr-16762 | release-0.20 branch (after v0.20.1) |
| Workload labels on cohort subtree admitted total; creation-latency gate GA | pr-16730, pr-16493 | main (v0.21 dev) |


## Related pages

- [[cluster-queue]] — where per-CQ labels come from.
- [[performance-and-scale]] — interpreting scheduling-loop metrics.
- [[visibility-api]] — complementary view.
- [[dashboard]] — KueueViz, the UI-layer consumer of the same data.
- [[workload-priority]] — `priority_class*` labels.
- [[debugging-guide]] — which metrics to check when triaging stuck workloads.
- [[unadmitted-workloads-observability]] — `kueue_unadmitted_workloads`.
- [[fair-sharing]] — weighted-share semantics.
- [[feature-gates]] — `CustomMetricLabels`, `LocalQueueMetrics`, `MetricForWorkloadCreationLatency`.
