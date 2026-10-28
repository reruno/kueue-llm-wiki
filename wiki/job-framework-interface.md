# Job Framework Interface

**Summary**: The Kueue job framework defines the `GenericJob` interface and base reconciler that any new job type must implement to get full Kueue integration — suspend/resume lifecycle, quota accounting, condition propagation, and webhook scaffolding — for free.

**Sources**: `raw/kueue/keps/369-job-interface/README.md`, `raw/kueue/pkg/controller/jobframework/interface.go`, `raw/kueue/pkg/controller/jobframework/reconciler.go`, pr-16370.md, pr-16436.md, pr-16460.md, pr-16461.md, pr-16470.md, pr-13375.md, pr-16773.md, pr-16774.md, pr-16779.md, pr-16881.md, pr-16972.md, pr-16973.md, pr-13775.md, pr-12948.md, pr-16994.md, pr-17529.md, pr-17530.md, issue-16736.md, pr-15412.md, issue-15400.md, pr-17053.md, raw/kueue/pkg/controller/jobframework/defaults.go, raw/kueue/pkg/controller/jobframework/validation.go, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, raw/kueue/CHANGELOG/CHANGELOG-0.19.md

**Last updated**: 2026-10-28

---

> **Stage: Stable** — KEP 369. (source: keps/369-job-interface/kep.yaml)

## Purpose

Without a common framework, every new job type would need to re-implement: detecting when Kueue admits/evicts the job, toggling `.spec.suspend`, managing finalizers, propagating status conditions, and webhook boilerplate. The `jobframework` package provides all of this generically. (source: keps/369-job-interface/README.md)

## The GenericJob interface

Every integration must implement `GenericJob` (defined in `pkg/controller/jobframework/interface.go`):

| Method | Purpose |
|---|---|
| `Object()` | Returns the job as a `client.Object` |
| `IsSuspended()` | Returns whether the job is currently suspended |
| `Suspend()` | Suspends the job (sets `spec.suspend=true` or equivalent) |
| `RunWithPodSetsInfo(podSetsInfo)` | Unsuspends the job; injects node affinity and pod counts from the admission |
| `RestorePodSetsInfo(podSetsInfo)` | Removes the injected node affinity (called on eviction) |
| `Finished(ctx)` | Reports whether the job has completed and what condition to set |
| `PodSets(ctx)` | Returns `[]kueue.PodSet` describing how many pods the job needs per role |
| `IsActive()` | Returns true if any pods are running |
| `PodsReady(ctx)` | Returns true when all pods are in Ready state |
| `GVK()` | Returns the GroupVersionKind of the job type |

(source: pkg/controller/jobframework/interface.go)

> **Signature change (action-required, [[pr-11310]]).** Removing global state from the TrainJob reconciler required passing the controller-runtime `client.Client` explicitly into several `GenericJob` methods rather than capturing it in package-level state. As of this change, `RunWithPodSetsInfo`, `PodSets`, `PodsReady`, and `ReclaimablePods` (the last on `JobWithReclaimablePods`) all take the client as an argument. This is a job-framework interface change that affects **every** integration, not just TrainJob — in-house/out-of-tree integrations must update their method signatures when upgrading.

## Optional interfaces

Additional optional interfaces enable specific features:

| Interface | Feature |
|---|---|
| `JobWithReclaimablePods` | Elastic jobs: report completed pods so quota can be reclaimed |
| `JobWithCustomStop` | Custom stop logic (beyond simple suspend toggle) |
| `JobWithFinalize` | Custom cleanup after job finishes |
| `JobWithSkip` | Skip reconciliation in certain states |
| `JobWithPriorityClass` | Read priority class from a job-specific field |
| `JobWithCustomValidation` | Custom webhook create/update validation |
| `JobWithManagedBy` | MultiKueue: the job has a `spec.managedBy` field for multi-cluster dispatch |
| `JobWithCustomQueueNameChange` | Override the default handling when the job's `queue-name` label changes (see below) |
| `JobWithOnHold` | `IsOnHold()`: the job asks for its Workload's quota to be released without requeueing (see below) |

(source: pkg/controller/jobframework/interface.go)

### `JobWithCustomQueueNameChange` (serving workloads)

```go
type JobWithCustomQueueNameChange interface {
    CustomQueueNameChange(ctx context.Context, c client.Client, wl *kueue.Workload) error
}
```

Added in [[pr-11191]] (documented in [[pr-11215]]). The base reconciler normally syncs/reverts the Workload's `queue-name` to match the job. For **serving workloads** — long-running, non-completing integrations, specifically **LeaderWorkerSet** and **StatefulSet** (both managed through the Pod controller) — that generic handling raced with manual queue-name edits and could **revert** a deliberate label change at the Workload-object level. A job type that implements `JobWithCustomQueueNameChange` opts out of the generic path; the integration's own `CustomQueueNameChange` decides what to do. When the queue-name does change, the reconciler now also logs structured `oldQueueName`/`newQueueName` fields ([[pr-11148]]).

### `JobWithOnHold`

`IsOnHold() bool`. In `ReconcileGenericJob` the on-hold check runs right after the Workload-deletion branch and **before** the finished check. If the job is on hold and its Workload holds quota, the reconciler sets `QuotaReserved=False` with reason **`OnHold`** (`kueue.WorkloadOnHold`) and returns. The quota is released and the Workload is not requeued. `RayJob` implements it as `status.jobDeploymentStatus == ValidationFailed`. StatefulSet uses the same reason for scale-to-zero from its own reconciler (source: raw/kueue/pkg/controller/jobframework/interface.go, raw/kueue/pkg/controller/jobframework/reconciler.go, raw/kueue/pkg/controller/jobs/rayjob/rayjob_controller.go). A *pending* Workload that turns `OnHold` is removed from the scheduling queue (`DeleteWorkload`), so it does not leave a stale queue entry. This fix (#12929) shipped in v0.19.0 and v0.18.3, with a release-0.17 backport ([[pr-12948]]) (source: pr-12948.md, raw/kueue/CHANGELOG/CHANGELOG-0.19.md).

## The base reconciler

`JobReconciler` (`pkg/controller/jobframework/reconciler.go`) wraps a `GenericJob` and handles:

1. **Finalizer management**: creates the Workload with the `kueue.x-k8s.io/resource-in-use` finalizer and removes it from the Workload when the job is finished or gone.
2. **Workload creation**: creates a `Workload` from `PodSets()` when the job is first observed.
3. **Suspend/unsuspend**: calls `Suspend()` when the workload is evicted; calls `RunWithPodSetsInfo()` when admitted — injecting flavor-assigned node affinities.
4. **Condition propagation**: copies the workload's `Admitted`/`Evicted`/`Finished` conditions to the job.
5. **Deactivation**: sets `spec.active=false` on the workload when the job exceeds its backoff limit.

(source: pkg/controller/jobframework/reconciler.go)

## Webhook scaffolding

`BaseWebhook` provides mutating and validating webhook handlers that every integration gets for free:

- **Defaulting**: injects `kueue.x-k8s.io/queue-name` from namespace default (when a `default` LocalQueue exists); ensures `spec.suspend=true` if the job has a queue label but is not yet admitted.
- **Validation on create**: validates the queue-name label format (a valid LocalQueue name), prebuilt-workload, max-exec-time and related annotations; it does not check that the LocalQueue exists.
- **Validation on update**: the queue label is immutable while the job is not suspended; a changed non-empty value on a suspended job is format-validated (see below).

(source: pkg/controller/jobframework/base_webhook.go)

## Integration registration

A new integration registers through `IntegrationManager.RegisterIntegration()` (wired from `pkg/controller/jobs/jobs.go`). The batch Job does:

```go
m.RegisterIntegration(FrameworkName /* "batch/job" */, jobframework.IntegrationCallbacks{
    SetupIndexes:      SetupIndexes,
    NewJob:            NewJob,
    NewReconciler:     NewReconciler,
    SetupWebhook:      SetupWebhook,
    JobType:           &batchv1.Job{},
    MultiKueueAdapter: &multiKueueAdapter{},
})
```

The integration manager enumerates all registered integrations to wire up controllers and webhooks during manager startup. (source: pkg/controller/jobframework/integrationmanager.go)

## How PodSets map to quota

`PodSets()` returns a list of `kueue.PodSet` objects, each with:
- `name`: a logical role (e.g. `driver`, `executor`, `leader`, `worker`).
- `count`: how many pods.
- `template`: a `PodTemplateSpec` — Kueue reads the resource requests from here.

Kueue sums the resource requests across all pods in each PodSet and tracks them as quota usage. When the workload is admitted, `RunWithPodSetsInfo()` injects node affinities (from the assigned ResourceFlavor's node labels/taints) back into the job's pod template.

## Writing a new integration (checklist)

1. Implement `GenericJob` for your CRD type.
2. Implement optional interfaces as needed (especially `JobWithReclaimablePods` for elastic jobs, `JobWithManagedBy` for MultiKueue support).
3. Create a `BaseWebhook` wrapping your type; register it with the webhook server.
4. Register through `IntegrationManager.RegisterIntegration()` (wired from `pkg/controller/jobs/jobs.go`).
5. Add integration tests under `test/integration/controller/jobs/yourkind/`.

## Mutate third-party CRDs with a merge patch, not `Update`

An integration that vendors a third-party CRD's Go types must not call `client.Update` on the job object. `Update` sends a **full replace** of the object as the *vendored* struct sees it, so any field the cluster's newer CRD has and the vendored struct lacks is silently dropped. The observed failure was TrainJobs stuck unadmitted because Kueue overwrote the older TrainJob scheme with the vendored one on admission ([[pr-14836]], [[issue-14722]]).

Use `clientutil.Patch` (JSON merge patch via `client.MergeFrom`) in `RunWithPodSetsInfo` and `Stop`, matching what `RestorePodSetsInfo` already did. A merge patch carries only the fields that actually changed, so unmodelled fields are never touched. The same hazard applies to MultiKueue's remote-job creation ([[issue-14837]], open).

## Ownership markers, not names

When a reconciler resolves a Workload from a **client-supplied** label or annotation (pod-group name, prebuilt-workload name, slice name), the name alone is not an identity. Require a second condition Kueue stamps itself — the `kueue.x-k8s.io/is-group-workload` marker plus an owner-reference *shape* check, in the pod-group case — and apply it on **every** path that reaches the lookup, including the finalize path that runs before the queue-name and namespace-selector checks. See [[integration-plain-pod#PodGroup Workload adoption is guarded by `is-group-workload`]] ([[pr-13960]]).

## `RestorePodSetsInfo` takes a context

`RestorePodSetsInfo` now receives `context.Context` (mirroring `RunWithPodSetsInfo`). **ACTION REQUIRED for in-house integrations:** pass the context when calling or implementing it. Integrations that guard on the pod set count (JobSet, MPIJob, Kubeflow Trainer, SparkApplication, RayJob, RayCluster, RayService) return `false` and skip the restore when the job's pod set count does not match the admitted Workload (for example after a worker group is added to a running RayCluster), and now log that at V(2) with expected and actual counts (source: pr-13114.md; the guard itself is pr-13025, backported in pr-13111.md). Per the interface contract, `RestorePodSetsInfo` returns whether it changed anything so callers such as `clientutil.Patch` can skip no-op patches; TrainJob's `Stop` relies on this to stay idempotent (source: pr-15652.md, see [[integration-trainjob]]).

## `FindMatchingWorkloads` only considers Workloads the job controls

`FindMatchingWorkloads` lists Workloads through the owner-reference field index, which matches **all** ownerReferences of the job's GVK, including non-controller ones. The reconciler used to treat every listed Workload as its own, causing a nil-pointer dereference in `EquivalentToWorkload` (a permanent reconcile error loop for that job), deletion of Workloads controlled by other objects (`toDelete` path) and spec overwrite of foreign Workloads for suspended jobs (`toUpdate` path). It now skips (V(2) log) any listed Workload not controlled by this job before the equivalence check. The UID is deliberately **not** compared there, so stale-UID cleanup through `FinishOrphanedWorkloads` still works; `EquivalentToWorkload` also got a nil guard on the controller owner reference. Pod-group Workloads are controller-less by design and use their own equivalence check, so they are unaffected (source: pr-13573.md; backports pr-15526.md, pr-15527.md).

## Defaulting must respect `managedJobsNamespaceSelector`

**The LocalQueue path (#13375, v0.20.0).** Before this fix, the Job and `BaseWebhook` `Default()` methods applied the default `queue-name` without checking `managedJobsNamespaceSelector`, so a Job in an *excluded* namespace got `kueue.x-k8s.io/queue-name: default` and was then suspended. Only the Pod webhook checked the selector first. The check now lives in `IntegrationManager.ApplyDefaultLocalQueue` itself, so every integration that calls it is covered: Job, Deployment, JobSet, LWS, MPIJob, Ray*, SparkApplication, StatefulSet, TrainJob and the Kubeflow jobs. It runs only after the cheap eligibility checks: a default LocalQueue exists, the object has no queue name, and its owner is not managed by Kueue. Only then is the Namespace read through the unexported helper `namespaceMatchesSelector`, and a read error is returned from the webhook. Jobs in excluded namespaces are left unchanged. The CHANGELOG lists this only for v0.20.0; no backport entry appears (source: pr-13375.md, raw/kueue/pkg/controller/jobframework/defaults.go, raw/kueue/CHANGELOG/CHANGELOG-0.20.md).

`ApplyDefaultLocalQueue` and `ApplyDefaultWorkloadPriorityClass` both check the namespace selector before mutating and return a Namespace read error from the webhook rather than swallowing it; every Job webhook passes the configured selector through, and the Pod webhook passes `nil` because it already enforced the selector. See [[workload-priority#Defaulting respects the namespace selector]] (source: pr-15851.md).

## Child jobs: `SkipChildJobSuspension`

A *non-top-level* job is one whose ancestor is a Kueue-managed job, for example a JobSet's child `batch/v1 Job` or a RayJob's RayCluster. For such a job, `ReconcileGenericJob` returns right after the namespace-selector check. Historically it first **suspended the child** if the child was not finished and not suspended and no unfinished ancestor Workload could be found (`shouldSuspendChildJob` → `getLatestNotFinishedWorkloadForObject(ancestor)`, with special cases for workload slicing). This dates from early integrations. Every supported parent controller (JobSet, Kubeflow Trainer v2, KubeRay ≥ 1.7) now suspends or deletes its own children, so the code mostly generated extra API traffic (source: pr-16370.md, raw/kueue/pkg/controller/jobframework/reconciler.go).

It is also **racy with elastic Workload slices under MultiKueue** (Ray autoscaling). Suppose a worker scales W0 → W1 → W2. Slice W1 is already finished, while W2 does not yet have an owner reference to the worker-side RayJob. In that window the ancestor lookup returns nil, and the generic reconciler suspends the running child RayCluster, even though W2 is already admitted.

- Gate **`SkipChildJobSuspension`**: when enabled, `shouldSuspendChildJob` returns `false` and the child's lifecycle is left to the ancestor's controller. When disabled, the old behaviour applies. #16370 introduced it as Beta and on; #16436 downgraded it to **Alpha, off by default** (versioned 0.20) "to have more time to evaluate". Graduation to Beta is tracked in issue-16457 (open) (source: pr-16436.md, raw/kueue/pkg/features/kube_features.go).
- Backports: release-0.19 ([[pr-16460]], **v0.19.8**) and release-0.18 ([[pr-16461]]), both Alpha/off, with the gate version adjusted to the branch (source: pr-16460.md, raw/kueue/CHANGELOG/CHANGELOG-0.19.md).
- **Dependency**: `MultiKueueRayInTreeAutoscaling` now requires `MultiKueue`, `ElasticJobsViaWorkloadSlices` **and `SkipChildJobSuspension`**. Startup validation rejects the combination if the last one is disabled or omitted ([[pr-16470]], v0.20.1 via pr-16814). **Action required** if you enable Ray in-tree autoscaling under MultiKueue (source: pr-16470.md, raw/kueue/pkg/features/kube_features.go).
- RayService caveat raised in review: KubeRay < 1.7 relied on Kueue to suspend a RayService's child. With KubeRay ≥ 1.7, suspending a RayService deletes its children (source: pr-16370.md). See [[integration-rayjob#RayService suspend uses the top-level `spec.suspend` (KubeRay ≥ 1.7)]].

## Internal labels and annotations are never inherited

Some Kueue labels and annotations are read by controllers that **trust** them. A configuration could ask for these keys to be copied from the Job or Pod onto its Workload, either through `integrations.labelKeysToCopy` or as `CustomMetricLabels` sources. That let a job author forge them. #14227 makes `WithLabelKeysToCopy` / `WithAnnotationsToCopy` drop these keys whatever the configuration says. Every path that copies metadata onto a Workload reads its keys from these two options, including the pod group and the LWS adapter (source: pr-16773.md, raw/kueue/pkg/controller/jobframework/reconciler.go):

- labels (`nonInheritableLabels`): `kueue.x-k8s.io/multikueue-origin`, `kueue.x-k8s.io/concurrent-admission-parent`, `kueue.x-k8s.io/job-uid`;
- annotations (`nonInheritableAnnotations`): `component-workload-index`, `job-owner-gvk`, `job-owner-name`, `priority-boost`, `workload-allowed-resource-flavors`, `workload-slice-name`, `workload-slice-replacement-for`, `is-group-workload` (all `kueue.x-k8s.io/`).

What the keys protect: `multikueue-origin` marks a Workload as MultiKueue-placed for the worker watch, the GC and `ValidateRemoteObjectOwnership`. `priority-boost` feeds effective priority. `job-owner-*` are read by MultiKueue ahead of the owner reference. MultiKueue's remote copy is built by `cloneForCreate`, not from these options, so it is unaffected. `job-uid` is filtered too, but integrations write the real owner UID right after building the Workload. Shipped in **v0.20.1 (pr-16773) and v0.19.8 (pr-16774)**.

The configuration is still **accepted**, because refusing it would break existing setups. Instead, since #16779 the manager logs any `labelKeysToCopy` entries that `NonInheritableLabelsIn` reports, once at startup at Info level (v0.20.1 pr-16874, v0.19.8 pr-16878). #16881 removed the log mention from the API field comment and added a "keep in sync" note on the two lists. Workload-scoped custom metric sources are not checked, because a metric naming an internal key reports the Workload's own value (source: pr-16779.md, pr-16881.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md). Copying annotations generally (`integrations.annotationKeysToCopy`) is an open feature request (issue-16471).

## A finished prebuilt Workload is not adopted

A job that names a prebuilt Workload (`kueue.x-k8s.io/prebuilt-workload-name`) is matched in the prebuilt branch of `ensureOneWorkload`. That branch already ignored a Workload controlled by another object. It did not check whether the Workload was finished. If a deleted predecessor had left a finished Workload with that name, a new job adopted it and was finalized at once: the Workload finalizer was removed and the job kept running **unmanaged and without a quota reservation** ([[issue-16736]]).

[[pr-16994]] adds a second guard right after the controller check (source: raw/kueue/pkg/controller/jobframework/reconciler.go):

- `workloadfinish.IsFinished(wl) && !workloadOwnedBy(wl, job)` → log `"WARNING: The prebuilt workload is already finished"` at V(2) and return no Workload. The job is then stopped with the usual missing-workload message and `ErrPrebuiltWorkloadNotFound`, the same path as a missing prebuilt Workload. The leftover Workload is not modified.
- A finished Workload that the job **does** own is still returned, so normal completion is unchanged: the job is finalized and the Workload finalizer is removed.
- The check is in the shared branch, so it covers every integration that supports prebuilt Workloads, including composable jobs, before `EnsureWorkloadOwnedByAllMembers` / `EnsurePrebuiltWorkloadOwnership` adds owner references.

Releases: `main` (merged 2026-10-20), release-0.20 (pr-17529) and release-0.19 (pr-17530), merged 2026-10-21, after v0.20.2 / v0.19.9. The automated cherry-picks (pr-17506, pr-17507) were closed and replaced by manual ones (source: pr-17529.md, pr-17530.md). The refusal emits no event, only the V(2) log. Issue-17542 asks for a Warning event (open).

## `kueue.x-k8s.io/workload` is always set on the PodTemplate

When a job starts, `getPodSetsInfoFromStatus` builds each PodSet's `PodSetInfo` from the admission, and `RunWithPodSetsInfo` merges it into the Pod template. Since [[pr-15412]] (fixes issue-15400; `main` only, merged 2026-10-19, not backported) the info **always** carries the annotation `kueue.x-k8s.io/workload: <workload name>`. Before, it was added only if `TopologyAwareScheduling` or `SchedulerLibraryIntegration` was enabled, or `WaitForPodsReadyUnscheduledTimeout` was enabled together with pod-scheduled tracking. The function lost its `annotateWorkload` parameter (source: raw/kueue/pkg/controller/jobframework/reconciler.go, pr-15412.md).

TAS, the scheduler-library (WAS) simulator, unscheduled-Pod tracking, the TAS node controller and the workload-slice Pod index all look Pods up by this annotation. With the write unconditional, out-of-tree consumers can rely on it whatever gates are set. The TAS KEP was updated to describe it as a generic Kueue annotation (source: issue-15400.md, pr-15412.md).

## Single-Pod Workloads: eviction depends on `IsSuspended()`

`clearAdmissionAfterEviction(ctx, job, wl)` now takes the job. With `SkipReassignmentForPodOwnedWorkloads`, a Workload that `workload.OwnedBySinglePod` matches is parked (`Requeued=False`) after preemption or node-failure eviction **only if `!job.IsSuspended()`**. A suspended (still gated) Pod's Workload is requeued. When quota is already released, the function also repairs Workloads that an older version parked in that state (source: raw/kueue/pkg/controller/jobframework/reconciler.go, pr-17053.md). Only the Pod integration matches `OwnedBySinglePod`. See [[integration-plain-pod#Single-Pod Workloads evicted while still gated are requeued]].

## Queue-name format is validated on update

`ValidateJobOnUpdate` now validates a **changed, non-empty** `kueue.x-k8s.io/queue-name`. Before, webhooks that do not re-run `ValidateJobOnCreate` on update (Pod, AppWrapper, and the Kubeflow jobs served by `BaseWebhook`) let a suspended job switch to a valid label value that is not a valid LocalQueue name, such as `Bad_Queue`. The reconciler then failed to update `spec.queueName` on every retry. Unchanged values are not re-validated, so a job already stored with an invalid name stays updatable. Integrations that also re-run create validation (Job, JobSet, MPIJob, Ray, Spark, TrainJob) now put the error into the `field.ErrorList` twice. `ToAggregate()` deduplicates it, so users see it once (#16221). Shipped in **v0.20.2** (pr-16972) and **v0.19.9** (pr-16973) (source: pr-16973.md, raw/github/kubernetes-sigs__kueue/pr-16221.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, CHANGELOG-0.19.md).

The serving integrations (StatefulSet, LeaderWorkerSet) have a separate, stricter rule: a queue-name change is rejected while a Workload holds quota, even when no replica is Ready. They share `ValidateQueueNameUpdate(old, new, isSuspended, hasQuotaReservation)`. The callback runs only when the name changes to a non-empty value while the object counts as suspended. The helper reads from the cache and is not atomic with quota reservation (source: raw/kueue/pkg/controller/jobframework/validation.go). See [[integration-statefulset#Queue changes are rejected while the Workload holds quota]] and [[integration-leaderworkerset]].

## Priority lookup takes an event recorder

`ExtractPriority` and `PrepareWorkloadPriority` now take an `events.EventRecorder`, so that a missing WorkloadPriorityClass can be reported on the object (see [[workload-priority#Missing WorkloadPriorityClass: Warning event]]). `ExtractPriority` stays exported. **Out-of-tree integrations that call these helpers must pass a recorder** (source: pr-13775.md).

## Related pages

- [[integrations]]
- [[workload]]
- [[admission]]
- [[webhooks]]
- [[elastic-jobs]]
- [[multikueue]]
- [[local-queue-defaulting]]
- [[testing-integration]]
- [[workload-priority]]
- [[integration-statefulset]]
- [[integration-rayjob]]
