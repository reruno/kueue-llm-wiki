# Integration: StatefulSet

**Summary**: Kueue can manage `apps/v1 StatefulSet` jobs through queue-based admission, using per-pod scheduling gates rather than a top-level `spec.suspend` field, and supports MultiKueue dispatch.

**Sources**: `raw/kueue/pkg/controller/jobs/statefulset/statefulset_controller.go`, `raw/kueue/pkg/controller/jobs/statefulset/statefulset_multikueue_adapter.go`, `raw/kueue/pkg/controller/jobs/statefulset/statefulset_webhook.go`

**Last updated**: 2026-04-28

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

## Related pages

- [[integrations]]
- [[integration-plain-pod]]
- [[job-framework-interface]]
- [[workload]]
- [[admission]]
- [[multikueue]]
- [[manage-jobs-selectively]]
