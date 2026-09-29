# Topology-Aware Scheduling (TAS)

**Summary**: TAS lets a [[workload]] request placement within a topology domain — a rack, a block, a zone — so bandwidth-sensitive Pods (ML training, MPI) don't get scattered across a data center. A ResourceFlavor references a `Topology` object that declares the topology levels; PodSets carry required/preferred annotations; Kueue picks a domain at admission and pins each Pod to nodes in that domain.

**Sources**: `raw/github/kubernetes-sigs__kueue/` (pr-15262, pr-15436, pr-15447, pr-15456, pr-15571, pr-15578, pr-15579, pr-15640, pr-15678, pr-15689, pr-15856, pr-15857, pr-15860, pr-15861, pr-15862, pr-15885, pr-16003, pr-16039, pr-16061, pr-16152, pr-16174, pr-16248, pr-16273, pr-16306, pr-16321 and others cited inline); `raw/kueue/pkg/features/kube_features.go`, `raw/kueue/pkg/util/tas/spreading.go`, `raw/kueue/apis/kueue/v1beta2/topology_types.go`.

**Last updated**: 2026-09-29

---

## Motivation

AI/ML researchers had no way to say "run this workload so that all Pods are on nodes within a rack (or block)" ([[issue-2724]]). Scattered Pods translate to longer training times and higher cost — cross-rack bandwidth is often the bottleneck.

TAS shipped as Alpha in Kueue v0.9 ([[issue-2724]] — Topology Aware Scheduling (Alpha)) and graduated to Beta tracked under [[issue-3450]].

## Shape of the API

- **`Topology`** (cluster-scoped CRD) — declares an ordered list of levels (e.g. `[datacenter, zone, block, rack, node]`). Nodes are assumed to carry labels matching each level.
- **ResourceFlavor opt-in** — a [[resource-flavor]] with `spec.topologyName: <topology>` participates in TAS. Only flavors that reference a Topology run through the TAS algorithm.
- **Workload PodSet annotations** — PodSets carry:
  - `kueue.x-k8s.io/podset-required-topology` — admission fails if pods can't fit entirely within one domain of this level.
  - `kueue.x-k8s.io/podset-preferred-topology` — attempt required-topology first, but fall back to higher levels if needed.
  - `kueue.x-k8s.io/podset-unconstrained-topology` — opt into TAS but without a specific locality requirement (useful for "use a TAS flavor's elastic behavior").
- **Rank-based ordering** — some jobs (MPI-style) need Pod rank → topology-domain assignment stability. Support for rank-based ordering is tracked per integration ([[issue-3533]] for Pods, [[issue-3663]] for custom CRDs).

## What Kueue picks, what kube-scheduler does

At [[admission]] time, TAS:

1. Reads the current per-domain free capacity from the cache.
2. Finds the smallest domain at the requested level that fits all PodSets (combined).
3. Writes `status.admission.podSetAssignments[].topologyAssignment` — a list of `{levels: [...], domain: <name>, count: N}` entries.
4. Injects node-affinity into the Pod template matching the chosen domain, so `kube-scheduler` places Pods only on nodes within it.

## Supported integrations

Not all job integrations shipped TAS support at once. "TAS: support all Job CRDs (including Pods)" ([[issue-3372]]) tracked the rollout; [[issue-3886]] enumerates supported frameworks. RayJob + TAS had dedicated e2e ([[issue-3716]]).

## Operational pain points

- **Memory usage.** The per-domain cache is a hot structure; "Optimize memory usage of TAS" ([[issue-3522]]) addresses it.
- **Node events vs cache staleness.** If a Node's labels change (or a ResourceFlavor's `nodeTaints`/`tolerations` change), the TAS cache must update ([[issue-3733]]). Topology updates/deletions likewise ([[issue-3614]]).
- **Non-ready nodes.** Excluding them at the TAS layer was an explicit ask ([[issue-3401]]) so admission doesn't promise capacity that's unavailable.
- **Panics during reconcile.** Node reconciler has had crash bugs ([[issue-3706]], [[issue-10640]], [[issue-10033]]).
- **Terminating pods.** TAS capacity accounting didn't track terminating Pods, so scheduling could fail until they fully disappeared ([[issue-10076]]).
- **Oversubscription with multiple flavors on same nodes.** A Node in two TAS ResourceFlavors led to over-counting ([[issue-10659]]) — **fixed in v0.18** behind the `TASHandleOverlappingFlavors` gate (see *Overlapping ResourceFlavors* below).
- **TAS + cohorts/preemption.** Reclaiming capacity within a topology domain constrains preemption more than the cohort-level case ([[issue-3761]] — make TAS compatible with cohorts and preemption; [[issue-10497]] — preemption can under-select candidates needed to free a topology domain).

## Bin-packing quality

Default placement is greedy. "Optimal bin-packing in TAS" ([[issue-10574]]) tracks algorithmic improvements; "Better accuracy of scheduling by tighter integration with kube-scheduler" ([[issue-3755]]) discusses reducing the split between Kueue's topology choice and the scheduler's node choice.

### Balanced placement → BestFit fallback

There are two placement algorithms in `findTopologyAssignment` (`pkg/cache/scheduler/tas_flavor_snapshot.go`): **BestFit** (pack tightly) and **Balanced Placement** (spread pods across domains to meet a per-domain `bestThreshold`). Before [[pr-11136]], if Balanced Placement could not satisfy the precomputed threshold it returned the failure reason and the assignment failed outright. Now it logs `Balanced placement threshold not met, falling back to BestFit` at V(3) and proceeds with BestFit instead of failing.

The non-obvious trigger this fixed (part of #7494): `bestThreshold` is computed *earlier* in the flow while more candidate domains are still in play, then placement is narrowed (e.g. a leader pod that only fits on one node forces the assignment into a single block), at which point the original threshold can become unsatisfiable. Example: a LeaderWorkerSet leader consuming most of one node's capacity narrows the workers to a single block where the previously-computed spread threshold can no longer be met — Balanced Placement fails, BestFit succeeds.

## Snapshot internals (`tas_flavor_snapshot.go`)

TAS placement is computed off a per-cycle topology snapshot. Each topology domain (region/spine/hostname leaf) carries three counters:

- `state` — capacity assuming a non-leader pod (worker-only).
- `stateWithLeader` — capacity assuming a leader pod is also placed in the domain. Smaller than `state` because the leader consumes some quota.
- `leaderState` — whether the domain (or any descendant) can host a leader at all (i.e. the domain has free capacity ≥ leader request on at least one node).

`fillInCounts` aggregates these from leaves up; `fillInCountsHelper` rolls a parent's `stateWithLeader` from its children's `state - stateWithLeader` differences. Two recurring bug classes have been fixed in this code:

### Empty-children over-estimation in `stateWithLeader` (v0.16.7 / v0.17.2)

Aggregation iterated **all** children including `state=0, stateWithLeader=0` reserved nodes, contributing a zero penalty that became the running minimum. Parent `stateWithLeader` then equalled `state`, so the scheduler believed a spine could host both a leader and the workers when in reality the only free node could only host one of them. Symptom: an infinite scheduling loop logging `unexpected remainingCount` / `code assumptions violated` followed by `topologyAssignment.slices: Required value` from CRD validation. Triggered on PodSet groups (e.g. PyTorchJob master + workers) when:

1. `leaderRequest ≤ nodeCapacity` (leader fits)
2. `workerCount × workerRequest ≤ nodeCapacity` (workers fit alone)
3. `leaderRequest + workerCount × workerRequest > nodeCapacity` (together they don't)

The fix in [[pr-10841]] (cherry-pick of #10783; preparatory cleanups [[pr-10843]]) restricts the penalty computation to children with `leaderState > 0` and clamps `stateWithLeader` to 0 when no child can host a leader. Tracked under [[issue-10778]]; #7446 still tracks the broader phase-1/phase-2 inconsistency. A follow-up cleanup ([[issue-10812]]) is decoupling non-leader TAS from `stateWithLeader` plumbing.

### Negative state propagating into `TopologyAssignment.podCounts.individual`

`CountInWithLimitingResource` could return a negative `int32` when `tasUsage` (or `tasUsage + assumedUsage` during preempt-mode) exceeded `freeCapacity`. That value was stored verbatim on `leaf.state` and propagated through `fillInCountsHelper` (`childrenCapacity += child.state`), eventually emitting a negative `Count` that the apiserver rejected with `podCounts.individual[*]` `Invalid value: -1: should be greater than or equal to 1`. The Workload would then re-queue with `requeueReason: FailedAfterNomination` indefinitely.

[[pr-10949]] adds two regression tests:
- `TestBuildTopologyAssignmentForLevels_DropsNonPositiveStateDomains` — output-side filter in `buildTopologyAssignmentForLevels` skips domains with `state ≤ 0`.
- `TestFillInCounts_ClampsNegativeRemainingCapacity` — source-side fix in `fillInCounts` clamps `leaf.state` to 0 when remaining capacity goes negative (covers both `tasUsage` over-subscription and the `assumedUsage` preempt-mode case).

### Multi-resource second-pass double-counting

The seed loop in `flavorassigner.assignFlavors` previously copied only the **first** preexisting flavor per PodSet. On the second scheduling pass (used for ProvisioningRequests and TAS NodeHotSwap), the remaining resources fell through to `fitsResourceQuota`, which double-counted the workload's own first-pass reservation. Multi-resource workloads (e.g. CPU + memory together) could fail admission for a resource that they had already correctly reserved in the first pass.

[[pr-11005]] preserves all preexisting flavor assignments for the PodSet so the second pass correctly accounts for the workload's already-reserved resources. The TAS scheduler test framework was updated to seed reserved-but-not-admitted workloads into the `cqCache` so the regression is observable in unit tests. Fixes #9048.

### Cumulative Pod-count across PodSets (`addAssumedUsage`)

When a Workload has **multiple PodSets**, each PodSet is fit into the topology one at a time. The fix in [[pr-11293]] (cherry-picked as [[pr-11326]]/0.17, [[pr-11331]]/0.16, fixes [[issue-11287]]) makes the per-node `pods` capacity respected *cumulatively* across PodSets: previously the assumed-usage accounting did not include the Pods of already-placed PodSets when fitting a later PodSet, so a node whose `pods` capacity was 1 could be assigned two single-Pod PodSets from the same Workload. Previous-pod capacity accounting is now routed through a unified `addAssumedUsage()` helper backed by `utiltas.ComputeUsagePerDomain`, which folds the `pods` resource (and all others) across every PodSet per topology domain. The reproduction: a node with `pods` capacity 1 and a two-PodSet Workload (each 1 Pod) now stays pending with `topology "tas-single-level" doesn't allow to fit any of 1 pod(s). Total nodes: 1; excluded: resource "pods": 1`.

## Performance: incremental non-TAS usage cache

Building the topology snapshot dominates scheduler-cycle latency on large clusters. PR #10366 (cherry-picked to release-0.16/0.17 in [[pr-11074]] / [[pr-11041]]) replaces the per-cycle full scan over non-TAS Pods with **incremental per-node aggregation in `nonTasUsageCache`**. The cache pre-aggregates non-TAS Pod usage per node and is updated event-by-event on Pod create/update/delete; the snapshot reads pre-computed totals instead of walking every Pod.

**Terminal-Pod cache leak.** Because the cache is event-driven, a non-TAS Pod that reaches a terminal phase (`Succeeded`/`Failed`) **without Kueue observing the expected status-update event** never had its usage removed, leaving stale per-node usage in the TAS cache (the node looked busier than it was). PR #11033 (cherry-picked in [[pr-11145]] / [[pr-11146]] to 0.16/0.17) fixes the Pod controller's **delete predicate** to also reconcile terminal Pods so their usage is released.

## NodeHotSwap "late pods"

When a node is marked unhealthy and a workload is partially evicted, replacement pods can land on the new healthy node before the unhealthy state is fully reconciled. The original NodeHotSwap logic added these "late pods" to `UnhealthyNodes` even though they belonged to the new topology assignment, polluting the unhealthy set on subsequent reconciles. The fix (PR #10760, cherry-picked in [[pr-10837]] / [[pr-10838]]) refines NodeHotSwap so `UnhealthyNodes` is only updated for workloads currently assigned to the node via a topology assignment — late pods from stale topologies no longer trigger inaccurate health reporting.

## NodeHotSwap: node-taint relocation uses effective tolerations

Behind the `TASReplaceNodeOnNodeTaints` gate, TAS NodeHotSwap relocates an admitted Workload's pods when a node it is placed on gains a `NoSchedule`/`NoExecute` taint. The classifier originally tested the taint only against `Workload.Spec.PodSets[*].Template.Spec.Tolerations` — the *raw* PodSet template. But an admitted Pod also carries tolerations injected from (1) the assigned [[resource-flavor]] and (2) AdmissionCheck `PodSetUpdates`. So a healthy tainted node that the *effective* PodSpec actually tolerates was misclassified as unhealthy and the Workload was wrongly evicted with `NodeFailures`.

[[pr-11185]] (fixes [[issue-11152]]; cherry-picks [[pr-11227]]/[[pr-11228]]) fixes `nodeReconciler` (`pkg/controller/tas/node_controller.go`) to build the **effective PodSet** — spec tolerations + ResourceFlavor tolerations (via `podsetinfo.FromAssignment`) + matching `wl.Status.AdmissionChecks[*].PodSetUpdates[*].Tolerations` — before evaluating taints (`hasSchedulingTaints`). **Invariant**: taint tolerance for an *admitted* Workload must be evaluated against the post-admission effective toleration set, never the raw template.

## Overlapping ResourceFlavors on shared nodes (`TASHandleOverlappingFlavors`)

The TAS cache historically assumed **ResourceFlavor : Node = 1 : N** — each node belongs to exactly one ResourceFlavor, so each `TASFlavorCache` tracked its own per-domain `usage` independently. In reality, two ResourceFlavors can reference the **same Topology and overlap on the same physical nodes** (e.g. identical `nodeLabels`, differentiated only by flavor-level `nodeTaints`). Under the old model each sibling flavor counted usage separately, so a node fully consumed via flavor A still looked free to flavor B → **node over-subscription** ([[issue-10659]]).

[[pr-11210]] adds the **`TASHandleOverlappingFlavors`** feature gate (Alpha, off by default in v0.18 — guarded so the old per-flavor behaviour is the default and there is no perf regression). When enabled, sibling flavors that share a Topology aggregate usage at the **hostname-leaf** level:

- **Cache-write aggregation** (`TASFlavorCache.updateUsage`): each add/sub of `tr.TotalRequests()` (plus a `corev1.ResourcePods` delta) is mirrored into a shared per-Topology `SyncMap` (`topologies[T].Usage`), using an atomic read-modify-write (`SyncMap.Update`) so concurrent sibling writers serialize.
- **Snapshot path**: `snapshotTopologyUsages()` clones each eligible Topology's usage once; every sibling-flavor snapshot for that Topology aliases the same fresh map, so in-cycle mutations (preemption, fair-sharing) propagate across flavors without leaking to the live cache.
- **In-flight reservations** (`FindTopologyAssignmentsForWorkload`): a per-workload `sharedAssumed` map prevents a single workload's PodSets landing on different sibling flavors from self-overlapping on a shared node; flavors are iterated in deterministic sorted order so placements are reproducible.

Cross-flavor overlap is only supported when both flavors reference the **same** Topology; overlapping flavors with different topologies on the same node is explicitly unsupported.

## Defaults

"TAS: reduce friction by defaulting the PodSet annotations" ([[issue-3754]]) — for a flavor that's already TAS-enabled, defaulting the annotation to "unconstrained" rather than requiring the user to repeat it.

## Cached topology trees (`TASCacheTopologyTree`)

Before [[pr-13819]] every scheduling cycle rebuilt the entire TAS topology tree from scratch — domain hierarchy, node-to-domain mapping, leaf capacities — even though almost none of it changes between cycles.

The gate (**Beta/on from v0.20, Alpha/off on release-0.19** — cherry-picks [[pr-14639]], [[pr-14644]]) makes the cache hold an **immutable tree per TAS flavor**:

- the tree is reused while scheduling-relevant Node data is unchanged;
- **mutable** scheduling state stays in each snapshot, so concurrently created snapshots remain isolated;
- invalidation is driven by *semantic* node changes — labels, taints, allocatable resources. Node updates that cannot affect TAS placement do not invalidate.

Benchmark, 2,500 nodes / 15 TAS flavors / one non-TAS pod per node:

| Scenario | CPU time | Allocated bytes | Allocations |
|---|---|---|---|
| Cached tree reused | −71.74% | −60.96% | −64.50% |
| Invalidated every cycle | +5.55% | +10.54% | +23.57% |
| Invalidated every 2nd cycle | −32.54% | −25.05% | −20.28% |

The pathological case (invalidation every cycle) is a small *regression*, which is why the gate ships off on the release branch.

## Elastic workloads: the leader's assignment is preserved

For an elastic Workload (`ElasticJobsViaWorkloadSlicesWithTAS`) with a leader/workers PodSet group, recomputing placement on a resize must not move the leader.

- **Scale-up** ([[pr-14064]], original #13574): a scale-up recomputed the placement for the whole group and **overwrote the running leader Pod's `TopologyAssignment`**, so the leader Pod was restarted and lost its state. Kueue now keeps the leader's existing assignment and places only the newly added workers.
- **Same-count and scale-down** ([[pr-14076]], original #12436): leader PodSet assignments *and* their capacity accounting are preserved when the worker count stays the same or shrinks.

## `ComputeTASNetUsage` ignores shrinking domain counts

`ComputeTASNetUsage` **skips** a topology domain whose recomputed count is lower than what the previous admission already accounted for — i.e. a negative delta contributes zero rather than a negative usage. This defensive branch was added by #14572 for a state that should not arise normally; [[pr-14754]] / [[pr-14759]] / [[pr-14760]] (fixes [[issue-14645]]) added the dedicated test case, and [[pr-14762]] dropped `EquateEmpty` from it so an empty-vs-nil result is not silently accepted.

## Topology domains are held across scheduling cycles for a preemptor

With `PrioritizePreemptorWorkloads` on, a preemptor waiting for several staggered evictions keeps its chosen nodes/blocks across cycles: it is evaluated first, `cq.AddUsage` re-locks the domains in `TASFlavorSnapshot`, and interim pending Workloads fail `FitsCheckNoTAS`. Placement is stable across cycles because `updateAssignmentForTAS` simulates removal of the remaining targets and `sortedDomains` falls back to the deterministic `compareDomainLevelValues` tie-break. See [[scheduler-internals#Preemptor prioritization]] ([[pr-13797]], covered by [[pr-14687]]).

## `TASRecomputeAssignmentWithinSchedulingCycle` requires TAS

The gate could previously be enabled with `TopologyAwareScheduling` off, which is meaningless. [[pr-14256]] (original #14237) makes it depend on the TAS gate. **Action required**: if you disable `TopologyAwareScheduling`, also set `TASRecomputeAssignmentWithinSchedulingCycle=false` before upgrading, or the manager rejects the configuration at startup.

## Node health filtering can be delegated (`SchedulerLibraryIntegration`, Alpha)

With the Alpha `SchedulerLibraryIntegration` gate on, Kueue no longer applies node-readiness and `spec.unschedulable` checks when building the TAS node cache — the scheduler library performs them instead ([[pr-14203]], [[pr-14613]]). With the gate off (the default) TAS keeps doing its own filtering.

## Feature-gate stages (main / v0.20 development)

Stages read from `pkg/features/kube_features.go` (source: kube_features.go). All TAS gates below depend on `TopologyAwareScheduling` (Beta, on since v0.14).

| Gate | Stage / default | Effect |
|---|---|---|
| `TASHandleOverlappingFlavors` | Beta, on (since v0.18) | Shared per-Topology usage; older text above says Alpha/off at introduction |
| `TASNodeFeasibilityForAllLevels` | Beta, on (v0.20) | Per-node capacity/feasibility checks even when the Topology's lowest level is not `kubernetes.io/hostname` |
| `TASLeaderPodSetFeasibility` | Beta, on (v0.20) | Leader PodSet's own node filters are applied when picking a domain |
| `TASPartialSlices` | Beta, on (v0.20) | Slice size need not divide PodSet count |
| `TASGroupedPodSetSlicing` | Beta, on (v0.20) | Slicing together with PodSet groups |
| `TASTopologySpreading` | Alpha, off (v0.20) | Cross-Workload spreading annotation |
| `TASRejectFalseUnconstrainedTopology` | Alpha, off (v0.20) | Reject `podset-unconstrained-topology: "false"` |
| `TASValidateWorkloadSliceSize` | Beta, on (v0.20; GA noted for 0.21) | Reject non-positive slice sizes on Workloads |
| `SchedulerLibraryIntegration` | Alpha, off (v0.19) | Delegate node feasibility to scheduler-library (see *Workload-aware scheduling simulator* below) |

## Annotations belong on the PodTemplate

TAS annotations are read from the PodSet **template** metadata. For a `batch/v1` Job they must be in `spec.template.metadata.annotations`; an annotation on the Job's own `metadata.annotations` is silently ignored, with no error, event or condition. The docs for topology spreading, multi-layer topology and balanced placement were corrected to say this ([[pr-15816]], fixes [[issue-15791]]).

## Unconstrained annotation: `"false"` is rejected

`kueue.x-k8s.io/podset-unconstrained-topology` is an opt-in whose only meaningful value is `"true"`. Before [[pr-15262]], `"false"` passed validation and the JobFramework builder produced `TopologyRequest.Unconstrained=&false`. That counts as an explicit TAS request (so implicit TAS fallback is skipped) but selects no level, so the Workload could never be admitted (`topology level not specified`). Behind `TASRejectFalseUnconstrainedTopology` it is now rejected in the webhook **and** in the topology request builder (defense in depth for objects that bypassed the webhook). [[pr-15856]] added the same rule to the Workload webhook for `spec.podSets[].topologyRequest.unconstrained: false` on create and update. Open follow-up: the gate has no declared dependency on the other TAS gates in the same way in all paths ([[issue-15873]]).

## StatefulSet TAS validation

The StatefulSet reconciler builds `podSet.TopologyRequest` from the Pod template (`jobframework.NewPodSetTopologyRequest(...).PodIndexLabel(...)`), but its validating webhook did not validate those annotations. [[pr-15857]] validates them on create and [[pr-16039]] on update (fixes [[issue-15880]]); both only run when `TopologyAwareScheduling` is enabled. Backported to 0.18/0.19 ([[pr-15881]], [[pr-15882]], [[pr-16104]], [[pr-16105]]).

## Topology spreading (`TASTopologySpreading`, Alpha)

Cross-**Workload** spreading (KEP 13746, [[issue-13746]]): limits how many Workloads matching a label selector may occupy one domain. It is driven by the PodTemplate annotation `kueue.x-k8s.io/podset-topology-spreading` holding JSON (source: topology_types.go, spreading.go):

- `workloadLabelSelectors` — list of `LabelSelectorRequirement`s selecting, among Workloads **in the same namespace**, which count against each other (empty means the default group).
- `rules` — 1 to 2 entries (`minSpreadingRules=1`, `maxSpreadingRules=2`), each `{topologyKey, maxShareAllowingPlacement, enforcementMode}`. `maxShareAllowingPlacement` must be strictly in (0, 1). `enforcementMode` is `Required` (default, applied at parse time; domains over the share are excluded) or `Preferred` (over-share domains are only deprioritised by spread-aware ordering).
- Must be combined with `podset-required-topology`: a PodSet group is counted as occupying one domain per rule level, which only holds for required topology. A rule whose level is **below** the requested level is rejected (`topology spreading level ... is below the podset topology ...`).
- `ExceedsShare(count,total)` is `count > maxShare * total` in exact `inf.Dec` arithmetic; `total == 0` (cold start) never exceeds. Before [[pr-15862]] it used `Quantity.ScaledValue(milli)`, which rounds *up*, so `0.4501` became `451m` and 45.1% was allowed (fixes [[issue-15789]]).
- `NewSpreadingSpec` now defaults an empty enforcement mode to `Required` like `ParseSpreadingAnnotation` (and clones its input) so `HasRequiredSpreadingLevels` and placement checks do not skip those rules ([[pr-15860]], [[issue-15788]]).
- **PodSet-group constraint**: a shared group used for spreading must have exactly two PodSets, at least one with `Count == 1` (`ValidatePodSetGroupingTopology`; documented in [[pr-15859]]).

Validation and enforcement points hardened in this cycle:

- Annotation validation moved from `jobframework` to `pkg/util/tas` as `ValidateSpreadingAnnotation` (selectors, topology keys, share values, enforcement modes, duplicate keys) ([[pr-16248]]).
- Directly created or prebuilt Workloads used to bypass it. [[pr-15885]] runs the same validation in the Workload webhook when the gate is on: requires structured `topologyRequest.required`, consistent annotations within a named PodSet group (equivalent JSON is accepted, not only byte-identical), with ratcheting per PodSet and per group so unrelated updates are not blocked by pre-existing errors ([[issue-15784]]). Broader TAS checks (group size) were deliberately left out.
- **TAS-implied workloads**: on a ClusterQueue whose flavors are all TAS, TAS is implied even without `RequiredTopologyRequest`; flavor assignment skipped topology-level checks there, so a flavor lacking a required spreading level could match. `checkRequiredSpreadingLevels` in `tas_flavorassigner.go` now covers both explicit and implied paths ([[pr-16003]], [[issue-15786]]).
- **Preemption**: spreading bans blocked preemption. In the `Preempt` representative-mode check `FindTopologyAssignmentsForWorkload` runs with `simulateEmpty=true` but `topologySpreadCountsForFlavor` ignored it and counted existing Workloads, banning domains and yielding `NoFit`; and `updateAssignmentForTAS` used `SimulateWorkloadUsageRemoval`, which left victims in `cq.Workloads`. Fix: spread counts are zero when `simulateEmpty`, and `SimulateWorkloadRemoval` removes victims (and their Pods) from `cq.Workloads` during assignment then restores them ([[pr-16061]], [[issue-16021]]).
- The two `filterOutBannedDomains` calls in the descent loops of `findTopologyAssignment` were no-ops and were removed; the only ban filter is in `findLevelWithFitDomains` (`bannedBySpreading` walks ancestors; counts are filled once in `fillInCounts`). Invariants: spreading rules exist only in Required mode (so the fit level equals the requested level), balanced placement requires `!required`, and rules below the requested level are rejected ([[pr-16306]], [[issue-16305]]).
- Known gap closed as not planned: with *Preferred* topology, a parent domain whose capacity lies only in children banned by a Required spreading rule can yield an incomplete assignment without failure reason ([[issue-15787]]). Tracker for remaining work: [[issue-15740]].

## Partial slices (`TASPartialSlices`, Beta/on in v0.20)

A PodSet with slice topology previously required `count % sliceSize == 0`; with 10 Pods and slice size 4 only 8 Pods entered `TopologyAssignment` and the trailing 2 stayed scheduling-gated forever ([[pr-15640]]; backports [[pr-16121]], [[pr-16122]]). With the gate, the trailing Pods form one incomplete **tail slice** in a single domain:

- Each domain carries four capacities: `sliceCount`, `sliceCountWithLeader`, `sliceCountWithTail`, `sliceCountWithLeaderAndTail` (child penalties tracked jointly by `tailPenaltyTracker`, so co-located vs split leader/tail can be evaluated).
- Whole slices are placed greedily first, then `placeTail` finds a home, preferring domains already hosting whole slices.
- `normalizeTailLast` reorders the published assignment so the domain with the incomplete slice is **last**, preserving the ungater's `RankToDomainID` contract (otherwise a partial slice would fragment later whole slices in rank space).
- Multi-layer slice constraints (`podset-slice-required-topology-constraints`) are rejected when the count is not divisible by the **outermost** slice size.
- Not supported for partial slices in this first part: failed-node replacement (falls back to full requeue), balanced placement (falls back to best-fit) and elastic scale-up. Interaction with PartialAdmission is open ([[issue-16116]]). The PR description calls the gate Alpha but its final release note says Beta/on; the code says Beta/on (source: pr-15640.md, kube_features.go).

## Leader/worker PodSet groups: feasibility fixes

- **Leader's own filters** (`TASLeaderPodSetFeasibility`, [[pr-15447]], fixes [[issue-15373]]): domains for a PodSet group were chosen with the workers' node selector/tolerations/affinity only, so a leader with a different template was admitted where it could not run and stayed Pending holding quota. Leader selector, tolerations, node affinity and DRA feasibility are now checked. Backport [[pr-15690]].
- **Leader on its own node** ([[pr-15678]], fixes [[issue-15636]]): with virtual-hostname topologies (no explicit hostname level) the leader and workers may take different feasible nodes inside one domain (e.g. a rack).
- **Leader leaf cache** ([[pr-15689]], fixes [[issue-15685]]): the leader's feasible leaves are cached alongside the workers'; reused across preemption simulations (500 nodes: 348us to 243us; 2500 nodes: 1.88ms to 1.26ms). Backport [[pr-15852]].
- **Worker-only path decoupled** ([[pr-15861]], fixes [[issue-10812]]): with no leader, placement uses worker slice counts and no longer reads `stateWithLeader`; leader-specific capacity/retry logic is gated on a leader being required. Isolating leader state further is open ([[issue-15981]]).
- **Zero-count PodSets** ([[pr-16174]], regression fix for [[issue-16083]]; backports [[pr-16246]], [[pr-16247]]): the "probe" that fits hypothetical Pods for zero-count members now applies only when **every** effective count in the group is zero; mixed groups pick flavors from actual requests. TAS checks placement after choosing a flavor and never retries a skipped flavor, which is why the probe steered admission wrongly. Open: an elastic group scaling workers 0 to 1 with a tied count panics because `findLeaderAndWorkers` picks roles by count ([[issue-16239]]).
- **Non-adjacent group members** ([[pr-16273]], part of [[issue-16266]]; backports [[pr-16286]], [[pr-16287]]): flavor assignment and a replaced slice's admission are in *group* order, not Workload order. `TotalRequestsFor` and the workload-slice replacement flavor check paired PodSets by position, which could use another PodSet's counts/flavors, panic the scheduler in preemption or leave the Workload Pending. They now match PodSets **by name**; other positional consumers remain to be converted.

## Elastic (workload-slice) TAS fixes

- **Ungating across slices** ([[pr-15578]]): Pod events reference the *origin* slice, but expectations were recorded under the replacement's name, so they never cleared and late Pods stayed gated (`pending ungate operations`). The controller resolves the latest active slice before reading its admission and uses the stable origin name (`kueue.x-k8s.io/workload-slice-name`) for ungating expectations. Backports [[pr-15693]], [[pr-15706]].
- **Double-counting** ([[pr-15579]]): growing 2 to 4 one-CPU Pods on a 4-CPU node was classified `Preempt` because the snapshot already charged the old slice and placement charged it again. The replaced slice's TAS usage is temporarily removed during placement and the snapshot restored afterwards; quota accounting and other Workloads' usage are untouched. Backports [[pr-15586]], [[pr-15634]]. Related open bugs: replaced slice still counted within the scheduling-cycle snapshot ([[issue-16119]]), slice replacement can overcommit cohort quota ([[issue-16118]]).
- Evicted slices are drained before releasing quota ([[pr-15661]]).

## Node replacement and second pass

- **Required domain must be known** ([[pr-16321]], fixes [[issue-16291]]): with `TASReplaceMultipleFailedNodes` a remaining assigned node can be missing from the snapshot before entering `UnhealthyNodes`; an undeterminable required domain was treated as unrestricted and replacement Pods could land outside the required rack. Replacement is now rejected (a replacement-failure event; original assignment unchanged) when a *required* request still has a remaining assignment but no known domain. Preferred requests and replacing the whole assignment remain allowed.
- **Reservation-free marked Workloads** ([[pr-15571]], fixes [[issue-15504]]; backports [[pr-15655]], [[pr-15656]]): a Workload with `status.unhealthyNodes` but `status.admission == nil` took the node-replacement branch in `FindTopologyAssignmentsForFlavor`, skipped every PodSet as having no prior assignment, and returned a vacuous success, so TAS-only ClusterQueues committed flavors without a `TopologyAssignment`. The replacement branch now requires a current admission; otherwise fresh placement (or a real failure reason). The second-pass queue now requeues by key and **re-reads the live Workload** when the backoff elapses, so `NeedsSecondPass` and the release path act on current state; healed or deleted entries are skipped without a status write. Open follow-ups on the same race: [[issue-15658]], [[issue-16330]], [[issue-16331]].
- **Requeue scope** ([[pr-16152]]; backports [[pr-16161]], [[pr-16162]]): a Node-triggered TAS ResourceFlavor reconcile requeued inadmissible Workloads of *every* active ClusterQueue (also resetting their equivalence-hash cache). Now only ClusterQueues using that flavor are requeued (Cohort members are still reached because `NotifyRetryInadmissible` requeues the whole Cohort tree); `Cache.ActiveClusterQueues()` was removed.

## Workload-aware scheduling simulator

With `SchedulerLibraryIntegration` (Alpha), TAS feasibility is answered by a simulator backed by `sigs.k8s.io/scheduler-library` (`pkg/cache/scheduler/was`). Existing wiki coverage of the gate: [[scheduler-internals]]. Behaviour and structure now in main:

- **Structure**: `simulator.SchedulerSimulator` (`FindFeasibleNodes`, `PreemptWorkload`, `Simulate`) with a default implementation (`scheduling_simulator_default.go`) and `wasSimulator`. `wasSimulator` holds a cluster snapshot with every tracked Pod on its node, `podsByWorkload` (the only Pods `PreemptWorkload` can release) and a lazily-built `emptyCluster` (same nodes, no Pods) used when `requirements.SimulateEmpty` is set. It calls `MakePlacement(candidateNodeNames)` then `CanSchedulePod`; `NodeExclusionStats.SchedulerLibraryNoFit` counts rejects. The interface was renamed from snapshot to a factory of simulators ([[pr-16064]], backport [[pr-16117]]); `SchedulingSimulator.Snapshot` takes variadic `SnapshotOption`s such as `WithAssumedWorkloads` ([[pr-16009]]); pod-removal simulation moved to `Snapshot` and `forgetSimulatedFeasibility` became private ([[pr-16267]]).
- **Merged constraints reach the simulator** ([[pr-15456]], fixes [[issue-15455]], [[issue-15629]]): `PodRequirements.PodTemplate` is a plain deep copy of the PodSet template, while the TAS snapshot merges `ResourceFlavor.spec.tolerations` and AdmissionCheck `PodSetUpdates` only into the field form (`Tolerations`, `Selector`). The WAS path read the template, so flavor-only tolerations were ignored (never admitted) and ProvisioningRequest `nodeSelector` was ignored (wrong placement). The template's `tolerations` and `nodeSelector` are now overwritten with the merged values right after the copy. Still open for worker clusters: [[issue-15450]].
- **Scheduler name ignored** ([[pr-15635]], fixes [[issue-15630]]; backport [[pr-15643]]): the simulator builds a single `default-scheduler` profile, so a PodSet with another `spec.schedulerName` failed with `profile not found for scheduler name ...`. The name is now forced to `default-scheduler` for feasibility.
- **Preemption-aware feasibility** ([[pr-15436]], part of [[issue-12422]]): "would it fit if everything were preempted" was answered against the current cluster, so a host port held by the would-be victim made the node look unusable and preemption was never attempted. Feasibility now uses the cluster preemption would leave behind while preserving unmanaged-Pod occupancy. [[pr-15651]] (fixes [[issue-15631]]) likewise removes selected victims' Pods from the simulator during TAS overlap recomputation and restores simulator state, including on error paths.
- **Virtual pods** ([[pr-15720]], part of [[issue-13700]]): admitted or quota-reserved Workloads without running Pods are synthesised (`virtual_pods.go`, `PodsForWorkload`): PodSet template and namespace copied, `Spec.NodeName` from the `TopologyAssignment`, deterministic truncated name. Per Workload, virtual Pods replace real Pods if any could be generated; otherwise real Pods from the `podTracker` are kept. This makes node reservations accurate in feasibility and preemption simulations.
- **Planner** ([[pr-16158]], part of [[issue-5333]]): new `assignment.Planner` interface (`Plan(ctx, initialAssignment, opts...) Plan`, with `Plan.Assignment` and `PreemptionTargets`; `CanFit()` is true for `Fit`, or `Preempt` with at least one target) abstracts "fit the workload given flavors, topology requests and preemption". Only the native implementation exists; a SchedulerLibrary planner and a hybrid are planned. [[pr-16000]] made preemption rely on a `Strategy` producing a dynamically computed candidate iterator to accommodate future integrations.
- **Cleanup**: `newTASFlavorSnapshot` takes a `flavorInformation` struct ([[pr-15545]]).

## Related pages

- [[dra]] — per-node device feasibility runs inside TAS.
- [[scheduler-internals]]
- [[resource-flavor]] — opts a flavor into TAS.
- [[workload]] — where topology annotations live per PodSet.
- [[admission]] — where topology assignments are computed.
- [[preemption]] — TAS-aware preemption.
- [[elastic-jobs]] — interaction with dynamic resizing.
