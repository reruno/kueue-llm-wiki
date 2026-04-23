# Preemption

**Summary**: When a pending [[workload]] can't fit with currently available quota, Kueue may evict one or more admitted workloads to free capacity. Preemption has three distinct triggers: within the same [[cluster-queue]] (priority-driven), reclaim within [[cohort]] (a CQ wants its own nominal quota back), and preemption-while-borrowing (an above-threshold borrower is displaced by a lower-priority reclaimer).

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

---

## The three triggers

Before they were distinguished in condition messages and metrics, all preemptions said the same generic thing — which made diagnosis painful ([[issue-1874]]). They are now separate reasons:

1. **Within ClusterQueue.** A higher-priority workload arrives; a lower-priority admitted workload in the same CQ is evicted to make room. Policy: `spec.preemption.withinClusterQueue` (`LowerPriority` | `Any` | `Never`).
2. **Reclaim within Cohort.** CQ-A lent quota to CQ-B. CQ-A has a new workload that needs that nominal quota back. A workload in CQ-B is preempted, regardless of priority. Policy: `spec.preemption.reclaimWithinCohort` (`LowerPriority` | `Any` | `Never`).
3. **Preemption while borrowing (`borrowWithinCohort`).** A borrower in CQ-A wants to displace a borrower in CQ-B that is below a priority threshold. Policy: `spec.preemption.borrowWithinCohort.policy` (`Never` | `LowerPriority`), with `maxPriorityThreshold` setting the cap. `LowerPriorityBorrowersOnly` was added to protect nominal-quota workloads from this path ([[issue-10171]]).

## How candidates are chosen

For each trigger, the scheduler gathers a candidate set (admitted workloads that, if evicted, would free enough quota), then picks a minimal subset ordered by lowest priority / most-recently-admitted. Workloads above priority threshold (for borrowWithinCohort) are excluded.

For TAS, preemption must free not just aggregate quota but a specific topology domain — this is more constrained ([[issue-10497]] — TAS preemption can under-select candidates needed to free a topology domain). See [[topology-aware-scheduling]].

## What eviction looks like on the victim

An evicted Workload:

1. Gets `status.conditions.Evicted=True` with a reason identifying the trigger.
2. Has `status.admission` cleared.
3. Integration controller re-suspends the underlying job; Pods are deleted.
4. Quota is released.
5. Workload is requeued with backoff (per `requeuingStrategy`), or deactivated if eviction count exceeds the limit ([[issue-2174]]).

## Priority-sorting-within-cohort vs fair-share

When fair-sharing is enabled, priority-based preemption interacts non-trivially. Fair-share may select a victim CQ without regard to workload priorities within it; combined with hierarchical cohorts this has produced non-deterministic preemption ([[issue-10131]]). The `PrioritySortingWithinCohort` flag controls the older path; interactions with `borrowWithinCohort` have caused infinite preemption loops ([[issue-2821]]).

## Overadmission

Preemption accounting must stay consistent with quota: if a CQ's quota is reduced while workloads are admitted, Kueue cannot retroactively evict them — they "overadmit" until they finish ([[issue-2678]] — overadmission after deleting resource from a borrowing CQ). Similarly, unexpected preemption between CQs in a cohort is usually an accounting edge case ([[issue-3210]]).

## Related pages

- [[admission]] — preemption happens during the scheduling cycle.
- [[cluster-queue]] — preemption policies live on the CQ.
- [[cohort]] — reclaim target.
- [[fair-sharing]] — alternate ordering that interacts with preemption.
- [[borrowing-and-lending]] — borrowing is the precondition for reclaim.
