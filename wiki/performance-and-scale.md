# Performance and scale

**Summary**: Kueue's throughput is bounded by its single scheduling loop, the cost of its in-memory cache updates, and the cost of the [[visibility-api]] snapshot. Scale pain has clustered around [[topology-aware-scheduling]] (per-domain accounting), cohort hierarchy updates, and visibility under load.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

---

## Where the loop spends time

Per scheduling cycle, cost drivers:

- Walking the per-CQ heap to pick candidates.
- For each candidate, computing the flavor-by-resource-group assignment.
- For TAS, computing the per-topology-domain fit.
- On preemption, collecting candidates and marking them evicted.

At moderate scale (hundreds of CQs, thousands of pending Workloads) the loop fits comfortably. At larger scale, hot spots appear:

- **TAS reconcile cost.** Listing all Workloads in the Node reconciler is expensive ([[issue-10037]] — TAS NodeHotSwap: Fix performance issue due to listing all Workloads in Reconcile).
- **TAS memory footprint.** "Optimize memory usage of TAS" ([[issue-3522]]) tracks the cache shape.
- **Visibility snapshot lock.** "Release the lock as soon as possible when computing the snapshot for CQ visibility" ([[issue-1098]]).
- **Cohort hierarchy updates.** "Unexport access to Cohorts and ClusterQueues maps in hierarchy.Manager" ([[issue-2996]]) was a cleanup that tightened mutation patterns so accesses could be made faster.
- **Terminating-pod accounting.** "TAS capacity accounting doesn't track Terminating pods" ([[issue-10076]]) caused false-negative admission decisions.

## Scale-oriented features

- **TAS NodeHotSwap** — a path for node replacement that avoids full re-reconcile.
- **Hierarchical cohort validation** — cheap checks that catch malformed trees before they enter the cache.
- **Subtree borrowing accounting** — correct subtree math was a bug ([[issue-10615]] — Subtree borrowing ignored when scheduling) whose fix also tightened the iteration hot path.

## Known non-linearities

- **`ClusterQueue.spec.resourceGroups` size.** Each resource group is walked per admission attempt; very wide groups multiply the cost per Workload.
- **Hierarchical cohort depth.** Borrowing walks upward at admission and preemption; deep trees pay that cost each time.
- **Number of TAS domains.** Per-domain accounting scales with the fanout at the innermost topology level.

## Integration-side scale

RayCluster with many worker groups, or a JobSet with many replicated jobs, creates multi-PodSet Workloads. Per-PodSet admission cost is linear; cohort-level preemption candidates include all admitted Workloads in the cohort, so CQ-per-namespace deployments keep this set small.

## Interpreting metrics

`kueue_admission_attempt_duration_seconds` and `kueue_admission_attempts_total` are the primary signals for loop health (see [[metrics]]). A climbing p99 with stable attempt count means per-attempt cost is rising (flavor groups grew, TAS domains grew, cohort deepened). A climbing attempt count with stable duration means demand is rising; tune queue strategy or split CQs.

## Related pages

- [[architecture]] — where the cache and queue live.
- [[metrics]] — scheduling-loop instrumentation.
- [[topology-aware-scheduling]] — main source of scale work.
- [[visibility-api]] — snapshot cost.
