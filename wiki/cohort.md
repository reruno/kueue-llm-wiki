# Cohort

**Summary**: A cohort is a group of [[cluster-queue]]s that can share unused quota with each other. Cohorts can be flat (CQs point to a cohort name) or hierarchical (cohorts have parents). The cohort is the scope in which [[fair-sharing]] and [[borrowing-and-lending]] are computed.

**Sources**: `raw/github/kubernetes-sigs__kueue/`, pr-16375.md, pr-16376.md, pr-16438.md, pr-16409.md, pr-15107.md, pr-16738.md, issue-16666.md, pr-16360.md, pr-16488.md, pr-17079.md, pr-17080.md, pr-17346.md, pr-17404.md, pr-17407.md, pr-16630.md, pr-13307.md, pr-17798.md, pr-17851.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, raw/kueue/CHANGELOG/CHANGELOG-0.19.md, raw/kueue/pkg/controller/core/cohort_controller.go, raw/kueue/pkg/cache/scheduler/cache.go, pr-17957.md, pr-18078.md, pr-18314.md, pr-18486.md, pr-18594.md

**Last updated**: 2026-11-24

---

## Flat cohorts

In the original design, a cohort was just a string: any ClusterQueue that set `spec.cohort: "team-alpha"` joined that cohort implicitly, and all such CQs could lend/borrow amongst themselves. No explicit `Cohort` object existed.

## Hierarchical cohorts

Later work added a first-class `Cohort` CRD with an optional parent reference, so cohorts form a tree. Borrowing is evaluated bottom-up: a CQ first tries its parent cohort, then that cohort's parent, and so on, subject to each level's `resourceGroups` limits ([[issue-3644]], [[issue-3583]]).

Hierarchical cohorts complicate preemption: the "cohort to reclaim from" is not obvious when multiple levels are in play. Issues like "Preemption only fetches candidates of ClusterQueue's parent Cohort" ([[issue-3583]]) and "Priority is not respected and causes non-deterministic preemption using hierarchical cohort with fair sharing" ([[issue-10131]]) track the edge cases.

## What cohort does and doesn't do

- **Does** let a CQ that's using less than its nominal quota lend that headroom to sibling CQs that are over-nominal — see [[borrowing-and-lending]].
- **Does** provide the scope for [[fair-sharing]] if enabled; fair-share weights and usage are computed across cohort members.
- **Does** provide a target for [[preemption]] reclaim — when a CQ needs to admit a workload using its nominal quota that's currently lent out, Kueue preempts borrowers in the same cohort ([[issue-1874]]).
- **Does not** guarantee borrowing. A `borrowingLimit` on a CQ caps how much it can borrow. A `lendingLimit` on a CQ caps how much it will lend.
- **Does not** mix resource types that aren't modeled in both CQs' `resourceGroups`. Borrowing is evaluated per resource group.

## Subtree borrowing

Fair-sharing and subtree borrowing across hierarchy levels had a bug where subtree borrowing was ignored during scheduling ([[issue-10615]]); that's the kind of subtle accounting issue that hierarchical cohorts introduce. Tests around cohort metrics reliability are also ongoing ([[issue-10195]], [[issue-10417]]).

## Cycles in the Cohort hierarchy

A Cohort update can make the parent chain cyclic (e.g. swapping two Cohorts' parents in two steps). Current behaviour (source: pr-16375.md, pr-16438.md, raw/kueue/pkg/controller/core/cohort_controller.go, raw/kueue/pkg/cache/scheduler/cache.go):

- **The cache applies the new parent anyway** and `AddOrUpdateCohort` returns `ErrCohortHasCycle`; it re-evaluates ClusterQueues when a cohort becomes or stops being cyclic.
- **ClusterQueues under the cycle become inactive** with `Active=False`, reason **`CohortCycleDetected`**, message `Cohort "<name>" has a cycle in hierarchy`; the Cohort reconciler notifies affected CQs through `ClusterQueueReconciler.NotifyCohortUpdate` / `Cache.ClusterQueuesUsingCohort`. While the cycle exists, CQ usage changes are applied to the CQ's own node only, because the recursive `addUsage`/`removeUsage` would loop forever through `parentHRN()`; ancestor usage is rebuilt when the cycle is resolved. The cache does not compute fair-sharing stats for a CQ whose parent chain is cyclic. This is #13774 ("Fixed a possible controller hang after an invalid Cohort hierarchy cycle update"), v0.20.0, backported in pr-16375 (0.18, v0.18.11) and pr-16376 (0.19, v0.19.7). Integration coverage: "Hierarchical Cohorts - t4 cohort cycle detection" (#15933; backports pr-16409, pr-16410).
- **The queue manager is updated too (pr-16438).** After #13774 the Cohort reconciler returned early on `ErrCohortHasCycle` *before* `qManager.AddOrUpdateCohort` and no longer retried, so when another Cohort later resolved the cycle the queue manager's tree no longer matched the cache and freeing quota could skip requeueing ClusterQueues now in the same tree (only an incidental CQ status update repaired it). Now the reconciler records the new parent in the queue manager (which tolerates cycles) and notifies watchers before returning; only consumers that need a valid tree (metrics resync) are skipped. Backports pr-17079 (0.20), pr-17080 (0.19), merged after v0.20.1/v0.19.8 and **shipped in v0.20.2 and v0.19.9** ("Scheduling: Fixed a bug that could prevent ClusterQueues in the same tree from requeueing workloads when quota became available after a Cohort cycle was resolved.") (source: raw/kueue/CHANGELOG/CHANGELOG-0.20.md, CHANGELOG-0.19.md).

**Correction (2026-10-21)**: [[cache-architecture]] described a cycle as "rejected". It is not rejected by the cache; it is recorded and surfaced as `CohortCycleDetected` on the affected ClusterQueues.

## Cohorts are cached on every replica (pr-17346)

Since pr-17346 the Cohort controller's `Create`/`Update`/`Delete` event handlers update the scheduler cache and queue manager on **every replica**, like the ClusterQueue and ResourceFlavor handlers; `Reconcile` (leader only) repeats the same idempotent update and owns status, ClusterQueue notifications and metrics. Before, a follower that took over leadership had no explicit Cohorts (and so none of their quota) for up to one lease duration, so borrowing ClusterQueues could not admit and subtrees were detached. An update event only touches the cache when `spec` or the effective Cohort resource groups changed. A cyclic parent is still recorded in both the cache and the queue manager. Release note: "Cohorts are now kept in the scheduler cache on every replica, so a replica that takes over leadership can admit from Cohort quota right away." Backports pr-17404 (0.20) and pr-17407 (0.19), merged after v0.20.2 / v0.19.9. The Cohort source is also one of those the scheduler waits on at startup (pr-16630). See [[cache-architecture#Initial-sync barrier and Cohorts on every replica]] (source: pr-17346.md, raw/kueue/pkg/controller/core/cohort_controller.go).

## Effective quota on a Cohort (DQO, Alpha)

With gate `DynamicQuotaOrchestration`, a Cohort's `status.effectiveQuotas.resourceGroups` replaces `spec.resourceGroups` for the scheduler cache (`resourcegroups.EffectiveCohortResourceGroups`), and the Cohort reconciler re-processes a Cohort when its effective resource groups change; clearing `status.effectiveQuotas` restores the spec quotas (source: pr-15107.md). See [[dynamic-quota-orchestration]].

## Lendable capacity and fair-share weight

The cache keeps each Cohort's lendable capacity (`resourceNode.Lendable`) next to `SubtreeQuota` so [[fair-sharing]] does not recompute it per preemption candidate (#15955; pr-16360/pr-16361). A Cohort with `fairSharing.weight: 0` that borrows has share `+Inf` (status `MaxInt64`, gauge NaN), including when it borrows only resources with nothing lendable (pr-16488).

## Borrowing inside a sub-cohort is not borrowing from outside

In fair-sharing preemption a candidate ClusterQueue counts as a borrower of a contested flavor-resource only if it **and every Cohort up to the lowest common ancestor with the preemptor** borrow that flavor-resource (`candidateBorrowsFromLCA`). A leaf CQ with zero local quota that borrows from a sibling inside a sub-cohort that is within its own quota is therefore not preemptable by an outside preemptor (issue-16666, fixed by pr-16738). See [[fair-sharing#Candidate ClusterQueues are pruned by the *contested* flavor-resources (pr-16738)]].

## A Cohort's own nominal quota gives its descendants a preemption claim (pr-13307)

With fair sharing and `FairSharingPreemptWithinNominal` (Beta, on), the "within nominal, bypass DRS" preemption claim is evaluated at the preemptor's `AlmostLCA` with each target. If that node is a Cohort, it is within nominal when its usage does not exceed its `SubtreeQuota` (own `nominalQuota` plus lendable child quota) for every flavor-resource the incoming Workload requests. Descendants of a Cohort therefore get preferential access to that Cohort's quota against outside borrowers, even when the Cohort borrows on an unrelated flavor. Conversely, a ClusterQueue within its own nominal quota has no claim against a target reached through a **borrowing** parent Cohort. Main 2026-10-27; backports pr-17798 (0.20) and pr-17851 (0.19) pending the next patch (source: pr-13307.md, pr-17798.md, pr-17851.md). See [[fair-sharing#Nominal claim is evaluated at the AlmostLCA with each target (pr-13307, fixes #9466)]].

## Notification and requeue behaviour (v0.21 main)

- A Cohort reconcile notifies its ClusterQueues only when the Cohort was created or its spec/quotas changed, or (with fair sharing) a CQ under it was created, deleted or had spec/quota changes; a CQ status write alone no longer re-sweeps the tree. With fair sharing the whole tree is enqueued since weighted share divides by the tree's lendable quota (source: pr-17957.md).
- `kueue_cohort_subtree_admitted_active_workloads` with `CustomMetricLabels`: each series counts only the CQs whose label values match; relabeling a CQ under the same parent moves its count at once via incremental per-label counts in the Cohort; an old series is deleted only when its last contributing CQ leaves (source: pr-18078.md, pr-18486.md; see [[metrics]]).

## DQO handoff between subtrees (Alpha)

A ClusterQueue or Cohort moving between two active DynamicQuotaOrchestrator subtrees kept its `orchestratorRef`, making the destination DQO report `EffectiveQuotasConflict` for the whole subtree. The destination may now take over once the previous DQO's resolved subtree no longer covers the target (also when the previous DQO changes root). Foreign owners are protected; missing roots, missing targets and cycles are treated conservatively; a referenced Cohort without an object is an implicit root. Membership uses the controller cache, so an in-flight reconcile may briefly use an older view; an object moved outside every eligible DQO subtree keeps its last effective quota (source: pr-18594.md).

Opt-in expiration: `spec.capacityDistribution.effectiveQuotasTTLSeconds` on the DQO (60 to 604800, no default) makes the DQO write `status.effectiveQuotas.expirationTime` (now + TTL on each successful distribution; kept while the quota is unchanged and more than half the TTL remains). ClusterQueue and Cohort controllers set condition `EffectiveQuotaActive` (`True` reason `Issued`/`Renewed`, `False` reason `Expired`) and requeue at `expirationTime`; cache, queue manager, metrics and the MultiKueue capacity provider fall back to `spec.resourceGroups` only when the condition is `False` (they read the condition, not the clock). Cohort also gains `status.conditions` (source: pr-18314.md).

## Related pages

- [[cluster-queue]] — member of a cohort.
- [[borrowing-and-lending]] — how idle capacity moves around.
- [[fair-sharing]] — how "fair" is computed across cohort members.
- [[preemption]] — reclaiming borrowed quota.
- [[dynamic-quota-orchestration]] — `status.effectiveQuotas` on Cohorts.
- [[cache-architecture]] — hierarchy manager and cycle handling.
