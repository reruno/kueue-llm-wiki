# Webhooks

**Summary**: Kueue ships validating and mutating admission webhooks for every CRD it defines and for every job type it integrates with. Validation enforces API-level invariants (flavor existence, immutability of certain fields). Mutation defaults fields, stamps finalizers, and — crucially — injects `.spec.suspend` or Pod scheduling gates so jobs are gated the instant they are created.

**Sources**: `raw/github/kubernetes-sigs__kueue/`., pr-13375.md, pr-16972.md, pr-16973.md, pr-16705.md, pr-16710.md, pr-17060.md, pr-13996.md, pr-16779.md, raw/kueue/pkg/controller/jobframework/defaults.go, pr-17090.md, pr-17201.md, pr-17202.md, issue-13991.md, pr-17147.md, raw/kueue/pkg/webhooks/workload_webhook.go

**Last updated**: 2026-10-28

---

## Scope

Webhooks run on:

- **Kueue CRDs** — ClusterQueue, ResourceFlavor, Workload, Cohort (LocalQueue registers an empty webhook; AdmissionCheck and Topology rely on CRD/CEL validation). Defaulting and validation ([[issue-171]] — original "Add webhook for APIs defaulting and validation"). AdmissionCheck webhook was added separately ([[issue-1218]]).
- **Integration types** — batch/v1.Job, JobSet, RayJob, PyTorchJob, etc. Each integration's mutating webhook:
  - Sets `.spec.suspend: true` on create if a queue-name label is present.
  - Defaults the queue-name (from a `default` LocalQueue), WorkloadPriorityClass and `managedBy`. (The Workload itself, and [[resource-flavor]] node labels/tolerations at un-suspend, come from the job reconciler; see [[job-framework-interface]].)
- **Plain Pods** — the mutating webhook stamps the `kueue.x-k8s.io/admission` scheduling gate (and the `kueue.x-k8s.io/managed` label) (see [[integration-plain-pod]]).

## Defaulting

Defaulting happens on create and on spec mutation where allowed:

- ResourceFlavor gets a finalizer so it can't be deleted while referenced ([[issue-283]] — Add the finalizer via webhook when creating resourceFlavor).
- Jobs (and Pods) get the default `kueue.x-k8s.io/queue-name` when a `default` LocalQueue exists (formerly the `LocalQueueDefaulting` gate; now unconditional; [[pr-3652]] — KEP-2936: LocalQueue defaulting).

## Validation

Validation enforces:

- Flavor references are well-formed (a ClusterQueue naming a missing flavor is admitted but becomes inactive with `FlavorNotFound`).
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

## MutatingAdmissionPolicy (MAP), not just webhooks

Since [[pr-13749]] Kueue also ships a **static `MutatingAdmissionPolicy` (MAP v1)** alongside its webhooks. It clears `status.nominatedClusterNames` on a [[workload]] inside kube-apiserver — using CEL `matchConditions` that fire when `status.clusterName` is newly set or an `Evicted: True` condition is newly added — rather than through an UPDATE mutating webhook, deliberately, to avoid the extra API-server latency and out-of-process call.

- Kustomize: `config/components/map/`
- Helm: `charts/kueue/templates/map/`, enabled by `enableMutatingAdmissionPolicy: true` in `values.yaml`

The `mworkload.kb.io` mutating webhook keeps `verbs=create`; an earlier attempt to extend it to UPDATE was reverted. Full context in [[multikueue#Clearing `status.nominatedClusterNames` via MutatingAdmissionPolicy]]. Rendering the MAP templates with `helm template` in GitOps CI is still a gap ([[issue-14592]]).

## Validation additions in v0.20

- **Partial admission bounds** (pr-15499, backports pr-16001/0.18, pr-16002/0.19): the Job webhook rejects `kueue.x-k8s.io/job-min-parallelism` values outside the `int32` range. Previously `"2147483648"` passed after narrowing on 64-bit platforms, the job controller propagated a negative `minCount` into the Workload PodSet, the Workload API rejected it and the job could never create a Workload.
- **Per-workload PodsReady annotation** (Alpha gate `WorkloadLevelWaitForPodsReady`): `kueue.x-k8s.io/wait-for-pods-ready` must be valid JSON with positive `timeoutSeconds`/`recoveryTimeoutSeconds` not above `waitForPodsReady.maxTimeoutOnWorkload` (default 2h); re-validated on update only when the annotation changed ([[wait-for-pods-ready]]).
- **ConcurrentAdmission flavor limit**: at most 32 flavors in the single ResourceGroup ([[concurrent-admission]]).
- **`PreemptionConfig`** is validated by CRD/CEL only (for example `minValue <= maxValue`), not by a webhook (pr-16124).
- **Workload `resourceUsage` divisibility message** now prints the pod count instead of a pointer address (pr-15736).
- **`ResourceTransformations`**: no overlap check with `excludeResourcePrefixes` ships; pr-15926 was reverted ([[resource-transformer]]).
- **Negative Pod overhead** (pr-17090, fixes issue-13991; v0.20.2 #17201, v0.19.9 #17202): under `WorkloadValidateResourcesAreNonNegative` the Workload webhook's `validatePodSetOverhead` rejects negative `podSets[].template.spec.overhead` quantities, which are part of the quota charge; on update only new or changed negative values are rejected, so existing objects stay updatable ([[workload#Negative Pod overhead is rejected (pr-17090, fixes issue-13991)]]).
- **Lowering `status.reclaimablePods` while quota is reserved** is rejected by the Workload webhook; since pr-17147 the job reconciler no longer attempts it for an evicted Workload that still holds quota, which had blocked eviction (v0.20.2 / v0.19.9; [[workload#`reclaimablePods` must not block eviction (pr-17147, fixes issue-14811)]]).
- **`DynamicQuotaOrchestrator`/`CapacityProvider`** use CEL (for example `resources` at most 64 entries; `orchestratedFlavors` 1-64, `controllerName` immutable) ([[dynamic-quota-orchestration]]).

## Update-rejection webhooks added in v0.19/v0.20

- Removing `kueue.x-k8s.io/queue-name` from a RayJob / RayCluster / RayService / SparkApplication is rejected — see [[integration-rayjob#Removing the `queue-name` label is rejected]] ([[pr-13293]], gate `ValidateRayAndSparkJobUpdates`, Beta/on).
- A quota-reserved Workload's `priorityClassRef` is frozen by CRD CEL; Kueue skips writes the API server would refuse rather than retrying them forever ([[pr-14565]]). See [[workload#`priorityClassRef` is frozen once quota is reserved]].
- Admission webhooks should return **no warnings** on the valid paths; [[pr-14688]] / [[pr-14715]] ([[issue-14665]], [[issue-14713]]) added assertions across the Ray, Spark and remaining webhook validation tests to keep it that way.

## Defaulting and validation fixes in the v0.20 line (job integrations)

- **The default `queue-name` is not injected in excluded namespaces** (#13375, v0.20.0). `ApplyDefaultLocalQueue` now checks `managedJobsNamespaceSelector` itself, for every integration. Before, Jobs in excluded namespaces got `queue-name: default` and were suspended. See [[job-framework-interface#Defaulting must respect `managedJobsNamespaceSelector`]] (source: pr-13375.md).
- **A queue-name change is validated on update** (#16221; pr-16972 / pr-16973). A changed, non-empty value must be a valid LocalQueue name. This matters for Pod, AppWrapper and Kubeflow (`BaseWebhook`), whose update path did not re-run create validation. See [[job-framework-interface#Queue-name format is validated on update]].
- **StatefulSet queue changes are rejected while the Workload holds quota**, even with zero ready replicas (#16320; v0.20.1 pr-16705, v0.19.8 pr-16710). See [[integration-statefulset#Queue changes are rejected while the Workload holds quota]].
- **RayService error paths** now use `spec.rayClusterConfig` ([[pr-17060]]). The **RayCluster autoscaling error** names the gate and annotation that make it valid ([[pr-13996]]). See [[integration-rayjob]].
- **`integrations.labelKeysToCopy` naming internal labels** is accepted but logged at startup ([[pr-16779]]); see [[job-framework-interface#Internal labels and annotations are never inherited]].
- **The Pod webhook does not rewrite `kueue.x-k8s.io/role-hash`.** Forged role hashes are caught at ungate time, not in the webhook (#13382); see [[integration-plain-pod#Role-hash forgery: requests are verified before ungating]].

## Related pages

- [[architecture]] — where webhooks sit in the control plane.
- [[integrations]] — integrations ship their own webhooks.
- [[resource-flavor]] — finalizer is webhook-added.
- [[feature-gates]] — feature-gated webhook behaviour.
- [[job-framework-interface]]
- [[integration-statefulset]]
