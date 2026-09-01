# Integration: StatefulSet

**Summary**: Kueue can manage `apps/v1 StatefulSet` jobs through queue-based admission, using per-pod scheduling gates rather than a top-level `spec.suspend` field, and supports MultiKueue dispatch.

**Sources**: `raw/kueue/pkg/controller/jobs/statefulset/statefulset_controller.go`, `raw/kueue/pkg/controller/jobs/statefulset/statefulset_multikueue_adapter.go`, `raw/kueue/pkg/controller/jobs/statefulset/statefulset_webhook.go`

**Last updated**: 2026-09-01

---

> **Stage: Beta** — The StatefulSet integration is stable for cluster operator use but may have rough edges in edge cases. Enable via `integrations.frameworks` in the Kueue Configuration.

## What is StatefulSet?

`apps/v1 StatefulSet` is a built-in Kubernetes workload for stateful applications. Kueue treats it as a job type, gating its pods through quota enforcement. (source: pkg/controller/jobs/statefulset/statefulset_controller.go)

## Suspend mechanism

StatefulSet has no `spec.suspend` field. Kueue uses **pod scheduling gates** instead: when gating the workload, Kueue adds a `kueue.x-k8s.io/admission` scheduling gate to the pod template. This prevents pods from being scheduled by kube-scheduler until Kueue removes the gate on admission.

This means Kueue's StatefulSet integration is built on top of the [[integration-plain-pod]] integration — it manages gates and finalizers at the pod level. The configuration requires `ImplicitlyEnabledFrameworkNames: ["pod"]`. (source: pkg/controller/jobs/statefulset/statefulset_controller.go)

## PodSets

A single PodSet matching all `spec.replicas`. Node affinity injected from the ResourceFlavor is applied to the pod template on admission. (source: pkg/controller/jobs/statefulset/statefulset_controller.go)

## MultiKueue support

**Supported** — a `multiKueueAdapter` exists. However, status sync from worker cluster is limited: StatefulSet does not have a `spec.managedBy` field, so the local controller on the manager cluster may overwrite synced status. This is a known limitation. (source: pkg/controller/jobs/statefulset/statefulset_multikueue_adapter.go)

## Namespace selector

The StatefulSet integration respects `managedJobsNamespaceSelector` (see [[manage-jobs-selectively]]). StatefulSets in non-selected namespaces are never gated even if `manageJobsWithoutQueueName=true`. (source: pkg/controller/jobs/statefulset/statefulset_webhook.go)

## Skipping other frameworks

If the StatefulSet's pod template annotations indicate it is already managed by another Kueue-recognized framework, the StatefulSet integration skips defaulting to avoid double-management. (source: pkg/controller/jobs/statefulset/statefulset_controller.go)

## `wlName` is resolved once per reconcile

`findWorkloadName` ran **twice** per reconcile — once in `Reconcile` to list Pods matching the group name, and again inside `reconcileWorkload`. [[pr-14721]] propagates `wlName` from `Reconcile` into `reconcileWorkload(ctx, sts, wlName)`, removing the duplicate lookup and the API calls it made. Legacy (UID-less) workload naming compatibility is preserved.

Note the related hazard the pod-group fix called out but deliberately left alone: `findWorkloadName` falls back to the legacy `GetWorkloadName("", sts.Name)`, but `reconcileWorkload` checks `HasOwnerReference` before mutating, so it is **not** exploitable the way the pod-group name lookup was (see [[integration-plain-pod#PodGroup Workload adoption is guarded by `is-group-workload`]]).

## Same-name replacement Pods and the managed finalizer

A StatefulSet-owned Pod that was evicted (not deleted) could keep the `kueue.x-k8s.io/managed` finalizer forever, and the API server refuses to create a replacement with the same ordinal name while the old object exists in etcd — a circular deadlock. Fixed for serving pod groups in [[pr-14632]]; see [[integration-plain-pod#Finalizer removal on eviction (serving pod groups)]].

Open: a Pod list failure still prevents the StatefulSet Workload reconcile from starting ([[issue-14211]]).

## Related pages

- [[integrations]]
- [[integration-plain-pod]]
- [[job-framework-interface]]
- [[workload]]
- [[admission]]
- [[multikueue]]
- [[manage-jobs-selectively]]
