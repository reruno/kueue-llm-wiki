# Fair sharing

**Summary**: Fair sharing (KEP-1714) is an optional admission policy that distributes unused [[cohort]] capacity across ClusterQueues in proportion to configured weights, DRF-style. Without it, first-come-first-served + nominal quota is the rule; with it, a noisy CQ borrowing heavily cannot starve its siblings.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

---

## Motivation

With borrowing enabled, a CQ that consistently has demand will tend to consume the cohort's idle capacity faster than a bursty sibling. Over time this looks unfair — the bursty sibling can't get its "fair share" of the shared headroom. Fair sharing formalizes what "fair share" means so the scheduler can rebalance.

The KEP-1714 PR ([[pr-1773]]) defines the formal model; subsequent work extends it to hierarchical cohorts.

## How it works

Each ClusterQueue gets a `fairSharing.weight` (default 1). The cohort's idle capacity is divided across members in proportion to weight. A CQ whose *consumption / weight* is lowest among siblings is preferred when admitting the next workload. This generalizes to multi-resource (dominant-resource) and to subtree weights in hierarchical cohorts.

## `FairSharingPrioritizeNonBorrowing`

A policy variant prefers admitting a workload to a CQ from its nominal quota over admitting it to a CQ that would need to borrow. Misordering between these classes caused a bug where borrowers were admitted before non-borrowers ([[issue-10126]] — Incorrect admission ordering with FairSharingPrioritizeNonBorrowing).

## Subtree accounting in hierarchical cohorts

For hierarchical cohorts, subtree borrowing has to be counted at each level of the tree. A recent bug: "Subtree borrowing ignored when scheduling" ([[issue-10615]]). Preemption under fair-sharing + hierarchy is similarly subtle: "Priority is not respected and causes non-deterministic preemption using hierarchical cohort with fair sharing" ([[issue-10131]]).

## Interaction with priority and preemption

Fair sharing picks *which CQ* gets the next admission slot. [[queueing-strategy]] and [[workload-priority]] still pick *which workload within that CQ* goes first. When fair-share decides CQ-B should go and CQ-B's head-of-queue is lower priority than CQ-A's, the lower-priority workload wins — which is surprising if you expected global priority ordering. This is intentional: fair-share is the whole point.

## Related pages

- [[cohort]] — the scope fair-share is computed over.
- [[borrowing-and-lending]] — what unused capacity means.
- [[cluster-queue]] — where `fairSharing.weight` is set.
- [[preemption]] — what fair-share triggers when a higher-share CQ wants its capacity back.
