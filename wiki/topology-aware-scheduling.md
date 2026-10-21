# Topology-Aware Scheduling (TAS)

**Summary**: TAS lets a [[workload]] request placement within a topology domain — a rack, a block, a zone — so bandwidth-sensitive Pods (ML training, MPI) don't get scattered across a data center. A ResourceFlavor references a `Topology` object that declares the topology levels; PodSets carry required/preferred annotations; Kueue picks a domain at admission and pins each Pod to nodes in that domain.

**Sources**: `raw/github/kubernetes-sigs__kueue/` (pr-15262, pr-15436, pr-15447, pr-15456, pr-15571, pr-15578, pr-15579, pr-15640, pr-15678, pr-15689, pr-15856, pr-15857, pr-15860, pr-15861, pr-15862, pr-15885, pr-16003, pr-16039, pr-16061, pr-16152, pr-16174, pr-16248, pr-16273, pr-16306, pr-16321, pr-12728, pr-13108, pr-13555, pr-13622, pr-15111, pr-15365, pr-16347, pr-16350, pr-16362, pr-16421, pr-16462, pr-16468, pr-16625, pr-16658, pr-16688, pr-16695, pr-16740, pr-16753, pr-16776, pr-16788, pr-16801, pr-16839, pr-16858, pr-16859, pr-16904, pr-17052, pr-14446, pr-16125, issue-16661, issue-16775 and others cited inline); `raw/kueue/pkg/features/kube_features.go`, `raw/kueue/pkg/util/tas/spreading.go`, `raw/kueue/apis/kueue/v1beta2/topology_types.go`.

**Last updated**: 2026-10-21

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
- **Node events vs cache staleness.** If a Node's labels change (or a ResourceFlavor's `nodeTaints`/`tolerations` change), the TAS cache must update ([[issue-3733]]). Topology updates/deletions likewise ([[issue-3614]]). Since v0.20.0, `spec.tolerations` of a ResourceFlavor with `spec.topologyName` set is **mutable**: the CRD rule blocking it was removed, and the TAS ResourceFlavor controller applies the new tolerations to the existing flavor cache in place (`TASFlavorCache.updateTolerations`, under the cache lock) *before* retrying inadmissible Workloads, so topology usage and per-Workload usage stay accounted across additions and removals (source: pr-13622.md, part of issue-3733). `spec.topologyName` stays immutable; the v0.20.0 CHANGELOG also lists separate changes making `spec.nodeLabels` updatable and `Topology.spec.levels` mutable when `kubernetes.io/hostname` is the lowest level (source: CHANGELOG-0.20.md; those PRs are not in this batch, and pr-13622.md still describes `nodeLabels` as immutable).
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

**Preemption candidates on overlapping flavors** (source: pr-16695.md, fixes issue-16141; backport pr-16919.md; listed under v0.20.2 in CHANGELOG-0.20.md at kueue@3bbb8cce4, a release cut after this snapshot). Usage was shared, but configurable preemption ([[configurable-preemptions]]) still picked only Workloads using one of the exact `{flavor, resource}` pairs that needed preemption. So a `PreemptionConfig` rule with the `QuotaFeasibleAndInsufficientTopology` trigger could never pick a Workload of a *sibling* flavor sitting on the nodes the preemptor needed. The preemptor stayed pending and the topology could not be defragmented. The fix adds `Snapshot.UsesOverlappingTASCapacity`, which reports whether a Workload's TAS usage on a source flavor sits on nodes that a target flavor also selects. It shares its condition (`propagatesTASUsage`) with `updateOverlappingTASUsage`, so the candidate filter and the usage propagation cannot drift apart. The check runs per Workload, against the domains of its topology assignment, and the resource name must match. Only the **resource filter** is wider, and only for the topology trigger. `Always` and `InsufficientQuota` keep the exact match, because only those Workloads free the quota the preemptor needs. Candidate selectors, the removal simulation and the minimality pass are unchanged, so sibling-flavor Workloads that are not needed for the fit are not preempted. The fix has no effect with `TASHandleOverlappingFlavors` off.

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
- **Workers scaling up from zero** (source: pr-16776.md, fixes issue-16775.md; backports pr-16817/0.19, pr-16820/0.20; shipped v0.19.8 / v0.20.1). Workers that had zero Pods have no `PreviousAssignment`, so `handleElasticWorkload` returned early. The whole group then went through fresh placement and the **running leader could be moved** to another domain. Now, when the workers have no previous assignment but the leader has one, the request is treated as a scale-up from zero and goes through `handleScaleUp`, which keeps the leader's assignment and places only the new workers.
- **Scheduler panic when workers reach the leader's count** (source: pr-16740.md, fixes issue-16239; backports pr-16810/0.20, pr-16812/0.19; shipped v0.19.8 / v0.20.1). `findLeaderAndWorkers` infers roles **by count**: the PodSet with fewer Pods is the leader. On a tie (leader 1, workers 0 to 1) it kept the *second* PodSet as leader, so with the leader listed first the workers were taken as the leader. Their nil `PreviousAssignment` was then dereferenced in `finalizeElasticAssignment`. On a tie, the PodSet that already has a previous assignment is now the leader. `PreviousAssignment` is set only for elastic slice replacements, so other Workloads are unaffected. Removing count-based role inference altogether is tracked in issue-16265. A scale-up from 0 to 1 needs both fixes.
- `TruncateAssignment` (`pkg/util/tas/tas_assignment.go`) handled `ta == nil` and `newCount <= 0` in one branch that dereferenced `ta.Levels`, so a nil assignment panicked. It now returns nil for a nil input. This path is not reachable today because `handleScaleDown` runs only after the nil-`PreviousAssignment` early return (source: pr-14446.md; backports pr-16755/0.19, pr-16756/0.20).

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
| `TASValidateWorkloadSliceSize` | Beta, on (v0.20; GA noted for 0.21) | Reject non-positive slice sizes on Workloads (see *Slice-size and subGroupCount validation*) |
| `SchedulerLibraryIntegration` | Alpha, off (v0.19) | Delegate node feasibility to scheduler-library (see *Workload-aware scheduling simulator* below). Since v0.20.0 it **depends on `TopologyAwareScheduling`** in `defaultFeatureGateDependencies` (source: pr-16362.md) |
| `SchedulerLibraryDeepIntegration` | Alpha, off (introduced on main for 0.21; not in any release) | Use the WAS planner (`ScheduleWorkload()`) for topology assignment and preemption targets; depends on `SchedulerLibraryIntegration` (source: pr-16347.md, kube_features.go). Inert for TAS Workloads at this snapshot |

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
- **Observability of spreading bans** (source: pr-16421.md, refactor with release-note NONE). When a Required rule banned domains and the rest lacked capacity, the pending message only mentioned capacity. `filterOutBannedDomains` now returns both the allowed and the banned domains. The banned ones are kept on the placement state (`spreadBannedDomains`), and the failure reason gets a suffix such as `; topology spreading excluded 1 topology domain(s) at level: cloud.com/topology-block`. A `V(3)` log also lists the Workload, PodSet, searched level, banned domains and rules (source: tas_flavor_snapshot.go). `domainIDs` moved from test code into production code for this log.
- Known gap closed as not planned: with *Preferred* topology, a parent domain whose capacity lies only in children banned by a Required spreading rule can yield an incomplete assignment without failure reason ([[issue-15787]]). Tracker for remaining work: [[issue-15740]].

## Partial slices (`TASPartialSlices`, Beta/on in v0.20)

A PodSet with slice topology previously required `count % sliceSize == 0`; with 10 Pods and slice size 4 only 8 Pods entered `TopologyAssignment` and the trailing 2 stayed scheduling-gated forever ([[pr-15640]]; backports [[pr-16121]], [[pr-16122]]). With the gate, the trailing Pods form one incomplete **tail slice** in a single domain:

- Each domain carries four whole-slice capacities: plain, with leader, with tail, and with leader plus tail. Child penalties are tracked jointly by `tailPenaltyTracker`, so a co-located leader and tail can be compared with a split one. **Update (2026-10-21)**: the four capacities were separate fields (`sliceCount`, `sliceCountWithLeader`, `sliceCountWithTail`, `sliceCountWithLeaderAndTail`). They are now one array, `domainState.sliceCount [4]int32`, indexed by an `obligationMask` (`obligationNone`, `obligationLeader = 1<<0`, `obligationTail = 1<<1`; `obligationMaskFor(withLeader, withTail)`) and read through `sliceCapacity(mask)`. This is a pure refactor and replaces the "leaderDomainState" idea from issue-15981, which could not cleanly capture the tail combinations (source: pr-16350.md, fixes issue-15981; backport pr-16434/0.19; tas_flavor_snapshot.go).
- Whole slices are placed greedily first, then `placeTail` finds a home, preferring domains already hosting whole slices.
- `normalizeTailLast` reorders the published assignment so the domain with the incomplete slice is **last**, preserving the ungater's `RankToDomainID` contract (otherwise a partial slice would fragment later whole slices in rank space).
- Multi-layer slice constraints (`podset-slice-required-topology-constraints`) are rejected when the count is not divisible by the **outermost** slice size.
- Not supported for partial slices in this first part: failed-node replacement (falls back to full requeue), balanced placement (falls back to best-fit) and elastic scale-up. Interaction with PartialAdmission is open ([[issue-16116]]). The PR description calls the gate Alpha but its final release note says Beta/on; the code says Beta/on (source: pr-15640.md, kube_features.go).

## Leader/worker PodSet groups: feasibility fixes

- **Leader's own filters** (`TASLeaderPodSetFeasibility`, [[pr-15447]], fixes [[issue-15373]]): domains for a PodSet group were chosen with the workers' node selector/tolerations/affinity only, so a leader with a different template was admitted where it could not run and stayed Pending holding quota. Leader selector, tolerations, node affinity and DRA feasibility are now checked. Backport [[pr-15690]].
- **Leader on its own node** ([[pr-15678]], fixes [[issue-15636]]): with virtual-hostname topologies (no explicit hostname level) the leader and workers may take different feasible nodes inside one domain (e.g. a rack).
- **Leader leaf cache** ([[pr-15689]], fixes [[issue-15685]]): the leader's feasible leaves are cached alongside the workers'; reused across preemption simulations (500 nodes: 348us to 243us; 2500 nodes: 1.88ms to 1.26ms). Backport [[pr-15852]].
- **Worker-only path decoupled** ([[pr-15861]], fixes [[issue-10812]]): with no leader, placement uses worker slice counts and no longer reads `stateWithLeader`; leader-specific capacity/retry logic is gated on a leader being required. The follow-up to isolate leader state ([[issue-15981]]) was closed by the `obligationMask` refactor (see *Partial slices*; source: pr-16350.md).
- **Zero-count PodSets** ([[pr-16174]], regression fix for [[issue-16083]]; backports [[pr-16246]], [[pr-16247]]): the "probe" that fits hypothetical Pods for zero-count members now applies only when **every** effective count in the group is zero; mixed groups pick flavors from actual requests. TAS checks placement after choosing a flavor and never retries a skipped flavor, which is why the probe steered admission wrongly. The panic when an elastic group scales workers 0 to 1 with a tied count ([[issue-16239]]) is fixed; see *Elastic workloads* above (source: pr-16740.md).
- **Non-adjacent group members** ([[pr-16273]], part of [[issue-16266]]; backports [[pr-16286]], [[pr-16287]]): flavor assignment and a replaced slice's admission are in *group* order, not Workload order. `TotalRequestsFor` and the workload-slice replacement flavor check paired PodSets by position, which could use another PodSet's counts/flavors, panic the scheduler in preemption or leave the Workload Pending. They now match PodSets **by name**; other positional consumers remain to be converted. **Update (2026-10-21)**: two more were converted, see *Non-adjacent PodSet groups: remaining positional pairings* below (source: pr-16658.md, pr-17052.md).

## Elastic (workload-slice) TAS fixes

- **Ungating across slices** ([[pr-15578]]): Pod events reference the *origin* slice, but expectations were recorded under the replacement's name, so they never cleared and late Pods stayed gated (`pending ungate operations`). The controller resolves the latest active slice before reading its admission and uses the stable origin name (`kueue.x-k8s.io/workload-slice-name`) for ungating expectations. Backports [[pr-15693]], [[pr-15706]].
- **Double-counting** ([[pr-15579]]): growing 2 to 4 one-CPU Pods on a 4-CPU node was classified `Preempt` because the snapshot already charged the old slice and placement charged it again. The replaced slice's TAS usage is temporarily removed during placement and the snapshot restored afterwards; quota accounting and other Workloads' usage are untouched. Backports [[pr-15586]], [[pr-15634]].
- **Replacement accounting within one scheduling cycle** (main #16125, fixes [[issue-16118]] and [[issue-16119]], both listed here as open before; backports pr-16601.md/0.20 and pr-16613.md/0.19; shipped v0.20.1 / v0.19.8). Two bugs: a resize could let the scheduler admit other Workloads beyond a Cohort's quota in the same cycle, and the replaced slice's TAS usage stayed in the cycle snapshot and pushed other Workloads to the next cycle. Now the old slice's usage is **released once** and the replacement is booked in full, while fair-sharing ranking still uses only the incremental request. `Snapshot.ReleaseWorkloadUsage` records the slice in a cycle-local `released` set. The slice stays in its ClusterQueue, so replacement and fork detection still find it, and later `RemoveWorkload`/`AddWorkload` calls in preemption or fit simulations skip its usage, so it is never released twice. A later preemptor that picks an already-released slice gains nothing from it and keeps looking for other victims. With `ElasticJobsViaWorkloadSlicesWithTAS` **off**, quota still moves to the replacement, but the old topology usage stays counted because those Pods are still running (source: pr-16125.md, pr-16601.md, snapshot.go).
- Evicted slices are drained before releasing quota ([[pr-15661]]).

## Node replacement and second pass

- **Required domain must be known** ([[pr-16321]], fixes [[issue-16291]]): with `TASReplaceMultipleFailedNodes` a remaining assigned node can be missing from the snapshot before entering `UnhealthyNodes`; an undeterminable required domain was treated as unrestricted and replacement Pods could land outside the required rack. Replacement is now rejected (a replacement-failure event; original assignment unchanged) when a *required* request still has a remaining assignment but no known domain. Preferred requests and replacing the whole assignment remain allowed.
- **Reservation-free marked Workloads** ([[pr-15571]], fixes [[issue-15504]]; backports [[pr-15655]], [[pr-15656]]): a Workload with `status.unhealthyNodes` but `status.admission == nil` took the node-replacement branch in `FindTopologyAssignmentsForFlavor`, skipped every PodSet as having no prior assignment, and returned a vacuous success, so TAS-only ClusterQueues committed flavors without a `TopologyAssignment`. The replacement branch now requires a current admission; otherwise fresh placement (or a real failure reason). The second-pass queue now requeues by key and **re-reads the live Workload** when the backoff elapses, so `NeedsSecondPass` and the release path act on current state; healed or deleted entries are skipped without a status write. Follow-ups on the same race: [[issue-15658]], [[issue-16330]] (fixed by pr-16462, below), [[issue-16331]].
- **Second-pass hardening** (all shipped v0.19.8 / v0.20.1; the second pass covers delayed topology assignment and failed-node replacement):
  - *Keep the reservation when a pass is already pending* (source: pr-16462.md, fixes issue-16330; backports pr-16491/0.20, pr-16494/0.19; regression). `QueueSecondPassIfNeeded` returned `false` when the Workload was already prequeued. `requeueAndUpdate` read that as "not requeued", and because `RequeueWorkload` refuses a Workload that still holds a reservation, a `notNominated` or `skipped` entry fell through and **unset the quota reservation**. For a failed-node replacement it could also clear the **admission**. An already-prequeued pass now counts as handled (`true`): the pending pass re-reads and retries the Workload, and `prequeueIfAbsent` still keeps a single pending timer (the #13745 behaviour).
  - *No lost request during re-read* (source: pr-16468.md, related issue-15658; backports pr-16503/0.20, pr-16533/0.19). `queueSecondPass` re-reads the Workload before deciding. A new request arriving between that read and the decision saw the old pass as pending, and the old pass then dropped the Workload based on its earlier read, so the retry was lost until the Workload changed again. The `secondPassQueue` lock is now held across the re-read and the queue decision, nested under the manager lock. This works because informer updates are stored before handlers run: a concurrent request is either seen by the re-read or arrives later and arms a new pass.
  - *Abort a stale admission write* (main #15761, carried here by backports pr-16858.md/0.20 and pr-16859.md/0.19). A second pass computed from an outdated Workload could overwrite a newer admission or drop status set in the meantime, such as an `Evicted` condition. When `workload.NeedsSecondPass(wl)`, `patchWorkloadAdmission` now sends the Workload's `resourceVersion` **without retry-on-conflict**, so an outdated write fails with `Conflict`. On that conflict the scheduler puts the version it read back into the cache with `Cache.UpdateWorkloadIfUnchanged`. That call stores it only if the cache still holds the same `resourceVersion`, so it is skipped when an event already replaced or removed the entry. The reservation is kept, a Warning event `OutdatedScheduleCycle` is emitted ("Skipped admission write because the workload changed while it was being scheduled"), and the pass is requeued (source: scheduler.go, cache.go). On release-0.19 `admit()` picks the strict patch options itself, and its `UnhealthyNodes` clearing applies only to the version the pass read.
- **Node replacement waited on unrelated Pods** (source: pr-15365.md, fixes issue-15360; shipped v0.20.0, cherry-pick to 0.18/0.19 requested). `workloadslicing.ListPodsForWorkloadSlice` dropped the caller's field selectors. With `TASReplaceNodeOnPodTermination`, replacement therefore waited for running Pods of *other* Workloads or unmanaged Pods on the failed node. Only the affected Workload's Pods are checked now.
- **Ungater ignores stuck Pods outside the current assignment** (source: pr-16788.md; backports pr-16795/0.19, pr-16796/0.20; shipped v0.19.8 / v0.20.1). Before assigning domains by rank, the topology ungater lists the Workload's non-terminated Pods. That list can include a Pod from a previous admission still **terminating on a failed node**. If it shares a rank with a new Pod, `readRanksIfAvailable` fails and the ungater falls back to greedy assignment, breaking rank-based placement after node replacement or re-admission. Pods that are already ungated and placed in a domain outside the current `TopologyAssignment` (`sets.New(slices.Collect(utiltas.DomainIDs(psa.TopologyAssignment))...)`) are now ignored, with a `V(3)` log. Known gap, open as of this snapshot: keeping rank-based ordering when a Pod's rank has no domain (pr-16771, open).
- **Requeue scope** ([[pr-16152]]; backports [[pr-16161]], [[pr-16162]]): a Node-triggered TAS ResourceFlavor reconcile requeued inadmissible Workloads of *every* active ClusterQueue (also resetting their equivalence-hash cache). Now only ClusterQueues using that flavor are requeued (Cohort members are still reached because `NotifyRetryInadmissible` requeues the whole Cohort tree); `Cache.ActiveClusterQueues()` was removed.

## Slice-size and subGroupCount validation

Job webhooks already rejected a `kueue.x-k8s.io/podset-slice-size` annotation below 1 (`must be greater than or equal to 1`). A hand-built Workload with `spec.podSets[].topologyRequest.podSetSliceSize: 0` was still accepted, and it could reach `count % 0` in the TAS snapshot. The scheduler has no `recover()`, so that would have crashed `kueue-controller-manager` (source: pr-12728.md). Maintainers decided not to support `PodSetSliceSize = 0`: allowing `replicas: 0` (scale to zero) is not an argument for a zero slice size, and validation can be relaxed later while tightening it is hard. The fix has three layers (shipped v0.20.0, **ACTION REQUIRED**):

- **CRD**: `podSetSliceSize` has `+kubebuilder:validation:Minimum=1` in v1beta1/v1beta2 (added by #13634 for v0.20). Schema changes are not cherry-picked, because patch upgrades often roll only the image.
- **Workload webhook** behind `TASValidateWorkloadSliceSize` (Beta, on): `validateTASSliceSize` requires `podSetSliceSize` when `podSetSliceRequiredTopology` is set (`must be set when ...`), forbids it otherwise (`may not be set when podSetSliceRequiredTopology is not specified`), and rejects any `podsetSliceRequiredTopologyConstraints[i].size <= 0`. Disabling the gate turns off only the webhook checks; the CRD minimum still applies.
- **Scheduler**: `getSliceSizeWithSinglePodAsDefault` returns 1 when no slice constraint exists, and the reason `slice topology requested, but slice size not provided` for a non-positive size. This also guards the node-replacement callers (`findReplacementAssignment`, `requiredReplacementDomain`) that review found would otherwise divide by zero (source: pr-12728.md, tas_flavor_snapshot.go, workload_webhook.go).

**Negative `subGroupCount`** (source: pr-13108.md, shipped v0.20.0): the Workload API again rejects a negative `spec.podSets[].topologyRequest.subGroupCount` through the schema (`Minimum=0`). The 0.19 line (#13101) had downgraded it to a deprecation warning (`warningsForWorkload`). Zero is accepted without a warning.

## PodSet slicing alongside grouping (`TASGroupedPodSetSlicing`, Beta/on in v0.20)

`ValidateTASPodSetRequest` (`pkg/controller/jobframework/tas_validation.go`) used to reject combining `kueue.x-k8s.io/podset-group-name` with `podset-slice-size` / `podset-slice-required-topology` (#6242). The placement algorithm already supported it. A typical case is a [[integration-leaderworkerset]] whose leader and workers share a required or preferred group domain (e.g. `cloud.com/block`) while the workers are also sliced at an inner level (e.g. `kubernetes.io/hostname`). The change only relaxes validation behind the gate, and the tests show the existing algorithm behaves correctly. Covered cases: hostname slicing with a leader that needs less; node-failure replacement that keeps co-location with the intact leader; best-fit block choice (1 leader + 19 workers, slice size 5); a GPU-less leader next to GPU-sliced workers; rejection when leader plus sliced workers fit no single required block; and preferred-block fallback that still honours required hostname slicing. With the gate off, the combination is still rejected (source: pr-15111.md; cherry-picks prepared because the limitation affected users).

## Non-adjacent PodSet groups: remaining positional pairings

When the members of a PodSet group are not adjacent in `spec.podSets` (e.g. spec order `leader, other, worker`), the flavor-assignment/admission order (group order) differs from spec order. Fixes in this batch, after [[pr-16273]]:

- **Flavor scan resume and TAS second pass** (source: pr-16658.md, fixes issue-16661, part of issue-16266; backports pr-16757/0.20, pr-16760/0.19; shipped v0.20.1 / v0.19.8). Two paths still paired PodSets by position. Flavor-scan resume could restore the wrong PodSet's scan state, leaving a Workload pending although an assignment fits. The TAS second pass could use another PodSet's data and **reorder the admission**, which the webhook then rejected on every retry. Reordered PodSets are now mapped back to spec indexes with the new `podset.SpecIndexes` helper (`pkg/util/podset`, next to `FindPodSetByName`). Grouping uses `tas.GroupKeyForPodSet`, whose keys are namespaced `podsetgroup/<group>` or `podset/<name>`. Before, decimal PodSet indexes and group names shared one key space, so a group named `"1"` could collide with the ungrouped PodSet at index 1 and `orderedgroups.Insert` merged unrelated requests and seeded flavors (issue-16661). The flavor-assigner side is documented on [[scheduler-internals]].
- **Starting the job** (source: pr-17052.md, fixes issue-16266; backport pr-17092/0.19; listed under v0.19.9 / v0.20.2 in the CHANGELOG at kueue@3bbb8cce4, releases cut after this snapshot). The job reconciler applied admission info by position, so with JobSet it could swap labels, node selectors and topology annotations between ReplicatedJobs and leave Pods `SchedulingGated` after admission. Assignments are now matched **by PodSet name** and the infos are built in spec order. A missing assignment follows the existing invalid-PodSet-info path and finishes the Workload with `FailedToStart`.
- Inferring leader/worker roles by count remains a general hazard (issue-16265).

## DRA-backed extended resources counted between PodSets

With `KueueDRADeviceFeasibility` (Alpha, v0.20), a DRA-backed extended resource is counted against a node that publishes it through a device plugin (`forLeaf`). But the usage TAS **records between the PodSets of one Workload** came from `SinglePodRequests`, where that resource is zeroed for the device check. A later PodSet therefore saw the device as still free: two PodSets needing one device each could both land on a node that publishes one, and a Pod stayed Pending. An elastic scale-up hit the same miscount and stayed pending, because placement kept picking the retained Pod's node and the final fit check kept rejecting it. The rule the flavor assigner applies to an assignment's TAS usage moved to `TASFlavorSnapshot.RequestsForDomain`, and `forLeaf` uses the same helper. All recording paths (regular placement, node replacement, elastic scale up/down) now go through it. Nothing changes with the gate off. Not backported to 0.19, which has neither the gate nor `tas_dra.go` (source: pr-16625.md; backport pr-16809/0.20, shipped v0.20.1). Documented remaining gaps:

- When the lowest topology level is above the node (e.g. rack), usage of admitted Workloads, or of Pods an elastic scale-up keeps, is recorded per rack, not per node. Placement does not see devices those Pods hold, so a Pod can still be placed in a rack whose device plugins are exhausted.
- `RequestsForDomain` counts delegated resources on a node only when the node publishes **every** one of them, whereas kube-scheduler decides per resource.

See [[dra]].

## Workload-aware scheduling simulator

With `SchedulerLibraryIntegration` (Alpha), TAS feasibility is answered by a simulator backed by `sigs.k8s.io/scheduler-library` (`pkg/cache/scheduler/was`). Existing wiki coverage of the gate: [[scheduler-internals]]. Behaviour and structure now in main:

- **Structure**: `simulator.SchedulerSimulator` (`FindFeasibleNodes`, `PreemptWorkload`, `Simulate`) with a default implementation (`scheduling_simulator_default.go`) and `wasSimulator`. `wasSimulator` holds a cluster snapshot with every tracked Pod on its node, `podsByWorkload` (the only Pods `PreemptWorkload` can release) and a lazily-built `emptyCluster` (same nodes, no Pods) used when `requirements.SimulateEmpty` is set. It calls `MakePlacement(candidateNodeNames)` then `CanSchedulePod`; `NodeExclusionStats.SchedulerLibraryNoFit` counts rejects. The interface was renamed from snapshot to a factory of simulators ([[pr-16064]], backport [[pr-16117]]); `SchedulingSimulator.Snapshot` takes variadic `SnapshotOption`s such as `WithAssumedWorkloads` ([[pr-16009]]); pod-removal simulation moved to `Snapshot` and `forgetSimulatedFeasibility` became private ([[pr-16267]]).
- **Merged constraints reach the simulator** ([[pr-15456]], fixes [[issue-15455]], [[issue-15629]]): `PodRequirements.PodTemplate` is a plain deep copy of the PodSet template, while the TAS snapshot merges `ResourceFlavor.spec.tolerations` and AdmissionCheck `PodSetUpdates` only into the field form (`Tolerations`, `Selector`). The WAS path read the template, so flavor-only tolerations were ignored (never admitted) and ProvisioningRequest `nodeSelector` was ignored (wrong placement). The template's `tolerations` and `nodeSelector` are now overwritten with the merged values right after the copy. Still open for worker clusters: [[issue-15450]].
- **Scheduler name ignored** ([[pr-15635]], fixes [[issue-15630]]; backport [[pr-15643]]): the simulator builds a single `default-scheduler` profile, so a PodSet with another `spec.schedulerName` failed with `profile not found for scheduler name ...`. The name is now forced to `default-scheduler` for feasibility.
- **Preemption-aware feasibility** ([[pr-15436]], part of [[issue-12422]]): "would it fit if everything were preempted" was answered against the current cluster, so a host port held by the would-be victim made the node look unusable and preemption was never attempted. Feasibility now uses the cluster preemption would leave behind while preserving unmanaged-Pod occupancy. [[pr-15651]] (fixes [[issue-15631]]) likewise removes selected victims' Pods from the simulator during TAS overlap recomputation and restores simulator state, including on error paths.
- **Virtual pods** ([[pr-15720]], part of [[issue-13700]]): admitted or quota-reserved Workloads without running Pods are synthesised (`virtual_pods.go`, `PodsForWorkload`): PodSet template and namespace copied, `Spec.NodeName` from the `TopologyAssignment`, deterministic truncated name. Per Workload, virtual Pods replace real Pods if any could be generated; otherwise real Pods from the `podTracker` are kept. This makes node reservations accurate in feasibility and preemption simulations.
- **Planner** ([[pr-16158]], part of [[issue-5333]]): new `assignment.Planner` interface (`Plan(ctx, initialAssignment, opts...) Plan`, with `Plan.Assignment` and `PreemptionTargets`; `CanFit()` is true for `Fit`, or `Preempt` with at least one target) abstracts "fit the workload given flavors, topology requests and preemption". At that point only the native implementation existed. [[pr-16000]] made preemption rely on a `Strategy` producing a dynamically computed candidate iterator to accommodate future integrations.
- **Cleanup**: `newTASFlavorSnapshot` takes a `flavorInformation` struct ([[pr-15545]]). The scheduler-library import alias `schedLibSnapshot` was renamed to `schedlib` (source: pr-16839.md; backports pr-16844, pr-16933).
- **hostPort feasibility** (source: pr-13555.md, partly addresses issue-13534; shipped v0.20.0). The simulator's single `default-scheduler` profile (`newWASSchedulerConfig` in `pkg/cache/scheduler/was/simulator_factory.go`) enables the `NodePorts` plugin at PreFilter and Filter, next to `NodeUnschedulable`, `TaintToleration` and `NodeAffinity`. Nodes whose requested `hostPort`/protocol is already taken are skipped. The simulator keeps per-Pod state as tracked Pods are added, updated or removed, so a removed Pod frees its ports. At merge time, reviewers noted this Pod awareness did not cover preemption simulations or in-flight (quota-reserved, Pod-less) Workloads. They chose not to add a separate gate, because Alpha carries no compatibility promise. Both gaps were then addressed by the preemption-aware feasibility ([[pr-15436]]) and virtual-pod ([[pr-15720]]) work above.

### Deep integration (`SchedulerLibraryDeepIntegration`, Alpha, main only)

Deep integration aims to let the scheduler library's `ScheduleWorkload()` decide topology assignments and preemption targets, not just node feasibility (issue-15333, umbrella issue-13151; a KEP is planned for v0.21). The gate added in pr-16347.md selects among four modes:

| `TopologyAwareScheduling` | `SchedulerLibraryIntegration` | `SchedulerLibraryDeepIntegration` | Mode |
|---|---|---|---|
| off | (any) | (any) | non-TAS scheduling |
| on | off | (any) | `tas-internal` (native TAS) |
| on | on | off | `tas-schedlib-feasibility` (WAS answers node feasibility only) |
| on | on | on | `tas-schedlib-deep` |

**Current state at this snapshot** (source: scheduler.go, `pkg/scheduler/assignment/was/was_planner.go`): in `getAssignments`, the gate picks `wasplanner.NewPlanner(wl, snap)` instead of `nativeplanner.NewPlanner(...)`. The WAS planner is **inert**. It returns the initial flavor assignment untouched for `NoFit`, and for `Fit` without TAS requests. Every other case (any TAS request, or `Preempt`) gets `Plan.Error = "was planner unable to process assignment"`. So with the gate on, TAS Workloads cannot be admitted: the scheduler logs `Failed to compute the initial assignment` and sets the inadmissible message with `quotaReservedReason = AssignmentError` (`WorkloadQuotaReservedReasonAssignmentError`). Do not enable it outside development.

Preparatory pieces merged with it:

- `assignment.Plan` gained an **`Error`** field. A set `Error` invalidates the whole plan, and `CanFit()` returns false. `getAssignments` now propagates the error, and partial admission is attempted only when `!CanFit() && Error == nil` (source: pr-16801.md).
- The flavor assigner was prepared for the WAS planner (source: pr-16688.md, backport pr-17021/0.20). The `Assignment` struct and dependent types moved into `pkg/scheduler/flavorassigner/assignment.go` with no logic change (source: pr-16847.md).
- `was.BuildVirtualPodGroup(wl)` builds an **in-memory gang `PodGroup`** (`scheduling.k8s.io/v1beta1`) for a whole Workload. `ScheduleWorkload()` needs PodGroups in its `ClusterSnapshot`, but real ones may not exist yet, for example because the job is suspended or has no WAS integration. The builder sets `MinCount` to the sum of all PodSet counts and rejects totals `<= 0` or above `MaxInt32`. Its name is `VirtualPodGroupName`: `virtual-pg-<workload>` truncated to fit, plus a SHA-1 suffix. It is not wired into any caller yet and has no TAS support. Real PodGroups are ignored for now; reconciling with them is future work (source: pr-16904.md, virtual_podgroups.go). See [[gang-scheduling]].
- Makefile targets `test-e2e-was-deep-tas-*` run the `singlecluster/tasapi` e2e suites with both scheduler-library gates on via `E2E_EXTRA_KUEUE_FEATURE_GATES` (source: pr-16753.md).

## Related pages

- [[dra]] — per-node device feasibility runs inside TAS.
- [[scheduler-internals]]
- [[resource-flavor]] — opts a flavor into TAS.
- [[workload]] — where topology annotations live per PodSet.
- [[admission]] — where topology assignments are computed.
- [[preemption]] — TAS-aware preemption.
- [[elastic-jobs]] — interaction with dynamic resizing.
- [[configurable-preemptions]] — `QuotaFeasibleAndInsufficientTopology` trigger and overlapping-flavor candidates.
- [[integration-leaderworkerset]] — grouped and sliced PodSets.
- [[gang-scheduling]] — virtual gang PodGroups for the WAS deep integration.
