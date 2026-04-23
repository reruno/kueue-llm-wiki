# Webhooks

**Summary**: Kueue ships validating and mutating admission webhooks for every CRD it defines and for every job type it integrates with. Validation enforces API-level invariants (flavor existence, immutability of certain fields). Mutation defaults fields, stamps finalizers, and — crucially — injects `.spec.suspend` or Pod scheduling gates so jobs are gated the instant they are created.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

---

## Scope

Webhooks run on:

- **Kueue CRDs** — ClusterQueue, LocalQueue, ResourceFlavor, Workload, AdmissionCheck, Cohort, Topology. Defaulting and validation ([[issue-171]] — original "Add webhook for APIs defaulting and validation"). AdmissionCheck webhook was added separately ([[issue-1218]]).
- **Integration types** — batch/v1.Job, JobSet, RayJob, PyTorchJob, etc. Each integration's mutating webhook:
  - Sets `.spec.suspend: true` on create if a queue-name label is present.
  - Creates the companion Workload.
  - Injects labels / tolerations from the [[resource-flavor]] at un-suspend.
- **Plain Pods** — the mutating webhook stamps `kueue.x-k8s.io/managed` scheduling gates (see [[integration-plain-pod]]).

## Defaulting

Defaulting happens on create and on spec mutation where allowed:

- ResourceFlavor gets a finalizer so it can't be deleted while referenced ([[issue-283]] — Add the finalizer via webhook when creating resourceFlavor).
- LocalQueue / Workload get the default `kueue.x-k8s.io/queue-name` under the `LocalQueueDefaulting` feature gate when enabled ([[pr-3652]] — KEP-2936: LocalQueue defaulting).

## Validation

Validation enforces:

- Flavor references point to existing flavors.
- `queueingStrategy` and some policy fields are immutable under circumstances (see [[queueing-strategy]]).
- PriorityClassSource is one of the known values.
- CEL validation for upgrade paths: "v1beta1 CEL validation fails on v1beta2-stored workloads: no such key: priorityClassSource" ([[issue-10593]]) — a cross-version CEL gotcha.

## Helm and webhook config sync

"Automatically sync webhookConfigurations to helm charts" ([[issue-1461]]) addresses a maintenance pain — hand-edited Helm charts drifted from generated webhook configs. "Helm chart: setting `integrations.podOptions.namespaceSelector` results in webhook selector being erased" ([[issue-1903]]) is a downstream symptom of that drift.

## Integration enablement

A webhook that runs unconditionally even when its integration is disabled is a bug — "batch/job webhook runs even when the integration is disabled" ([[issue-10314]]) addresses it. "Missing create verb for job webhook" ([[issue-1034]]) is the mirror: a webhook registered without enough verbs.

## Related pages

- [[architecture]] — where webhooks sit in the control plane.
- [[integrations]] — integrations ship their own webhooks.
- [[resource-flavor]] — finalizer is webhook-added.
- [[feature-gates]] — LocalQueueDefaulting controls a mutating default.
