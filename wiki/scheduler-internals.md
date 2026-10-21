# Scheduler Internals

**Summary**: The Kueue scheduler runs a continuous scheduling cycle that snapshots the cluster state, assigns resource flavors to pending workloads, and admits or preempts them according to quota and fair-sharing rules.

**Sources**: `raw/kueue/pkg/scheduler/scheduler.go`, `raw/kueue/pkg/scheduler/flavorassigner/flavorassigner.go`, `raw/kueue/pkg/scheduler/logging.go`, pr-15444.md, pr-16078.md, pr-15829.md, pr-15844.md, pr-16167.md, pr-16290.md, pr-16130.md, issue-14792.md, pr-13956.md, pr-15432.md, pr-16765.md, pr-16766.md, pr-17069.md, pr-16466.md, issue-16443.md, pr-16658.md, issue-16661.md, pr-13616.md, pr-17010.md, pr-16479.md, pr-16492.md, pr-16527.md, pr-16672.md, pr-16682.md, pr-14520.md, pr-13668.md, issue-16405.md, issue-16486.md, pr-13844.md, pr-16521.md, pr-16858.md, pr-16630.md, pr-17455.md, issue-16624.md, pr-17346.md, pr-17041.md, pr-17474.md, issue-17040.md, pr-17461.md, pr-17514.md, pr-17517.md, pr-17227.md, pr-17107.md, pr-17146.md, pr-17168.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, raw/kueue/CHANGELOG/CHANGELOG-0.19.md, raw/kueue/pkg/cache/scheduler/initial_sync.go, raw/kueue/pkg/workload/flavor_scan_state.go

**Last updated**: 2026-10-21

---

## The scheduling cycle

The scheduler runs as a single goroutine via `wait.UntilWithBackoff`. Each call to `schedule()` is one cycle. The cycle number is tracked in `schedulingCycle` for log correlation. (source: pkg/scheduler/scheduler.go)

### Phase 0: wait for the initial cache sync (pr-16630)

`Scheduler.Start` (a leader-elected Runnable) now blocks on `Cache.WaitForInitialSync(ctx)` before it launches the loop, then logs `Cache event handlers synced, starting the scheduling loop` at V(2) with the time waited. **Why**: controller-runtime's informer sync only means the informer store is full; the event handlers that fill Kueue's cache could still be walking the initial list when the scheduler took the lease. `AddClusterQueue` backfills only the queue being added and `isTASSynced` only checks that queue, so after a cold leader start a ClusterQueue could go active while ClusterQueues whose admitted Workloads occupy the same nodes (or the same Cohort quota) were still missing. TAS then double-booked nodes, and missing Cohort quota could cause over-admission followed by preemption storms (a reviewer reported 3k of 6k ClusterQueues in the cache when scheduling started) (source: pr-16630.md, issue-16624.md).

How the barrier works ([[cache-architecture#Initial-sync barrier and Cohorts on every replica]]): the ClusterQueue, Cohort, ResourceFlavor, Workload and LocalQueue controllers, plus the TAS Topology and TAS ResourceFlavor controllers when TAS runs, wrap their `source.Kind` with `Cache.TrackInitialSync`. A Kind source reports synced only after its handler has returned for every object in the informer's initial list. There is no polling, no list comparison and no timeout of its own; a source that never syncs fails the manager through `CacheSyncTimeout`, which cancels the wait. Those controllers run on every replica (`NeedLeaderElection` false), so a warm follower is already synced when it takes the lease and does not wait. No feature gate (source: raw/kueue/pkg/cache/scheduler/initial_sync.go, raw/kueue/pkg/scheduler/scheduler.go).

Release note: "TAS: Fix double-booking of nodes when the scheduler starts before every ClusterQueue is in the cache..." Main merged 2026-10-19; release-0.20 backport pr-17455 merged 2026-10-19 (after v0.20.2). The release-0.19 backport needs a manual cherry-pick and is not in this snapshot (source: pr-16630.md, pr-17455.md).

### Phase 1: Get heads

```go
headWorkloads := s.queues.Heads(ctx)  // blocks while queue is empty
```

`Heads()` returns one workload per ClusterQueue — the highest-priority workload at the front of each queue. If any ClusterQueue has borrowing candidates, those are also included as additional heads. (source: pkg/scheduler/scheduler.go)

### Phase 2: Snapshot

```go
snapshot, err := s.cache.Snapshot(ctx, snapshotOpts...)
```

An immutable snapshot of all ClusterQueue/Cohort usage and quotas is taken. The scheduler works entirely against this snapshot — it does not re-read from the live cache during a cycle. If [[admission-fair-sharing]] is enabled, AFS penalties and consumed-resource data are injected into the snapshot here. (source: pkg/scheduler/scheduler.go)

`Snapshot()` runs under the cache's **read lock** and must not mutate cache state. A TAS ClusterQueue whose TAS usage is not yet synced is therefore *skipped* rather than synced inline — see [[cache-architecture#Snapshot is strictly read-only]] ([[pr-11286]]). (source: pkg/scheduler/scheduler.go)

### Phase 3: Nominate

```go
entries, inadmissibleEntries := s.nominate(ctx, headWorkloads, snapshot)
```

For each head workload, the FlavorAssigner runs (see below). Workloads that cannot fit (NoFit) are immediately moved to `inadmissibleEntries`. Workloads that can fit or preempt become `entries`. (source: pkg/scheduler/scheduler.go)

### Phase 4: Iterator

```go
iterator := makeIterator(ctx, entries, s.workloadOrdering, fairsharing.Enabled(s.fairSharing))
```

The iterator orders `entries` for processing. With [[fair-sharing]] disabled, entries are processed in priority+timestamp order. With fair sharing enabled, a `fairSharingIterator` interleaves ClusterQueues by weighted DRS share, so no single CQ monopolizes the cycle. (source: pkg/scheduler/scheduler.go)

### Phase 5: processEntry (per workload)

For each entry the iterator yields, `processEntry` runs the admission pipeline:

1. **TAS unhealthy node check** — if topology assignment requires a failing node and mode is not Fit, the workload is evicted.
2. **NoFit** — skip immediately.
3. **Preemption gate** — if mode is Preempt and the workload has a closed preemption gate (MultiKueueOrchestratedPreemption), mark `preemptionGated` and return.
4. **Overlapping targets** — if this cycle already issued preemptions that overlap with this workload's targets, mark `skipped`.
5. **Fits check** — verify the snapshot still accommodates this workload (earlier admissions in this cycle may have consumed quota).
6. **Issue preemptions** (Preempt mode) — send delete requests to preemption targets; mark entry as pending.
7. **WaitForPodsReady** — block admission if the previous workload cycle left pods not ready.
8. **Admit** — write the `QuotaReservation` and `Admitted` conditions; toggle `.spec.suspend = false` on the job. Admission is **asynchronous** (`admissionRoutineWrapper.Run()` launches a goroutine; `admit` returns `nil` before `PatchAdmissionStatus` completes). On a write error the first-pass rollback uses `Cache.DeleteWorkloadIfUnchanged`, not an unconditional delete; see [[scheduler-internals#Admission write errors keep a committed admission in the cache (pr-17041)]].
9. **WorkloadSlice replacement** — for elastic jobs, finish the *old* slice. As of [[pr-11195]] (fixes #9015) this happens **inside `admit`'s success path**, after `PatchAdmissionStatus` succeeds — i.e. the old slice is finished only once the new (larger) slice is confirmed admitted. Doing it before admission could leave the old slice `Finished` while the new one failed to admit, leaking quota (the job keeps running unsuspended with no admitted slice holding quota). `admit` now takes the `oldWorkloadSlice *preemption.Target`. pr-16521 (behaviour-preserving; backports pr-16541/0.19, pr-16542/0.20) inlined the single-use `replaceOldWorkloadSlice` wrapper: the success path calls `replaceWorkloadSlice` directly when `ElasticJobsViaWorkloadSlices` is on and an old slice exists; a failure is only logged and recovery is left to the job reconciler, no admission rollback. See [[elastic-jobs]].
10. **Second-pass writes are fenced (TAS).** For a second pass (failed-node replacement, delayed topology assignment) the admission write now carries the entry's `resourceVersion` (strict patch) and the assume goes through `Cache.UpdateWorkloadIfUnchanged`; on Conflict the scheduler keeps the reservation, emits an `OutdatedScheduleCycle` warning event and requeues the second pass. First-pass writes are unchanged (#15761; backports pr-16858/0.20, pr-16859/0.19; v0.20.1). Details on [[topology-aware-scheduling]].

(source: pkg/scheduler/scheduler.go)

### Phase 6: Requeue

All entries not `assumed` (successfully admitted) or `evicted` are re-queued with appropriate reasons: `PendingPreemption`, `PreemptionFailed`, `Inadmissible`, `PreemptionGated`. The queue manager uses these reasons to decide delay and ordering. A preemption-gated entry writes `QuotaReserved=False` with reason `PreemptionGated` (not `AdmissionGated`, which the workload controller rewrote to `PendingEvaluation`), and its `QuotaReserved`/`resourceRequests` updates are no longer dropped when `BlockedOnPreemptionGates` is already set ([[preemption#Preemption-gated Workloads report `PreemptionGated` (pr-16627)]]).

**Scheduling-equivalence bulk requeue.** When the `SchedulingEquivalenceHashing` gate is on (**Beta, default on, since v0.18** — [[pr-11097]]), a Workload requeued to the inadmissible set carries its other scheduling-equivalent Workloads (same `SchedulingHash`) with it, so they aren't re-evaluated one-by-one. v0.18 **narrows** this to two requeue reasons only — `RequeueReasonNoFit` and `RequeueReasonPreemptionNoCandidates`. The earlier broad `!immediate` condition also bulk-moved `NamespaceMismatch` and `PreemptionGated` Workloads, which was wrong: it cross-contaminated namespace-mismatched Workloads and broke MultiKueue per-item processing ([[issue-10005]]). Side effect: a single Workload that needs ~100% of a CQ's quota now waits for the requeue batch (≈1s) or a capacity event, so its time-to-admission regresses. (source: pkg/scheduler/scheduler.go)

### Inadmissible-workload requeue guard

`Manager.RequeueWorkload` is called from many places (eviction, condition flips, finished-cleanup). It must refuse to enqueue Workloads that have already become inadmissible — specifically, anything where `workload.IsAdmissible(&w)` is false (e.g. `Finished=True`, deactivated, owner gone). Without this guard, a Workload that is concurrently marked Finished can be re-added to the queue and then keep winning the fair-sharing tournament in subsequent cycles, blocking other Workloads from making progress (the scheduler skips it once it sees the Finished condition, but the head-slot is consumed). [[pr-11014]] tightens `RequeueWorkload` to drop inadmissible Workloads. Part of [[issue-10901]].

The same issue motivated the [[failure-recovery]]-related FG **`FinishOrphanedWorkloads`** to be downgraded to Alpha in [[pr-11010]] (release note: "Fix the bug that Kueue may mark workloads as finished immediately after their creation, which could result in blocking the queues by such a workload"). The root cause is that `workload_controller` queries owners via `PartialObjectMetadata`, which has its own informer separate from the structured per-kind informer used by the JobReconciler — the JobReconciler can already see the JobSet and create the Workload before the metadata informer has caught up, so the workload controller sees an absent owner and finishes the Workload as orphaned. The structural fix landed in [[pr-11296]] (`ReconcileGenericJob` only *finishes* an orphaned Workload under the proper conditions instead of finishing it right after owner creation), and the gate was re-graduated to **Beta, default-on at v0.18** as part of the same PR. See [[workload-garbage-collection]] and [[feature-gates]].

### Admitted workloads must leave `preemptionExpectations`

When the scheduler issues preemptions for a workload, it records the targets in an in-memory `preemptionExpectations` map and refuses to re-issue the same preemption until it has *observed* the eviction (this is what produces the "Preemption already issued, waiting for observation" head-of-line behaviour). Because admission is asynchronous (Phase 8), a subtle race existed ([[issue-11480]], fixed by [[pr-11502]] on main; manual cherry-picks [[pr-11648]]/0.17, [[pr-11647]]/0.16): the admission patch for a lower-priority workload `wl1` is written with Server-Side Apply and **omits** the `Evicted` condition, so a lagging admission goroutine from an earlier cycle could overwrite a concurrent eviction of `wl1` triggered by a higher-priority `wl2`. The consequences were severe and observed in production:

- **Stuck preemption / head-of-line blocking** — `wl1` keeps its quota reservation, `wl2`'s eviction is never observed in `preemptionExpectations`, so `wl2` waits indefinitely and the ClusterQueue stops admitting entirely.
- **Quota oversubscription** — alternatively, the goroutine admits an already-evicted workload with no quota check.

The fix guarantees that once a workload is Admitted it is removed from `preemptionExpectations` (a new `scheduler.WithPreemptionExpectations(...)` option wires this and is now required by the inadmissible integration suite). See [[preemption]].

## FlavorAssigner

The `flavorassigner.FlavorAssigner` runs during Phase 3. For each [[workload]]'s PodSets, it evaluates ResourceGroups in the [[cluster-queue]] and assigns a [[resource-flavor]] to each resource.

### Assignment modes

| Mode | Meaning |
|---|---|
| `Fit` | Workload fits within nominal quota (no borrowing, no preemption needed) |
| `Preempt` | Workload can fit if some lower-priority workloads are preempted |
| `NoFit` | Workload cannot fit regardless |

The "representative mode" across all PodSets determines the entry's overall mode. (source: pkg/scheduler/flavorassigner/flavorassigner.go)

### Flavor scoring

Within a ResourceGroup, flavors are tried in order. The assigner scores each flavor:
- Prefer flavors that don't require borrowing.
- Prefer flavors that don't require preemption.
- Within a tie, follow the order defined in the ClusterQueue's `resourceGroups[*].flavors` list.

The `FlavorFungibility` field (`whenCanPreempt`, `whenCanBorrow`) controls how aggressively the assigner searches beyond the first candidate. (source: pkg/scheduler/flavorassigner/flavorassigner.go)

**`isPreferred` ordering (pr-13616, v0.20.0; backports pr-13896/0.19, pr-13903/0.18).** Comparison of two candidate flavors (`granularMode` = preemption mode + borrowing level) is: `noFit` is always worst; then a flavor whose preemption simulation found **no candidates** (`noPreemptionCandidates`) ranks below every viable mode; only then the configured preference applies. `BorrowingOverPreemption` (and the default) compares preemption mode first, then borrowing level; `PreemptionOverBorrowing` compares borrowing level first. Before the fix, `PreemptionOverBorrowing` let a no-candidates flavor at a shallower borrowing level beat a later flavor that **fits**, so the Workload stayed pending forever with idle quota (needs a two-level cohort to reproduce; in a flat cohort both flavors tie on level). Noted but not changed: the implementation compares the full `borrowingLevel` depth, so in a hierarchy `(Preempt, level 1)` still beats `(Fit, level 2)`, unlike the binary borrow key in the KEP/docs (source: pr-13616.md, raw/kueue/pkg/scheduler/flavorassigner/flavorassigner.go).

**Borrowing Workloads may still preempt inside their own CQ (#16060).** `fitsResourceQuota` simulates preemption when the request fits nominal, the hierarchy allows reclaim, or `canPreemptWhileBorrowing()`; a last branch now also simulates it when `withinClusterQueue != Never` and returns `Preempt` only if candidates exist ([[preemption#Fixed: classical preemption within a borrowing ClusterQueue (#16060)]]).

### Zero-count PodSets: probe one pod per empty group (pr-15444, backports pr-16078/0.19, pr-16079/0.18)

A PodSet with `count: 0` (an elastic Job at `parallelism: 0`, a drained RayCluster worker group, fully reclaimed pods) has all-zero requests, so `fitsResourceQuota` said "0 fits" for every flavor and the **first flavor in the list won by position**. Its `nodeLabels` were then stamped into the pod template at unsuspend (elastic Jobs never re-suspend), and after scaling up the replacement slice fit neither flavor (`gpu` failed node affinity, `on-demand` failed capacity) and the Job was stuck forever (issue-14792.md; damage is in the template, so an already-stuck Job is not recovered). Current behaviour (`probeRequestsFor`, `raw/kueue/pkg/scheduler/flavorassigner/flavorassigner.go`):

- The probe is applied **per PodSet group, only when every PodSet of the group has count 0**: each flavor is checked against **one pod per PodSet** (per-pod requests; `pods` is set to the number of PodSets when the ClusterQueue has a `pods` resource group). If any PodSet in the group has a non-zero count, actual requests drive flavor selection and the zero-count members ride along.
- The probe compares against **potential capacity, not currently available quota** (a busy flavor is still fine for a PodSet not asking for anything yet), and the probe value never enters the request map, so accounted usage stays 0 and preemption is never reached.
- If no flavor passes the probe, assignment falls back to the pre-fix behaviour so workloads whose PodSets are all zero-count still get admitted; the assignment records `ZeroCountFlavorFallback`, which becomes a warning after quota reservation ("Assigned flavor X to zero-count PodSets [...] ... Review capacity and flavor constraints before scaling up.").
- PodSets missing from the assignment or the replaced slice in `TotalRequestsFor`/the replaced-slice flavor check are logged at V(1) (pr-16290; the same wave used V(2) for missing-PodSet scheduler logs, issue-16302.md).
- **Retries restart the probe (pr-16466, main; backports pr-17107/0.20 and pr-17146/0.19, shipped in v0.20.2 and v0.19.9).** With scan progress preservation on, a zero-count group that picked a suitable flavor while *another* PodSet blocked admission resumed **after** that flavor on retry and could fall back to a flavor with no capacity (issue-16443: flavors `large` (2 GPU) then `empty` (0 GPU); PodSet A count 0, B count 1; on retry A got `empty`, and A's later 0-to-1 scale-up stayed pending). Now, when `probeRequestsFor` returns a probe for the group (`zeroCount`), `findFlavorForPodSets` ignores `TriedFlavorsForGroup` and starts at the first flavor, for both the probe and the fallback, and it clears the group's tried set afterwards so a zero-count group never triggers extra retries while another PodSet is blocked. Groups containing a non-zero PodSet keep normal scan behaviour (source: pr-16466.md, raw/kueue/pkg/scheduler/flavorassigner/flavorassigner.go).

### Flavor scan progress across cycles (`FlavorScanState`)

`workload.Info.FlavorScanState` (renamed from `LastAssignment` / `AssignmentClusterQueueState` by pr-15432, moved to `pkg/workload/flavor_scan_state.go` by pr-17069, backported to release-0.20 as pr-17168) records where the flavor search for each PodSet and resource stopped, so the next cycle continues with the next flavor instead of re-nominating the same one (source: pr-15432.md, pr-17069.md, raw/kueue/pkg/workload/flavor_scan_state.go).

Fields: `TriedFlavors []map[ResourceName]sets.Set[ResourceFlavorReference]` (per PodSet index, per resource), `AllocatableResourceGeneration` (CQ generation at scan time), `SchedulingCycle`, `SchedulingHash` (equivalence hash of the Workload shape). Helpers: `NewFlavorScanState`, `IsOutdated`, `MatchesSchedulingShape`, `PendingFlavors`, `TriedFlavorsForGroup`, `RecordPodSet`, `RestoreAfterRecompute`.

**Why it was needed (pr-13956, fixes #13658; v0.20.0).** On a busy cluster the progress was always lost before it could be used, so a Workload whose quota fit flavor A but whose topology could not be placed there was re-nominated to A forever and never tried B. Three things discarded it: (1) the staleness check dropped it whenever the CQ's `AllocatableResourceGeneration` advanced, which happens on every admission or eviction anywhere in the Cohort; (2) `markSkipped` cleared it when another Workload earlier in the cycle took the capacity or preemption targets; (3) any Workload update rebuilt `workload.Info` and dropped it. The log signature: "Re-computing the assignment as it doesn't fit for TAS" then `newMode: Preempt`, "no candidate workloads allowed for preemption", requeue `PreemptionNoCandidates`, every cycle (source: pr-13956.md).

Gate **`FlavorFungibilityPreserveScanProgress`** (Beta, default on, v0.20; the PR text calls it `PreserveFlavorScanProgress`, the code name is authoritative) (source: raw/kueue/pkg/features/kube_features.go). With it on:

- `IsOutdated(currentGen, currentCycle, currentHash)`: a shape change (`SchedulingHash` differs, when both hashes are known) is always outdated; otherwise state from the **current or immediately preceding** cycle is kept regardless of generation; older state falls back to `currentGen > AllocatableResourceGeneration`. The decision moved out of `FlavorAssigner.Assign` (which ran once per reduced count under partial admission and cleared the Workload's state as a side effect) into the scheduler's `getAssignments`.
- `markSkipped` keeps the state (in-cycle contention, not a verdict on the flavor), and the state survives a Workload update.
- Sites that still reset it to `nil` on purpose: `markPreemptionGated`, `markPreemptionOutcome` (after issuing preemptions), the flavor-migration eviction, the overlapping-preemption-targets deferral ("force a full re-evaluation ... could lock the workload into a suboptimal flavor"), the refill path that cannot act on its assignment, and the TAS in-cycle recompute, which restarts the scan pinned by `NominationMapping` and then calls `RestoreAfterRecompute(nominationScanState)` so the nomination's progress survives (source: raw/kueue/pkg/scheduler/scheduler.go).
- Limits called out in pr-13956: when the scan ends on the last flavor the state resets (there is nothing to preserve), and `noPreemptionCandidates` resets it *before* any fungibility policy is consulted, so no `flavorFungibility` setting helps in that case.

**Tried set instead of an index (pr-16766, fixes a follow-up of #13658; backports pr-17070/0.20, pr-17072/0.19).** The state used to be a scalar `LastTriedFlavorIdx`/`LastTriedFlavorIndexes`. Advancing it to the last inspected flavor broke `TryNextFlavor` in two ways: when every flavor needed borrowing (`whenCanBorrow: TryNextFlavor`) the scan walked to the end and reset to `-1`; and when a later flavor `Fit` while an earlier one needed borrowing, selecting the later one advanced past the earlier flavor, which was then skipped forever if TAS failed on the later one. Now only flavors that cannot fit (`NoFit`/`noPreemptionCandidates`) or that were selected as `bestAssignment` are added to the set; a scan resets when all current flavors are tried (`HasAll`, so a flavor removed from the CQ between cycles does not count) or the best mode is `noPreemptionCandidates` or worse (source: pr-16766.md, raw/kueue/pkg/scheduler/flavorassigner/flavorassigner.go). Test: `TestScheduleForPreserveFlavorScanProgress` (parameterized by pr-16765).

### PodSet groups are keyed by name, not position (pr-16658, fixes issue-16661)

PodSets that share a `podset-group-name` are assigned together. When group members are **non-adjacent** in the spec, admission/group order differs from spec order, and several flavor-assignment paths still paired PodSets by position, so (a) scan state was resumed for the wrong PodSet, leaving a Workload pending although an assignment fit, and (b) the TAS second pass used the wrong PodSet data and reordered the admission, so the webhook rejected every retry. The fix maps reordered PodSets back to spec indexes through `podset.SpecIndexes` and keys groups with `tas.GroupKeyForPodSet`, which prefixes the key (`group/` + group name, or `podset/` + PodSet name); the old scheme mixed decimal PodSet indexes and group names in one namespace, so a group named `"1"` collided with the ungrouped PodSet at index 1 and `orderedgroups.Insert` merged unrelated requests (issue-16661). Backports pr-16757 (0.20, v0.20.1) and pr-16760 (0.19, v0.19.8). Remaining positional pairing is tracked by #16266 (source: pr-16658.md, issue-16661.md, raw/kueue/pkg/util/tas/tas.go). TAS-side consequences are on [[topology-aware-scheduling]].

### Preempt mode is also entered for `PreemptionConfig` ClusterQueues

`canPreemptWhileBorrowing()` is true if `borrowWithinCohort.policy != Never`, or fair sharing is on with `reclaimWithinCohort != Never`, **or** (Alpha `ConfigurablePreemptions`) the CQ references a `PreemptionConfig`. See [[configurable-preemptions]].

### Second-pass seeding (multi-resource workloads)

`assignFlavors` runs in two passes for workloads that already hold a partial reservation: the first pass picks flavors from scratch; the second pass seeds the result with whatever the workload had previously reserved (used by ProvisioningRequests and TAS NodeHotSwap re-admission). The seed loop must copy **every** preexisting flavor for each PodSet — copying only the first one (the original behaviour) leaves the remaining resources unassigned, and they fall through to `fitsResourceQuota`, which double-counts the workload's own first-pass reservation. The result was that a multi-resource workload (e.g. CPU + memory) could fail second-pass admission for a resource it had already correctly reserved. Fixed in [[pr-11005]] (Fixes #9048); the TAS scheduler test harness was updated to seed reserved-but-not-admitted workloads into `cqCache` so the regression is observable in unit tests. See [[topology-aware-scheduling#Multi-resource second-pass double-counting]].

## Quota tiers

The scheduler evaluates three tiers of capacity in order:

1. **Nominal** — quota the ClusterQueue owns outright; never needs borrowing or preemption.
2. **Borrowing** — unused nominal quota from other ClusterQueues in the same [[cohort]]; requires borrowing.
3. **Preemption** — quota held by lower-priority workloads; requires evicting them.

If a workload can fit in tier 1 → `Fit`. If it needs tier 3 → `Preempt`. If none fit → `NoFit`.

## Quota arithmetic and integer-overflow safety

Quota arithmetic is done in `int64` (milli-units for CPU, absolute units otherwise). Several v0.18 fixes hardened this against wraparound, which was a real **quota-limit bypass**: when a sum or product overflowed `int64` it wrapped *negative*, and a negative value silently passes the "fits within quota" comparison, so an over-large Workload got admitted.

- **`flavorassigner.fitsResourceQuota`** ([[pr-11137]]): `assumedUsage + requestUsage` could overflow when two PodSets' combined requests exceed `MaxInt64`; replaced with an overflow-checked add (extracted to a `pkg/util` helper).
- **`resources.ResourceValue`** ([[pr-11139]]): converting a near-`MaxInt64` CPU quantity to milliCPU multiplies by 1000 and overflowed; now **clamps/saturates** to `math.MaxInt64`/`MinInt64` via `SafeMilliValue` (`pkg/util/math/math.go`).
- **`TotalRequests`** ([[pr-11182]]): per-pod-request × pod-count overflowed for a Workload with many pods; now uses a saturating multiply `SaturatingMul(a, b int64) int64` (overflow detected via `res/b != a`, returns `MaxInt64`/`MinInt64` by sign).

The strategic consolidation is the **`resources.Amount`** quota type ([[pr-11156]], fixes #9843) — quota *storage* flows through one type so per-site clamps become a type-enforced invariant. That type first saturated at an `Unlimited` sentinel; **pr-15026 (v0.20) made `Amount` exact** (`int64` while it fits, immutable `big.Int` otherwise; no sentinel). See [[cache-architecture#Quota amounts are exact past int64 (pr-15026)]].

**Correction (2026-10-21): workload requests are exact too.** This page said the request path kept saturating behaviour. pr-16479 (fixes issue-16405; backports pr-16549/0.20 in v0.20.1, pr-16671/0.19 in v0.19.8) moved both `resources.Requests` implementations (`MapRequests`, `SliceRequests`) and pending-resource totals onto `Amount`, so `Add`/`Sub`/`Mul`/`Divide` are exact past `int64`. Before, a Workload whose **total** (e.g. pod count times per-pod CPU) overflowed was recorded as `MaxInt64` and could be **admitted against a quota it did not fit**. In-range values still marshal as JSON numbers, so scheduling-equivalence hashes are unchanged; `SaturatingAdd/Sub/Mul` remain only for DRA capacity/counter code; a single non-CPU `Quantity` is still capped at what a `Quantity` holds (source: pr-16479.md).

Related request-path changes in the same wave:

- **Partial admission scales from the per-pod request** (pr-14520, part of #14371; backport pr-16519 in v0.20.1). `PodSetResources.ScaledTo` used to divide the (possibly saturated) total by the old count; three pods of 4e18 against a 7e18 quota then admitted two pods "costing" 6148914691236517204. It now multiplies `PerPodRequests` by the new count; the admitted path (`totalRequestsFromAdmission`) still divides the admitted total. Because partial admission depends on `PerPodRequests`, `computeSchedulingHash`/`sameHashedRequests` now read it too (DRA charges only show up in the total, so two Workloads differing in per-pod DRA charges could otherwise share a hash) (source: pr-14520.md).
- **`AmountFromQuantity` fast path** (pr-16492): a non-negative in-range Quantity uses `Value()`/`MilliValue()` (0 allocations, ~10 ns instead of ~150 ns); negative or out-of-range values use the decimal path. pr-16527 then avoided `Quantity.CmpInt64` for the range test, because for a huge exponent it builds 10^n: a ClusterQueue quota of `1e10000000` passes the webhooks and took ~1.6 s and 46 MB to convert; an `AsApproximateFloat64` estimate now routes such values to the decimal path. Both backported to 0.20 and 0.19 (pr-16496/pr-16495, pr-16571/pr-16580) (source: pr-16492.md, pr-16527.md).
- **Messages keep the unit** (pr-16682): `ExactAmountString` printed a CPU amount past the Quantity limit as raw milli digits without `m` (two times `MaxInt64` cores appeared as `18446744073709551614000`, reading as cores); the CPU fallback now keeps the `m` suffix (source: pr-16682.md).
- Cleanups: `NewRequestsFromMap` builds `SliceRequests` directly when `VectorizedResourceRequests` is on (pr-16672; `BenchmarkSchedulerTAS` -22% allocations); concrete `MapRequests` uses outside `pkg/resources` were replaced by the `Requests` interface (pr-13668).

**Known gap, open as of this snapshot (issue-16486):** the admitted PodSet total is written to `status.admission.podSetAssignments[].resourceUsage` as a `Quantity`, which caps a non-CPU total at `MaxInt64`; the cache then rebuilds usage from the capped value, and because the webhook requires `resourceUsage` to be divisible by `count`, an even count with a capped (odd) total is rejected and the scheduler retries indefinitely without setting a condition.

## `Admitted` event reports the real reservation wait time (pr-15829)

The `Admitted` event ("Admitted by ClusterQueue X, wait time since reservation was Ns") used to hardcode `0s`. It now computes `workload.QuotaReservedWaitTime`, the time since the `QuotaReserved` condition's `LastTransitionTime` (0 when the condition is missing). The admission-check metric behaviour is unchanged. This matters for Workloads that wait on [[admission-check]]s between reservation and admission; the "Quota reserved ... wait time since queued" event is the separate queue-side number.

## AFS entry penalties are pushed only where they will be settled (pr-13844)

When a Workload is assumed, the scheduler pushes an [[admission-fair-sharing]] entry penalty for its LocalQueue and takes it back if the admission patch fails. `shouldApplyEntryPenalty(e)` now gates **both** the push and the rollback, so they always pair up. It returns true only if AFS is enabled, the ClusterQueue's `AdmissionScope.AdmissionMode` is `UsageBasedAdmissionFairSharing` (other CQs never settle a penalty, so it would inflate the LocalQueue's usage until restart and also defeat the LocalQueue reconciler's sampling-interval short-circuit), and the Workload does **not** already hold a quota reservation (a second pass for delayed topology or node replacement re-assumes an already-reserved Workload; one reservation contributes at most one push). Fixes #13495; backports pr-13851/0.19, pr-13853/0.18; v0.20.0 (source: pr-13844.md, raw/kueue/pkg/scheduler/scheduler.go). Tests: `TestShouldApplyEntryPenalty`, `TestSecondPassDoesNotRepushEntryPenalty`, `TestFailedAdmissionWriteRemovesEntryPenalty`.

## Preemption target selection uses the assignment

Preemption target selection (`GetTargetsWithStrategy` -> `getTargets`; the public `GetTargets` was removed by pr-16537) sizes the preemptor from the flavor assignment (assigned PodSet counts and `pods` quota), not from the raw spec; see [[preemption#Target selection sizes the preemptor from the assignment (v0.20, cherry-picked to 0.19/0.18)]].

## Inflight (popped) Workloads are tracked per Workload

`Manager.Heads` pops heads before the snapshot; the queue now records each popped Workload in an `inflight` map keyed by `workload.Reference` instead of a single slot per ClusterQueue (pr-15844). Behaviour is unchanged today; it enables popping more than one head per cycle for the fair-sharing refill KEP (issue-14596, open, `scheduler/refill.go` still has a `TODO(#14190)` for making it configurable). Inflight cleanup still happens inside `RequeueWorkload` ([[cache-architecture#`RequeueWorkload` owns the inflight cleanup]]).

## Fair-sharing iterator

When fair sharing is enabled, the iterator uses DRS (Dominant Resource Share) to order ClusterQueues. The queue with the lowest share (least over its nominal quota) gets to admit next. This prevents any single ClusterQueue from monopolizing borrowable capacity across a cycle. See [[fair-sharing]] for the DRF algorithm details.

## Speed signal

The `schedule()` function returns `KeepGoing` if at least one workload was admitted, and `SlowDown` otherwise. The `wait.UntilWithBackoff` caller uses this to add a brief pause when no progress was made, reducing wasted CPU cycles. (source: pkg/scheduler/scheduler.go)

## What triggers a new cycle

- A new workload enters the queue.
- A workload is evicted or preempted (freeing quota).
- A ClusterQueue's `nominalQuota` or `borrowingLimit` is updated.
- A ResourceFlavor is created/deleted.
- A cohort membership changes.
- A WaitForPodsReady timeout fires.

## Preemptor prioritization

Guarded by the Alpha, off-by-default `PrioritizePreemptorWorkloads` gate ([[pr-13797]], fixes #13662).

**The failure it fixes.** When a Workload needs the *combined* quota of several victims across a cohort, the victims rarely finish evicting at the same instant. Between the first victim releasing quota and the last one finishing, the preemptor holds no reservation and no lock on that quota, so:

1. victim `wlA` finishes evicting and frees quota;
2. the preemptor still cannot be admitted — it is waiting on `wlB`;
3. any workload with nominal capacity (or a favourable fair share) grabs the freed quota, including `wlA` itself being re-admitted;
4. the preemptor re-issues preemption against `wlA`; when `wlB` finishes, the same thing happens there.

The result is an unbounded eviction loop that never admits the preemptor.

**The mechanism.**

- **Preemptor tracking.** When preemption is issued, the ClusterQueue records the active `preemptorWorkload` together with the `.metadata.generation` it was evaluated at. `manager.Heads()` calls `cq.IsPreemptor(wl)` — which requires a **strict generation match** — and stamps `IsPreemptor: true` on the scheduler's `Head` struct.
- **Iterator ordering.** With the gate on, both `makeClassicalIterator` and the fair-sharing `entryComparer.less` sort `IsPreemptor == true` entries first.
- **Snapshot locking.** Being evaluated first means the preemptor runs `cq.AddUsage(usage)` in `processEntry` before anyone else, reserving its capacity **in the cycle snapshot** — even when `ReclaimWithinCohort: Any` (`CanAlwaysReclaim`) would otherwise let a reclaimer through. Interim workloads then fail `cq.Fits` and are skipped.

**TAS domains are locked too.** The same `AddUsage` call re-locks the preemptor's chosen topology domains in `TASFlavorSnapshot`, and the placement is stable across cycles because `updateAssignmentForTAS` simulates removal of the *remaining* targets (`SimulateWorkloadRemoval(targets)`) and `sortedDomains` breaks ties deterministically via `compareDomainLevelValues` (lexicographic over domain-hierarchy level values, e.g. `rack-1/node-1` before `rack-2/node-2`). An interim workload trying to claim those domains fails `FitsCheckNoTAS`. Pinned by integration coverage in [[pr-14687]] / [[pr-14894]] / [[pr-14895]].

Consistency of preemptor state between the queue snapshot and second-pass scheduling is still being tightened ([[issue-14681]], open).

## Recompute an assignment when preemption targets overlap

Phase 5 step 4 used to simply mark an entry `skipped` when its nomination-time preemption targets overlapped targets already claimed earlier in the same cycle. On a busy cluster a large "hero" Workload collided with earlier entries every cycle and never got scheduled (#13320). Under the **Beta** `RecomputeAssignmentUponPreemptionTargetsOverlap` gate the scheduler instead **recomputes** the assignment against the already-updated snapshot ([[pr-14246]], [[pr-14248]]; original #13863). The TAS-specific counterpart is `TASRecomputeAssignmentWithinSchedulingCycle`, which now requires `TopologyAwareScheduling` to be enabled ([[pr-14256]]).

## Popped heads must survive a snapshot failure

`Manager.Heads` pops one head from every active ClusterQueue **plus** all ready second-pass Workloads *before* `cache.Snapshot()` runs. If `Snapshot()` returns an error the cycle used to return immediately, leaving those Workloads out of the queue until some unrelated event happened to requeue them — an indefinite stall.

[[pr-13885]] (fixes [[issue-13884]]) restores them on the error path:

- regular heads are requeued with the new reason `SnapshotFailed`;
- second-pass Workloads go back through the existing retry/backoff path.

The inflight cleanup was moved **into `Manager.RequeueWorkload`, before `info.Update` clears the source ClusterQueue**. That placement also fixes two pre-existing accounting bugs on the `requeueAndUpdate` path and on LocalQueue retargeting, where the *previous* ClusterQueue kept counting the Workload as pending after it moved.

Known trade-off, accepted in the PR: a *persistent* snapshot failure now produces a tight retry loop, because heads are requeued immediately and the scheduling-cycle slowdown is capped at 10 ms. A dedicated backoff for repeated snapshot failures was left as a follow-up.

Backported to **release-0.19** ([[pr-14938]]) and **release-0.18** ([[pr-14939]]), both merged 2026-08-31; the regression test lives in `scheduler_afs_test.go` ([[pr-14956]] and its branch variants [[pr-14959]], [[pr-14960]]).

## Scheduling-equivalence hash: what it does and does not include

The hash is computed over each PodSet's scheduling-relevant shape plus its effective `TotalRequests.Requests`. It deliberately **excludes** the PodSet `Name` when `SchedulingEquivalenceHashingIgnorePodSetName` is on (Beta/on from v0.20, Alpha/off on release-0.19) — flavor assignment never reads the name, but the Pod-group integration derives it from the client-settable `kueue.x-k8s.io/role-hash` annotation, so a client stamping a unique role hash per Workload produced one equivalence class per Workload and defeated the bulk-move optimization entirely ([[pr-14784]], part of #14534). PodSet **ordering** still matters, and the gate requires `SchedulingEquivalenceHashing`.

Related open gaps: equivalence hashing interacts badly with `UsageBasedAdmissionFairSharing` ([[issue-14231]]), and the hash is recomputed unnecessarily on requeue ([[issue-14604]]).

**The hash is computed only for Infos that enter the queue (pr-17461).** Only the queue manager uses `Info.SchedulingHash`, but the scheduler cache, the unadmitted-condition resolver and the DRA checks in the Workload controller also build `workload.Info`s and paid for the hash on every Workload event. They now pass `workload.WithSkipSchedulingHash()`; in `make run-performance-scheduler` the hash work outside the queue dropped from 1.79 s to 0 (about 1.7% of Kueue CPU). Invariant from review: every `workload.Info` that enters the queue manager must have its hash computed for its current shape, so never use the option on an Info you add to or update in the queue manager. Backports pr-17514 (0.20) and pr-17517 (0.19), merged after v0.20.2 / v0.19.9 (source: pr-17461.md, raw/kueue/pkg/workload/workload.go, raw/kueue/pkg/cache/scheduler/cache.go).

## Admission write errors keep a committed admission in the cache (pr-17041)

`Scheduler.admit` assumes the Workload into the scheduler cache, then writes its admission status. The apiserver can commit that write while the client sees an error (timeout, connection reset). If the Workload's update event arrived **before** the rollback, the event replaced the assumed entry with the admitted Workload and the unconditional rollback then removed it; nothing re-added it, so the ClusterQueue under-counted usage until the Workload's next update (issue-17040). That divergence lets the scheduler over-admit against quota it thinks is free (source: pr-17041.md, issue-17040.md).

Now, for a first pass (or a NotFound error), the rollback calls `Cache.DeleteWorkloadIfUnchanged(log, cacheWl)`, which removes the entry only if the cache still holds the **same `resourceVersion`** the scheduler assumed (shared helper `clusterQueueForUnchangedWorkloadWithoutLock`, V(3) "Skipping cache operation as the workload resourceVersion differs"); watchers are notified only when it actually deleted. The second-pass branch already restored with `UpdateWorkloadIfUnchanged`. If the event arrives after the rollback, the Update handler re-adds the Workload as before. An earlier revision repaired the cache from the Workload reconciler instead; it was dropped because that Reconcile can run before the rollback, which is exactly the failing order (source: raw/kueue/pkg/scheduler/scheduler.go, raw/kueue/pkg/cache/scheduler/cache.go, pr-17041.md). Test: `TestSchedulerKeepsAdmittedWorkloadWhenCommittedAdmissionWriteReportsError`.

Main merged 2026-10-20; release-0.20 backport pr-17474 merged 2026-10-20 (after v0.20.2). The automated release-0.19 cherry-pick pr-17476 was closed for a manual one, which is not in this snapshot (source: pr-17041.md, pr-17474.md).

## Scheduler progress logs are at V(3) (pr-17227, main only)

A Workload waiting for preemption is retried every cycle (backoff capped at 10 ms), and each cycle logged eight progress lines at V(2): `Scheduling cycle starts`, `Obtained heads`, `Snapshot taken`, `Nomination done`, `Attempting to schedule workload`, `Workload re-queued`, `Workload processing done`, `Scheduling cycle complete`. One reported case was about 740 lines per second from a single preemptor. On main these eight messages are now **V(3)**, and the logging policy classifies scheduler-cycle progress as V(3). Release note marks it ACTION REQUIRED for dashboards built on those lines (raise verbosity to 3). Events and scheduling behaviour are unchanged. The release-branch counterparts (pr-17370, pr-17371) are not merged at this snapshot, so v0.20.x and v0.19.x still log them at V(2) (source: pr-17227.md, raw/kueue/pkg/scheduler/scheduler.go, raw/kueue/site/content/en/community/contribution_guidelines/logging_policy.md).

## Workload-aware scheduling (`SchedulerLibraryIntegration`, Alpha)

Two pieces have shipped behind the Alpha, off-by-default `SchedulerLibraryIntegration` gate:

- Kueue stops filtering unready / `spec.unschedulable` nodes when building the TAS node cache and lets the scheduler library apply those checks ([[pr-14203]], [[pr-14613]]).
- Every Pod created by a Kueue-managed job is annotated `kueue.x-k8s.io/workload` with its Workload name, so preemption decisions can be mapped onto concrete Pods in the library's cluster cache ([[pr-14551]], [[pr-14796]]). Previously only `TopologyAwareScheduling` set this annotation. The name is resolved in order: explicit workload annotation → prebuilt-workload → pod group → workload slice.

## Related pages

- [[admission]]
- [[cluster-queue]]
- [[resource-flavor]]
- [[cohort]]
- [[preemption]]
- [[fair-sharing]]
- [[admission-fair-sharing]]
- [[topology-aware-scheduling]]
- [[cache-architecture]]
- [[workload]]
- [[concurrent-admission]] — Variant Workloads racing in the same scheduling cycle.
- [[debugging-guide]] — translating scheduler decisions into operator-visible symptoms.
