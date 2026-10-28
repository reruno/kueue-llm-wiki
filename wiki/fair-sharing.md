# Fair sharing

**Summary**: Fair sharing (KEP-1714) is an optional admission policy that distributes unused [[cohort]] capacity across ClusterQueues in proportion to configured weights, DRF-style. Without it, first-come-first-served + nominal quota is the rule; with it, a noisy CQ borrowing heavily cannot starve its siblings.

**Sources**: `raw/github/kubernetes-sigs__kueue/`, pr-16343.md, pr-16911.md, pr-16912.md, pr-16738.md, issue-16665.md, issue-16666.md, pr-16487.md, pr-16488.md, pr-16528.md, pr-16581.md, pr-17057.md, issue-16530.md, pr-14348.md, pr-16360.md, pr-16361.md, pr-13433.md, pr-10776.md, issue-16529.md, issue-17022.md, pr-17034.md, pr-17349.md, pr-17390.md, pr-17285.md, pr-17171.md, pr-17196.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, raw/kueue/CHANGELOG/CHANGELOG-0.19.md, raw/kueue/pkg/scheduler/preemption/preemption.go, raw/kueue/pkg/features/kube_features.go, raw/kueue/pkg/scheduler/preemption/fair_strategy.go, raw/kueue/pkg/scheduler/preemption/fairsharing/ordering.go, raw/kueue/pkg/cache/scheduler/fair_sharing.go

**Last updated**: 2026-10-28

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

The cache stores per-ancestor `SubtreeQuota` values used to compute fair-share denominators and the `kueue_cohort_subtree_quota` / `kueue_cohort_subtree_resource_reservations` metrics. When a child Cohort or ClusterQueue is deleted, all of its ancestors' `SubtreeQuota` values must be recomputed in the same transaction; otherwise the next `RecordCohortMetrics` call will republish the **pre-deletion** numbers (and the scheduler will admit against stale denominators, leading to over-admission). Fixed in [[pr-10797]] (Fixes #10417 and #10771). The fix walks all ancestors of the deleted cohort and re-derives `SubtreeQuota` immediately after the cache mutation. History: an earlier attempt (#10579) was reverted by pr-10776 (fixes #10771, a flaky cohort-deletion integration test) before pr-10797 landed (source: pr-10776.md). The precomputed `Lendable` (see Performance note) must be refreshed on the same path.

### Nil-pointer panic on cohort-less CQs

`TargetClusterQueueOrdering.Iter()` (`pkg/scheduler/preemption/fairsharing/ordering.go`) has a special-case branch for a preemptor ClusterQueue that has **no parent cohort** (`!t.preemptorCq.HasParent()`). Without an explicit return at the end of that branch, control fell through to the general path and dereferenced `t.preemptorCq.Parent().Root()` — `Parent()` is nil for a cohort-less CQ, so the scheduler panicked. The bug only triggers on clusters that enable FairSharing **and** have ClusterQueues outside any cohort. [[pr-10891]] adds the missing `return` and a regression test. Released in v0.18.0.

## Interaction with priority and preemption

Fair sharing picks *which CQ* gets the next admission slot. [[queueing-strategy]] and [[workload-priority]] still pick *which workload within that CQ* goes first. When fair-share decides CQ-B should go and CQ-B's head-of-queue is lower priority than CQ-A's, the lower-priority workload wins — which is surprising if you expected global priority ordering. This is intentional: fair-share is the whole point.

## Preemption strategies compare `AlmostLCA`, not the preemptor's ClusterQueue

The two fair-sharing preemption strategies are named after a share comparison:

- `LessThanOrEqualToFinalShare` (rule **S2-a**)
- `LessThanInitialShare` (rule **S2-b**)

The user documentation used to describe both in terms of "the share of the preempting ClusterQueue". That is only correct for a flat, two-level cohort. KEP-1714 states the rule over **`AlmostLCA(x, y)`** — the child of the lowest common ancestor of the preemptor `x` and the target `y`, on `x`'s side of the tree. In a hierarchy deeper than two levels `AlmostLCA(x, y)` is an ancestor *cohort*, not the preempting ClusterQueue, so the share being compared is a subtree share. The docs were corrected to match the KEP and the code ([[issue-14548]], fixed by #14701; branch/website ports [[pr-14741]], [[pr-14742]], [[pr-14743]]).

Concretely, S2-a reads: the value of `AlmostLCA(y, x)` without target `z` is still higher than or equal to the value of `AlmostLCA(x, y)` with the incoming workload `w` admitted.

## Unsatisfiable tournaments are skipped (`+Inf` dominant resource share)

A preemptor whose `DominantResourceShare` is `+Inf` — it borrows while its cohort's fair weight is zero — is ranked above **every** finite-share target by `CompareDRS`, so both default strategies reject every candidate. Before [[pr-14490]] (fixes #14487) `runFirstFsStrategy` still walked the full per-candidate tournament (each walk goes to the cohort root) and `runSecondFsStrategy` iterated the same candidates again, all provably failing. On a saturated cluster this is `O(candidate workloads)` of wasted work per attempt, every cycle, and it was the dominant source of the `Evaluating FairSharing strategy` log line at `V(4)`.

`fsStrategyUnsatisfiable` now detects the case and skips the per-candidate loop, **draining the candidates into `retryCandidates`** so rule S2-b still runs against a snapshot the loop may have mutated (it deliberately does not `DropQueue`).

The zero-vs-zero case (target also `+Inf`) is **not** skipped: `CompareDRS` falls back to the raw ratio there and preemption can still succeed.

Follow-up [[pr-14765]] (fixes [[issue-14675]]) replaced the ad-hoc `math.IsInf(PreciseWeightedShare(...))` test with the cache's own predicate, exported as `ZeroWeightBorrows()`. `PreciseWeightedShare` returns `+Inf` exactly when `isWeightZero() && !IsZero()`, which is what `zeroWeightBorrows` already checked.

## Re-evaluating candidates after preempting from the preemptor's own CQ

Preempting Workloads from the **preemptor's own** ClusterQueue lowers that CQ's DRS, which can make candidates in *other* CQs newly fair to preempt. The old algorithm did not notice: if the first strategy walked all candidates, found nothing fair, then reached the preemptor's own CQ and took workloads from there without fitting, it fell through to the second strategy — which might pick worse targets, or not enough of them.

Under the `FairSharingReevaluatePreemptionCandidates` gate, the first strategy is re-run over the retry candidates in exactly that situation ([[pr-14128]], fixes [[issue-14122]]; cherry-picks [[pr-14767]], [[pr-14768]]). The release note carried an explicit caveat: enabling the gate increased exposure to the fair-sharing infinite preemption loop [[issue-14543]]. **Update (2026-10-21)**: that loop is now fixed by final-target verification, see the next section (source: pr-16343.md).

**Gate stage (updated 2026-10-21).** The gate is **Alpha, off** at version `0.20` and **Beta, on** at `0.21` (main only; no backport), promoted by pr-17285 because issue-14543, the stated blocker in the gate comment, is resolved. So v0.20.x and v0.19.x still need it enabled explicitly; main enables it by default (source: pr-17285.md, raw/kueue/pkg/features/kube_features.go).

## Final-target verification stops the "own-workload" preemption loop (`FairSharingVerifyFinalTargets`)

**The loop (issue-14543).** The fair-sharing strategies compare shares while the candidates are being *removed one by one* from the snapshot. Removing a Workload from the **preemptor's own** ClusterQueue lowers the preemptor's DRS, which can make a cross-ClusterQueue victim look fair. But `fillBackWorkloads` (or the next scheduling cycle) can put that own Workload back, so the preemptor's real post-admission share is higher than the share used to justify the cross-CQ eviction. The evicted cross-CQ Workload then wins the next round and preempts the preemptor back, forever (source: pr-16343.md).

Counter-example from the PR analysis: Cohort of 100 CPU, `QP` and `QT` both with nominal 0 and weight 1, default strategies `[LessThanOrEqualToFinalShare, LessThanInitialShare]`. `QP` runs `P_small` (30 CPU) and receives `P_hero` (60 CPU), so its share with `P_hero` is 0.90; `QT` runs `T_hero` (70 CPU, share 0.70). `QP` cannot preempt `T_hero` at 0.90, so it evicts `P_small` (share drops to 0.60), now `0.60 < 0.70` passes and `T_hero` is chosen; fill-back then restores `P_small`, leaving `QP` at 0.90 against an empty `QT`, and `T_hero` preempts `P_hero` on the next cycle (source: pr-16343.md).

**The fix ("fast path").** `fairPreemptionStrategy` now attaches a `verify` callback to its `PreemptionStrategy` (`withVerify`). In `Preemptor.getTargets`, after a candidate set fits and `fillBackWorkloads` has run, `verifyFairSharingTargets` re-simulates the incoming Workload's usage and checks **every surviving cross-CQ target** against the **final** state: preemptor share = `AlmostLCA(preemptor, target)` DRS, `TargetNewShare` = target-side AlmostLCA DRS with the target removed, `TargetOldShare` = same with the target's usage temporarily added back. At least one configured strategy must still pass for each target. If any target fails, the whole target set is discarded (V(6) log "Discarding preemption targets: strategy verification failed" with the shares, serialized via `PreciseWeightedShareSerialized`) and no preemption is issued this attempt (source: raw/kueue/pkg/scheduler/preemption/fair_strategy.go, raw/kueue/pkg/scheduler/preemption/preemption.go).

Targets that are **not** re-verified: reason `InClusterQueue`, reason `ConfigurablePreemption` ([[configurable-preemptions]]), and `InCohortReclamation` when `FairSharingPreemptWithinNominal` applies (since pr-17034: the preemptor CQ, with the incoming Workload simulated, does not borrow **any** flavor-resource the Workload requests; see the partial-borrowing fix below) (source: raw/kueue/pkg/scheduler/preemption/fair_strategy.go).

**Gate.** `FairSharingVerifyFinalTargets`, **Beta, default on** (registered at version `0.21` in `kube_features.go`); disabling it restores the old behaviour. The gate was added at reviewers' request as a mitigation (source: pr-16343.md, raw/kueue/pkg/features/kube_features.go). Backported to release-0.20 (pr-16912.md) and release-0.19 (pr-16911.md); shipped in **v0.20.1** and **v0.19.8** (source: raw/kueue/CHANGELOG/CHANGELOG-0.20.md, CHANGELOG-0.19.md).

**Accepted trade-off.** Some "own-only" scenarios — where the only fair answer evicts only the preemptor's own Workloads — are no longer admitted, because the candidate walk still visits cross-CQ targets first and verification then rejects the set. Reviewers framed it as choosing guarantee 1 ("no infinite preemption loops") over guarantee 2 ("a CQ can always use up to its nominal quota") for these cases; a "fast-path + locking" variant was rejected as too invasive. Treat a preemptor stuck pending behind repeated "strategy verification failed" V(6) lines as this limitation; turning the gate off unsticks it at the cost of re-exposing the loop (source: pr-16343.md).

## Candidate ClusterQueues are pruned by the *contested* flavor-resources (pr-16738)

`TargetClusterQueueOrdering` walks the Cohort tree from the root picking the highest-DRS child; it prunes nodes that are not borrowing. It used to test `drs.IsBorrowing()`, i.e. borrowing on **any** flavor-resource. Two bugs followed (source: issue-16665.md, issue-16666.md, pr-16738.md):

- **issue-16665**: a victim CQ within nominal on the contested flavor but borrowing heavily on an unrelated flavor stayed a candidate, so Workloads within its nominal quota were preempted (repro: victim with 2 CPU nominal on `default` running 3 CPU, plus 10 CPU on `other`; a 5-CPU preemptor evicted two `default` Workloads although after the first eviction the victim no longer borrowed `default`).
- **issue-16666**: with hierarchical Cohorts, a leaf CQ borrowing *inside its own sub-cohort* looked like a borrower to an outside preemptor even though the sub-cohort was within its quota on that flavor. Preemption used the global DRS (inflated by another flavor), while the admission tournament (`FairSharingPrioritizeNonBorrowing`) only looks at the requested flavor, so the two disagreed and produced an infinite preempt/re-admit loop. This was **distinct** from issue-14543 and not fixed by pr-16343.

The fix passes `frsNeedPreemption` into `MakeClusterQueueOrdering`:

- `isBorrowing(drs)` uses the new `DRS.IsBorrowingOnAny(frsNeedPreemption)` when the set is non-empty (falls back to `IsBorrowing()` otherwise), for both ClusterQueues and non-ancestor Cohorts.
- `hasWorkload` now drops, from the head of each CQ's candidate list, Workloads that do not use a borrowed contested flavor-resource (`candidateUsesBorrowedResource`, V(6) "Skipping candidate workload whose flavor-resources are not borrowed"). A Workload qualifies only if `candidateBorrowsFromLCA` holds: the CQ borrows that flavor-resource **and every Cohort on the path up to (excluding) the first ancestor shared with the preemptor** also borrows it (`CohortSnapshot.Borrowing(fr)`). The preemptor's own CQ is exempt, so in-CQ preemption is unaffected.

Release note: "Fixed the preemption bug where workloads within nominal quota were preempted if the ClusterQueue borrowed on an uncontested flavor or within an internal sub-cohort." Backports: release-0.20 pr-17031, release-0.19 pr-17095 (manual, because `fair_strategy.go` does not exist on 0.19). Merged 2026-10-09, after v0.20.1/v0.19.8 were cut; **shipped in v0.20.2 (#17031) and v0.19.9 (#17095)** (source: pr-16738.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, CHANGELOG-0.19.md). A reviewer noted that two bypasses of DRS now exist (this one and `FairSharingPreemptWithinNominal`) and suggested DRS may need to be computed only over contested resources (source: pr-16738.md).

## Fixed: preemption loop from partial borrowing (issue-17022, pr-17034)

**The loop.** Preemption and admission defined "within nominal" differently. With `FairSharingPreemptWithinNominal` (Beta, on since 0.17), the nominal-first shortcut (`queueWithinNominalInResourcesNeedingPreemption`) looked only at the flavor-resources **needing preemption** in the preemptor's CQ. A preemptor within nominal on CPU but borrowing memory therefore preempted a CPU borrower without any DRS check, `FairSharingVerifyFinalTargets` skipped that within-nominal `InCohortReclamation` target, and the admission tournament then re-admitted the victim first because the preemptor was still borrowing memory: preempt, re-admit, preempt. Repro: `cq-p` (4 CPU, 2Gi) with `p` asking 4 CPU / 6Gi, `cq-w` (0/0) running `w1` on 4 CPU borrowed from `cq-p` (source: issue-17022.md, pr-17034.md).

**The fix.** The shortcut is now `queueWithinNominalInRequestedResources(preemptionCtx)`: with the incoming Workload's usage already simulated, it iterates `workloadUsage.Quota.Assigned` and returns false if the preemptor CQ is `Borrowing(fr)` (nominal < usage) for **any** flavor-resource with a positive request. Requests `<= 0` are skipped; a reviewer pointed out they can be negative for `ElasticJobsViaWorkloadSlices` scale-down. It treats usage equal to nominal as within nominal. The same predicate is used in `fairPreemptionStrategy` (to bypass the strategy check and take cross-CQ candidates unconditionally) and in `verifyFairSharingTargets` (to exempt `InCohortReclamation` targets), so the two stay consistent. If any requested resource borrows, the normal DRS strategies apply (source: raw/kueue/pkg/scheduler/preemption/preemption.go, raw/kueue/pkg/scheduler/preemption/fair_strategy.go, pr-17034.md).

Release note: "Scheduling: Fixed a bug where fair-sharing preemption could repeatedly evict and re-admit Workloads when a preemptor was within nominal quota for one requested resource but still borrowing another." Merged on main 2026-10-16; backports pr-17349 (release-0.20, merged 2026-10-16) and pr-17390 (release-0.19, manual, adapted to the 0.19 preemption layout, merged 2026-10-19). All three merged **after v0.20.2 / v0.19.9 were tagged** (2026-10-15), so no tagged release carries the fix at this snapshot (source: pr-17034.md, pr-17349.md, pr-17390.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md).

## Weighted share edge cases (v0.20.1 / v0.19.8)

`DRS.PreciseWeightedShare()` (float64) drives `CompareDRS`; `status.fairSharing.weightedShare` (int64) and the weighted-share gauges are derived from it. Three fixes from umbrella issue-16477 (source: pr-16487.md, pr-16488.md, pr-16528.md):

| Case | Before | Now |
|---|---|---|
| Finite share `>= 2^63` (e.g. weight `2n` borrowing 30000 CPU against `1m` lendable) | `int64(math.Ceil(f))` is implementation-defined; on amd64 status read `-9223372036854775808` | `SaturatingCeil` (`pkg/util/math`) reports `math.MaxInt64`, like `+Inf` already was (pr-16487) |
| Weight 0, borrowing only resources the Cohort has nothing lendable for (reachable when quota is withdrawn under a running Workload) | ratio 0, so share 0: ranked as within quota | `ZeroWeightBorrows()` reads the `borrowing` flag (`IsBorrowing`) instead of inferring it from a non-zero ratio; share is `+Inf`, status `MaxInt64` (pr-16488) |
| Positive ratio that divides down to 0 in float64 (weight `1e308`, or `1e400` which is `+Inf` as a float) | share 0, tied with a non-borrower | floor at `math.SmallestNonzeroFloat64`; status reports `1`, gauges `5e-324` (pr-16528) |

Caveats from the PRs: two floored shares compare equal and float64 ordering for such extreme weights is still lossy; `fsStrategyUnsatisfiable` relies on "removing a Workload can only clear `borrowing`, never set it", which still holds. Scheduling comparisons other than these edge cases are unchanged. All three shipped in **v0.20.1** and **v0.19.8** (source: raw/kueue/CHANGELOG/CHANGELOG-0.20.md, CHANGELOG-0.19.md).

**Known gap, open as of this snapshot (issue-16529):** a **positive-weight** CQ that borrows only resources with nothing lendable still gets share 0 (status shows `borrowed: "4"` next to `weightedShare: 0`), contradicting the API doc "0 means usage is below nominal".

**Metric semantics.** `kueue_cluster_queue_weighted_share` and `kueue_cohort_weighted_share` report **NaN** when the weight is 0 and the node borrows; the Cohort gauge used to report `+Inf` (issue-16530, fixed by pr-16581, shipped v0.20.1/v0.19.8). pr-17057 made all four reporting sites test `ZeroWeightBorrows()` (now carried in the usage stats the controllers read) instead of `share == +Inf`; values unchanged. Backported as pr-17171 (release-0.20) and pr-17196 (release-0.19, manual because `Cache.AddOrUpdateWorkload` takes no context there; the automated pr-17170 was closed), both merged 2026-10-14, before the v0.20.2 / v0.19.9 tags; release note NONE (source: pr-17171.md, pr-17196.md). Status keeps `MaxInt64` because an int64 cannot hold NaN. Metric details belong to [[metrics]].

## LocalQueue weight lookup: one cached path for heap and snapshot (AFS ordering)

With [[admission-fair-sharing]] the pending queue orders Workloads by LocalQueue usage divided by LocalQueue weight. Two code paths sort pending Workloads: the live heap comparator (`queueOrderingFunc`) and the lock-free `Snapshot()` used by the [[visibility-api]] (`buildSnapshotSort`). The heap always read weights from the per-ClusterQueue cache `c.lqWeights` (kept in sync by LocalQueue add/update/delete hooks, no API read). The snapshot path used to call `afs.ResolveLQWeight`, i.e. a LocalQueue `client.Get` per sort, and on a transient lookup error **fell back to base ordering for the whole snapshot**, so the visibility API could show a different order than the scheduler would use.

pr-16241 (fixes issue-13602; backports pr-16307 to 0.19 and pr-16308 to 0.18) makes both paths use the shared helper `lookupLQWeight(lqWeights, lqKey)` (default weight `1.0` when the LocalQueue is unknown). `Snapshot()` clones the map with `maps.Clone(c.lqWeights)` under the same `c.rwm.RLock()` that dumps the pending Workloads, then sorts after releasing the lock; that keeps comparisons transitive even if `UpdateLocalQueueWeight`, `addLocalQueue` or `deleteLocalQueue` run concurrently. Release note: "AdmissionFairSharing: Fix incorrect pending-workload ordering in the visibility API caused by failed LocalQueue lookups." (source: pr-16241.md, issue-13602.md, raw/kueue/pkg/cache/queue/cluster_queue.go)

Invariant to preserve when touching this code: never read `c.lqWeights` during the sort without either the lock or a pre-taken copy.

History: before pr-16241, pr-13433 (v0.20.0; backports pr-13546/0.19, pr-13525/0.18) had made the snapshot sort fall back to base ordering for the **whole** snapshot when any LocalQueue lookup failed, because a partially populated usage cache mixed fair-sharing and base comparisons and made the comparator non-transitive (fixes #12534). pr-16241 removed the per-sort lookup, which made the fallback moot (source: pr-13433.md).

## Performance note: lendable capacity is precomputed per Cohort

`dominantResourceShare` used to recompute the cohort's lendable capacity (`calculateLendable`, walking to the root and summing `potentialAvailable` for every FlavorResource) once per preemption candidate, although nothing it reads changes during the tournament; ~11.5% of sampled CPU on two preemption-heavy v0.19.3 clusters (source: issue-15957.md).

**Correction (2026-10-21)**: the previous version of this page said maintaining lendable per Cohort was not merged. It was merged as #15955 (main, 2026-09-29) and backported to release-0.18 (pr-16360.md, manual) and release-0.19 (pr-16361.md); release note "Improved preemption performance by up to 20%", shipped in **v0.19.7** and **v0.18.11** (source: pr-16360.md, raw/kueue/CHANGELOG/CHANGELOG-0.19.md, CHANGELOG-0.18.md). **Correction (2026-10-21)**: this page said no 0.20 changelog lists it. CHANGELOG-0.20.md lists #15955 under **v0.20.0** ("FairSharing: Improved preemption performance by up to 20% by precomputing lendable Cohort capacity..."), so all 0.20.x releases carry it (source: raw/kueue/CHANGELOG/CHANGELOG-0.20.md). The cache keeps `resourceNode.Lendable` next to `SubtreeQuota` (`updateCohortLendable`), carries it into the snapshot, and `dominantResourceShare` reads the parent's `Lendable`; `computeLendable` is the fresh derivation used only for maintenance and tests. Invariant: every `SubtreeQuota` mutation, including `DeleteCohort` where the deleted cohort survives because a child still references it, must refresh `Lendable` (source: raw/kueue/pkg/cache/scheduler/resource_node.go, pr-16360.md).

## Preemption logging volume

pr-14348 (v0.20.0; branch ports [[pr-14531]], [[pr-14532]]) collapsed the per-candidate `V(4)` "Evaluating FairSharing strategy" entry into **one entry per candidate ClusterQueue**, carrying the constant fields (preemptor share, target CQ, target old share) once plus a `strategyEvaluations` array with `targetWorkload`, `targetNewShare`, `strategyPassed` per evaluated candidate; nothing is accumulated when V(4) is off. All DRS values are logged through `PreciseWeightedShareSerialized()` (strings), because a raw `+Inf` float made zapcore drop the whole array. Benchmark at 100 candidates: log bytes -69%, logging time -83% (source: pr-14348.md). Companion to the `+Inf` skip above.

## Related pages

- [[configurable-preemptions]] — **[Alpha]** configurable candidates are merged after both fair-sharing strategies fail.

- [[cohort]] — the scope fair-share is computed over.
- [[borrowing-and-lending]] — what unused capacity means.
- [[cluster-queue]] — where `fairSharing.weight` is set.
- [[preemption]] — what fair-share triggers when a higher-share CQ wants its capacity back.
