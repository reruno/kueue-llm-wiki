# Cohort

**Summary**: A cohort is a group of [[cluster-queue]]s that can share unused quota with each other. Cohorts can be flat (CQs point to a cohort name) or hierarchical (cohorts have parents). The cohort is the scope in which [[fair-sharing]] and [[borrowing-and-lending]] are computed.

**Sources**: `raw/github/kubernetes-sigs__kueue/`, pr-16375.md, pr-16376.md, pr-16438.md, pr-16409.md, pr-15107.md, pr-16738.md, issue-16666.md, pr-16360.md, pr-16488.md, raw/kueue/pkg/controller/core/cohort_controller.go, raw/kueue/pkg/cache/scheduler/cache.go

**Last updated**: 2026-10-21

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
- **The queue manager is updated too (pr-16438).** After #13774 the Cohort reconciler returned early on `ErrCohortHasCycle` *before* `qManager.AddOrUpdateCohort` and no longer retried, so when another Cohort later resolved the cycle the queue manager's tree no longer matched the cache and freeing quota could skip requeueing ClusterQueues now in the same tree (only an incidental CQ status update repaired it). Now the reconciler records the new parent in the queue manager (which tolerates cycles) and notifies watchers before returning; only consumers that need a valid tree (metrics resync) are skipped. Backports pr-17079 (0.20), pr-17080 (0.19), merged after v0.20.1/v0.19.8.

**Correction (2026-10-21)**: [[cache-architecture]] described a cycle as "rejected". It is not rejected by the cache; it is recorded and surfaced as `CohortCycleDetected` on the affected ClusterQueues.

## Effective quota on a Cohort (DQO, Alpha)

With gate `DynamicQuotaOrchestration`, a Cohort's `status.effectiveQuotas.resourceGroups` replaces `spec.resourceGroups` for the scheduler cache (`resourcegroups.EffectiveCohortResourceGroups`), and the Cohort reconciler re-processes a Cohort when its effective resource groups change; clearing `status.effectiveQuotas` restores the spec quotas (source: pr-15107.md). See [[dynamic-quota-orchestration]].

## Lendable capacity and fair-share weight

The cache keeps each Cohort's lendable capacity (`resourceNode.Lendable`) next to `SubtreeQuota` so [[fair-sharing]] does not recompute it per preemption candidate (#15955; pr-16360/pr-16361). A Cohort with `fairSharing.weight: 0` that borrows has share `+Inf` (status `MaxInt64`, gauge NaN), including when it borrows only resources with nothing lendable (pr-16488).

## Borrowing inside a sub-cohort is not borrowing from outside

In fair-sharing preemption a candidate ClusterQueue counts as a borrower of a contested flavor-resource only if it **and every Cohort up to the lowest common ancestor with the preemptor** borrow that flavor-resource (`candidateBorrowsFromLCA`). A leaf CQ with zero local quota that borrows from a sibling inside a sub-cohort that is within its own quota is therefore not preemptable by an outside preemptor (issue-16666, fixed by pr-16738). See [[fair-sharing#Candidate ClusterQueues are pruned by the *contested* flavor-resources (pr-16738)]].

## Related pages

- [[cluster-queue]] — member of a cohort.
- [[borrowing-and-lending]] — how idle capacity moves around.
- [[fair-sharing]] — how "fair" is computed across cohort members.
- [[preemption]] — reclaiming borrowed quota.
- [[dynamic-quota-orchestration]] — `status.effectiveQuotas` on Cohorts.
- [[cache-architecture]] — hierarchy manager and cycle handling.
