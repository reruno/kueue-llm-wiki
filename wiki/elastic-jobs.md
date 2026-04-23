# Elastic jobs

**Summary**: Elastic jobs let an already-admitted [[workload]] change its Pod count (scale up or down) without going back through admission from scratch. Implemented via **WorkloadSlices** (KEP-77), the feature splits a Workload's quota into slices so that a scale-down releases quota immediately and a scale-up only needs incremental admission.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

---

## Why this is hard

A vanilla Kueue [[admission]] is binary: a Workload is either Admitted (quota reserved for its full size) or not. If a user wants to scale the underlying job — e.g. a RayCluster auto-scaling up, a Deployment scaling replicas — there's no good path: evicting and re-admitting a whole training job to change its replica count is too disruptive.

WorkloadSlices (feature gate `ElasticJobsViaWorkloadSlices`) decouples admission into slices. The initial admission creates slice 1. A scale-up creates slice 2 that gets independently admitted against the remaining quota; scale-down releases the newest slices.

## Opt-in per integration

Elastic behavior is opt-in per Workload / integration. The initial implementation tracks a couple of integrations:

- **RayCluster** — add/remove worker replicas dynamically ([[issue-10170]] — RayCluster with elastic jobs via workload-slices support should support scheduling pending workload after freeing capacity on scale-down).
- **batch/v1 Job with parallelism changes** — scale parallelism while running ([[issue-6161]] — flaky integration test for elastic Job scale-down/up).

KEP-77 adoption was tracked under [[issue-5528]] (Initial implementation of KEP-77: Elastic Jobs via WorkloadSlices).

## Scheduling gates as the vehicle

For Pod-level integrations (plain Pods, RayCluster's dynamic Pods), Kueue uses Pod scheduling gates rather than `.spec.suspend`. Gates can be removed per-Pod, so new Pods appearing during a scale-up can be independently gated and admitted.

Bugs have clustered around gate removal edge cases:

- "Kueue sometimes does not inject scheduling gates for elastic jobs" ([[issue-10167]]).
- "Kueue does not remove the scheduling gate from Ray's redis-cleanup jobs" ([[issue-8443]]).
- "Kueue will say a workload is admitted if its scheduling gates are removed" — externally removing the gate confuses the accounting ([[issue-9482]]).
- Kubernetes 1.30 behavior change broke gate removal temporarily ([[issue-2029]]).

## Interaction with TAS

Elastic + [[topology-aware-scheduling]] is genuinely complex: a scale-up needs to add replicas to the same topology domain. "Job controller with TAS and ElasticJobsViaWorkloadSlices should scale up an elastic job with TAS unconstrained topology" ([[issue-9341]]) captures the bridge work.

## Interaction with gang scheduling

Elastic is almost the opposite of [[gang-scheduling]]'s all-or-nothing: one says "partial is fine, add/remove on the fly," the other says "evict if any Pod isn't ready." Integrations must pick one; enabling both on the same CQ is nonsensical for training jobs but reasonable for services-on-Kueue patterns.

## Documentation gap

Elastic Jobs documentation has lagged the implementation ([[issue-6349]] — Document the feature of Elastic Jobs / Workloads).

## Related pages

- [[workload]] — gets sliced when elastic.
- [[admission]] — per-slice.
- [[integration-rayjob]] — primary elastic consumer.
- [[gang-scheduling]] — the anti-pattern.
