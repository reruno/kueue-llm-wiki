# Workload Garbage Collection

**Summary**: An optional retention policy that Kueue uses to automatically delete finished or deactivated Workload objects after a configurable delay, reducing etcd storage and Kueue's memory footprint.

**Sources**: `raw/kueue/keps/1618-optional-gc-of-workloads/README.md`, `raw/kueue/keps/1618-optional-gc-of-workloads/kep.yaml`

**Last updated**: 2026-06-29

---

> **Stage: Stable**. (source: keps/1618-optional-gc-of-workloads/kep.yaml)

## Problem

By default Kueue never deletes its own [[workload]] objects. On busy clusters, finished Workloads accumulate indefinitely: they consume etcd storage and are loaded into Kueue's in-memory cache on startup, increasing memory usage and slowing initialization. (source: keps/1618-optional-gc-of-workloads/README.md)

## Solution

Add an `objectRetentionPolicies` section to the Kueue `Configuration` API. When configured, the workload controller evaluates each Workload that transitions to a terminal state (Finished or Deactivated) and deletes it after the configured duration. (source: keps/1618-optional-gc-of-workloads/README.md)

## Configuration

```yaml
apiVersion: config.kueue.x-k8s.io/v1beta2
kind: Configuration
objectRetentionPolicies:
  workloads:
    afterFinished: 10m        # delete 10 minutes after a Workload finishes
    afterDeactivatedByKueue: 1h   # delete 1 hour after Kueue deactivates a Workload
```

- `afterFinished`: duration after the `Finished` condition becomes `True`.
- `afterDeactivatedByKueue`: duration after Kueue sets `spec.active=false` due to backoff limit exceeded or maximum execution time.
- A duration of `0s` means **immediately** on transition.
- `nil` (absent) means the policy is disabled (backward-compatible default).

(source: keps/1618-optional-gc-of-workloads/README.md)

## Behavior details

1. **Startup scan**: On Kueue manager start, all existing finished/deactivated Workloads are evaluated. Those already past their retention window are deleted immediately. The rest are re-queued to reconcile after their remaining window expires.
2. **Ongoing reconciliation**: Each time a Workload transitions to finished/deactivated, the reconciler schedules a deletion after the configured duration.
3. **Finalizer prerequisite**: Deletion only succeeds if the Workload has no finalizers. The job framework removes the `kueue.x-k8s.io/resource-in-use` finalizer when the Workload transitions to finished; if other finalizers exist, Kubernetes marks the object for deletion but does not actually delete it until they are removed.

(source: keps/1618-optional-gc-of-workloads/README.md)

## Gotcha: WorkloadSlices stuck after retention (v0.18 fix)

KEP-1618 assumed finished Workloads carry no finalizers, so the GC path called `client.Delete()` directly. **WorkloadSlices** (added later, for [[elastic-jobs]]) broke that assumption: a slice is finished by the *scheduler* (`replaceWorkloadSlice → workload.Finish`), which sets the `Finished` condition but does **not** remove the `resource-in-use` finalizer (only the job-reconciler finalize path does). So when the retention window elapsed, Kubernetes set `deletionTimestamp` but the object stuck forever ([[pr-11181]], fixes [[issue-11130]]).

The fix introduces a `workload.Delete(ctx, c, wl) (bool, error)` helper that **removes the finalizer first, then deletes**. If deletion is already in progress (`DeletionTimestamp` set), removing the finalizer alone lets Kubernetes finish cleanup, so it returns `false` (no second delete) and the GC path only emits the "Deleted" event when a delete was actually requested. The fix was cherry-picked to the release branches as [[pr-11307]] (release-0.16) and [[pr-11308]] (release-0.17), shipping in v0.16.9 / v0.17.4.

## Related: don't *finish* a Workload right after creation

A sibling bug in the "finishing" path (not retention): with the **`FinishOrphanedWorkloads`** gate enabled, the workload controller could mark a Workload `Finished` within milliseconds of its owner Job/JobSet being created — a race between the JobReconciler's structured informer and the workload-controller's `PartialObjectMetadata` informer — which then blocked the queue. [[pr-11296]] makes `ReconcileGenericJob` finish an orphaned Workload only under the proper conditions and re-graduated the gate to Beta/default-on. See [[feature-gates]] and [[scheduler-internals#Admitted workloads must leave preemptionExpectations]].

## Cascade deletion warning

Deleting a Workload deletes its owner (the Job, JobSet, etc.) via owner references, which in turn garbage-collects all dependent resources (Pods, Services, etc.). Verify that finished jobs are no longer needed before enabling `afterDeactivatedByKueue`. (source: keps/1618-optional-gc-of-workloads/README.md)

## Risk: slow startup with many expired objects

If a large number of Workloads have expired retention windows when Kueue starts, the initial reconciliation loop will issue many delete API calls. This can delay Kueue's readiness and increase kube-apiserver load. Consider raising `clientQPS` or enabling the feature gradually. (source: keps/1618-optional-gc-of-workloads/README.md)

## Related pages

- [[workload]]
- [[admission]]
- [[workload-max-execution-time]]
- [[preemption]]
