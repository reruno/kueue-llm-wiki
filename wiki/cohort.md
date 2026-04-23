# Cohort

**Summary**: A cohort is a group of [[cluster-queue]]s that can share unused quota with each other. Cohorts can be flat (CQs point to a cohort name) or hierarchical (cohorts have parents). The cohort is the scope in which [[fair-sharing]] and [[borrowing-and-lending]] are computed.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

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

## Related pages

- [[cluster-queue]] — member of a cohort.
- [[borrowing-and-lending]] — how idle capacity moves around.
- [[fair-sharing]] — how "fair" is computed across cohort members.
- [[preemption]] — reclaiming borrowed quota.
