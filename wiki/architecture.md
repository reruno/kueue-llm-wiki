# Architecture

**Summary**: Kueue is a single controller-manager binary hosting a set of controllers (queue, workload, job integrations, scheduler, cache) plus validating/mutating webhooks. It watches jobs, wraps each one in a [[workload]], and toggles `.spec.suspend` (or Pod scheduling gates) to release the job when quota is available.

**Sources**: `raw/github/kubernetes-sigs__kueue/`; pr-16312.md, issue-16232.md, `raw/kueue/charts/kueue/values.yaml`, `raw/kueue/charts/kueue/templates/manager/_config.tpl`; pr-17227.md; pr-16630.md.

**Last updated**: 2026-10-21

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

On main (pr-16630, fixes issue-16624; backport pr-17455 to release-0.20 after v0.20.2) `Scheduler.Start` calls `Cache.WaitForInitialSync` before the first cycle. The cache wraps the controller-runtime sources whose handlers fill it (`Cache.TrackInitialSync`: ClusterQueue, Cohort, ResourceFlavor, Workload, LocalQueue, and Topology plus the TAS ResourceFlavor source when TAS runs). A source counts as synced only after its handler has returned for every object in the informer's initial list; there is no extra timeout (a source that never syncs already stops the manager through `CacheSyncTimeout`). Before, a cold leader could schedule while ClusterQueue create handlers were still running, and TAS double-booked nodes held by ClusterQueues not yet in the cache. Cohort handlers now also update the cache on **every replica**, as ClusterQueue, ResourceFlavor and Topology handlers do, so a follower that takes the lease can admit from Cohort quota at once instead of after up to one lease duration (source: pr-16630.md). See [[cache-architecture]].

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
