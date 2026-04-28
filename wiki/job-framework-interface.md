# Job Framework Interface

**Summary**: The Kueue job framework defines the `GenericJob` interface and base reconciler that any new job type must implement to get full Kueue integration — suspend/resume lifecycle, quota accounting, condition propagation, and webhook scaffolding — for free.

**Sources**: `raw/kueue/keps/369-job-interface/README.md`, `raw/kueue/pkg/controller/jobframework/interface.go`, `raw/kueue/pkg/controller/jobframework/reconciler.go`

**Last updated**: 2026-04-28

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

(source: pkg/controller/jobframework/interface.go)

## The base reconciler

`BaseReconciler` (`pkg/controller/jobframework/reconciler.go`) wraps a `GenericJob` and handles:

1. **Finalizer management**: adds `kueue.x-k8s.io/resource-in-use` on the job; removes it when the job is finished or the workload is gone.
2. **Workload creation**: creates a `Workload` from `PodSets()` when the job is first observed.
3. **Suspend/unsuspend**: calls `Suspend()` when the workload is evicted; calls `RunWithPodSetsInfo()` when admitted — injecting flavor-assigned node affinities.
4. **Condition propagation**: copies the workload's `Admitted`/`Evicted`/`Finished` conditions to the job.
5. **Deactivation**: sets `spec.active=false` on the workload when the job exceeds its backoff limit.

(source: pkg/controller/jobframework/reconciler.go)

## Webhook scaffolding

`BaseWebhook` provides mutating and validating webhook handlers that every integration gets for free:

- **Defaulting**: injects `kueue.x-k8s.io/queue-name` from namespace default (if LocalQueueDefaulting enabled); ensures `spec.suspend=true` if the job has a queue label but is not yet admitted.
- **Validation on create**: rejects non-suspended jobs with a queue label (users shouldn't create unsuspended Kueue-managed jobs); validates queue-name exists.
- **Validation on update**: prevents changing the queue label after creation; validates resource requests match supported patterns.

(source: pkg/controller/jobframework/base_webhook.go)

## Integration registration

A new integration calls `jobframework.RegisterIntegration()` at startup:

```go
jobframework.RegisterIntegration("batch/v1", jobframework.IntegrationCallbacks{
    SetupIndexes:            jobframework.SetupIndexes,
    NewReconciler:           NewReconciler,
    SetupWebhook:            SetupWebhook,
    JobType:                 &batchv1.Job{},
    AddToScheme:             batchv1.AddToScheme,
    IsManagingObjectsOwner:  IsManagingObjectsOwner,
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
4. Call `RegisterIntegration()` from your `init()` or setup function.
5. Add integration tests under `test/integration/controller/jobs/yourkind/`.

## Related pages

- [[integrations]]
- [[workload]]
- [[admission]]
- [[webhooks]]
- [[elastic-jobs]]
- [[multikueue]]
- [[local-queue-defaulting]]
- [[testing-integration]]
