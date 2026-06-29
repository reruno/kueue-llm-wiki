# Topology-Aware Scheduling (TAS)

**Summary**: TAS lets a [[workload]] request placement within a topology domain — a rack, a block, a zone — so bandwidth-sensitive Pods (ML training, MPI) don't get scattered across a data center. A ResourceFlavor references a `Topology` object that declares the topology levels; PodSets carry required/preferred annotations; Kueue picks a domain at admission and pins each Pod to nodes in that domain.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-06-29

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

## Related pages

- [[resource-flavor]] — opts a flavor into TAS.
- [[workload]] — where topology annotations live per PodSet.
- [[admission]] — where topology assignments are computed.
- [[preemption]] — TAS-aware preemption.
- [[elastic-jobs]] — interaction with dynamic resizing.
