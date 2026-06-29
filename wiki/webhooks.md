# Webhooks

**Summary**: Kueue ships validating and mutating admission webhooks for every CRD it defines and for every job type it integrates with. Validation enforces API-level invariants (flavor existence, immutability of certain fields). Mutation defaults fields, stamps finalizers, and — crucially — injects `.spec.suspend` or Pod scheduling gates so jobs are gated the instant they are created.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-06-29

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

## Namespace exclusion: `kube-system` and the install namespace (v0.18, action-required)

Before v0.18 only the Pod, Deployment, and StatefulSet integration webhooks excluded `kube-system` and Kueue's own install namespace; **all other** workload integration webhooks (Job, JobSet, RayJob, the Kubeflow jobs, AppWrapper, LeaderWorkerSet, SparkApplication, etc.) ran in those namespaces. [[pr-11192]] (fixes [[issue-11006]]) makes the exclusion **consistent across every workload integration webhook** (both mutating `m*.kb.io` and validating `v*.kb.io`). Kueue's own CRD webhooks (ClusterQueue, etc.) are intentionally **not** changed — those objects aren't created by system components.

The mechanism is a `namespaceSelector` on each webhook:

```yaml
matchExpressions:
- key: kubernetes.io/metadata.name
  operator: NotIn
  values: [kube-system, kueue-system]   # Helm installs: kube-system + .Release.Namespace
```

For manifest installs the second value is `kueue-system`; for Helm it is the release namespace. The point is to stop Kueue suspending critical system components (e.g. kubeadm-run jobs) and to avoid a circular dependency during cluster upgrades. **Action required**: move any Kueue-managed workloads out of `kube-system` / the install namespace before upgrading, or widen `managedJobsNamespaceSelector` and the webhook `namespaceSelector`s to re-include them. See [[manage-jobs-selectively]].

## Related pages

- [[architecture]] — where webhooks sit in the control plane.
- [[integrations]] — integrations ship their own webhooks.
- [[resource-flavor]] — finalizer is webhook-added.
- [[feature-gates]] — LocalQueueDefaulting controls a mutating default.
