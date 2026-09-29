# Preemption

**Summary**: When a pending [[workload]] can't fit with currently available quota, Kueue may evict one or more admitted workloads to free capacity. Preemption has three distinct triggers: within the same [[cluster-queue]] (priority-driven), reclaim within [[cohort]] (a CQ wants its own nominal quota back), and preemption-while-borrowing (an above-threshold borrower is displaced by a lower-priority reclaimer).

**Sources**: `raw/github/kubernetes-sigs__kueue/`, pr-16167.md, pr-16130.md, pr-16208.md, issue-16049.md, issue-14608.md.

**Last updated**: 2026-09-29

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

1. Gets `status.conditions.Evicted=True` with reason `Preempted`, plus a separate `Preempted=True` condition whose reason identifies the trigger (`InClusterQueue`, `InCohortReclamation`, `InCohortFairSharing`, `InCohortReclaimWhileBorrowing`, or `ConfigurablePreemption`); both carry the same message. (source: raw/kueue/pkg/scheduler/preemption/preemption.go, raw/kueue/apis/kueue/v1beta2/workload_types.go)
2. Has `status.admission` cleared.
3. Integration controller re-suspends the underlying job; Pods are deleted.
4. Quota is released.
5. Workload is requeued with backoff (per `requeuingStrategy`), or deactivated if eviction count exceeds the limit ([[issue-2174]]).

## Priority-sorting-within-cohort vs fair-share

When fair-sharing is enabled, priority-based preemption interacts non-trivially. Fair-share may select a victim CQ without regard to workload priorities within it; combined with hierarchical cohorts this has produced non-deterministic preemption ([[issue-10131]]). The `PrioritySortingWithinCohort` flag controls the older path; interactions with `borrowWithinCohort` have caused infinite preemption loops ([[issue-2821]]).

## Overadmission

Preemption accounting must stay consistent with quota: if a CQ's quota is reduced while workloads are admitted, Kueue cannot retroactively evict them — they "overadmit" until they finish ([[issue-2678]] — overadmission after deleting resource from a borrowing CQ). Similarly, unexpected preemption between CQs in a cohort is usually an accounting edge case ([[issue-3210]]).

## The `preemptionExpectations` store

After the scheduler issues preemptions for a workload it records the targets in an in-memory `preemptionExpectations` map and will not re-issue the same preemption until it observes the eviction (this is the "Preemption already issued, waiting for observation" behaviour). Because admission is *asynchronous*, an admitted workload that was never removed from `preemptionExpectations` could wedge a whole ClusterQueue: the eviction of a lower-priority victim gets overwritten by a lagging Server-Side-Apply admission patch (which omits the `Evicted` condition), so the preemptor waits forever (head-of-line blocking) or, alternatively, the goroutine admits an already-evicted workload with no quota check (oversubscription). This was a confirmed production outage ([[issue-11480]], fixed in [[pr-11502]]; manual cherry-picks [[pr-11648]]/0.17, [[pr-11647]]/0.16, shipped in v0.17.4 / v0.16.9). The fix guarantees a workload is dropped from `preemptionExpectations` once it becomes Admitted. Full mechanics on [[scheduler-internals#Admitted workloads must leave preemptionExpectations]].

## Preemptor tracking on the ClusterQueue

A ClusterQueue records the Workload that most recently issued preemption as its `preemptorWorkload`, together with the `.metadata.generation` at which it was evaluated. `cq.IsPreemptor(wl)` requires a **strict generation match**, so a Workload that has since been modified stops being the tracked preemptor. Under the Alpha `PrioritizePreemptorWorkloads` gate this drives iterator ordering and lets the preemptor lock freed quota — and its TAS topology domains — into the cycle snapshot while it waits for staggered evictions. Full mechanism in [[scheduler-internals#Preemptor prioritization]] ([[pr-13797]]).

## Fair-sharing preemption changes

See [[fair-sharing]] for: the `AlmostLCA` correction to how the two strategies are described, the `+Inf` dominant-resource-share tournament skip, and the Alpha `FairSharingReevaluatePreemptionCandidates` re-run. A fair-sharing infinite preemption loop remains open ([[issue-14543]]).

## Target selection sizes the preemptor from the assignment (v0.20, cherry-picked to 0.19/0.18)

`Preemptor.GetTargets` decides how many victims are needed by asking `workloadFits` (quota **and**, for TAS, topology) after removing candidates one by one, then `fillBackWorkloads` re-adds any victim that turned out unnecessary. The amount it must fit is `workloadUsage.Quota.Assigned = assignment.TotalRequestsFor(wl)`. pr-16167 (fixes issue-16142; backports pr-16200, pr-16201) changed that request to be built from the **assignment being admitted**, not the raw Workload spec: it uses the *assigned PodSet counts* (so partially admitted Workloads and workload-slice replacements are sized by what will actually be admitted) and **includes `pods`** when the ClusterQueue has quota for `pods`. A Workload that already holds a reservation may already carry `pods` in its requests, so it is not added twice. Symptom before the fix: too few (or the wrong) victims for pods-bound or partially-admitted elastic Workloads. `TotalRequestsFor` is used only by `GetTargets`. PodSets missing from the assignment or from the replaced slice are now logged at V(1) instead of silently skipped (pr-16290).

The `frsNeedPreemption` set (flavor/resources whose assignment mode is `Preempt`) restricts candidates to Workloads actually using those flavor-resources (`classical.WorkloadUsesResources`).

## Configurable preemptions (Alpha, v0.20)

A ClusterQueue that references a cluster-scoped `PreemptionConfig` (annotation `kueue.x-k8s.io/preemption-config-name`, gate `ConfigurablePreemptions`) gets extra fallback candidates after the classical or fair-sharing candidates are exhausted, with new eviction reason `ConfigurablePreemption`. Details on [[configurable-preemptions]].

## Known limitation: classical preemption within a borrowing ClusterQueue

Reported and still open (issue-16049.md): with `withinClusterQueue: LowerPriority`, `reclaimWithinCohort: Any` and `borrowWithinCohort.policy: Never`, a high-priority Workload in a CQ that is **already borrowing** does not preempt a lower-priority Workload of the *same* CQ, because the attempt that keeps the CQ within nominal quota finds no candidate and the borrowing attempt is forbidden by `borrowWithinCohort: Never`. Fair-sharing preemption does not have this problem. Treat it as expected behaviour of the current classical algorithm until the issue is resolved; a `PreemptionConfig` rule with scope `WithinClusterQueue` is a workaround in Alpha.

## A rejected AdmissionCheck during eviction now deactivates

An AdmissionCheck flipping to `Rejected` while an eviction is in flight used to be dropped silently, leaving `Admitted=True` next to a `Rejected` check. See [[admission-check#A `Rejected` check during an in-flight eviction]] ([[pr-14309]]).

## Related pages

- [[admission]] — preemption happens during the scheduling cycle.
- [[cluster-queue]] — preemption policies live on the CQ.
- [[cohort]] — reclaim target.
- [[fair-sharing]] — alternate ordering that interacts with preemption.
- [[borrowing-and-lending]] — borrowing is the precondition for reclaim.
- [[configurable-preemptions]] — **[Alpha, v0.20]** cluster-scoped `PreemptionConfig` rules add fallback candidates.
- [[preemption-cost]] — **[Alpha]** external controllers can boost a workload's effective priority via annotation.
- [[multikueue-orchestrated-preemption]] — **[Alpha]** serializes preemption across MultiKueue worker clusters.
