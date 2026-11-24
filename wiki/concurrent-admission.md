# Concurrent Admission

**Summary**: An alpha feature that lets a Workload simultaneously pursue admission on multiple ResourceFlavors in parallel, enabling flavor migration and racing long-running AdmissionChecks across different accelerator types.

**Sources**: `raw/kueue/keps/8691-concurrent-admission/README.md`, `raw/kueue/keps/8691-concurrent-admission/kep.yaml`, pr-15553.md, pr-15781.md, pr-15949.md, pr-16282.md, issue-15500.md, issue-15547.md, issue-15838.md, pr-15000.md, pr-17144.md, pr-17337.md, pr-17338.md, issue-16872.md, pr-17157.md, raw/kueue/pkg/controller/concurrentadmission/controller.go, pr-14954.md, pr-17946.md, pr-18222.md, pr-18086.md, pr-17012.md, pr-17176.md, pr-19075.md, issue-17944.md, issue-18079.md, issue-18093.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md

**Last updated**: 2026-11-24

---

> **Stage: Alpha** — Feature gate `ConcurrentAdmission`, disabled by default. (source: keps/8691-concurrent-admission/kep.yaml)

## Problem

Kueue's current admission model evaluates one [[resource-flavor]] at a time. A workload picks a flavor and pursues it until admitted. This prevents two useful scenarios:

1. **Flavor migration**: a workload starts on `spot` but should upgrade to `reservation` when it becomes available, without being manually re-queued.
2. **Racing AdmissionChecks**: a workload could try `nvidia-a100` and `nvidia-h100` simultaneously and take whichever checks pass first.

(source: keps/8691-concurrent-admission/README.md)

## Core concepts

### Parent and Variant Workloads

Concurrent Admission introduces two new Workload roles:

- **Parent Workload**: the original Workload. It is excluded from Kueue's scheduling loop; it acts only as an owner and status aggregator.
- **Variant Workload**: a clone of the parent with specific `AdmissionConstraints` restricting it to a subset of ResourceFlavors. Variants are scheduled independently by Kueue's regular scheduling loop.

A Parent has a 1:N relationship with its Variants. Each Variant is a distinct Kubernetes object in etcd. (source: keps/8691-concurrent-admission/README.md)

### Variant controller

The ConcurrentAdmission controller (`variantReconciler`) manages the lifecycle of Variants:
- **Creation**: creates Variant Workloads from the Parent, one per flavor of the ClusterQueue's single ResourceGroup, when `spec.concurrentAdmissionPolicy` is set (source: raw/kueue/pkg/controller/concurrentadmission/controller.go).
- **Aggregation**: collects Variant statuses and rolls them up to the Parent.
- **Policy enforcement**: ensures only one Variant is admitted at a time. If a preferred Variant becomes available (higher flavor), the currently admitted Variant is evicted.
- **Eviction**: when the admitted Variant needs to be evicted (to migrate), the controller triggers eviction and re-queues the parent flow.

(source: keps/8691-concurrent-admission/README.md)

## ClusterQueue API extension

The [[cluster-queue]] spec gains `concurrentAdmissionPolicy` (`migration.mode`, `migration.constraints.lastAcceptableFlavorName`; see below). Variants are not listed explicitly: Kueue creates one per flavor, in `resourceGroups[0].flavors` order, and that order is the flavor preference (source: raw/kueue/apis/kueue/v1beta2/clusterqueue_types.go, raw/kueue/pkg/controller/concurrentadmission/controller.go).

## Workload API extension

Each Variant carries the annotation `kueue.x-k8s.io/workload-allowed-resource-flavors` naming its flavor (source: raw/kueue/pkg/controller/concurrentadmission/controller.go). A `spec.admissionConstraints` field exists only as a KEP alternative for Beta (source: keps/8691-concurrent-admission/README.md).

Only one Variant per Parent may be admitted at a time. The Variant controller enforces this. (source: keps/8691-concurrent-admission/README.md)

## Key use cases

**Story 1 — Flavor upgrade**: A workload starts on `spot`. When `reservation` quota becomes available, the `reservation` Variant can be admitted, the `spot` Variant is evicted, and the job migrates.

**Story 2 — Racing admission checks**: Two Variants target different GPU types. Each runs its [[provisioning-request]] or custom [[admission-check]] independently. The Variant whose check passes first wins; the other is deactivated.

**Story 3 — Delay fallback**: Configure a timeout before falling back to a less preferred flavor, giving the preferred flavor a chance to free up.

(source: keps/8691-concurrent-admission/README.md)

## Constraints

- Only works with job types that can tolerate pod recreation (migration involves pod deletion and restart).
- **`StrictFIFO` queueing strategy is rejected at the webhook layer** when ConcurrentAdmission is enabled on a CQ — the [[cluster-queue]] validation webhook now returns an error if both are configured ([[pr-11022]]; per the KEP, ConcurrentAdmission cannot be combined with StrictFIFO because Variants migrating in and out of admission would violate strict ordering).
- Increases API object count in etcd (one Variant per flavor per pending workload).

(source: keps/8691-concurrent-admission/README.md)

## Migration policy: how an admitted Variant moves to a better flavor

The ClusterQueue's `spec.concurrentAdmissionPolicy` controls what happens once one Variant is admitted. The policy has two modes (`migration.mode`), implemented in the ConcurrentAdmission controller (`pkg/controller/concurrentadmission/controller.go`):

- **`TryPreferredFlavors`** (default) — keep trying to migrate the workload toward a more-favorable flavor. When a more-preferred Variant becomes admissible, the controller activates it and deactivates the currently admitted (less-favorable) Variant, so the job migrates upward.
- **`RetainFirstAdmission`** ([[pr-11236]], fixes [[issue-10911]]) — once **any** Variant is admitted, deactivate **every other** Variant and never migrate. The workload is pinned to its first admitted flavor permanently, even if a more-preferred flavor frees up later. Useful when migration churn (pod recreation) is more expensive than running on a sub-optimal flavor. (The mode was implemented as `HoldFirstAdmission` and renamed to `RetainFirstAdmission` just before merge.)

### Flavor floor: `lastAcceptableFlavorName` (renamed from `minPreferredFlavorName`)

`spec.concurrentAdmissionPolicy.migration.constraints.lastAcceptableFlavorName` (a `ResourceFlavorReference`, optional) names the **lowest-ordered flavor that is still acceptable to migrate to**. Under `TryPreferredFlavors`, when a sibling Variant is already running, the scheduler's `isMigrationAllowed` check ([[pr-11125]]) **blocks** migrating the workload to any flavor ranked *below* (higher index in `resourceGroups[0].flavors`) this floor. With the field unset (or the flavor unresolvable) migration is unconstrained.

> **Field rename.** This field was originally introduced as `minPreferredFlavorName` and renamed to `lastAcceptableFlavorName` across the codebase in [[pr-11317]] (no remaining references to the old name). Use `lastAcceptableFlavorName`.

A validation webhook rule ([[pr-11126]], `validateConcurrentAdmissionPolicy` in `clusterqueue_webhook.go`) rejects a ClusterQueue whose `lastAcceptableFlavorName` does not name a flavor that actually exists in the ResourceGroup's flavor list. This sits alongside the rule that a ConcurrentAdmission ClusterQueue must have a single ResourceGroup with **at most 32 resource flavors** (raised from 16 in v0.20; see below).

## Implementation details (v0.18 hardening)

### Variant scheduling-equivalence hash

Kueue's scheduler skips re-evaluating Workloads whose **scheduling hash** matches one already determined inadmissible in the same cycle (the `SchedulingEquivalenceHashing` optimization — graduated to **Beta, default on, in v0.18** via [[pr-11097]]; see [[feature-gates]]). Variants of the same Parent share PodSets and most spec fields, so without an extra disambiguator they would all hash to the same value and only the first Variant's NoFit decision would matter — a pessimistic same-flavor result on Variant A would suppress Variant B even though B targets a different ResourceFlavor.

[[pr-10910]] adds the Workload annotation `WorkloadAllowedResourceFlavorAnnotation` (its value in the tree is `kueue.x-k8s.io/workload-allowed-resource-flavors`, a comma-separated flavor list such as `reservation,spot`; the older `allowed-resource-flavor` spelling no longer matches the code) into the scheduling-hash computation, so each Variant gets its own bucket and is evaluated independently.

### Indexer for parent → Variant lookup

[[pr-10921]] swaps the ConcurrentAdmission controller's manual scan over Workloads for the existing `OwnerReferenceUID` indexer, so finding all Variants of a given Parent is an O(1) hash lookup. Closes [[issue-10904]].

### Skipping less-favorable Variants while a more-favorable one is running

Without this guard, the scheduler can admit a less-favorable Variant (e.g. `spot`) while a more-favorable Variant (e.g. `reservation`) is already running — typically because the more-favorable Variant's evaluation took longer in the same cycle. [[pr-10917]] makes the scheduler skip admission of a less-favorable Variant when **any** more-favorable Variant of the same Parent is already running; the ConcurrentAdmission controller subsequently deactivates the skipped Variant. Fixes [[issue-10913]].

### Events on Variant lifecycle

The ConcurrentAdmission controller now emits Kubernetes Events on Variant **creation, activation, and deactivation** ([[pr-10951]]), making the migration lifecycle visible via `kubectl describe` and metrics.

### Comma-separated annotation parsing cleanup

[[pr-10957]] consolidates the parsing of comma-separated annotation values used by the controller (e.g. for the allowed-flavor list).

### Preemption.Target wrapping removed

[[pr-10954]] removes a redundant `preemption.Target` wrapping around `workload.Info` in the ConcurrentAdmission scheduler path; no behaviour change but cleaner internal types.

### Flavor count limit raised from 16 to 32 (v0.20)

The ClusterQueue webhook (`clusterqueue_webhook.go`) rejects a ClusterQueue with `concurrentAdmissionPolicy` whose single ResourceGroup lists more than **32** flavors ("cannot have more than 32 resource flavors in the ResourceGroup when ConcurrentAdmissionPolicy is defined"). It was 16; pr-15949 raised it after a user with 14 flavors asked for headroom (issue-15500.md, who intended to race on at most three at a time). Every flavor becomes a Variant Workload that goes through the scheduler, so cost grows with flavors times ClusterQueues; the docs and the API comments on `flavors` (pr-16282) now warn about the performance implications of many flavors, especially with very many ClusterQueues. The gate stays **Alpha** (`ConcurrentAdmission`, since 0.18, off by default).

### Preemption gate must not open on a less favorable Variant (pr-15553, cherry-picked to 0.19 as pr-15639)

`firstCandidateVariant` chooses which Variant may have its preemption gate opened. It must distinguish "scheduler evaluated this Variant and it needs no preemption" from "not evaluated yet". A `WorkloadQuotaReserved` condition with reason `PendingEvaluation` means *not evaluated*; the earlier check only tested for the condition's presence, so after an eviction (`clearWorkloadAdmission` stamps `PendingEvaluation`) or on a Variant's first reconcile the controller could ungate a less favorable Variant and pin the choice for `preemptionTimeout` (5 minutes; `latestOpenGateTime`), while the preferred Variant was locked out. Sibling Variants are created within the same second, so their timestamps tie after RFC3339 truncation and ordering falls back to UID comparison: gate selection has to be right for any arrival order. The `PendingEvaluation` distinction only exists with `UnadmittedWorkloadsObservability` on (default in v0.20); see [[unadmitted-workloads-observability]]. Related event: `PreemptionUngatedVariant`.

### Panic on parent names without a dash (pr-15781, backport pr-15850)

Kueue-generated Workload names always end in `-<hash>`, but a user-created (e.g. prebuilt) parent may have any DNS-subdomain name. `getWorkloadBaseName` sliced at the last `-` unconditionally, so a parent named `wl` panicked (`slice bounds out of range [:-1]`); controller-runtime recovered it, so the reconcile retried forever and the parent never got Variants. It now returns the whole name when there is no `-`.

### Removing a flavor from the ClusterQueue evicts the parent admitted on it (pr-17144)

Current behaviour of `variantReconciler.syncAdmissionStatus` when a flavor is removed from a ClusterQueue with `concurrentAdmissionPolicy` (source: raw/kueue/pkg/controller/concurrentadmission/controller.go, pr-17144.md):

- `deleteStaleVariants` deletes the Variant of the removed flavor (behaviour since #12501). If that Variant was the admitted one, no admitted Variant is left, and the parent is evicted with `Evicted` reason `ConcurrentAdmission`, message "No variant is running". This is the case reported in issue-15838 (against v0.20.0-rc.1; the issue is still open, and a reviewer of pr-17144 described the eviction as existing behaviour covered by the integration test "Should evict the parent when the admitted variant's flavor is removed").
- **New branch (pr-17144, fixes the flake issue-16872).** If the scheduler had already admitted **another** Variant (for example `spot`) before the Variant reconciler saw the ClusterQueue update, the controller took the "Parent and Variant admitted" branch, which only syncs `PodsReady`, so the parent stayed admitted on a flavor the ClusterQueue no longer offers. Now, when `admittedVariant != nil`, the parent is admitted, and `hasRemovedAdmissionFlavor(parent, flavorOrder)` finds a `status.admission.podSetAssignments[].flavors` value missing from the ClusterQueue's flavor order, the parent gets `Evicted` reason `ConcurrentAdmission`, message "The admitted flavor is no longer in the ClusterQueue" (V(2) log "Parent admitted flavor is no longer in the ClusterQueue, evicting parent"). An existing eviction is preserved while the parent releases quota. The parent can then be re-admitted on a remaining flavor.

Note that this differs from non-ConcurrentAdmission ClusterQueues, where removing a flavor does not evict running Workloads; a maintainer raised this in review. Release note: "ConcurrentAdmission: Fixed a bug where a parent `Workload` could remain admitted on a flavor removed from its `ClusterQueue` when a surviving variant was already admitted..." Backports pr-17337 (0.20) and pr-17338 (0.19), merged 2026-10-16, after v0.20.2 / v0.19.9 (source: pr-17144.md, pr-17337.md, pr-17338.md).

### Preemption gate states are no longer written as `Closed` (pr-17157)

ConcurrentAdmission readers of `status.preemptionGates` (`HasOpenPreemptionGate`, `latestOpenGateTime`) already treat a gate with no recorded state as closed, so the pr-17157 change that stops writing `Closed` states for never-opened gates does not change Variant gating ([[multikueue-orchestrated-preemption#Gate states are written only when a gate opens (pr-17157)]]).

### Policy removed from the ClusterQueue: parents and variants are cleaned up (pr-14954; v0.20.5 / v0.19.12)

`variantReconciler.Reconcile` used to keep treating leftover Parent/Variant Workloads as active after `spec.concurrentAdmissionPolicy` was removed (it had an unimplemented TODO), running `createVariants`/`deleteStaleVariants`/`syncVariantEvictionStatus` against a policy that no longer existed and leaving quota held. When `cq.Spec.ConcurrentAdmissionPolicy == nil` the reconciler now deactivates each Variant (`deactivateVariant`), clears the admission of an admitted Parent with the same `PatchAdmissionStatus` + `SetEvictedCondition` pattern as the "no variant is running" path (the Parent returns to `Pending` and is scheduled as a normal single Workload, not deleted or deactivated), and removes `ConcurrentAdmissionParentLabelKey` from the Parent so `IsParent()` is false and the reconciler stops touching it (source: pr-14954.md, CHANGELOG-0.20.md).

### Finished or deleting Parents get no new Variants (pr-18086, fixes issue-18079; v0.20.7 / v0.19.14)

Adding a flavor to a ClusterQueue enqueues all its Parents; `Reconcile` created a Variant for each **finished** Parent too and the scheduler could admit it. The workload controller then set `Evicted` on the finished Parent and returned before `syncFinished`, so the Variant never got `Finished`. For a Parent with a `deletionTimestamp`, Variants deleted first were recreated and re-collected by GC. `Reconcile` now returns before `createVariants` for a finished or deleting Parent; for a finished Parent it first runs `syncFinished` on existing Variants. Both checks sit **after** the policy-removed cleanup above, so that cleanup still runs. A finished Parent also skips `deleteStaleVariants`, `deactivateVariants`, `activateVariants` and opening the preemption gate (source: pr-18086.md).

### `generateVariant` must not alias parent metadata (pr-17946, fixes issue-17944; v0.20.5 / v0.19.12)

`generateVariant` assigned the Parent's `Labels`/`Annotations` maps to the Variant and then edited them, so removing `ConcurrentAdmissionParentLabelKey` from a Variant also removed it from the Parent, and setting the allowed-flavor annotation (`workload-allowed-resource-flavors`) on one Variant changed it on the Parent and every sibling built from it. Both maps are now cloned (like `Spec.PreemptionGates` already was). No evidence the mutated Parent was written back to the API server (source: pr-17946.md).

### Migration must not re-evict an already evicted Variant (pr-18222, fixes issue-18093; v0.20.5 / v0.19.12)

`issueMigration` evicted the migration victim on every scheduling cycle even if it was already `Evicted`. Each eviction is a loose SSA apply built from the scheduler snapshot (no `resourceVersion`) that bumps `schedulingStats.evictions`, so the controller's "Parent has no quota, clearing variant admission" write conflicted, and when it landed the next stale-snapshot eviction restored `status.admission` (about 80 times per second); the Parent was never re-admitted and `EvictedDueToFlavorMigration` events and `kueue_evicted_workloads_total` spammed. It now returns before `Evict` when the victim is already evicted, as `IssuePreemptions` does for evicted targets. The entry still gets `RequeueReasonPendingMigration` / "Pending the migration" (source: pr-18222.md).

### `migration.mode` defaults to `TryPreferredFlavors` in the CRD (pr-17012)

The webhook and controller already treated an empty `Mode` as `TryPreferredFlavors`, but the Go field was `+required` without a default, so the CRD rejected `concurrentAdmissionPolicy.migration` without `mode`. `ConcurrentAdmissionMigration.Mode` is now `*ConcurrentAdmissionMigrationMode` with `+kubebuilder:default=TryPreferredFlavors`. ACTION REQUIRED for Go consumers of `apis/kueue/v1beta2`: pass a pointer and handle nil when reading (source: pr-17012.md).

### Admission checks of the admitted Variant are mirrored onto the Parent (pr-17176)

Admission checks run on Variants, but the job starts from the Parent, which had no checks, so pod set updates (e.g. ProvisioningRequest `consume-provisioning-request` / `provisioning-class-name` annotations, node selectors) never reached the pods (pods unschedulable on DWS pools). `syncAdmissionStatus` now copies the admitted Variant's admission checks onto the Parent in the same patch that gives it its quota reservation and `Admitted`; stale checks from a Variant on another flavor are replaced, and they are reset when the Parent is evicted. The job reconciler reads the Parent's own checks. The workload controller already skips Parents when syncing/evicting on checks, and the **ProvisioningRequest controller now skips Parents** too (the requests belong to Variants; otherwise deleting the ProvisioningRequestConfig would flip the Parent's mirrored check to Pending and create a second request) (source: pr-17176.md).

### Pending counts count each Parent once (pr-19075 and cherry-picks; v0.20.7 / v0.19.14)

ClusterQueue `status.pendingWorkloads` / `kueue_pending_workloads` and LocalQueue `status.pendingWorkloads` / `kueue_local_queue_pending_workloads` counted a pending Workload once per Variant. `PendingWorkloads.Pending()` now subtracts the extra Variants; the LocalQueue count also stops counting the Parent after a Kueue restart or eviction. (source: pr-19075.md, CHANGELOG-0.20.md).

### Interaction with AdmissionFairSharing

Each reservation obtained by a more-preferred Variant can settle another entry penalty; deduplication per Workload and LocalQueue is not implemented ([[admission-fair-sharing#Accounting anchor: quota reservation, not admission (v0.20, Beta)]]).

## Related pages

- [[admission]]
- [[resource-flavor]]
- [[cluster-queue]]
- [[workload]]
- [[admission-check]]
- [[provisioning-request]]
- [[elastic-jobs]]
- [[feature-gates]]
