# Configurable preemptions (PreemptionConfig)

**Summary**: `PreemptionConfig` (KEP-13396, `kueue.x-k8s.io/v1alpha1`, cluster-scoped) lets an administrator declare extra preemption rules with triggers and candidate selectors; a [[cluster-queue]] opts in through an annotation. **Alpha, feature gate `ConfigurablePreemptions`, off by default, new in v0.20.** Rules add *fallback candidates* on top of the classical and fair-sharing algorithms; they never replace them.

**Sources**: pr-15889.md, pr-15913.md, pr-15992.md, pr-16062.md, pr-16124.md, pr-16130.md, pr-16139.md, pr-16202.md, pr-16208.md, pr-16269.md, pr-16324.md, issue-15892.md, issue-15893.md, issue-16295.md, raw/kueue/apis/kueue/v1alpha1/preemptionconfig_types.go, raw/kueue/pkg/scheduler/preemption/config/, raw/kueue/keps/13396-configurable-preemptions/README.md

**Last updated**: 2026-09-29

---

## Stage and gate

- `ConfigurablePreemptions`: Alpha, default `false`, since 0.20. It has no gate dependency on `TopologyAwareScheduling`; a topology trigger used without TAS is meant to be an error on the trigger, not a gate dependency (source: pr-15889.md).
- The gate was first added as a no-op (source: pr-15889.md), then the API (pr-15913), evaluator (pr-16062), selector filters (pr-16139), scheduler integration (pr-16130), eviction reasons (pr-16208) and RBAC (pr-15992, pr-16202) merged as separate PRs.
- Beta graduation is tracked in issue-15892.md. Planned for Beta: a real `ClusterQueue` field instead of the annotation, and making configurable preemption **exclusive** with classical/fair-sharing preemption so the merge code can be deleted (issue-15893.md, the `TODO(#15893)` markers in `flavorassigner.go` and `fair_strategy.go`).

## Opting a ClusterQueue in

In Alpha the link is an **annotation on the ClusterQueue**: `kueue.x-k8s.io/preemption-config-name: <PreemptionConfig name>` (`PreemptionConfigNameAnnotation`, to be removed when it becomes a field in Beta) (source: pr-15913.md). The cache reads it only when the gate is on and stores it as `ClusterQueueSnapshot.PreemptionConfigName`; ClusterQueue labels are also copied into the snapshot only when the gate is on, to avoid clone overhead otherwise (source: pr-16139.md, raw/kueue/pkg/cache/scheduler/clusterqueue.go).

The `PreemptionConfig` is read with a client `Get` **once per preemption attempt** (`NewEvaluatorForClusterQueue`); if the gate is off, the annotation is absent, or the object cannot be read, the evaluator is `nil` and the classical/fair-sharing behaviour is untouched (source: raw/kueue/pkg/scheduler/preemption/config/preemption.go).

## API shape (v1alpha1)

`PreemptionConfig.spec.rules[]` (max 64, list-map keyed by `name`, name is a DNS-label of at most 63 chars). Each rule:

| Field | Meaning |
|---|---|
| `preemptorSelector` | Label selector on the *preemptor Workload*. Nil = every Workload (unlike `LabelSelectorAsSelector(nil)`, which matches nothing). |
| `activationPolicy.trigger` | Required. `Always`, `InsufficientQuota`, or `QuotaFeasibleAndInsufficientTopology`. |
| `candidateSelectors[]` | Max 32. Candidates from all selectors are unioned. **No selectors = empty candidate set** (rule disallows preemption). |

Each candidate selector (`PreemptionConfigPreemptionCandidateSelector`):

- `scope` (required): `WithinLocalQueue` (same namespace and LocalQueue name), `WithinClusterQueue`, `WithinParentCohort` (same immediate Cohort **plus the preemptor's own CQ even when it has no cohort**), `WithinCohortTree` (same root Cohort, plus own CQ), `AnyClusterQueue`.
- `clusterQueueSelector`: label selector on candidate ClusterQueues.
- `labelSelector`: label selector on candidate Workloads.
- `numericLabels[]` (max 32, AND-ed): `key`, optional `fallbackValue` (int32), optional `comparison`, `minValue`, `maxValue`.
- `priority`: `mode` (`Base` = `spec.priority`; `Boosted` = effective priority including [[preemption-cost]] boost) and `comparison` against the preemptor.

`comparison` values are `LessThan`, `GreaterThan`, `LessThanOrEqual`, `GreaterThanOrEqual`, always "candidate value compared with preemptor value".

Numeric-label semantics worth remembering (source: raw/kueue/pkg/scheduler/preemption/config/filters/numeric_label_filters.go):

- Labels are parsed as int32 base 10. A missing or unparsable label uses `fallbackValue`; **without a fallback the candidate is excluded**. Kubernetes label values cannot start with `-`, so a negative `fallbackValue` is how you make unlabeled workloads compare smaller than every labeled one.
- If the *preemptor* lacks the label and there is no fallback, a `comparison` matches no candidate (logged at V(2)).
- Labels are not copied from the job to the Workload automatically; add them to the Kueue configuration's label-copy list first.
- With none of `comparison`/`minValue`/`maxValue`, the constraint only requires the key to exist with a valid integer.
- A CEL rule rejects `minValue > maxValue` ("minValue must be less than or equal to maxValue"); `minValue`/`maxValue` are `>= 0` (source: pr-16124.md). This validation is done by the API server (CRD), not a webhook.

## Triggers and the evaluation order

`PreemptionEvaluator.FindCandidates` yields candidates lazily in this order (source: raw/kueue/pkg/scheduler/preemption/config/preemption.go):

1. **`Always`** rules: contribute unconditionally. Together with the CQ's own `spec.preemption` policy they form the *baseline*.
2. **`InsufficientQuota`** rules: only if `workloadQuotaFits()` is still false after the baseline candidates were removed from the snapshot.
3. **`QuotaFeasibleAndInsufficientTopology`** rules: only if quota now fits but the workload still does not fit, i.e. topology is what blocks it (see [[topology-aware-scheduling]]).

Candidates are deduplicated by Workload UID across rules and selectors of a trigger; the candidate remembers every `rule -> selector indexes` that selected it (used in the message). Each candidate must be **still admitted in the snapshot** and must **use a flavor/resource that needs preemption** (`classical.WorkloadUsesResources`). Ordering within a trigger uses the same `CandidatesOrdering` as classical preemption (priority, admission time, AFS usage). `HasRules()`/`HasConditionalRules()` inspect only the config so the expensive fit checks are skipped when no conditional rule exists.

## Integration with classical and fair-sharing preemption (pr-16130)

- **Classical** (`classicalPreemptionStrategy`): after the classical candidate iterator is exhausted (`cont == true`), the evaluator is run for each `allowBorrowing` attempt.
- **Fair sharing** (`fairPreemptionStrategy`): run after both fair-sharing strategies fail and the simulation was reverted; `noCandidates()` does not short-circuit when the config has any rule.
- The shared `getTargets` loop still applies: yielded candidates are removed from the snapshot, `workloadFits` (quota **and** topology) is checked after each, then `fillBackWorkloads` re-adds candidates that turned out unnecessary.
- **Flavor assignment**: `canPreemptWhileBorrowing()` returns true whenever the gate is on and the CQ references a PreemptionConfig, so `FlavorAssigner` can enter `Preempt` mode even if the CQ would borrow afterwards and the classical policies (`borrowWithinCohort: Never`) would forbid it. Whether any rule fires is decided later by the preemption algorithm (source: raw/kueue/pkg/scheduler/flavorassigner/flavorassigner.go). This widening is scheduled for removal (issue-15893.md).

## Eviction reasons and observability (pr-16208, pr-16324)

A Workload preempted by a rule gets:

- `Evicted` condition reason `Preempted` (unchanged, so requeue logic keeps working).
- `Preempted` condition reason **`ConfigurablePreemption`** (`kueue.ConfigurablePreemptionReason`), alongside `InClusterQueue`, `InCohortReclamation`, `InCohortFairSharing`, `InCohortReclaimWhileBorrowing`.
- Message `Preempted by <ns/name> because of preemption config <config> rule <rule>/<selectorIdx>[,<idx>...]` (multiple rules joined with `; `).
- `status.schedulingStats.evictions[]` entry with `reason: Preempted` and **`underlyingCause` = the PreemptionConfig name**; `count` increments per preemption. The KEP originally said `reason: ConfigurablePreemption`; it was corrected to match the implementation (source: issue-16295.md, pr-16324.md).
- The preemption metrics use the target's reason string, so the `ConfigurablePreemption` reason appears as a label value ([[metrics]]).

If `ConfigurablePreemptionReasonData` is nil the code logs an error and falls back to the generic message.

## Error handling for bad rules (pr-16269)

Candidate-filter compilation used to return a `rejectAll` boolean and silently skip the selector. Now `NewCandidateFilters` returns typed `FilterBuildError`s (unsupported scope, invalid label selector, unsupported comparison or priority mode) and `PreemptionEvaluator.Candidates` **fails fast**: any build error for a matching rule makes that trigger return no candidates and logs the errors, consistent with an invalid `preemptorSelector` (source: pr-16269.md, issue-16147.md). Because the API has enums, this only triggers for objects that bypassed CRD validation.

## RBAC

`PreemptionConfig` is cluster-scoped, so `preemptionconfig-editor-role` and `preemptionconfig-viewer-role` ClusterRoles aggregate into `kueue-batch-admin-role` (viewer also into the built-in `admin`), and carry no `batch-user` label (source: pr-15992.md). pr-16202 added the manager RBAC found missing on manual verification. The same wave added roles for `AdmissionCheck`, `MultiKueueCluster`, `MultiKueueConfig`, `ProvisioningRequestConfig`, `WorkloadPriorityClass` (pr-16028, fixes issue-15890) and `AppWrapper` (pr-16096), and `hack/testing/rbac/verify.sh` in `make verify` now fails when a manager resource lacks an editor and viewer role (pr-16240). `/status` get rules exist only for CRDs with a status subresource.

## Open follow-ups (not shipped)

Topology candidates from overlapping TAS flavors (issue-16141), strongly typed identifiers (issue-16210), defragmentation test isolation (issue-16207) and review follow-ups (issue-16203) remain open.

## Related pages

- [[preemption]] — classical triggers this feature extends.
- [[fair-sharing]] — the other algorithm that merges configurable candidates.
- [[preemption-cost]] — `Boosted` priority mode.
- [[cluster-queue]] — the annotation lives here.
- [[feature-gates]]
- [[topology-aware-scheduling]] — `QuotaFeasibleAndInsufficientTopology`.
