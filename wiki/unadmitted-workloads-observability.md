# Unadmitted workloads observability (tiered QuotaReserved reasons)

**Summary**: With `UnadmittedWorkloadsObservability` (KEP-10852) a Workload without quota reservation reports a specific reason on `QuotaReserved=False` (`WaitingForQuota`, `NoMatchingFlavor`, `PendingEvaluation`, ...) instead of the generic `Pending`/`Inadmissible`, and two gauges count unadmitted Workloads per reason. **Beta and on by default from v0.20**; off by default on the release-0.18/0.19 branches (declared Beta there but default `false`, see below).

**Sources**: pr-15553.md, pr-15562.md, pr-15623.md, issue-15564.md, issue-15547.md, raw/kueue/keps/10852-inadmissible-workloads-observability/README.md, raw/kueue/pkg/features/kube_features.go, raw/kueue/apis/kueue/v1beta2/workload_types.go, raw/kueue/pkg/controller/core/workload_controller.go, raw/kueue/pkg/metrics/metrics.go, pr-13063.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, pr-16483.md, pr-17093.md, pr-17294.md, issue-11843.md

**Last updated**: 2026-10-21

---

## Gates and their status

| Gate | Stage | Effect |
|---|---|---|
| `UnadmittedWorkloadsObservability` | main's versioned spec: Alpha 0.19 (off), **Beta 0.20 (on)** | Tiered reasons on `QuotaReserved`/`Admitted`; `kueue_unadmitted_workloads` and `kueue_local_queue_unadmitted_workloads` metrics. |
| `UnadmittedWorkloadsExplicitStatus` | Alpha 0.19 (off); requires the gate above | Writes both `QuotaReserved=False` (`PendingEvaluation`) and `Admitted=False` (`NoReservation`) at the Workload's *first* reconcile. When off, new Workloads have no conditions, saving API writes under heavy load, and equivalence-hash bypass on creation is also skipped. |

pr-15562 and pr-15623 (fixing issue-15564.md) only clean up the gate's declared stage on main: the gate had been mislabelled Beta on the release-0.18/0.19 branches while defaulting off. The maintainers discussed backporting it as Alpha; the result is a metadata correction, not a behaviour change (source: pr-15562.md, issue-15564.md).

## Reason tiers on `QuotaReserved=False`

Precedence, strongest first (source: KEP README, `workload_types.go`):

1. **Workload-wide** (evaluated before any flavor): `Deactivated`, `OnHold` (quota intentionally released, e.g. StatefulSet scale-to-zero), `Misconfigured` (missing LocalQueue/ClusterQueue, invalid namespace selector, admissibility validation failure such as LimitRange violations), `NoMatchingFlavor`, `Suspended` (queue inactive or stop policy), `AdmissionGated` (see [[admission-gated-by-annotation]]), `WaitingForPodsReady` (blockAdmission, see [[wait-for-pods-ready]]).
2. **Nominated flavor**: `ExceedsMaxQuota`, `WaitingForQuota`, `TopologyPlacementFailed` (TAS only), `WaitingForPreemptedWorkloads`. With several PodSet groups the most severe reason among the evaluated groups wins.
3. **`PendingEvaluation`**: active in the queue, not yet evaluated by the scheduler.

`Admitted=False` uses `NoReservation`, `UnsatisfiedAdmissionChecks`, `PendingDelayedTopologyRequests`; the hybrid `NoReservationUnsatisfiedChecks` is deliberately not used. The legacy reasons `Pending` and `Inadmissible` are deprecated in the API; with the gate off `requeueAndUpdate` collapses every scheduler verdict to `Pending`.

Controller behaviour (`syncQuotaReservedFalseCondition`): the workload controller keeps scheduler-set reasons (`WaitingForQuota`, `NoMatchingFlavor`, `ExceedsMaxQuota`, `TopologyPlacementFailed`, `WaitingForPreemptedWorkloads`, `WaitingForPodsReady`, `PendingEvaluation`) until the next scheduler cycle, but deliberately re-evaluates `Suspended` and `Misconfigured` so they can return to `PendingEvaluation` once the blockage is fixed. A Workload whose scheduling hash is in the no-fit set is given the recorded no-fit reason with message "Bypassed scheduling evaluation because an equivalent workload recently failed"; this can leave a stale reason until a cluster event clears the hashes ([[scheduler-internals#Scheduling-equivalence hash: what it does and does not include]]).

## Metrics

`kueue_unadmitted_workloads{cluster_queue, reason, underlying_cause, replica_role, ...custom labels}` and `kueue_local_queue_unadmitted_workloads{name, namespace, cluster_queue, reason, underlying_cause, ...}` are gauges, emitted only when the gate is on. They count Workloads that never entered a queue structure (missing queues) unlike `kueue_pending_workloads`, which only sees `active` and `inadmissible` (source: KEP README, `metrics.go`). See [[metrics]].

## Dependent behaviour: ConcurrentAdmission variants (pr-15553)

[[concurrent-admission]] uses the `PendingEvaluation` reason to tell "the scheduler has not looked at this Variant yet" from "the scheduler evaluated it and no preemption is needed". The check used to test only for the *presence* of a `QuotaReserved` condition, and `PendingEvaluation` (stamped when the controller clears a Variant's admission after eviction, or on a Variant's first reconcile) counted as "evaluated", so the preemption gate opened on a less favorable Variant and locked out the preferred one for `preemptionTimeout` (5 minutes). Fixed by treating `PendingEvaluation` as not evaluated (issue-15547.md). Caveat noted in the PR: with the observability gate disabled the distinction does not exist (everything collapses to `Pending`), and widening the check to `Pending` would stop any Variant from ever being ungated; the interaction between the two gates was left as a separate decision.

## Graduation to Beta/on (pr-13063, v0.20.0)

pr-13063 (merged 2026-08-03, shipped in v0.20.0) flipped `UnadmittedWorkloadsObservability` to default-on. Review notes that matter for later work (source: pr-13063.md):

- The maintainers deliberately **split** it from `UnadmittedWorkloadsExplicitStatus`: the observability gate only changes condition reasons and metrics, while explicit status adds API writes at the first reconcile and needs a release of scale evidence first. `UnadmittedWorkloadsExplicitStatus` therefore stays Alpha/off.
- At Beta, tests should be **adjusted to the new behaviour rather than pinning the gate off**, so that GA graduation is a mechanical change (a GA gate cannot be disabled). A side effect surfaced in a TAS second-pass test: each `QuotaReserved=False` status update triggers `WorkloadReconciler.Update`, which calls `QueueSecondPassIfNeeded` with iteration 0 and registers an extra backoff timer, so second-pass wake-ups can exceed one per backoff interval.
- Unit tests for controllers now expect `PendingEvaluation` where they used to expect `Pending`.

## Reasons added after the first version

Read from `apis/kueue/v1beta2/workload_types.go` at the snapshot and the v0.20 changelogs:

- **`DRAResourcesUnresolved`** — set on `QuotaReserved=False` and on `Requeued=False` when the Workload's DRA resources cannot be resolved (with this gate on); the `underlying_cause` label of the unadmitted metrics changes accordingly (#16123, v0.20.0). See [[dra]].
- **`AssignmentError`** — Kueue failed to build an assignment because of an unexpected downstream error.
- **`PreemptionGated`** — a Workload blocked by a closed preemption gate used to keep a stale `QuotaReserved` condition and `status.resourceRequests` and showed `AdmissionGated`; since v0.20.1 (#16699) it reports `PreemptionGated` on `QuotaReserved` (the separate `BlockedOnPreemptionGates` condition also uses `PreemptionGated`). See [[multikueue-orchestrated-preemption]].

- **`SchedulingSimulationFailed`** — main only (v0.21 dev): with the Alpha `SchedulerLibraryDeepIntegration` gate, the scheduler-library planner reports this reason when its scheduling simulation cannot place the Workload's Pods (source: raw/kueue/apis/kueue/v1beta2/workload_types.go, pr-16483.md). See [[topology-aware-scheduling]].

## Logging of reason changes (pr-17093)

The workload controller logs each `QuotaReserved` reason change as `Workload status updated` with `reason` and `message` at **V(3)**, and only **after** the status write succeeds, so a failed write does not produce a misleading log line. DRA validation failures no longer log an error on every reconcile. The `queue`/`prevQueue` log keys were renamed to `localQueue`/`prevLocalQueue` and now include the namespace (`klog.KRef(namespace, name)`). A follow-up (pr-17294) replaced the Warning Events that pr-17093 had added for these transitions with logs, before either was released (source: pr-17093.md, pr-17294.md, raw/kueue/pkg/controller/core/workload_controller.go). Backported to release-0.20 (pr-17332) and release-0.19 (pr-17410) after v0.20.2 / v0.19.9, so the log-key rename reaches users in the next patch releases.

## A `reason` label on `kueue_pending_workloads`?

issue-11843 asked for one; it was closed in favour of this feature's `kueue_unadmitted_workloads` gauges, which already carry `reason` and `underlying_cause` (source: issue-11843.md). Use those for per-cause alerting.

## Related pages

- [[admission]] — where reasons are produced.
- [[metrics]]
- [[debugging-guide]] — how to read the reason.
- [[feature-gates]]
