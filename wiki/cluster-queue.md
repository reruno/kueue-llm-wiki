# ClusterQueue

**Summary**: A ClusterQueue (CQ) is a cluster-scoped resource that owns a pool of quota. It groups quota into resource groups of flavors, limits how workloads queue up, and optionally joins a [[cohort]] so unused capacity can be lent to peers.

**Sources**: `raw/github/kubernetes-sigs__kueue/`, pr-15633.md, pr-16140.md, pr-15949.md, pr-16282.md, pr-15913.md, pr-16168.md, raw/kueue/apis/kueue/v1beta2/clusterqueue_types.go, pr-15371.md, pr-16375.md, pr-16438.md, pr-15040.md, pr-17010.md, pr-16487.md, pr-16488.md, pr-16528.md, pr-16728.md, pr-17479.md, pr-17480.md, raw/kueue/pkg/controller/core/workload_controller.go, raw/kueue/pkg/cache/queue/manager.go

**Last updated**: 2026-10-28

---

## Purpose

A ClusterQueue is the quota pool that [[workload]]s are admitted against. Tenants don't write to it directly — they submit jobs into a namespaced [[local-queue]], which points at a ClusterQueue. That indirection keeps quota policy (platform-team-owned) separate from queue naming (tenant-owned).

A CQ models:

- The total nominal quota the tenant is guaranteed, broken down by **resource group** and within that by **flavor** — see [[resource-flavor]].
- Borrowing/lending limits — see [[borrowing-and-lending]].
- Queueing strategy (FIFO variants) — see [[queueing-strategy]].
- Preemption policy — see [[preemption]].
- Cohort membership — see [[cohort]].
- Optional [[admission-check]]s that must pass before admission.

## Resource groups and flavors

A CQ's quota is not a single scalar. It's structured as **resource groups**, each covariant in one or more resources (e.g. CPU+memory+`nvidia.com/gpu`) and with one or more flavors (e.g. `on-demand`, `spot`, `h100`, `a100`). A Workload that asks for a combination must fit entirely within a single flavor of a group — flavors are not combined within a single PodSet. This is Kueue's answer to heterogeneous hardware.

ResourceFlavor labels are applied as node selectors on admission so `kube-scheduler` places Pods on the right nodes ([[issue-425]] — the labels are not "misappropriated", they are intentionally injected).

See [[resource-flavor]] for flavor mechanics.

## Cohort membership

A CQ's `spec.cohortName` field (`spec.cohort` in v1beta1) joins it into a [[cohort]]. CQs in the same cohort can borrow unused nominal quota from each other subject to `borrowingLimit` and `lendingLimit` ([[pr-10406]]). Hierarchical cohorts (a CQ can point at a Cohort which itself has a parent Cohort) are supported ([[issue-3644]], [[issue-3583]]) — see [[borrowing-and-lending]].

## State fields to watch

`status.flavorsReservation` and `status.flavorsUsage` are the authoritative view of what's reserved and what's actually consumed. `status.pendingWorkloads`, `status.reservingWorkloads` and `status.admittedWorkloads` count pending, quota-reserving and admitted (unfinished) Workloads. `status.conditions` includes `Active` (the CQ is healthy, referenced flavors exist, webhooks pass).

A CQ becomes inactive if a referenced [[resource-flavor]] is missing or a referenced [[admission-check]] is not `Active` — by design ([[issue-3645]] — TAS: CQ is not deactivated when there is no Topology, which was fixed). It also becomes inactive with reason **`CohortCycleDetected`** (`ClusterQueueActiveReasonCohortCycleDetected`) when its Cohort's parent chain contains a cycle (#13774, v0.20.0, backported to 0.19.7/0.18.11); see [[cohort#Cycles in the Cohort hierarchy]].

`status.fairSharing.weightedShare` is an int64 view of the float share: `MaxInt64` for zero-weight borrowers and for shares at or past 2^63, and at least `1` for any positive share (pr-16487, pr-16488, pr-16528; [[fair-sharing#Weighted share edge cases (v0.20.1 / v0.19.8)]]).

## `kubectl get -o wide` shows ACTIVE and REASON (v0.20)

`kubectl get clusterqueue -o wide` and `kubectl get localqueue -o wide` gained `ACTIVE` and `REASON` columns (priority-1 printer columns, so default output is unchanged) that read the existing `Active` condition; the quick-start and MultiKueue examples were updated (source: pr-15633.md, closes issue-15566.md). No schema change.

## Fields and annotations added around the ClusterQueue in v0.20

- **`kueue.x-k8s.io/preemption-config-name` annotation** (Alpha, gate `ConfigurablePreemptions`) references a cluster-scoped `PreemptionConfig`; it becomes a real field in Beta ([[configurable-preemptions]]).
- **`status.effectiveQuotas`** (`orchestratorRef` + `resourceGroups`, max 16 groups): written by a `DynamicQuotaOrchestrator` under gate `DynamicQuotaOrchestration` (Alpha); when set, the scheduler uses it instead of `spec.resourceGroups` (via `resourcegroups.EffectiveResourceGroups`, pr-15040), and an empty list is a complete override. Webhooks still validate only `spec` ([[dynamic-quota-orchestration]]).
- **`spec.concurrentAdmissionPolicy`** requires a single ResourceGroup with at most **32** flavors (was 16) ([[concurrent-admission]]).
- The API comments on `resourceGroups[].flavors` now warn that many flavors have performance implications (pr-16282).
- The manager-side `MultiKueueManagerQuotaAutomation` condition's `observedGeneration` is refreshed even when the condition itself is unchanged (pr-16140; [[multikueue]]).

## Stop policies

`spec.stopPolicy` can be set to `Hold` or `HoldAndDrain` to halt admission (and optionally evict admitted workloads). Useful for planned maintenance.

**Fixed: `HoldAndDrain` skipped Workloads of held or deleted LocalQueues (pr-16728).** Two gaps let admitted Workloads keep running after their ClusterQueue switched to `HoldAndDrain` (source: pr-16728.md, raw/kueue/pkg/controller/core/workload_controller.go, raw/kueue/pkg/cache/queue/manager.go):

- The Workload reconciler resolved the ClusterQueue through the queue manager, which drops held and deleted LocalQueues, so the lookup returned `""` and `reconcileOnClusterQueueActiveState` never evicted. `Manager.ClusterQueueNameForWorkloadWithoutLock` now returns `status.admission.clusterQueue` for any Workload with a quota reservation.
- For a **deleted** LocalQueue, the ClusterQueue event handler never enqueued the Workload, because `queueReconcileForWorkloadsOfClusterQueue` found Workloads only through existing LocalQueues. It now also lists Workloads by the `status.admission.clusterQueue` index (`indexer.WorkloadClusterQueueKey`) and enqueues them; a List error is only logged, since it reads the informer cache.

Release note: "Fixed a bug where setting a ClusterQueue's `stopPolicy` to `HoldAndDrain` did not evict admitted Workloads whose LocalQueue was held or deleted." Main merged 2026-10-20; backports pr-17480 (0.20) and pr-17479 (0.19) merged the same day, after v0.20.2 / v0.19.9.

## Finalizer (`kueue.x-k8s.io/resource-in-use`)

A CQ carries a finalizer that is only removed once the CQ has no Workloads holding quota in it (the cache's `ClusterQueueEmpty`). The finalizer drop is driven by the CQ reconciler, which re-checks emptiness every time it is enqueued.

The scheduler can also create a transient race: when admission fails, the scheduler removes the assumed Workload from its in-memory cache. If it forgets to nudge the CQ reconciler after that cleanup, the CQ may stay stuck with the finalizer indefinitely after the user deletes all Workloads and LQs in a narrow window (deleting Workloads while they are evicting, then deleting the LQ shortly after). [[pr-10821]] (cherry-picked to release-0.16, release-0.17 in v0.16.7 / v0.17.2) closes the race by making the scheduler enqueue the CQ on assumed-cache cleanup so the finalizer is dropped on the next reconcile. Tracked in [[issue-10759]].

## Configuration: `quotaCheckStrategy` (alpha, v0.18)

The top-level `resources.quotaCheckStrategy` configuration field (gated behind the `QuotaCheckStrategy` feature gate) lets operators choose how strictly Kueue checks Workload requests against the CQ's declared resources. Default is the historical "all requested resources must be declared" behaviour; setting it to `IgnoreUndeclared` admits Workloads that ask for resources the CQ does not list (those resources simply don't count against quota). Introduced in v0.18.0 ([[issue-10861]] release notes; KEP linked from PR #9808).

## Common pitfalls

- **Nominal quota versus usage.** A CQ with pending workloads in one flavor blocking borrowing across flavors within the cohort is an intentional-but-tricky behavior ([[issue-1036]]). StrictFIFO amplifies this — see [[queueing-strategy]].
- **Immutable fields.** `queueingStrategy` was historically immutable to avoid re-sorting the queue mid-flight; it was made immutable and then made mutable again in v0.7 (#1934) ([[issue-1877]], [[issue-434]]).
- **Over-admission after quota change.** Removing or lowering quota on a CQ that has admitted workloads does not retroactively evict them; the CQ can be "over-nominal" until they finish ([[issue-2678]]).

## Shrinking capacity never evicts admitted Workloads

An invariant that is easy to assume but was previously untested: reducing the *effective* schedulable capacity of a cohort does **not** evict Workloads that are already admitted. [[pr-14598]] (fixes [[issue-13716]]; cherry-picks [[pr-14806]], [[pr-14807]]) pins it with four integration scenarios, each reaching reduced capacity by a different path:

1. reparenting a child [[cohort]] under a smaller root;
2. reducing an ancestor Cohort's nominal quota **below current usage**;
3. tightening `lendingLimit` on a lender Cohort while a sibling subtree holds borrowed Workloads;
4. setting `borrowingLimit: 0` on a ClusterQueue that is actively borrowing.

In all four the admitted Workloads keep running; only *future* admissions see the smaller capacity. See [[borrowing-and-lending]].

## `RejectUpdatesToCQWithInvalidOnFlavors` is Beta

The gate that makes the validating webhook reject ClusterQueue updates referencing invalid flavors in `AdmissionCheckStrategy.OnFlavors` graduated **Alpha → Beta, on by default** ([[pr-14776]]). Fix pre-existing invalid references before upgrading. See [[feature-gates]].

## Configuration: `scheduling.quotaReleaseStrategy` (removed before v0.20)

**Correction (2026-10-21)**: this section described `scheduling.quotaReleaseStrategy` (`OnTermination` default, `OnTerminalBestEffort`), the Configuration field added in `v1beta1`/`v1beta2` by [[pr-13224]] for KEP-6143. **pr-15371 reverted it** (merged 2026-09-09, ahead of the v0.20 code freeze): the field, its type, defaults, validation, tests and reference docs are gone, and no `quotaReleaseStrategy` exists in `apis/config` at this snapshot. The design moved to a **per-integration** setting (`.integrations.frameworkConfigs[].quotaReleaseStrategy`, KEP-10076 / #15146), which is **not merged** in this batch, so there is currently no released configuration knob for "hold quota until Pods are terminal" (source: pr-15371.md, raw/kueue/apis/config/).

## Related pages

- [[local-queue]] — the namespace-scoped handle users actually target.
- [[cohort]] — quota borrowing across peers.
- [[resource-flavor]] — how flavors attach to node labels.
- [[admission]] — the admission pipeline.
- [[preemption]] — what happens when a higher-priority workload needs this CQ's quota.
