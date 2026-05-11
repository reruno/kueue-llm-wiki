# Fair sharing

**Summary**: Fair sharing (KEP-1714) is an optional admission policy that distributes unused [[cohort]] capacity across ClusterQueues in proportion to configured weights, DRF-style. Without it, first-come-first-served + nominal quota is the rule; with it, a noisy CQ borrowing heavily cannot starve its siblings.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-05-08

---

## Motivation

With borrowing enabled, a CQ that consistently has demand will tend to consume the cohort's idle capacity faster than a bursty sibling. Over time this looks unfair — the bursty sibling can't get its "fair share" of the shared headroom. Fair sharing formalizes what "fair share" means so the scheduler can rebalance.

The KEP-1714 PR ([[pr-1773]]) defines the formal model; subsequent work extends it to hierarchical cohorts.

## How it works

Each ClusterQueue gets a `fairSharing.weight` (default 1). The cohort's idle capacity is divided across members in proportion to weight. A CQ whose *consumption / weight* is lowest among siblings is preferred when admitting the next workload. This generalizes to multi-resource (dominant-resource) and to subtree weights in hierarchical cohorts.

## Where you can set `fairSharing.weight` — CQ vs Cohort

`fairSharing.weight` lives on **both** [[cluster-queue]] (`spec.fairSharing.weight`) and [[cohort]] (`spec.fairSharing.weight`). They are not redundant; they apply at different levels of the cohort tree:

- The **cohort weight** governs how the parent cohort's headroom is split among its **child cohorts**.
- The **CQ weight** governs how a leaf cohort's headroom is split among its **child ClusterQueues**.

Reading the comparison goes top-down. At each cohort node, the iterator (`pkg/scheduler/fair_sharing_iterator.go`) computes share = consumption / weight per child and visits the lowest-share child next. Children that are themselves cohorts apply the same logic to their own children using the per-CQ (or sub-cohort) weights. If you set a weight on a CQ but leave the cohort unset, the cohort defaults to weight 1, which means peer cohorts each get an equal slice regardless of how skewed their child-CQ weights are. To make a multi-level cohort tree behave the way you expect, you generally need to set weights at **every** level you care about. ([[issue-10872]] tracks the documentation gap; the canonical implementation reference is `fair_sharing_iterator.go` lines 63–97.)

## `FairSharingPrioritizeNonBorrowing`

A policy variant prefers admitting a workload to a CQ from its nominal quota over admitting it to a CQ that would need to borrow. Misordering between these classes caused a bug where borrowers were admitted before non-borrowers ([[issue-10126]] — Incorrect admission ordering with FairSharingPrioritizeNonBorrowing).

## Subtree accounting in hierarchical cohorts

For hierarchical cohorts, subtree borrowing has to be counted at each level of the tree. A recent bug: "Subtree borrowing ignored when scheduling" ([[issue-10615]]). Preemption under fair-sharing + hierarchy is similarly subtle: "Priority is not respected and causes non-deterministic preemption using hierarchical cohort with fair sharing" ([[issue-10131]]).

### `SubtreeQuota` invalidation on cohort deletion

The cache stores per-ancestor `SubtreeQuota` values used to compute fair-share denominators and the `kueue_cohort_subtree_quota` / `kueue_cohort_subtree_resource_reservations` metrics. When a child Cohort or ClusterQueue is deleted, all of its ancestors' `SubtreeQuota` values must be recomputed in the same transaction; otherwise the next `RecordCohortMetrics` call will republish the **pre-deletion** numbers (and the scheduler will admit against stale denominators, leading to over-admission). Fixed in [[pr-10797]] (Fixes #10417 and #10771). The fix walks all ancestors of the deleted cohort and re-derives `SubtreeQuota` immediately after the cache mutation.

### Nil-pointer panic on cohort-less CQs

`fair_sharing_iterator.Iter()` has a special-case branch for a preemptor ClusterQueue that has **no parent cohort** (`!t.preemptorCq.HasParent()`). Without an explicit return at the end of that branch, control fell through to the general path and dereferenced `t.preemptorCq.Parent().Root()` — `Parent()` is nil for a cohort-less CQ, so the scheduler panicked. The bug only triggers on clusters that enable FairSharing **and** have ClusterQueues outside any cohort. [[pr-10891]] adds the missing `return` and a regression test. Released in v0.18.0.

## Interaction with priority and preemption

Fair sharing picks *which CQ* gets the next admission slot. [[queueing-strategy]] and [[workload-priority]] still pick *which workload within that CQ* goes first. When fair-share decides CQ-B should go and CQ-B's head-of-queue is lower priority than CQ-A's, the lower-priority workload wins — which is surprising if you expected global priority ordering. This is intentional: fair-share is the whole point.

## Related pages

- [[cohort]] — the scope fair-share is computed over.
- [[borrowing-and-lending]] — what unused capacity means.
- [[cluster-queue]] — where `fairSharing.weight` is set.
- [[preemption]] — what fair-share triggers when a higher-share CQ wants its capacity back.
