# Borrowing and lending

**Summary**: Within a [[cohort]], a [[cluster-queue]] that's below its nominal quota can lend its headroom to a sibling that's above. The lending CQ can reclaim it at any time via [[preemption]]. Per-CQ `borrowingLimit` and `lendingLimit` cap how much can move.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

---

## Nominal, borrowed, lent

- **Nominal quota** — configured in `ClusterQueue.spec.resourceGroups[].flavors[].resources[].nominalQuota`. The CQ's guaranteed floor.
- **Borrowed** — the CQ is using more than its nominal quota because siblings have headroom.
- **Lent** — the CQ is using less than its nominal quota; siblings may borrow the difference.

## Limits

- `borrowingLimit` (per resource) caps how much a CQ can consume *above* its nominal. `nil` means unlimited; `0` disables borrowing.
- `lendingLimit` caps how much of the CQ's nominal quota can be loaned out. Without a lending limit, the entire nominal is available for siblings; with a limit, some of the nominal is "protected" and can't be borrowed even if idle.

## When reclaim happens

If CQ-A is lending and a new workload arrives at CQ-A needing that nominal quota, the scheduler preempts borrowers in the cohort to free it ([[issue-1149]] — reclaim consumed resources once quit from cohort; [[issue-1337]] — support preemption while borrowing). This is the "reclaim within cohort" preemption trigger described in [[preemption]].

## Fungibility across flavors

Within a CQ, `flavorFungibility` controls what to try first when a flavor is full: the next flavor in the list, or preemption in the current one, or borrowing from the cohort. Mis-interactions with preemption and borrowing are well-represented in the issue tracker ([[issue-1344]], [[issue-2560]]).

## Blocking: one CQ blocks the cohort

A pending workload at the head of a StrictFIFO CQ can block borrowing by other flavors in the cohort — because the scheduler treats the head as the next thing it's trying to satisfy ([[issue-1036]]). Whether this is desirable is situational; BestEffortFIFO avoids the block at the cost of strict ordering.

## Hierarchical cohorts

When cohorts have parents, borrowing walks up: sibling CQs in the immediate cohort first, then the parent cohort's other subtrees, subject to each level's group limits. Hierarchical borrowing math is tricky enough that dedicated validation is needed ([[issue-3644]] — HierarchicalCohort: Support validations to avoid accidental parent cohort removal).

## Monitoring

Per-CQ metrics expose `admitted_usage`, `reserved_usage`, `nominal_quota`, and borrow-specific counters; dashboards typically surface "usage / nominal" per CQ and "borrowed / lendingLimit" per pair. See [[metrics]].

## Related pages

- [[cluster-queue]] — where limits are configured.
- [[cohort]] — the scope of borrowing.
- [[preemption]] — how lent capacity is reclaimed.
- [[fair-sharing]] — an alternate policy over the same borrowing substrate.
