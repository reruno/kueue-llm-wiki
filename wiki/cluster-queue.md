# ClusterQueue

**Summary**: A ClusterQueue (CQ) is a cluster-scoped resource that owns a pool of quota. It groups quota into resource groups of flavors, limits how workloads queue up, and optionally joins a [[cohort]] so unused capacity can be lent to peers.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-05-08

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

A CQ's `spec.cohort` field joins it into a [[cohort]]. CQs in the same cohort can borrow unused nominal quota from each other subject to `borrowingLimit` and `lendingLimit` ([[pr-10406]]). Hierarchical cohorts (a CQ can point at a Cohort which itself has a parent Cohort) are supported ([[issue-3644]], [[issue-3583]]) — see [[borrowing-and-lending]].

## State fields to watch

`status.flavorsReservation` and `status.flavorsUsage` are the authoritative view of what's reserved and what's actually consumed. `status.pendingWorkloads` and `status.admittedWorkloads` count head-of-queue and admitted jobs. `status.conditions` includes `Active` (the CQ is healthy, referenced flavors exist, webhooks pass).

A CQ becomes inactive if a referenced [[resource-flavor]] is missing or a referenced [[admission-check]] is not `Active` — by design ([[issue-3645]] — TAS: CQ is not deactivated when there is no Topology, which was fixed).

## Stop policies

`spec.stopPolicy` can be set to `Hold` or `HoldAndDrain` to halt admission (and optionally evict admitted workloads). Useful for planned maintenance.

## Finalizer (`kueue.x-k8s.io/cluster-queue`)

A CQ carries a finalizer that is only removed once the CQ has no Workloads or LocalQueues referencing it. The finalizer drop is driven by the CQ reconciler, which re-checks emptiness every time it is enqueued.

The scheduler can also create a transient race: when admission fails, the scheduler removes the assumed Workload from its in-memory cache. If it forgets to nudge the CQ reconciler after that cleanup, the CQ may stay stuck with the finalizer indefinitely after the user deletes all Workloads and LQs in a narrow window (deleting Workloads while they are evicting, then deleting the LQ shortly after). [[pr-10821]] (cherry-picked to release-0.16, release-0.17 in v0.16.7 / v0.17.2) closes the race by making the scheduler enqueue the CQ on assumed-cache cleanup so the finalizer is dropped on the next reconcile. Tracked in [[issue-10759]].

## Configuration: `quotaCheckStrategy` (alpha, v0.18)

The top-level `resources.quotaCheckStrategy` configuration field (gated behind the `QuotaCheckStrategy` feature gate) lets operators choose how strictly Kueue checks Workload requests against the CQ's declared resources. Default is the historical "all requested resources must be declared" behaviour; setting it to `IgnoreUndeclared` admits Workloads that ask for resources the CQ does not list (those resources simply don't count against quota). Introduced in v0.18.0 ([[issue-10861]] release notes; KEP linked from PR #9808).

## Common pitfalls

- **Nominal quota versus usage.** A CQ with pending workloads in one flavor blocking borrowing across flavors within the cohort is an intentional-but-tricky behavior ([[issue-1036]]). StrictFIFO amplifies this — see [[queueing-strategy]].
- **Immutable fields.** `queueingStrategy` was historically immutable to avoid re-sorting the queue mid-flight; the restriction was tightened and then reconsidered ([[issue-1877]], [[issue-434]]).
- **Over-admission after quota change.** Removing or lowering quota on a CQ that has admitted workloads does not retroactively evict them; the CQ can be "over-nominal" until they finish ([[issue-2678]]).

## Related pages

- [[local-queue]] — the namespace-scoped handle users actually target.
- [[cohort]] — quota borrowing across peers.
- [[resource-flavor]] — how flavors attach to node labels.
- [[admission]] — the admission pipeline.
- [[preemption]] — what happens when a higher-priority workload needs this CQ's quota.
