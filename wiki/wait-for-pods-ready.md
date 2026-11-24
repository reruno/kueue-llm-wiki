# WaitForPodsReady: timeouts, per-workload overrides, unscheduled timeout, max not-ready

**Summary**: Reference for the `waitForPodsReady` Configuration block and the four v0.19/v0.20 knobs around it: enabled-by-default with a 30 minute timeout, per-Workload overrides, a separate unscheduled-Pods timeout, and a not-ready Pod budget for Pod groups. Complements the conceptual description in [[gang-scheduling]].

**Sources**: pr-15503.md, pr-15672.md, pr-15734.md, pr-16059.md, pr-15531.md, pr-15627.md, pr-16217.md, issue-13502.md, raw/kueue/apis/config/v1beta2/configuration_types.go, raw/kueue/apis/config/v1beta2/defaults.go, raw/kueue/pkg/util/waitforpodsready/waitforpodsready.go, raw/kueue/pkg/controller/core/workload_controller.go, raw/kueue/pkg/controller/jobframework/validation.go, raw/kueue/pkg/config/validation.go, raw/kueue/pkg/features/kube_features.go, pr-15372.md, pr-15402.md, issue-16366.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, issue-14811.md, pr-17147.md, pr-17643.md, pr-17765.md, pr-17772.md, pr-16754.md, pr-17816.md, pr-17874.md, pr-17591.md, pr-17603.md, pr-17604.md, pr-17451.md, pr-17576.md, pr-17610.md, pr-17618.md, raw/kueue/pkg/controller/jobframework/reconciler.go, raw/kueue/pkg/controller/jobframework/interface.go, raw/kueue/pkg/controller/jobs/job/job_controller.go, raw/kueue/pkg/controller/jobs/raycluster/raycluster_controller.go, raw/kueue/CHANGELOG/CHANGELOG-0.19.md, pr-18446.md, pr-18547.md, pr-18772.md

**Last updated**: 2026-11-24

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

- `NewWorkload` copies the annotation onto the Workload only when the gate is enabled and the feature is not disabled. For Deployments the webhook mirrors the annotation into the Pod template (and deletes it there when removed from the Deployment). Unit tests added by pr-17451 (backport pr-17576/0.20; tests only) check that with the gate **off** the annotation is not propagated to the Workload on create or update, for batch Job, elastic Jobs, LeaderWorkerSet and StatefulSet (source: pr-17451.md).
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

## Where the job reconciler writes `PodsReady`

The `PodsReady` block of `JobReconciler.Reconcile` (`pkg/controller/jobframework/reconciler.go`) is the helper `reconcilePodsReadyCondition(ctx, job, wl) (updated bool, err error)`. It was extracted by pr-17610 (cleanup, release note NONE; backport pr-17618/0.20) (source: pr-17610.md). The helper:

1. picks the target Workload with `podsReadyWorkload` (see next section; added by pr-17643);
2. builds the condition with `generatePodsReadyCondition`, which calls `job.PodsReady(ctx, c, WithWorkload(target))` (option added by pr-16754);
3. returns without writing when the condition already has the same type and reason (V(3) `No update for PodsReady condition`);
4. writes with `workload.SetConditionAndUpdate` (manager prefix `constants.JobControllerName`);
5. records ready-wait metrics only on `PodsReady=True`. Reason `Started` records `ReadyWaitTime` and `AdmittedUntilReadyWaitTime`, plus their LocalQueue variants when LocalQueue metrics are exposed for the Workload. Reason `Recovered` records `WorkloadRecoveryWaitTime`, only when the previous reason was `WaitForRecovery`.

## Elastic jobs: PodsReady stays on the admitted slice

Applies with `ElasticJobsViaWorkloadSlices` and the `kueue.x-k8s.io/elastic-job` annotation. During a scale-up the replacement slice may wait for quota while the new Pods stay scheduling-gated. The job reconciler's selected Workload is then the pending replacement, but the workload controller runs the `PodsReady` timeout on the **admitted** slice. Before these fixes, the admitted slice could be evicted with `PodsReadyTimeout` even after its Pods became ready. The job was suspended; for a RayCluster used as a devbox, the head the user was working on was deleted (source: pr-17643.md, pr-17591.md).

- **Target slice (pr-17643; backports pr-17765/0.20, pr-17772/0.19).** `podsReadyWorkload(ctx, job, wl)` returns `wl` unchanged when slicing is not enabled for the job or `wl` is admitted. Otherwise it returns `workloadslicing.FindLatestAdmittedWorkload(ctx, c, wl, true)`: the newest admitted, non-finished, non-evicted slice of the chain, excluding ConcurrentAdmission variants. If there is none, it falls back to `wl`. A lookup error is returned as `finding the admitted workload slice for PodsReady: ...`. The timeout is **not** suspended during a scale-up: if the Pods never become ready, the admitted slice is evicted as before. An earlier revision of the PR skipped the timeout while a replacement was pending; review reverted it because that removed PodsReady protection during scale-up (source: pr-17643.md, reconciler.go).
- **Contract for integrations.** The `GenericJob.PodsReady` doc comment now says that, for an elastic job, it should consider only the Pods admitted by the latest admitted slice and ignore the Pods of a pending scale-up, such as scheduling-gated Pods. An integration whose `PodsReady` waits for gated Pods still reports `PodsReady=False` on the admitted slice and can be evicted (source: interface.go).
- **batch/v1 Job (pr-16754; backports pr-17816/0.20, pr-17874/0.19).** The interface method is now `PodsReady(ctx, c, options ...PodsReadyOption) bool`, with `WithWorkload(wl)` and the reader `PodsReadyWorkload(options...)` (the last option wins). When slicing is enabled and the passed Workload is admitted, `Job.PodsReady` uses `min(podsCount(), granted)` as its target, where `granted` is the `main` PodSet count from `workload.ExtractGrantedPodSetCounts` and `podsCount()` is `min(parallelism, completions)`. Ready means `succeeded + ready + len(uncountedTerminatedPods.succeeded) >= target`. Only the Job integration reads the option; the others accept it and ignore it (source: pr-16754.md, job_controller.go). Out-of-tree `GenericJob` implementations must adopt the new variadic signature.
- **RayCluster (pr-17591).** `RayCluster.PodsReady` uses the `HeadPodReady` condition behind `RayClusterHeadPodReady` (Beta, on, on main; Alpha, off, on release-0.20 and release-0.19). See [[integration-rayjob#RayCluster PodsReady uses the head Pod (`RayClusterHeadPodReady`)]]. pr-17591 alone did not cover the case where the pending replacement is the reconciler's target; pr-17643 covers it.

Release status: all of the above merged on main and was backported to release-0.20 and release-0.19 after v0.20.3 / v0.19.10 were prepared, so it is pending the next patch releases (source: CHANGELOG-0.20.md, CHANGELOG-0.19.md). See also [[elastic-jobs#PodsReady while a scale-up slice is pending]].

## Interactions found in the v0.20 line

- **Pod groups with an oversized Pod.** With `PodIntegrationVerifyRoleRequests`, a group member that requests more than its role's PodSet stays gated. The group can then never become `PodsReady`, and `waitForPodsReady` evicts and requeues the Workload up to the requeue limit. See [[integration-plain-pod#Role-hash forgery: requests are verified before ungating]].
- **SparkApplication `SUBMISSION_FAILED`** no longer finishes the Workload, so an application the operator resubmits stays under `waitForPodsReady` (see [[integration-spark]]).
- **Recovery-timeout eviction left quota reserved (issue-14811, fixed by pr-17147; v0.20.2 / v0.19.9).** A JobSet `Recreate` restart recreated already-succeeded child Jobs, lowering the reclaimable count; a `PodsReadyTimeout` eviction with `underlyingCause: WaitForRecovery` then suspended the JobSet, but the job reconciler kept failing on the webhook-rejected `reclaimablePods` decrease before it reached the eviction step, so `Admitted`, `QuotaReserved` and `Evicted` stayed `True` and the Workload was never requeued. Details on [[workload#`reclaimablePods` must not block eviction (pr-17147, fixes issue-14811)]].
- Known gap, open as of this snapshot: controller-manager memory grows during repeated JobSet `PodsReadyTimeout` / requeue cycles (issue-16629, reopened).

## `timeoutSeconds` is optional in the per-Workload annotation (pr-18446)

In the `kueue.x-k8s.io/wait-for-pods-ready` annotation (`WorkloadLevelWaitForPodsReady`) the field `timeoutSeconds` became optional, so an object can override only `recoveryTimeoutSeconds` and keep the cluster-level startup `timeout`. This continues the alpha2 plan of KEP-4803 (source: pr-18446.md). The validation rules above ("`timeoutSeconds > 0`") now apply when the field is present; the exact handling in `determineTimeouts` for an absent value is not stated in the PR and is unverified.

## SparkApplication PodsReady

SparkApplication counts ready executor Pods of the current submission (not `status.executorState`), and with dynamic allocation waits for the starting executors before falling back to `minExecutors`; see [[integration-spark#Elastic SparkApplication (main, not in a release as of v0.20)]] (source: pr-18547.md, pr-18772.md).

## Related pages

- [[gang-scheduling]] — why all-or-nothing matters and the eviction flow.
- [[failure-recovery]] — zombie Pod handling that interacts with `WaitForRecovery`.
- [[integration-plain-pod]] — Pod-group readiness rules.
- [[feature-gates]]
- [[workload]]
- [[integration-spark]]
- [[elastic-jobs]] — slice selection for `PodsReady` during a scale-up.
- [[integration-rayjob]] — `RayClusterHeadPodReady`.
- [[job-framework-interface]] — `GenericJob.PodsReady` signature.
