# Issue #7065: MultiKueue workload race between `GenericJobReconciler` and `multikueue` workload controllers.

**Summary**: MultiKueue workload race between `GenericJobReconciler` and `multikueue` workload controllers.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7065

**Last updated**: 2025-09-30T09:02:20Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2025-09-29T21:39:19Z
- **Updated**: 2025-09-30T09:02:20Z
- **Closed**: 2025-09-30T09:02:20Z
- **Labels**: `kind/bug`
- **Assignees**: [@ichekrygin](https://github.com/ichekrygin)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

Kueue Workloads have a controller reference to their originating Job so that Job changes trigger Workload reconciliation. On this path there are three largely independent reconcilers:

* **GenericJobReconciler**: projects Job changes into CRUD operations on the Workload.
* **core/workload controller**: reconciles changes to the Workload.
* **multikueue/workload controller**: reconciles changes to the Workload in the MultiKueue context.

### Where races appear

* **Job creation**: there is no associated Workload yet, so no race.
* **Job update**: all three controllers react to the same update. The core and multikueue controllers can reconcile a **stale** Workload, that is, a Workload that does not yet reflect the Job’s new spec.

Historically, pre-ElasticJobs, Workloads were effectively immutable. Any Job change resulted in deleting and recreating the Workload, so the race existed but rarely caused meaningful divergence from the desired state.

With **ElasticJobs**, Workloads are mutable with respect to pod count. Updates now require careful synchronization. We use critical sections to detect a changed Job context and handle the Workload according to whether it is a scale-down or scale-up.

### The issue in MultiKueue ElasticJobs

In recently added MultiKueue support for ElasticJobs, a critical section on the **scale-up** path was missing.

**Context**: when a Job scales up, `old.parallelism < new.parallelism`, the multicluster Workload controller did not recognize that the Workload under reconciliation was the **old** slice. At that moment it may be the only Workload, because the GenericJobReconciler may not yet have created the new Workload slice for the updated Job spec. Because the multikueue control plane still considered the old Workload admitted, the controller allowed syncing the Job changes to the worker cluster. This produced an `UnexpectedCondition` on the worker, manifesting as “Job without Workload.”

### Proposed Fix

The MultiKueue Workload controller is not coordinated with the GenericJobReconciler, so we cannot rely on reconciliation order. From a Workload alone, we cannot reliably tell whether it is current or stale. We must look at the **Job** to derive the update context, for example, detect scale-up.

Since the MultiKueue Workload controller does not operate on Jobs directly and delegates Job operations to the **MultiKueueAdapter**, we also delegate **scale-up detection** to the adapter’s `SyncJob` implementation. This is a pragmatic, low-friction workaround.

**Tradeoff**: every adapter that supports ElasticJobs must implement the “scaled-up” check. Today that is only `batch/v1 Job`.

### Longer-term option

Expose the Job update context, specifically scale-up information, through the **MultiKueueAdapter** interface. This would centralize detection and reduce the risk of missing per-adapter implementations while keeping the Workload controller decoupled from Job types.

### Why it is hard to reproduce in testing

This race condition is **timing-dependent** between the `GenericJobReconciler` and the `multikueue` Workload controller. Both react to the same Job update, but the order of execution and the observed object state are nondeterministic. Depending on the relative scheduling of the reconcilers, the multikueue controller may process a **stale Workload** before the GenericJobReconciler has created the new slice.

As a result, the bug is intermittent. In practice it shows up only once every **10–20 test runs**, making it hard to catch with automated regression testing. Typical test environments, where reconciliation is fast and not heavily loaded, further reduce the likelihood of hitting the precise interleaving required to expose the issue.

**Anything else we need to know?**:
* Related to: #7033 
* Related to: #7062

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-29T21:39:42Z

/assign
