# Integration: StatefulSet

**Summary**: Kueue can manage `apps/v1 StatefulSet` jobs through queue-based admission, using per-pod scheduling gates rather than a top-level `spec.suspend` field, and supports MultiKueue dispatch.

**Sources**: `raw/kueue/pkg/controller/jobs/statefulset/statefulset_controller.go`, `raw/kueue/pkg/controller/jobs/statefulset/statefulset_multikueue_adapter.go`, `raw/kueue/pkg/controller/jobs/statefulset/statefulset_webhook.go`, pr-13316.md, pr-16399.md, pr-16401.md, issue-14013.md, pr-16705.md, pr-16710.md, pr-16751.md, pr-16770.md, pr-13775.md, pr-12948.md, pr-16044.md, pr-17540.md, pr-17541.md, issue-16043.md, issue-14266.md, pr-17255.md, pr-16474.md, pr-17309.md, pr-17313.md, issue-16333.md, pr-15142.md, pr-15412.md, raw/kueue/pkg/controller/jobs/statefulset/statefulset_reconciler.go, raw/kueue/pkg/controller/jobframework/validation.go, raw/kueue/pkg/controller/core/workload_controller.go, raw/kueue/CHANGELOG/CHANGELOG-0.20.md

**Last updated**: 2026-10-28

---

> **Stage: Stable** (docs integrations table, `site/content/en/docs/overview/_index.md`) — Enable via `integrations.frameworks` in the Kueue Configuration.

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

**Correction (2026-10-21)**: this page said a Pod list failure still kept the Workload reconcile from starting ([[issue-14211]]). At the snapshot that is no longer true; see the next section.

## Reconcile shape: two independent branches

`Reconciler.Reconcile` reads the StatefulSet and resolves the Workload once with `findWorkload`. It then runs two branches in a plain `errgroup.Group`. There is deliberately **no derived context**, so a failing branch cannot cancel the other (source: raw/kueue/pkg/controller/jobs/statefulset/statefulset_reconciler.go):

- `ungatePods` lists the Pods by owner-reference index. Each Pod then gets **one** patch with three parts: `setDefault` (managed label, queue and priority labels, pod-group annotations), ungating when the StatefulSet is gone, and `syncQueueLabel`.
- `reconcileWorkload` runs only when the StatefulSet exists.

So neither a failing Pod queue-label patch ([[issue-14013]]) nor a Pod list error stops the Workload from being reconciled. issue-14013 was closed as fixed by this restructure plus #13921, which stopped one branch's error from cancelling the other. Both shipped in v0.20.0 ("Fixed reconciliation errors in one independent branch cancelling the other branches"; the single per-Pod patch is #14597) (source: issue-14013.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md).

`findWorkload` still falls back to the legacy UID-less Workload name, with a `TODO(#9497, v0.20): Remove legacy fallback`.

## Validation and label sync fixes

- **TAS metadata is validated.** The reconciler builds a topology request from `spec.template.metadata` annotations (`jobframework.NewPodSetTopologyRequest(...).PodIndexLabel(...)`) when `TopologyAwareScheduling` is enabled, but the validating webhook did not validate them on create (source: pr-15857.md; backports pr-15881.md, pr-15882.md) or on update (source: pr-16039.md, fixes issue-15880.md; backports pr-16104.md, pr-16105.md). Conflicting annotations are now rejected; corrected ones accepted; skipped when the gate is off.
- **`queue-name` is synced only onto gated Pods.** The reconciler copies the StatefulSet's `kueue.x-k8s.io/queue-name` onto its Pods, but the Pod webhook rejects queue-name changes on ungated Pods, while the StatefulSet webhook allows the change while `ReadyReplicas == 0`. Changing it after ungating but before any Pod was Ready made every reconcile fail, and could keep a Pod scheduling-gated during a rolling update. Now only Pods still gated are updated (source: pr-16270.md; backports pr-16334.md, pr-16335.md).
- **Pod indexing.** The pod-owner index uses `metadata.ownerReferences.name`, and `podList` is scoped inside `ungatePods` (source: pr-15609.md, issue-15563.md).
- **`WorkloadAnnotation` on Pods.** `kueue.x-k8s.io/workload` must be on every Pod of a Kueue-managed job so that `wasSimulator.TrackPod`, the TAS indexers and the workload-slice index can map Pods to Workloads. StatefulSet Pods get it from the shared write site in `getPodSetsInfoFromStatus`, applied when the Pod integration ungates a Pod. Since [[pr-15412]] (`main` only, merged 2026-10-19) that write is **unconditional**. Before, it required `TopologyAwareScheduling`, `SchedulerLibraryIntegration`, or `WaitForPodsReadyUnscheduledTimeout` with pod-scheduled tracking (source: raw/kueue/pkg/controller/jobframework/reconciler.go, pr-15412.md). **Correction (2026-10-21)**: this page said the StatefulSet path was fixed by pr-15056. That PR was closed without merging. See [[job-framework-interface#`kueue.x-k8s.io/workload` is always set on the PodTemplate]].
- Empty PodGroup eviction: see [[integration-plain-pod#Empty PodGroups of StatefulSet / LeaderWorkerSet]] (source: pr-14578.md).

## Rollouts: current-revision Pods stay gated until admission

During a rolling update the StatefulSet and LeaderWorkerSet reconcilers removed **both** scheduling gates from Pods at the current revision without checking whether the Workload was admitted. Those Pods could run without quota. With `rollingUpdate.partition` the rollout never completes, so this lasted as long as the partition was set. In addition, a StatefulSet Pod created during the rollout stayed gated forever: its defaulting and its ungating went into one patch, and the Pod webhook rejects that patch (#16329; source: pr-16401.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md).

The fix leaves ungating of these Pods to Workload admission. It still ungates Pods whose StatefulSet is gone (Kueue stops managing them), and gated Pods receive the current queue label. On `main` it also **removed the LeaderWorkerSet StatefulSet watch**, which only served the rollout rule (see [[integration-leaderworkerset]]). Shipped in **v0.20.0, v0.19.7 ([[pr-16401]]) and v0.18.11 ([[pr-16399]])**. The release-0.19 backport still has the legacy finalizer removal, so there `UngateAndFinalizePod` is split into `UngatePod` and `FinalizePod`, and the LWS StatefulSet watch remains because it still drives that removal (source: pr-16401.md).

## Legacy parent-suspended Pod finalizer cleanup removed (v0.20)

Since v0.16 Kueue has not added the `kueue.x-k8s.io/managed` finalizer to Pods suspended by a parent integration. StatefulSet and LeaderWorkerSet kept code to remove that finalizer from older Pods for a migration window through v0.18/v0.19, because serving workloads live a long time. [[pr-13316]] (fixes #8571) completes the cleanup for v0.20 (source: pr-13316.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md):

- The finalizer-removal branches are removed from the StatefulSet and LWS reconcile paths, and `utilstatefulset.ShouldFinalizePod` no longer exists. Ungating during rollouts and after the parent is deleted is kept, including Pods that carry both the standard and the topology scheduling gate.
- The locked `SkipFinalizersForPodsSuspendedByParent` gate (GA in 0.18) is removed and recorded in the removed-feature list.
- The generic Pod-group finalizer lifecycle is unchanged.
- **Upgrade note**: a Pod that still carries the legacy `kueue.x-k8s.io/managed` finalizer from a pre-v0.16 install is no longer cleaned up by Kueue. Remove the finalizer by hand before or after upgrading. (Needs verification: this is inferred from the removal and is not stated in the PR.)

A follow-up was agreed in review: fold the remaining `statefulset_pod_reconciler.go` defaulting logic into the main reconciler (source: pr-13316.md).

## Queue changes are rejected while the Workload holds quota

The StatefulSet webhook rejected a queue change only when `readyReplicas > 0`. If the Workload had reserved quota but no Pod was Ready yet (images still pulling), the webhook accepted a change to another LocalQueue. The reconciler then hit the Workload CRD rule that `queueName` is immutable while quota is reserved, and retried with backoff indefinitely. The webhook now also rejects the change while the Workload (UID-derived or legacy name) holds quota. Before quota reservation the change is still allowed (#16320). Shipped in **v0.20.1 ([[pr-16705]]) and v0.19.8 ([[pr-16710]])**. The 0.19 backport uses `findWorkloadName` + `client.Get`, because that branch has no `findWorkload` (source: pr-16710.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md). [[issue-14266]], which reported the same bug, was closed on 2026-10-15 as already fixed by #16320 (source: issue-14266.md).

Since [[pr-17255]] the rule lives in the shared helper `jobframework.ValidateQueueNameUpdate(old, new, isSuspended, hasQuotaReservation)`, which the LeaderWorkerSet webhook also uses (source: raw/kueue/pkg/controller/jobframework/validation.go):

- Same name: allowed.
- Not suspended (`status.readyReplicas > 0` on the **old** object), or new name empty: immutable.
- Otherwise the `hasQuotaReservation` callback runs. For StatefulSet it looks up the Workload and checks `workload.HasQuotaReservation`. If quota is reserved, the change is rejected.

StatefulSet behaviour did not change. The webhook reads Workloads from the informer cache, and the check is not atomic with quota reservation. A reservation made just before the update can still slip through (source: pr-17255.md).

## `labelKeysToCopy` and custom-metric sources are copied

The StatefulSet reconciler created its prebuilt Workload with `nil` label and annotation copy sets. Labels listed in `integrations.labelKeysToCopy`, and the `CustomMetricLabels` label/annotation sources, were therefore never copied, a gap that dated from #9344, which moved Workload creation out of the pod-group path. #16187 (fixes #13277) passes the configured sets into `NewGroupWorkload`, as LWS already did. The values come from the **StatefulSet's own metadata**, not from the Pod template. Shipped in **v0.20.1 ([[pr-16751]]) and v0.19.8 ([[pr-16770]])** (source: pr-16770.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md). Kueue's internal labels are never copied; see [[job-framework-interface#Internal labels and annotations are never inherited]].

## Scale-to-zero puts the Workload `OnHold`

When a StatefulSet is scaled to zero, `putWorkloadOnHold` sets `QuotaReserved=False` with reason **`OnHold`** (`kueue.WorkloadOnHold`). This releases the quota and keeps the Workload from being requeued. Scaling back up (`clearOnHold`) moves it out of hold ("Workload no longer on hold; waiting for quota reservation") (source: raw/kueue/pkg/controller/jobs/statefulset/statefulset_reconciler.go, raw/kueue/apis/kueue/v1beta2/workload_types.go). **Correction (2026-10-21)**: this page named the function `releaseScaleDownReservation`. #16044 renamed it. A pending Workload that turns `OnHold` is also removed from the scheduling queue (#12929, v0.19.0 / v0.18.3; 0.17 backport [[pr-12948]]); see [[job-framework-interface#`JobWithOnHold`]].

### Scale-to-zero keeps quota while owned Pods are active

Before [[pr-16044]] (fixes [[issue-16043]]), the reservation was released as soon as `spec.replicas` became 0, even if a Pod of the StatefulSet was still Running. Another Workload could then be admitted onto resources the old Pod still used (source: issue-16043.md, pr-16044.md).

Now `reconcileWorkload` first calls `hasActiveOwnedPods` (source: raw/kueue/pkg/controller/jobs/statefulset/statefulset_reconciler.go, raw/kueue/pkg/controller/jobs/pod/pod_controller.go):

- It lists Pods through the owner-reference index and keeps only Pods whose **controller** owner matches the StatefulSet's UID, Kind and APIVersion. Pods without the `SuspendedByParentAnnotation` count too.
- Each Pod is classified with the Pod integration's `PodActivity`, so the rules match pod groups: only `Running` Pods are active; with `FastQuotaReleaseInPodIntegration` a terminating Pod is inactive at once; a terminating Pod without a recorded grace period stays active; one with a grace period is active until its `deletionTimestamp`.
- If any active Pod exists, the Workload keeps its reservation. This is logged at V(4) ("Waiting for active StatefulSet Pods before putting Workload on hold").
- When every active Pod is terminating with a known deadline, the reconcile returns `RequeueAfter` just past the latest deadline. This covers a Pod that stays Running past its deadline without another Pod event. If any active Pod has no computable deadline, Kueue relies on Pod events only. There is no polling.
- The Pod watch now wakes the StatefulSet for all its Pods, not only annotated ones. When a Pod's owner reference changes, the former owner is woken too, so it does not keep quota for a Pod it no longer owns. A management check keeps Pod events in namespaces outside `managedJobsNamespaceSelector` from defaulting Pods.
- A zero-replica Workload that has already lost its reservation moves from `PendingEvaluation` to `OnHold`.

`OnHold` is now stable against the Workload controller (source: raw/kueue/pkg/controller/core/workload_controller.go, pr-16044.md):

- With `AdmissionGatedBy`, the admission-gated condition update returns early for an `OnHold` Workload. The `kueue.x-k8s.io/admission-gated-by` annotation still blocks admission after the hold is cleared.
- On the legacy path (`UnadmittedWorkloadsObservability` off, the release-0.19 default), the queue-blocker check used to replace `OnHold` with `Inadmissible` when the LocalQueue or ClusterQueue was missing, stopped or inactive. The StatefulSet reconciler then set `OnHold` again, and the two controllers looped. An `IsOnHold` early return now prevents that. The granular path already checked `IsOnHold` first.

Releases: `main` (merged 2026-10-21), release-0.20 ([[pr-17540]]) and release-0.19 ([[pr-17541]]). All merged after v0.20.2 / v0.19.9, so the next patch releases are the first to include it. The 0.19 backport keeps that branch's legacy Workload-name fallback and separate StatefulSet Pod reconciler, and adds the Pod-owner index that branch lacked (source: pr-17541.md).

## Default WorkloadPriorityClass is not added on update to a running StatefulSet

With `WorkloadPriorityClassDefaulting`, the mutating webhook also runs on update. It used to add `kueue.x-k8s.io/priority-class: default` to StatefulSets created before the `default` class existed, including ones Kueue does not manage. When such a StatefulSet had Ready replicas, the validating webhook rejected the label, so **every** update to it failed. Since [[pr-16474]] the defaulting is skipped in exactly that case. Details and releases: [[workload-priority#Default WorkloadPriorityClass is skipped on updates to running serving workloads]].

## WorkloadPriorityClass on StatefulSets

The StatefulSet reconciler resolves `kueue.x-k8s.io/priority-class` only when it **creates** the Workload (`PrepareWorkloadPriority` in `createPrebuiltWorkload`). So the `WorkloadPriorityClassNotFound` Warning (v0.20.0) appears only on that path. Changing the label on a StatefulSet whose Workload already exists is accepted and ignored (#13827) (source: pr-13775.md). See [[workload-priority#Missing WorkloadPriorityClass: Warning event]].

## Related pages

- [[integrations]]
- [[integration-plain-pod]]
- [[job-framework-interface]]
- [[workload]]
- [[admission]]
- [[multikueue]]
- [[manage-jobs-selectively]]
- [[integration-leaderworkerset]]
- [[workload-priority]]
