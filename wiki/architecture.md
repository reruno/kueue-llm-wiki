# Architecture

**Summary**: Kueue is a single controller-manager binary hosting a set of controllers (queue, workload, job integrations, scheduler, cache) plus validating/mutating webhooks. It watches jobs, wraps each one in a [[workload]], and toggles `.spec.suspend` (or Pod scheduling gates) to release the job when quota is available.

**Sources**: `raw/github/kubernetes-sigs__kueue/`; pr-16312.md, issue-16232.md, `raw/kueue/charts/kueue/values.yaml`, `raw/kueue/charts/kueue/templates/manager/_config.tpl`; pr-17227.md; pr-16630.md; 2026-10-28 batch: pr-17455.md, pr-17582.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md (v0.20.3), CHANGELOG-0.19.md (v0.19.10).; 2026-11-24 batch: pr-18139.md, pr-17965.md, pr-17966.md, pr-18353.md, pr-18354.md, pr-18693.md, pr-18694.md, CHANGELOG-0.20.md, CHANGELOG-0.19.md

**Last updated**: 2026-11-24

---

## The binary

Kueue ships as a single `kueue-controller-manager` Deployment with leader election. It uses controller-runtime and exposes `/metrics` for Prometheus. The in-memory `cache` and `queue` packages are the scheduling source-of-truth; reconcilers write to them, and the scheduling loop reads from them.

Scale hardening over time has focused on making those in-memory structures cheaper: node reconciler rewrites for TAS ([[issue-10037]]), cohort hierarchy manager refactors ([[issue-2996]]), and generic controller-cache tuning.

## Reconciliation flow

At the level of a single job, the pipeline is:

1. **User** creates an `X` (e.g. `batch/v1` Job, JobSet, RayJob, …) in a namespace that has a [[local-queue]].
2. **Job-specific integration controller** observes the new object. If it carries `kueue.x-k8s.io/queue-name: <local-queue>`, the controller sets `.spec.suspend: true` (or injects Pod scheduling gates for Pod-level integrations), and creates a corresponding [[workload]] object owned by the job. See [[integrations]].
3. **Webhooks** validate the Workload/ClusterQueue/LocalQueue/ResourceFlavor, inject finalizers, default missing fields. See [[webhooks]].
4. **Workload controller** reconciles the Workload, mirroring status from the underlying job (finished, PodsReady, etc.).
5. **Scheduler** (Kueue's own scheduling loop, not `kube-scheduler`) picks the next admissible Workload for a ClusterQueue based on the [[queueing-strategy]], verifies quota, and sets `QuotaReservation`. Any configured [[admission-check]]s run next; once they pass, the Workload is marked `Admitted`. See [[admission]].
6. **Job-specific integration controller** observes `Admitted=True`, sets `.spec.suspend: false` (or removes scheduling gates), and `kube-scheduler` now sees the Pods and places them.
7. **On completion**, the Workload controller marks the Workload `Finished`, quota is released, and the next Workload in the ClusterQueue is reconsidered.
8. **On preemption**, the scheduler marks the Workload `Evicted`, the integration re-suspends the job, Pods are deleted, quota is released, and the Workload is requeued ([[issue-1874]]).

## In-memory state

Two packages hold state that the scheduler reads on every cycle:

- **`cache`** — per-[[cluster-queue]] and per-[[cohort]] accounting of admitted usage, nominal quota, borrowing limits, and lending limits. The cache is also where [[topology-aware-scheduling]] tracks per-topology-domain free capacity.
- **`queue`** — per-ClusterQueue heap of pending Workloads, ordered by the [[queueing-strategy]]. The priority of a Workload comes from its PriorityClass or [[workload-priority]] class.

These structures are kept consistent with API state via the reconcilers. Bugs here manifest as over-admission or under-admission ([[issue-2678]] — overadmission after deleting resources from a borrowing CQ).

## Controllers at a glance

| Controller | Watches | Writes |
|---|---|---|
| ClusterQueue | ClusterQueue | Status: active, pendingWorkloads, admittedWorkloads |
| LocalQueue | LocalQueue | Status summary of ClusterQueue it points to |
| Workload | Workload | Conditions: QuotaReserved, Admitted, Evicted, Finished |
| Job integrations (one per supported type) | batch/v1 Job, JobSet, RayJob, PyTorchJob, … | `.spec.suspend`, scheduling gates, owned Workload |
| Scheduler loop | internal queues + cache | QuotaReservation, Admitted, preemption |
| AdmissionCheck | AdmissionCheck, Workload | Workload.status.admissionChecks |

## Startup: the scheduler waits for the initial cache

On main (pr-16630, fixes issue-16624), and **shipped in v0.20.3 / v0.19.10** through backports pr-17455 (release-0.20) and pr-17582 (release-0.19; the v0.19.10 changelog cites the main PR #16630), `Scheduler.Start` calls `Cache.WaitForInitialSync` before the first cycle. The cache wraps the controller-runtime sources whose handlers fill it (`Cache.TrackInitialSync`: ClusterQueue, Cohort, ResourceFlavor, Workload, LocalQueue, and Topology plus the TAS ResourceFlavor source when TAS runs). A source counts as synced only after its handler has returned for every object in the informer's initial list; there is no extra timeout (a source that never syncs already stops the manager through `CacheSyncTimeout`). Before, a cold leader could schedule while ClusterQueue create handlers were still running, and TAS double-booked nodes held by ClusterQueues not yet in the cache. Since pr-17346 (on which pr-16630 builds), Cohort handlers also update the cache on **every replica**, as ClusterQueue, ResourceFlavor and Topology handlers do, so a follower that takes the lease can admit from Cohort quota at once instead of after up to one lease duration (source: pr-16630.md, pr-17346.md). The Cohort change also shipped in v0.20.3 / v0.19.10 (#17404, and #17346 as cited in the v0.19.10 changelog) (source: CHANGELOG-0.20.md, CHANGELOG-0.19.md). See [[cache-architecture]].

## Configuring the manager through Helm

The manager reads one Configuration object (`config.kueue.x-k8s.io/v1beta2`) from a ConfigMap. With Helm, pr-16312 (fixes issue-16232, main only) adds structured overrides so users no longer copy the whole YAML to change one field (source: pr-16312.md, raw/kueue/charts/kueue/values.yaml):

| `managerConfig` input (mode omitted) | Configuration used |
|---|---|
| neither | chart defaults |
| only `structuredOverrides` | overrides merged into chart defaults (an empty map = defaults) |
| `controllerManagerConfigYaml` set, with or without overrides | the YAML, as a complete replacement; overrides ignored |
| `controllerManagerConfigYaml: ""` | the legacy empty configuration (certificate-management settings still apply) |

`managerConfig.mode: structured` ignores the YAML and merges overrides; `mode: yaml` ignores the overrides. Defaults now live only in `templates/manager/_config.tpl`, and the manager and webhook templates consume one resolved configuration. The experimental populator follows the same selection.

**Action required only if:** your values have other keys directly under `managerConfig` (only `mode`, `structuredOverrides`, `controllerManagerConfigYaml` are allowed), invalid types (mode must be `yaml`/`structured`; overrides a map; YAML a string; checked even for the unused input), or your tooling read the default YAML from `values.yaml` (read the rendered ConfigMap instead).

**Upgrade gotcha with `--reuse-values`:** the first reuse upgrade without an explicit `mode: structured` can keep the old default YAML, which then wins over the new overrides. To migrate, copy intentional YAML customisations into `structuredOverrides` and pass `mode: structured` in the upgrade values, and keep it there. Reuse flags also keep saved overrides you omitted and can drop `null` removals; to remove an override, use `--reset-values` with all customisations you want to keep. Field values are still validated by Kueue when it loads the configuration, not by Helm.

**Null inputs (pr-18139, merged 2026-11-13, fixes #17717):** `mode`, `controllerManagerConfigYaml` and `structuredOverrides` set to `null` are treated as absent in both the Kueue and Populator charts (schemas, config selection, tests and migration docs updated). Before, migrating from the old chart's `controllerManagerConfigYaml: null` with `--reuse-values` worked once, but Helm saved the null and the next upgrade failed schema validation. An explicit empty string keeps its legacy meaning, and wrong non-null types and unknown keys are still rejected. Docs now explain what `--reuse-values`, `--reset-then-reuse-values` and `--reset-values` do with inherited defaults and saved overrides. Related: the KueueViz auth mode is validated in the values schema ([[dashboard]]).


**Install notes (pr-19275, v0.21).** The chart now ships `NOTES.txt`: every `helm install`/`upgrade` prints commands to check the controller-manager rollout and view the manager configuration, plus a warning only when part of the configuration is ignored — `structuredOverrides` ignored because `controllerManagerConfigYaml` takes precedence when `managerConfig.mode` is unset (even an empty string, and including YAML kept from an older chart by `--reuse-values`) or because `mode: yaml`; or a note that `mode: structured` ignores YAML, so settings not copied into `structuredOverrides` do not apply. A `kueue.managerConfigSource` helper (`yaml`, `structured` or `defaults`) is shared by `kueue.managerConfig` and the notes, so the notes match the rendered configuration; rendered output is unchanged (source: pr-19275.md).

## Shipping status of fixes (patch releases, 2026-10-29 to 2026-11-12)

Details per release are in [[release-process]]. Architecture-relevant items and where they shipped (source: CHANGELOG-0.20.md, CHANGELOG-0.19.md):

| Area | Fix | Shipped in |
|---|---|---|
| API / CRDs | CRD conversion restored for unserved `v1beta1` APIs, so kube-apiserver can initialise watch caches for ClusterQueue, Cohort, LocalQueue, MultiKueueCluster, Workload (#18411; see [[api-versions]]) | v0.20.6 |
| Admission / scheduling | Pod node selectors deterministic when flavors conflict on a label (first flavor in sorted resource-name order, #18369); preemption capacity reservation no longer negative (#18618); FairSharing second-pass workloads no longer skipped (#18674); PodSet totals past the largest Quantity no longer stored as MaxInt64 | v0.20.6 / v0.19.13; PodSet overflow v0.20.4 / v0.19.11 |
| Cache / controllers | Cohort and ClusterQueue status writes no longer fan out to every CQ in the Cohort tree (#18205); RuntimeClass events requeue only Workloads using that class (#17386); namespace-creation race for Jobs | v0.20.5 / v0.19.12; RuntimeClass v0.20.6 / v0.19.13; namespace race v0.20.4 / v0.19.11 |
| Elastic jobs | slice plus replacement no longer double-charged (#18648); rank-based Pod ungating (#18269) | v0.20.6 / v0.19.13; v0.20.5 / v0.19.12 |
| MultiKueue | resync on worker reconnect (v0.20.4), skip finished Workloads in resync and skip remote reads for replaced slices (v0.20.5), retry when no worker is connected, late ClusterProfile CRD, richer pending message (v0.20.6) | as listed |
| TAS | LWS hot swap keeps group in domain (v0.20.5); `TASAncestorCapacityTieBreak` (v0.20.6); gate-off/on requeue (v0.20.6) | as listed |
| Observability | scheduler log levels (v0.20.4), job reconciler log levels (v0.20.5): both ACTION REQUIRED for log-based alerts | as listed |

## Why a separate scheduling loop

`kube-scheduler` is Pod-centric and cannot coordinate "all 256 Pods of this Job must start together, counted against the team's GPU quota." Kueue's loop is deliberately independent so it can make whole-job decisions before any Pod exists. Once a Workload is admitted, placement is still `kube-scheduler`'s job. This split is the central design choice — see [[kueue-overview]].

## Related pages

- [[admission]] — scheduler internals and the admission state machine.
- [[webhooks]] — admission webhooks.
- [[workload]] — the central CRD.
- [[metrics]] — what the binary exposes for observability.
- [[importer]] — the one-shot tool for backfilling Workloads on an existing cluster.
- [[debugging-guide]] — diagnosing workloads stuck in pending.
- [[scheduler-internals]] — the 6-phase scheduling cycle.
- [[cache-architecture]] — in-memory cache and per-cycle snapshot.
