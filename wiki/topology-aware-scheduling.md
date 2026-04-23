# Topology-Aware Scheduling (TAS)

**Summary**: TAS lets a [[workload]] request placement within a topology domain — a rack, a block, a zone — so bandwidth-sensitive Pods (ML training, MPI) don't get scattered across a data center. A ResourceFlavor references a `Topology` object that declares the topology levels; PodSets carry required/preferred annotations; Kueue picks a domain at admission and pins each Pod to nodes in that domain.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

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
- **Oversubscription with multiple flavors on same nodes.** A Node in two TAS ResourceFlavors led to over-counting ([[issue-10659]]).
- **TAS + cohorts/preemption.** Reclaiming capacity within a topology domain constrains preemption more than the cohort-level case ([[issue-3761]] — make TAS compatible with cohorts and preemption; [[issue-10497]] — preemption can under-select candidates needed to free a topology domain).

## Bin-packing quality

Default placement is greedy. "Optimal bin-packing in TAS" ([[issue-10574]]) tracks algorithmic improvements; "Better accuracy of scheduling by tighter integration with kube-scheduler" ([[issue-3755]]) discusses reducing the split between Kueue's topology choice and the scheduler's node choice.

## Defaults

"TAS: reduce friction by defaulting the PodSet annotations" ([[issue-3754]]) — for a flavor that's already TAS-enabled, defaulting the annotation to "unconstrained" rather than requiring the user to repeat it.

## Related pages

- [[resource-flavor]] — opts a flavor into TAS.
- [[workload]] — where topology annotations live per PodSet.
- [[admission]] — where topology assignments are computed.
- [[preemption]] — TAS-aware preemption.
- [[elastic-jobs]] — interaction with dynamic resizing.
