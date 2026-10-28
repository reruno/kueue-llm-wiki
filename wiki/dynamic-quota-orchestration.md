# Dynamic Quota Orchestration (DQO, CapacityProvider)

**Summary**: Dynamic Quota Orchestration (KEP-12382) lets an external source of capacity (autoscaler, node inventory, cloud reservation) drive [[cluster-queue]] and [[cohort]] nominal quota through two alpha cluster-scoped APIs, `CapacityProvider` and `DynamicQuotaOrchestrator` (DQO). **Alpha, feature gate `DynamicQuotaOrchestration`, off by default, new in v0.20.**

**Sources**: pr-15505.md, pr-16168.md, pr-15040.md, pr-15107.md, pr-15199.md, pr-15283.md, pr-15286.md, pr-16349.md, issue-16356.md, raw/kueue/pkg/util/resourcegroups/effective.go, raw/kueue/keps/12382-dynamic-quota-orchestration/README.md, raw/kueue/apis/kueue/v1alpha1/dynamicquotaorchestrator_types.go, raw/kueue/apis/kueue/v1alpha1/capacityprovider_types.go, raw/kueue/pkg/controller/core/dqo/, pr-16767.md, raw/kueue/pkg/controller/core/dqo/discovery.go, pr-17698.md, issue-17697.md, pr-17523.md, pr-17709.md, issue-17522.md, raw/kueue/pkg/controller/core/dqo/reconciler.go

**Last updated**: 2026-10-28

---

## How it landed (all v0.20.0, Alpha)

The feature arrived as a PR stack: scheduler/cache/controller support for `status.effectiveQuotas` on ClusterQueues (pr-15040) and Cohorts (pr-15107); Phase 1 capacity discovery reconciler (pr-15199); field indexers (#15260); Phase 2 distribution logic, largest-remainder math and soft validation with 22 table-driven tests (pr-15283); watches and envtest integration tests (pr-15286); then the bug fixes pr-15505/pr-16168 and API-comment clarifications (pr-16349, docs only: capacity synchronization, flavor coverage, zero-capacity flavors) (source: pr-15040.md, pr-15107.md, pr-15199.md, pr-15283.md, pr-15286.md, pr-16349.md).

## Two phases

The `DynamicQuotaOrchestrator` reconciler (`pkg/controller/core/dqo`) runs two phases per DQO (source: raw/kueue/pkg/controller/core/dqo/reconciler.go):

1. **Capacity discovery** (`spec.capacityDiscovery.providers`, 1-8 entries). For each referenced `CapacityProvider` the DQO requires the `CapacitySynchronized=True` condition **for the provider's current `metadata.generation`** (since pr-17523; see *Stale CapacityProvider status is not ready*), then adds the provider's `status.capacity` into `status.effectiveCapacity`, optionally scaled by `effectiveCapacityMultiplier` (non-negative, default 1). Only flavors listed in the provider's `spec.orchestratedFlavors` are taken. Result condition: `EffectiveCapacityComputed` with reasons `Computed`, `ProviderNotReady`, `Misconfigured` (provider missing), `AggregationFailed`.
2. **Quota distribution** (only when `spec.capacityDistribution.subtreeRootQuotaRef` is set; otherwise the DQO is *discovery-only* and the `Distributed` condition is removed). The DQO resolves the subtree under a `ClusterQueue` or `Cohort` root and writes `status.effectiveQuotas` on every ClusterQueue and Cohort in it, with an `orchestratorRef` back to the DQO. Condition `Distributed` with reasons `QuotasDistributed`, `EffectiveCapacityNotComputed`, `ConflictingDynamicQuotaOrchestrator`, `EffectiveQuotasConflict`, `Misconfigured`.

## Effective quota is the source of truth for the scheduler

When the gate is on and `status.effectiveQuotas` is set, Kueue components use `status.effectiveQuotas.resourceGroups` instead of `spec.resourceGroups`; an empty list is a valid complete override (no fallback to spec). `EffectiveQuotaStatus` is on the ClusterQueue and Cohort status. The scheduler cache records the owning orchestrator name (`dqo.EffectiveOrchestrator`) (source: raw/kueue/pkg/util/dqo/effective.go, raw/kueue/keps/12382-dynamic-quota-orchestration/README.md).

The switch is centralized in `resourcegroups.EffectiveResourceGroups(cq)` and `EffectiveCohortResourceGroups(cohort)` (`pkg/util/resourcegroups/effective.go`): effective groups when the gate is on and `status.effectiveQuotas != nil`, otherwise `spec.resourceGroups` (so **clearing** `status.effectiveQuotas` falls back to spec). Consumers: scheduler cache ClusterQueue/Cohort quotas, pending-workloads view, ClusterQueue metrics, the ClusterQueue/Cohort/ResourceFlavor controllers' update predicates (a change in effective groups triggers reconciliation), admission-check flavor lists, ConcurrentAdmission and `workload` flavor lookups. Deliberately still on `spec`: webhooks (they validate spec, effective quota is status), MultiKueue manager quota automation (to be replaced by DQO), kueueviz and the importer (source: pr-15040.md, pr-15107.md, raw/kueue/pkg/util/resourcegroups/effective.go).

How the quota is built (source: raw/kueue/pkg/controller/core/dqo/distribution.go, KEP README):

- Start from a copy of `spec.resourceGroups` and overlay `nominalQuota` for every `(flavor, resource)` pair of each flavor present in `status.effectiveCapacity`.
- Capacity is split among the participants proportionally to their spec nominal quota using the **largest-remainder method** (CPU in milli units, other resources as integers; ties broken by object UID) so the sum equals the capacity exactly.
- `borrowingLimit` is copied unchanged; a non-nil `lendingLimit` is copied unchanged for Cohorts but capped at the effective `nominalQuota` for ClusterQueues.
- DQO does not apply resource transformations or DRA mappings: providers publish normalized `(flavor, resource)` tuples and the scheduler applies transformations afterwards ([[resource-transformer]]).
- Stale effective quota (DQO deleted, distribution disabled, or a foreign controller stops managing it) **remains in force** until an administrator intervenes; no automatic expiry.

## Providers own all resources of their flavors (pr-16168)

A provider used to be unable to say "this flavor now has no capacity": CEL demanded 1-64 entries in `resources`, and pairs missing from the aggregate silently kept their `spec.resourceGroups` value. Now (source: pr-16168.md):

- Discovery adds **every** flavor in `spec.orchestratedFlavors` to `status.effectiveCapacity`, with `resources: {}` if nothing was reported.
- Distribution treats any declared `(flavor, resource)` pair of a flavor present in the aggregate but missing from its `resources` as **0**.
- The CEL rule on `resources` (CapacityProvider status and DQO effective capacity) is relaxed to `size <= 64`; empty `spec.orchestratedFlavors` is still rejected (1-64 entries).
- Pairs of flavors no provider orchestrates keep their spec value.
- Partial orchestration of a flavor (only some resources) is not supported.

## Ownership and precedence between DQOs (pr-15505)

Overlapping DQOs are not rejected by webhook; the controller does "soft validation" (source: raw/kueue/pkg/controller/core/dqo/distribution.go):

- A DQO whose root is a *strict descendant* of another distributing DQO's root is deactivated (`Distributed=False`, `ConflictingDynamicQuotaOrchestrator`); the ancestor wins and may take over queues already owned by a descendant.
- Two DQOs on the same root: the older wins, UID breaks ties.
- A target queue whose `effectiveQuotas.orchestratorRef` is a foreign controller (not `DynamicQuotaOrchestrator` in the kueue group) or an active non-descendant DQO yields `EffectiveQuotasConflict`.
- Takeover is allowed when the previous owner is being deleted, has no `capacityDistribution`, or has `Distributed=False`.

**Bug fixed by pr-15505**: a waiting DQO stayed blocked after the previous owner flipped to `Distributed=False` because the DQO watch filtered out that status-only update. The watch predicate (`otherDQOUpdatePredicate`) now also passes updates where `Distributed=False` appears or disappears, so waiting DQOs retry the takeover. The reconciler also watches CapacityProvider (via an index of DQO -> provider), and ClusterQueue/Cohort with `GenerationChangedPredicate`.

## Discovery-only mode

Omit `capacityDistribution` to validate what capacity a DQO computes (`status.effectiveCapacity`) before it starts writing quotas. Aggregated capacity is capped at 128 flavors in DQO status vs 64 per provider (source: KEP README, raw/kueue/apis/kueue/v1alpha1/dynamicquotaorchestrator_types.go).

**Correction (2026-10-21)**: this page said exceeding the limits deactivates the DQO. That is the KEP intent, but per issue-16356 discovery could aggregate more than 128 distinct flavors from valid providers (e.g. 64 + 64 + 1), and the `status.effectiveCapacity.flavors` update (`MaxItems=128`) was then **rejected by the API server**, leaving effective capacity unavailable (source: issue-16356.md).

**Fixed on main by pr-16767 (merged 2026-10-19; no backport in this snapshot).** `reconcileDiscovery` aggregates provider capacity, then, if the number of distinct flavors exceeds `maxEffectiveCapacityFlavors = 128` (a constant that must match the `MaxItems` marker on `EffectiveCapacity.Flavors`), sets `EffectiveCapacityComputed=False` with reason **`AggregationFailed`** and message "Aggregated capacity covers N distinct flavors, which exceeds the supported limit of 128", clears `status.effectiveCapacity`, and returns without attempting the invalid status update. Exactly 128 flavors is accepted. The maintainers chose this soft validation over raising `MaxItems`; the API comment and generated CRDs now describe the limit. Release note: "DQO: when the referenced CapacityProviders orchestrate more than 128 distinct flavors in total, the DQO now sets EffectiveCapacityComputed=False with reason AggregationFailed instead of failing to update its status." (source: pr-16767.md, raw/kueue/pkg/controller/core/dqo/discovery.go, raw/kueue/apis/kueue/v1alpha1/dynamicquotaorchestrator_types.go)

**Per-flavor resource limit (pr-17698, fixes issue-17697; merged on main 2026-10-23; no backport in the raw files).** The same overflow existed one level down. Each provider may report up to 64 resources per flavor, but the DQO sums providers per flavor, and `status.effectiveCapacity.flavors[].resources` has a CEL size rule of 64. Example (issue-17697.md): provider A reports `example.com/r-00` to `r-63` for `f1`, and provider B switches from `r-00` to `example.com/extra`, giving 65 resources. The API server rejected the status update (`resource capacity must have at most 64 entries`) and the reconciler kept retrying. Meanwhile the DQO kept its old `effectiveCapacity` with `EffectiveCapacityComputed=True`, so it looked healthy while its capacity was stale. Now `reconcileDiscovery` checks each flavor, in sorted order and after the 128-flavor check, against `maxEffectiveCapacityResourcesPerFlavor = 64`. This constant must match the CEL rule on `EffectiveCapacityFlavor.Resources`. On overflow it sets `EffectiveCapacityComputed=False`, reason `AggregationFailed`, message `Aggregated capacity for flavor "<f>" covers N distinct resources, which exceeds the supported limit of 64`, and clears `status.effectiveCapacity`. Exactly 64 is accepted. The KEP had named a `TooManyResourcesInAggregatedCapacity` reason for this case; `AggregationFailed` was chosen to match pr-16767. Release note: "DQO: when the referenced CapacityProviders together report more than 64 distinct resources for a flavor, the DQO now sets EffectiveCapacityComputed=False with reason AggregationFailed instead of failing to update its status." (source: pr-17698.md, issue-17697.md, discovery.go)

## Stale CapacityProvider status is not ready (pr-17523)

Source: pr-17523.md (fixes issue-17522.md); manual backport pr-17709 (release-0.20), merged 2026-10-26, so pending the next patch release. Release note: "DynamicQuotaOrchestrator: Fixed a bug where stale CapacityProvider status could drive effective-capacity computation after a provider specification update. DQO now waits for current-generation synchronization."

A CapacityProvider spec update bumps `metadata.generation` but does not clear the previous `CapacitySynchronized` condition or `status.capacity`. Discovery accepted any `CapacitySynchronized=True`, so capacity published for the old spec drove effective capacity until the provider caught up. Now `providerNotReadyMessage(cp)` (`pkg/controller/core/dqo/discovery.go`) reports a provider as not ready in two cases:

- the condition is missing or not `True`: `CapacityProvider "<name>" is not synchronized`;
- `cond.ObservedGeneration != cp.Generation`: `CapacityProvider "<name>" synchronization is stale (observedGeneration=X, currentGeneration=Y)`.

Either case sets `EffectiveCapacityComputed=False` with reason `ProviderNotReady` and clears `status.effectiveCapacity`. Distribution then sets `Distributed=False` with reason `EffectiveCapacityNotComputed` ("Capacity discovery not ready") and leaves already-applied `effectiveQuotas` in force; they are not revoked automatically (source: reconciler.go). Discovery resumes once the provider reports `True` for the current generation.

**Contract for provider implementations** (API comment on the CapacityProvider status, KEP README): when publishing capacity for the current spec, set the `CapacitySynchronized` condition's `ObservedGeneration` to `metadata.generation`. DQO treats a missing, zero or mismatched value as not ready for any nonzero current generation, even when the condition is `True`. So a provider that never sets `ObservedGeneration` now keeps every DQO that references it in `ProviderNotReady`. The release-0.20 backport leaves out the main-only capacity-limit checks (pr-16767, pr-17698) (source: pr-17709.md).

## Related pages

- [[cluster-queue]] — `status.effectiveQuotas`.
- [[cohort]]
- [[multikueue]] — manager quota automation (KEP-9988) is the sibling feature that keeps a manager CQ equal to worker quota.
- [[feature-gates]]
- [[api-versions]]
