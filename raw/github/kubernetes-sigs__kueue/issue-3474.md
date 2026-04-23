# Issue #3474: Set `Requeued` condition, and unset `QuotaReserved` condition on eviction in Workload Reconciler

**Summary**: Set `Requeued` condition, and unset `QuotaReserved` condition on eviction in Workload Reconciler

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3474

**Last updated**: 2025-11-09T10:06:11Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-11-06T10:09:23Z
- **Updated**: 2025-11-09T10:06:11Z
- **Closed**: 2025-11-09T10:06:10Z
- **Labels**: `kind/feature`, `kind/cleanup`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 16

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
Currently the `Requeued`, and `QuotaReserved` conditions are set by the [jobframework reconciler](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobframework/reconciler.go#L451-L471)

Ideally this logic should be moved to the Workload Controller to simplify logic, ease maintenance and adding new features, and avoid unpredictable race conditions. The logic should be atomic with eviction

**Why is this needed**:

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-11-06T10:09:51Z

/kind feature

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-06T10:14:42Z

I agree it would be cleaner, but for that we need to figure out how solve the dependency issue on the Job, as currently workload controller is Job-agnostic: https://github.com/kubernetes-sigs/kueue/blob/e5dd891432f61c4a418e69405c840110553c07b0/pkg/controller/jobframework/reconciler.go#L458

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-06T18:25:47Z

As far as I know, during introducing this mechanism, we evaluated this proposed solution. But, we declined that based on the  Michal mentioned reason. I guess that we need to introduce another mechanism or a lot of refactoring...

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-02-04T19:00:06Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-04T20:17:25Z

/remove-lifecycle stale

### Comment by [@Horiodino](https://github.com/Horiodino) — 2025-03-03T14:17:29Z

If this is open, i would like to take it forward.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-03-03T15:58:00Z

Hi @Horiodino, great! Thanks for expressing interest. As this issue requires a lot of changes, please let us know in advance how to plan to tackle this

### Comment by [@Horiodino](https://github.com/Horiodino) — 2025-03-06T13:58:50Z

Is there any diagram or documentation for the JobFramework and Workload? Also, can you point me to where the Workload Reconciler is implemented?

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-03-10T09:04:53Z

Unfortunately we don't have any diagram. Here's the Workload's reconciler implementation: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/core/workload_controller.go#L137

### Comment by [@Horiodino](https://github.com/Horiodino) — 2025-03-12T12:31:59Z

1. Use Workload Conditions/Spec Fields: The `WorkloadReconciler` uses `workload.IsActive(&wl)` to determine job activity by checking `wl.Spec.Active` and the absence of the `WorkloadFinished` condition. The `JobFramework Reconciler` updates `wl.Spec.Active` to `false` when stopping a job (e.g., in `stopJob`) or setting `WorkloadFinished`. On eviction, the `WorkloadReconciler` sets `WorkloadEvicted` and may reset admission, implicitly assuming `wl.Spec.Active` reflects job state. Replace direct calls to `job.IsActive()` with checks against `wl.Spec.Active` and conditions like `WorkloadFinished`. Ensure `JobFramework Reconciler` reliably syncs job state to `wl.Spec.Active`, reducing dependency on direct job queries.

2. Introduce Job State Field in Workload Status: Add a new field, `Status.JobActive`, to `kueue.Workload`. The `JobFramework Reconciler` sets `wl.Status.JobActive = job.IsActive()` during reconciliation. The `WorkloadReconciler` checks `wl.Status.JobActive` rather than calling `job.IsActive()`. Decouples job state checks from job-specific logic, centralizing status management within `Workload`. Enhances readability and traceability of job state. Update the `kueue.Workload` spec to include `Status.JobActive`. Ensure the `JobFramework Reconciler` sets this field during state transitions. Adjust `workload.IsActive()` to use `Status.JobActive`.

3. Event-Driven Job State Notification: Leverage event-based communication between `JobFramework Reconciler` and `WorkloadReconciler`. The `WorkloadReconciler` already has support for notifications through `WorkloadUpdateWatcher` (via `NotifyWorkloadUpdate`). Add a watcher mechanism in `WorkloadReconciler` to receive job state change events. The `JobFramework Reconciler` triggers `NotifyWorkloadUpdate` when job state changes (e.g., active to inactive). Introduce a new event type for job state changes. Extend `WorkloadReconciler` to handle job state events and update workload conditions accordingly.

Wdyt folks?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-10T13:01:14Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-06-12T08:22:10Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-10T08:45:47Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-10T09:30:25Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-09T10:06:05Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-09T10:06:11Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3474#issuecomment-3507888620):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
