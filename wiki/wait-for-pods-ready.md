# WaitForPodsReady: timeouts, per-workload overrides, unscheduled timeout, max not-ready

**Summary**: Reference for the `waitForPodsReady` Configuration block and the four v0.19/v0.20 knobs around it: enabled-by-default with a 30 minute timeout, per-Workload overrides, a separate unscheduled-Pods timeout, and a not-ready Pod budget for Pod groups. Complements the conceptual description in [[gang-scheduling]].

**Sources**: pr-15503.md, pr-15672.md, pr-15734.md, pr-16059.md, pr-15531.md, pr-15627.md, pr-16217.md, issue-13502.md, raw/kueue/apis/config/v1beta2/configuration_types.go, raw/kueue/apis/config/v1beta2/defaults.go, raw/kueue/pkg/util/waitforpodsready/waitforpodsready.go, raw/kueue/pkg/controller/core/workload_controller.go, raw/kueue/pkg/controller/jobframework/validation.go, raw/kueue/pkg/config/validation.go, raw/kueue/pkg/features/kube_features.go, pr-15372.md, pr-15402.md, issue-16366.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, issue-14811.md, pr-17147.md

**Last updated**: 2026-10-21

---

## Baseline behaviour (Configuration `waitForPodsReady`)

- The block is **defaulted even when omitted**: `Timeout` defaults to `30m` (`DefaultWaitForPodsReadyTimeout`), `BlockAdmission=false`, `RecoveryTimeout` defaults to the value of `timeout` (`0s` disables recovery checking), `requeuingStrategy` gets `timestamp`, `backoffBaseSeconds=60`, `backoffMaxSeconds=3600`, and `maxTimeoutOnWorkload=2h` (source: raw/kueue/apis/config/v1beta2/defaults.go).
- `DisableWaitForPodsReady` (**Alpha, off by default, since 0.19, deprecated, planned removal in 0.21**) is the migration escape hatch that turns the whole feature off again; `waitforpodsready.Enabled(cfg)` returns false when it is on (source: raw/kueue/pkg/features/kube_features.go).
- Timer start: `Admitted=True` transition time. Not-ready reasons on `PodsReady=False`: `WaitForStart`, `WaitForRecovery` (after a Pod failed post-start; measured from the last `PodsReady` transition against `recoveryTimeout`), and, with the unscheduled gate, `WaitForScheduling`. Expiry evicts with reason `PodsReadyTimeout` and requeues per `requeuingStrategy` (see [[gang-scheduling]], [[workload]]).
- Doc defaults for `timeout`/`recoveryTimeout` examples were refined in pr-15672 (docs only).

## Succeeded Pods count as ready (pr-15734)

The kubelet flips a Pod's `PodReady` to `False` once it completes, so the Pod integration reported `PodsReady=False` as soon as one member of a Pod group finished; with `recoveryTimeout` the Workload went to `WaitForRecovery` and was evicted, deleting the still-running Pods. `PodsReady` now treats a `Succeeded` Pod as ready, like the batch/Job integration. Gate `PodIntegrationCountSucceededPodsAsReady`: **Beta, default on, since 0.20**; disable it to restore the old behaviour. Cherry-picked to release-0.19 and 0.18 (pr-15910, pr-15912). See [[integration-plain-pod]].

## Per-Workload timeout: `WorkloadLevelWaitForPodsReady` (pr-15503)

**Alpha, off by default, since 0.20** (KEP-4803). Set annotation `kueue.x-k8s.io/wait-for-pods-ready` on any Kueue-managed object to a JSON value:

```json
{"timeoutSeconds": 3600, "recoveryTimeoutSeconds": 600}
```

Rules (source: raw/kueue/pkg/util/waitforpodsready/waitforpodsready.go, raw/kueue/pkg/controller/jobframework/validation.go, raw/kueue/pkg/controller/core/workload_controller.go):

- `NewWorkload` copies the annotation onto the Workload only when the gate is enabled and the feature is not disabled. For Deployments the webhook mirrors the annotation into the Pod template (and deletes it there when removed from the Deployment).
- Webhook validation (create, and update only when the annotation changed): must be valid JSON; `timeoutSeconds > 0`; `recoveryTimeoutSeconds > 0` when present; both `<= waitForPodsReady.maxTimeoutOnWorkload` (default 2h). An unparsable annotation on the Workload at reconcile time is logged and the cluster-level values are used.
- `determineTimeouts`: an annotation replaces the cluster `timeout`; `recoveryTimeoutSeconds` present and >0 replaces `recoveryTimeout`; absent falls back to the cluster value. (An explicit `0` cannot arrive through the webhook.)
- Config validation refuses enabling the gate together with `DisableWaitForPodsReady`.
- `maxTimeoutOnWorkload` has no effect on Workloads without an override.
- The Configuration never lacks a `waitForPodsReady` block: v1beta2 defaulting always creates it (`cmp.Or(cfg.WaitForPodsReady, &WaitForPodsReady{})`) and defaults `timeout` to 30m. So `determineTimeouts` cannot hit a nil config when the annotation omits `recoveryTimeoutSeconds`. [[issue-16366]] (a feared nil-config panic) was closed for this reason (source: issue-16366.md, raw/kueue/apis/config/v1beta2/defaults.go).
- Known gap, open as of this snapshot: a huge `timeoutSeconds` in the annotation can wrap around and bypass validation (issue-16970).

## Separate timeout for unscheduled Pods: `WaitForPodsReadyUnscheduledTimeout` (KEP-13502)

**Alpha, off by default, since 0.20** (owner @tenzen-y; issue-13502.md). Config field `waitForPodsReady.unscheduledTimeout` bounds the time from `Admitted=True` until all Pods required by the admission are scheduled or succeeded, so that Pods stuck unscheduled (stale scheduler state) are recovered faster than the long readiness `timeout` needed for image pulls.

- Validation: non-negative, must not exceed `timeout`, and setting the field (even `0s`) **requires the gate**. `nil`/`0s` disables scheduling tracking entirely (`PodsScheduledTrackingEnabled`).
- New condition `PodsScheduled` (`WaitForScheduling` / `AllRequiredPodsScheduled`); the deadline never exceeds `timeout` since admission; eviction needs a **current-admission** `PodsScheduled=False` observation, so a late observation does not restart the timer. Eviction reason stays `PodsReadyTimeout` with a `WaitForScheduling` underlying cause.
- For elastic jobs the workload-slice tracker only tracks the *active* slice (pr-15531).
- How the pieces landed: [[pr-15372]] added the config field `waitForPodsReady.unscheduledTimeout` to v1beta2. The v1beta1 Configuration type also got it, for the API reference docs. [[pr-15402]] added the `PodsScheduled` condition (`AllRequiredPodsScheduled` | `WaitForScheduling`) and `WaitForScheduling` as a `PodsReady` reason, and made that reason trigger eviction. In `admittedNotReadyWorkload`, a `PodsReady` reason of `WaitForScheduling` (with tracking enabled) uses `schedulingDeadline`. Otherwise the normal `WaitForStart` deadline (`admittedAt + timeout`) applies. The `WaitForScheduling` cause also appears in eviction events, metrics and scheduling statistics. The evicted Workload is requeued after the usual backoff. Release note: "Requires a positive timeout and the WaitForPodsReadyUnscheduledTimeout feature gate" (v0.20.0) (source: pr-15372.md, pr-15402.md, raw/kueue/pkg/controller/core/workload_controller.go, raw/kueue/CHANGELOG/CHANGELOG-0.20.md).
- Enabling it with `DisableWaitForPodsReady` is rejected at startup.

## Not-ready budget for Pod groups: `WaitForPodsReadyMaxNotReady` (pr-16059)

**Alpha, off by default, since 0.20** (KEP-15423, owner @j-skiba). Annotation `kueue.x-k8s.io/pod-group-max-not-ready-count: "M"` on the Pods of a plain Pod group lets `PodsReady` be satisfied once `notReady = pod-group-total-count - readyCount <= M`; it applies to both startup `timeout` and `recoveryTimeout` (source: pr-16059.md).

- Valid `M` is an integer in `[0, total-count - 1]`; missing/invalid on any Pod falls back to `0` (all-or-nothing) for the group.
- The group uses the **lowest** value across its Pods, so tightening takes effect when any Pod carries it, relaxing only when all do.
- Pods not yet created or deleted count as not ready; all Pods count regardless of role (leader vs worker).
- Admission and quota reservation still use the full `pod-group-total-count`.
- Works for StatefulSet and LeaderWorkerSet only if the annotation is in their Pod template(s); Kueue does not copy it from the parent object. Other integrations, MultiKueue and a descriptive `PodsReady=False` message are out of scope for Alpha; the generic message `Not all pods are ready or succeeded` is kept.

## Interactions found in the v0.20 line

- **Pod groups with an oversized Pod.** With `PodIntegrationVerifyRoleRequests`, a group member that requests more than its role's PodSet stays gated. The group can then never become `PodsReady`, and `waitForPodsReady` evicts and requeues the Workload up to the requeue limit. See [[integration-plain-pod#Role-hash forgery: requests are verified before ungating]].
- **SparkApplication `SUBMISSION_FAILED`** no longer finishes the Workload, so an application the operator resubmits stays under `waitForPodsReady` (see [[integration-spark]]).
- **Recovery-timeout eviction left quota reserved (issue-14811, fixed by pr-17147; v0.20.2 / v0.19.9).** A JobSet `Recreate` restart recreated already-succeeded child Jobs, lowering the reclaimable count; a `PodsReadyTimeout` eviction with `underlyingCause: WaitForRecovery` then suspended the JobSet, but the job reconciler kept failing on the webhook-rejected `reclaimablePods` decrease before it reached the eviction step, so `Admitted`, `QuotaReserved` and `Evicted` stayed `True` and the Workload was never requeued. Details on [[workload#`reclaimablePods` must not block eviction (pr-17147, fixes issue-14811)]].
- Known gap, open as of this snapshot: controller-manager memory grows during repeated JobSet `PodsReadyTimeout` / requeue cycles (issue-16629, reopened).

## Related pages

- [[gang-scheduling]] — why all-or-nothing matters and the eviction flow.
- [[failure-recovery]] — zombie Pod handling that interacts with `WaitForRecovery`.
- [[integration-plain-pod]] — Pod-group readiness rules.
- [[feature-gates]]
- [[workload]]
- [[integration-spark]]
