# Preemption

**Summary**: When a pending [[workload]] can't fit with currently available quota, Kueue may evict one or more admitted workloads to free capacity. Preemption has three distinct triggers: within the same [[cluster-queue]] (priority-driven), reclaim within [[cohort]] (a CQ wants its own nominal quota back), and preemption-while-borrowing (an above-threshold borrower is displaced by a lower-priority reclaimer).

**Sources**: `raw/github/kubernetes-sigs__kueue/`, pr-16167.md, pr-16130.md, pr-16208.md, issue-16049.md, issue-14608.md, pr-17010.md, pr-16343.md, pr-16738.md, pr-16537.md, pr-16619.md, pr-16627.md, pr-17016.md, pr-17034.md, pr-17285.md, pr-16340.md, pr-17295.md, pr-17296.md, issue-16338.md, pr-17081.md, pr-17394.md, pr-17403.md, issue-10824.md, pr-16766.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, raw/kueue/CHANGELOG/CHANGELOG-0.19.md, raw/kueue/pkg/cache/scheduler/candidate_order_cache.go, raw/kueue/pkg/scheduler/preemption/classical/cache_candidate_generator.go, raw/kueue/pkg/scheduler/preemption/preemption.go, raw/kueue/pkg/scheduler/flavorassigner/flavorassigner.go

**Last updated**: 2026-10-21

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

After the scheduler issues preemptions for a workload it records the targets in an in-memory `preemptionExpectations` map and will not re-issue the same preemption until it observes the eviction (this is the "Preemption already issued, waiting for observation" behaviour). Because admission is *asynchronous*, an admitted workload that was never removed from `preemptionExpectations` could wedge a whole ClusterQueue: the eviction of a lower-priority victim gets overwritten by a lagging Server-Side-Apply admission patch (which omits the `Evicted` condition), so the preemptor waits forever (head-of-line blocking) or, alternatively, the goroutine admits an already-evicted workload with no quota check (oversubscription). This was a confirmed production outage ([[issue-11480]], fixed in [[pr-11502]]; manual cherry-picks [[pr-11648]]/0.17, [[pr-11647]]/0.16, shipped in v0.17.4 / v0.16.9). The fix guarantees a workload is dropped from `preemptionExpectations` once it becomes Admitted. Full mechanics on [[scheduler-internals#Admitted workloads must leave `preemptionExpectations`]].

## Preemptor tracking on the ClusterQueue

A ClusterQueue records the Workload that most recently issued preemption as its `preemptorWorkload`, together with the `.metadata.generation` at which it was evaluated. `cq.IsPreemptor(wl)` requires a **strict generation match**, so a Workload that has since been modified stops being the tracked preemptor. Under the Alpha `PrioritizePreemptorWorkloads` gate this drives iterator ordering and lets the preemptor lock freed quota — and its TAS topology domains — into the cycle snapshot while it waits for staggered evictions. Full mechanism in [[scheduler-internals#Preemptor prioritization]] ([[pr-13797]]).

## Fair-sharing preemption changes

See [[fair-sharing]] for: the `AlmostLCA` correction to how the two strategies are described, the `+Inf` dominant-resource-share tournament skip, the `FairSharingReevaluatePreemptionCandidates` re-run (Alpha/off in 0.20; Beta/on at 0.21 on main since pr-17285), and these loop fixes:

- **Correction (2026-10-21)**: this page said the fair-sharing infinite preemption loop [[issue-14543]] "remains open". It is fixed by pr-16343 (gate `FairSharingVerifyFinalTargets`, Beta/on; shipped v0.20.1 and v0.19.8): after fill-back, every cross-CQ target must still satisfy a fair-sharing strategy against the final simulated state, otherwise the target set is discarded ([[fair-sharing#Final-target verification stops the "own-workload" preemption loop (`FairSharingVerifyFinalTargets`)]]).
- pr-16738 (fixes issue-16665 and issue-16666) prunes candidate ClusterQueues/Cohorts that do not borrow the **contested** flavor-resources, along the path to the LCA with the preemptor ([[fair-sharing#Candidate ClusterQueues are pruned by the *contested* flavor-resources (pr-16738)]]).
- **Update (2026-10-21)**: issue-17022 (a loop caused by `FairSharingPreemptWithinNominal` and the admission tournament disagreeing on "within nominal") is fixed by pr-17034: the nominal-first shortcut now requires the preemptor CQ not to borrow **any** requested flavor-resource, not only the contested ones (`queueWithinNominalInRequestedResources`). Backports pr-17349 (0.20) and pr-17390 (0.19) merged after v0.20.2 / v0.19.9 ([[fair-sharing#Fixed: preemption loop from partial borrowing (issue-17022, pr-17034)]]).

## Target selection sizes the preemptor from the assignment (v0.20, cherry-picked to 0.19/0.18)

Entry points: the scheduler calls `Preemptor.GetPreemptionStrategyIterator` and then `GetTargetsWithStrategy`, which runs the internal `getTargets` loop. The old public `Preemptor.GetTargets` (left only for tests after #16000) was removed by pr-16537 (backport pr-16594 to 0.20). Each `PreemptionStrategy` carries its candidate iterator, `allowBorrowing`, the shared `preemptionCtx`, and an optional `verify` callback that runs after fill-back (used by fair sharing) (source: pr-16537.md, raw/kueue/pkg/scheduler/preemption/preemption.go). The shared candidate-ordering helpers moved from package `pkg/scheduler/preemption/common` to `pkg/scheduler/preemption/policy` (pure rename for the revive `package-naming` lint, pr-16619; backports pr-16803/0.20, pr-16804/0.19).

`getTargets` decides how many victims are needed by asking `workloadFits` (quota **and**, for TAS, topology) after removing candidates one by one, then `fillBackWorkloads` re-adds any victim that turned out unnecessary. The amount it must fit is `workloadUsage.Quota.Assigned = assignment.TotalRequestsFor(wl)`. pr-16167 (fixes issue-16142; backports pr-16200, pr-16201) changed that request to be built from the **assignment being admitted**, not the raw Workload spec: it uses the *assigned PodSet counts* (so partially admitted Workloads and workload-slice replacements are sized by what will actually be admitted) and **includes `pods`** when the ClusterQueue has quota for `pods`. A Workload that already holds a reservation may already carry `pods` in its requests, so it is not added twice. Symptom before the fix: too few (or the wrong) victims for pods-bound or partially-admitted elastic Workloads. `TotalRequestsFor` is used only by preemption target selection. PodSets missing from the assignment or from the replaced slice are now logged at V(1) instead of silently skipped (pr-16290).

The `frsNeedPreemption` set (flavor/resources whose assignment mode is `Preempt`) restricts candidates to Workloads actually using those flavor-resources (`classical.WorkloadUsesResources`).

## Classical preemption reuses a per-cycle candidate ordering (`ClassicalPreemptionCandidateOrderCache`)

**Problem (issue-16338).** Every preemptor and every flavor probe built the full classical candidate list and ran `slices.SortFunc` over it, although within one scheduling cycle a ClusterQueue's candidates sort the same way each time and usually only a few are consumed. Flame graphs at scale showed sorting as the hotspot (source: issue-16338.md).

**Mechanism (pr-16340).** With the gate on, `NewCandidateIterator` returns a `cacheCandidateIterator` instead of the flat sorted list (source: raw/kueue/pkg/scheduler/preemption/classical/candidate_generator.go):

- `Snapshot.CandidateOrder()` lazily creates a `CandidateOrderCache` scoped to the **snapshot (one cycle)**. Per ClusterQueue it stores the CQ's workloads sorted by the preemption `CandidatesOrdering`, their key set, and the length of the evicted prefix (evicted workloads must sort first; found with `sort.Search`). One entry is shared by all preemptors: the preemptor-dependent inputs of the ordering are equal for any two workloads of the same CQ, so they do not change the intra-CQ order (source: raw/kueue/pkg/cache/scheduler/candidate_order_cache.go).
- Reuse rule (`matches`): an entry is valid while the CQ's current workloads are a **subset** of the cached keys. Inside one cycle the scheduler only removes and restores existing snapshot workloads, never adds keys or replaces values, so a subset can reuse the original order. Missing entries are built concurrently with `Warm` (`parallelize.Until`).
- Candidates are produced lazily by a k-way merge over per-CQ buckets in **6 fixed segments**, consumed in order: evicted hierarchy, evicted priority, evicted same-queue, then the same three for non-evicted workloads. You pay only for the candidates actually consumed (source: raw/kueue/pkg/scheduler/preemption/classical/cache_candidate_generator.go).
- Ordering and semantics are meant to match the old iterator; maintainers preferred this approach over the pruning approach in #14610 for that reason (source: pr-16340.md). Fair-sharing preemption is not covered.

Benchmark from the issue (pure reclaim, 20 ClusterQueues in two child Cohorts, up to 10,000 Workloads, run with the extended performance scheduler from pr-16463): v0.20-rc.1 managed 18 to 36 scheduling ops/s, the cache raised it to 104 to 117 ops/s (source: issue-16338.md).

**Gate.** `ClassicalPreemptionCandidateOrderCache`: on **main** it is registered **Beta, default on, at 0.21**. The backports pr-17296 (release-0.20) and pr-17295 (release-0.19), merged 2026-10-16 (after v0.20.2 / v0.19.9), register it as **Alpha, default off** (source: raw/kueue/pkg/features/kube_features.go, pr-17295.md, pr-17296.md, pr-16340.md). Turning the gate off restores the old sort-per-preemptor iterator.

## `TryNextFlavor` with ghost quota falls back to preemption (issue-10824)

The scenario: a ClusterQueue with several TAS flavors and `flavorFungibility.whenCanPreempt: TryNextFlavor`. The Workload needs preemption on flavor 1, so the assigner moves to flavor 2, which has free nominal quota but no reachable topology capacity (for example a cordoned node, "ghost quota"). TAS placement on flavor 2 fails, and nothing re-entered the flavor search to retry flavor 1 with preemption, so the Workload stayed Pending with `topology "<t>" doesn't allow to fit any of N pod(s)` while preemptable lower-priority Workloads kept running on flavor 1 (source: issue-10824.md).

It is fixed by the set-based flavor tracking of pr-16766: flavor 2 is recorded in `FlavorScanState.TriedFlavors`, so a later cycle skips it and the assigner falls back to `Preempt` mode on flavor 1, preempting the lower-priority Workload there ([[scheduler-internals#Flavor scan progress across cycles (`FlavorScanState`)]]). This needs `FlavorFungibilityPreserveScanProgress` (Beta, on, v0.20). pr-17081 (main; backports pr-17394/0.20 and pr-17403/0.19, all merged 2026-10-19, release note NONE) only adds coverage: flavorassigner unit cases and an integration test that cordons the second flavor's node and expects preemption plus admission on the first flavor. The behaviour itself shipped with pr-16766's backports in v0.20.2 (#17070) and v0.19.9 (#17072) (source: pr-17081.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, CHANGELOG-0.19.md). TAS details are on [[topology-aware-scheduling]].

## Configurable preemptions (Alpha, v0.20)

A ClusterQueue that references a cluster-scoped `PreemptionConfig` (annotation `kueue.x-k8s.io/preemption-config-name`, gate `ConfigurablePreemptions`) gets extra fallback candidates after the classical or fair-sharing candidates are exhausted, with new eviction reason `ConfigurablePreemption`. Details on [[configurable-preemptions]].

## Fixed: classical preemption within a borrowing ClusterQueue (#16060)

**Correction (2026-10-21)**: this was listed as an open limitation. issue-16049 is now closed by #16060 (main, merged 2026-10-09). Backports: release-0.20 pr-17010, **shipped in v0.20.2**; release-0.19 pr-17016 (merged 2026-10-14; the first attempt pr-17009 was closed), **shipped in v0.19.9** (source: raw/kueue/CHANGELOG/CHANGELOG-0.20.md, CHANGELOG-0.19.md, pr-17016.md).

The symptom: with `withinClusterQueue: LowerPriority`, `reclaimWithinCohort: Any` and `borrowWithinCohort.policy: Never`, a high-priority Workload in a CQ that would need to **borrow** never preempted a lower-priority Workload of its *own* CQ, because `fitsResourceQuota` only simulated preemption when the request fit nominal quota, the hierarchy allowed reclaim, or `canPreemptWhileBorrowing()` was true; otherwise it returned `NoFit` (source: issue-16049.md).

Now `fitsResourceQuota` has a last branch: if `withinClusterQueue` is set and not `Never` (`canPreemptWithinClusterQueue()`), it runs `oracle.SimulatePreemption`; if that finds candidates the flavor gets `Preempt` mode, otherwise it stays `NoFit` "so the Workload doesn't hold capacity in the cohort". The user docs now list a third eligibility condition: "`withinClusterQueue` preemption is enabled and there are preemption candidates in the same ClusterQueue" (source: raw/kueue/pkg/scheduler/flavorassigner/flavorassigner.go, pr-17010.md). Release note: "Scheduling: Fixed a bug where a Workload that needed to borrow quota could not preempt Workloads in its own ClusterQueue, even when withinClusterQueue allowed preemption."

## Preemption-gated Workloads report `PreemptionGated` (pr-16627)

When a Workload is in `Preempt` mode but its preemption gate is closed (MultiKueue orchestrated preemption, [[multikueue-orchestrated-preemption]]), `requeueAndUpdate` used to overwrite its `updated` flag with the result of `SetBlockedOnPreemptionGatesCondition`; once `BlockedOnPreemptionGates` was already set, the `QuotaReserved` and `status.resourceRequests` changes in the same patch were dropped. Fixing that exposed a status loop, because the scheduler wrote reason `AdmissionGated`, which the workload controller rewrites to `PendingEvaluation`. Now the flag is only set when the gate condition changes, and the `QuotaReserved=False` reason is **`PreemptionGated`**, which the workload controller preserves. Shipped v0.20.1 (pr-16699) and v0.19.8 (pr-16761) (source: pr-16627.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md).

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
