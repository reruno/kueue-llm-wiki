# MultiKueue

**Summary**: MultiKueue dispatches [[workload]]s from a **manager cluster** to one of several **worker clusters**. Users submit jobs on the manager as usual; MultiKueue (implemented as an [[admission-check]]) picks a worker cluster with capacity, forwards the job, and mirrors status back. It's how one Kueue installation governs a fleet of clusters.

**Sources**: `raw/github/kubernetes-sigs__kueue/`, pr-15288.md, pr-15962.md, pr-15986.md, pr-15989.md, pr-16140.md, pr-15871.md, pr-16315.md, pr-16235.md, issue-16172.md, issue-16010.md, issue-15380.md, issue-13243.md, raw/kueue/pkg/controller/admissionchecks/multikueue/multikueuecluster.go, raw/kueue/pkg/metrics/metrics.go, raw/kueue/pkg/features/kube_features.go, pr-13244.md, pr-13996.md, pr-16470.md, pr-16370.md, pr-14036.md, pr-15280.md, pr-15387.md, pr-16473.md, pr-16772.md, pr-13706.md, pr-15092.md, raw/kueue/pkg/controller/jobs/raycluster/common.go, raw/kueue/pkg/controller/jobs/raycluster/raycluster_multikueue_adapter.go, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, pr-17228.md, pr-17360.md, pr-17362.md, pr-17331.md, pr-17118.md, pr-17357.md, pr-17358.md, pr-16259.md, pr-17466.md, pr-17464.md, pr-17513.md, pr-17157.md, raw/kueue/pkg/controller/admissionchecks/multikueue/clusterqueue.go, raw/kueue/pkg/controller/admissionchecks/multikueue/controllers.go, raw/kueue/pkg/controller/jobs/ray/ray_multikueue_adapter.go, raw/kueue/pkg/controller/jobs/rayservice/rayservice_multikueue_adapter.go, raw/kueue/apis/kueue/v1beta2/multikueue_types.go

**Last updated**: 2026-10-21

---

## Topology

- **Manager cluster** — runs Kueue with MultiKueue configured. Has ClusterQueues, LocalQueues, Workloads, but no actual worker Pods.
- **Worker clusters** — run their own Kueue. They are registered on the manager via `MultiKueueCluster` (a connection config) and `MultiKueueConfig` (which worker clusters to use for a given AdmissionCheck).
- **AdmissionCheck** — a `MultiKueue`-typed AdmissionCheck on the manager's ClusterQueue gates admission on a worker cluster accepting the job.

## Flow

1. User creates a Job on the manager cluster, labeled with a [[local-queue]].
2. Manager's integration controller creates a suspended Workload with QuotaReserved.
3. MultiKueue check kicks in: it picks a worker cluster (preferring clusters with capacity per the Workload's requirements) and creates a mirror Job there.
4. Worker cluster's Kueue admits the mirror Workload through its own pipeline.
5. Once the worker Workload is Admitted, the MultiKueue check on the manager returns Ready.
6. The manager Workload is Admitted; the integration unsuspends the manager Job (cosmetically — Pods don't exist on the manager).
7. Status (conditions, active Pods, completion) is mirrored from the worker Workload back to the manager Workload on a reconcile loop.

## Why a check rather than a scheduler plugin

Using the [[admission-check]] extension point kept MultiKueue out of Kueue's core scheduler. Any number of dispatch policies can be implemented as checks; MultiKueue is one such implementation. This is why there's no dedicated "MultiKueue controller" in the core — it reuses the existing check mechanism.

## Which integrations are supported

Not every job integration trivially mirrors. MultiKueue has specific integration work per job type:

- batch/v1 Job, JobSet — early and stable.
- Kubeflow jobs (PyTorchJob, MPIJob, TFJob, etc.) — rolled out later.
- RayJob, RayCluster — worker-side reconciliation is complex because Ray's state is non-trivial.
- Plain Pods and PodGroups — added with caveats ([[issue-2341]], [[issue-4719]]).
- Priority class mutation on managed workloads ([[issue-7429]] — support mutating the priority class for workloads managed by MultiKueue).

A general tracking theme: "Fair Share Preemption with MultiKueue + Plain Pods - Preempted Pod not Terminated in the Manager Cluster" ([[issue-5979]]) captures the cross-cluster preemption mirroring problem.

## Worker cluster selection

Worker choice is per-Workload: when the MultiKueue check evaluates, it queries each candidate worker cluster for free capacity (via a lightweight RPC reading the worker's ClusterQueue status), chooses one, and dispatches. There's no cross-worker global optimization — each admission cycle picks independently.

## KEP tracker and graduation

MultiKueue was built under its own KEP; graduation work is tracked in recurring issues (representative: [[issue-10626]], [[pr-10684]], [[pr-10656]]). Priority-class mutation ([[issue-7429]]) is indicative of the feature area still being shaped.

## MultiKueueCluster reconnect mechanics

When a worker cluster's apiserver becomes unreachable, the manager's `clustersReconciler` retries on an exponential backoff (`pkg/controller/admissionchecks/multikueue/multikueuecluster.go`).

**Backoff formula.** `retryAfter(n) = 2^(min(n, 7) - 1) * 5s`, where `n = failedConnAttempts`. Sequence: `5s, 10s, 20s, 40s, 80s, 160s, 320s`, capped at ~5m20s. `retryIncrement = 5s`, `retryMaxSteps = 7`.

**State.** `failedConnAttempts` is held on the `remoteClient`. It's incremented on each watch failure inside `setConfig` and reset to `0` only when the watch is successfully (re)established or when the kubeconfig itself changes. The `connecting` atomic flag stays `true` across failures, so subsequent reconciles re-enter the connect path even if the config is unchanged.

**Trigger sources for a reconcile.** A retry can be queued by any of:
- The `RequeueAfter` returned from the previous failed reconcile (this is the throttled path).
- A `watch-ended` event when a previously running watch goroutine exits.
- A change to the `MultiKueueCluster` object — **including the controller's own status patch**.

**Why two consecutive failures appear in the same second.** When a healthy cluster first goes down, the `MultiKueueClusterActive` condition flips `True/Connected → False/ClientConnectionFailed`. That status write produces an object-change event that immediately enqueues a second reconcile (before the `RequeueAfter` from the first one fires). The second reconcile increments `failedConnAttempts` to 2 and logs `retryAfter: 10s`; its status update is a no-op because `cmpConditionState` sees the same condition, so the cascade stops there. From that point on, retries are paced strictly by `RequeueAfter`.

This is an artifact of condition-flip + reconcile-on-status-update, not two real connection attempts being deliberately scheduled in the same second.

### A hung remote watch no longer stalls all clusters

The `multikueuecluster` reconciler runs a **single worker**, and `Reconcile → setRemoteClientConfig` holds the controller-wide `clustersReconciler.lock` through the whole `setConfig → establishWatch → client.Watch()` chain. So if `client.Watch()` against one unreachable worker **hung**, that single worker was blocked indefinitely: every other cluster behind it never reconciled, stayed `connecting=true`, was excluded by the dispatcher, and **admission stopped cluster-wide** ([[issue-11206]]).

[[pr-11207]] (cherry-picked to 0.16/0.17) bounds the **watch-establishment** phase with a timeout (`watchWithEstablishTimeout`): on timeout it cancels the in-flight `Watch` and returns `errWatchEstablishTimeout`, falling back to the normal `failedConnAttempts`/`retryAfter` backoff. The default was set to **10 minutes** (not seconds): `client.Watch()` returns once HTTP 200 headers arrive, but a server with a cold cache + conversion-webhook warmup can legitimately block sending headers for several minutes at high workload counts, so a short timeout would cancel-and-retry forever. Successful-watch stream lifetime is unchanged.

**Per-cluster locking (the real concurrency fix).** The 10-minute timeout still parked the single reconciler worker for up to 10 minutes per hung cluster, and bumping `controller.groupKindConcurrency["MultiKueueCluster.kueue.x-k8s.io"]` above 1 did *not* help — every worker serialized on the same controller-wide `clustersReconciler.lock` held across the synchronous watch-establishment ([[issue-11297]]). [[pr-11305]] (cherry-picked as [[pr-11332]]/0.16, [[pr-11333]]/0.17 — v0.16.9 / v0.17.4) narrows `c.lock` to just the `remoteClients` map find-or-insert (new `findOrCreateRemoteClient`) and introduces a per-cluster `setConfigLock` on each `remoteClient` to guard the slow connect path. Different clusters now reconcile genuinely in parallel, so one slow/unresponsive remote no longer blocks healthy ones.

**Exponential establish timeout (detect a hung remote in 1 minute).** [[pr-11304]] (cherry-picked as [[pr-11328]]/0.16, [[pr-11329]]/0.17 — v0.16.9 / v0.17.4, fixes [[issue-11303]]) replaces the static 10-minute establish timeout with an exponential schedule: it starts at **1 minute** and doubles per consecutive `failedConnAttempts`, capped at 10 minutes (`1m, 2m, 4m, 8m, 10m, 10m…`). Implemented via `pkg/util/wait.NewBackoff(initialEstablishTimeout, maxEstablishTimeout, 2, 0)` with `establishBackoff.WaitTime(int(rc.failedConnAttempts)+1)`; `establishWatch` now takes an explicit `timeout` argument. `failedConnAttempts` resets to zero on a successful establishment or on a config change. A truly hung remote is therefore caught in ~1 minute on the first failure instead of parking a worker for the full 10.

### Reconnect backoff guardrail

[[pr-11275]] / [[pr-11276]] (cherry-picks of #10990) add a reconnect-backoff guardrail to the `MultiKueueCluster` reconciler that **suppresses redundant reconciles while a cluster is still inside its backoff window** (before `retryAfter` elapses). This cuts the reconcile churn caused by repeated requeues/events for a cluster that is already waiting to reconnect.

### `clustersReconciler` as an event-filter predicate

[[pr-11153]] (cherry-picks [[pr-11271]]/[[pr-11272]]) turns `clustersReconciler` into a `predicate.Predicate` wired via `WithEventFilter`, primarily to restore the **`replica-role`** field that was missing from this controller's logs (it now logs through `roletracker.WithReplicaRole` / a `LogConstructor`). It is also explicit prep for finer event filtering in follow-up #11001.

## Manager quota automation (KEP-9988, Alpha)

[[pr-11141]] implements the **Alpha1** scope of KEP-9988 behind the `MultiKueueManagerQuotaAutomation` feature gate (off by default). It keeps a manager [[cluster-queue]]'s nominal quota equal to the **sum of the corresponding worker-cluster quotas**, so administrators don't hand-maintain the manager's quota to mirror the fleet.

- **Opt-in is per-config**: `MultiKueueConfig.spec.quotaManagement` is an enum (`Manual` | `Automated`). Unset means `Manual`. `Automated` takes effect only with the feature gate on (source: raw/kueue/apis/kueue/v1beta2/multikueue_types.go). **Correction (2026-10-21)**: this page named the field `spec.quotaAutomation.mode` and said the default depends on the gate.
- A new `CQReconciler` (`pkg/controller/admissionchecks/multikueue/clusterqueue.go`) watches manager ClusterQueues, finds the MultiKueue AdmissionCheck, resolves the `MultiKueueConfig`, and writes the summed `nominalQuota` into the CQ's single flavor (only when changed).
- **Constraint**: the manager CQ must have **exactly one ResourceGroup with exactly one Flavor**, else the CQ gets condition `MultiKueueManagerQuotaAutomation=False` with reason `UnsupportedConfiguration`. Worker clusters that are still `connecting` are skipped in the sum.
- New CQ status **condition** `MultiKueueManagerQuotaAutomation` (reasons: `QuotaAutomated`, `NotRequested`, `UnsupportedConfiguration`). Remote ClusterQueue/LocalQueue reads use a new `SelectivelyCachingClient` + informers so reconciles fire only on relevant remote changes.

### How the `cqReconciler` aggregates worker quotas

Doc comments added in [[pr-17118]] (backports pr-17357, pr-17358; no behaviour change) and the code describe the reconcile order (source: raw/kueue/pkg/controller/admissionchecks/multikueue/clusterqueue.go):

1. A ClusterQueue without a MultiKueue AdmissionCheck is skipped. Its worker-status metrics and its quota-automation condition are removed. A deleted ClusterQueue also has its worker-status series cleared.
2. Worker cluster status metrics are reported **before** any quota-automation check, so they exist for every manager ClusterQueue, including `Manual` ones.
3. A missing `MultiKueueConfig` → `UnsupportedConfiguration`. `quotaManagement` unset or `Manual` → `NotRequested`. More than one ResourceGroup or flavor → `UnsupportedConfiguration`.
4. `aggregateWorkerQuotas` takes the manager LocalQueues that point at this ClusterQueue. For each cluster in `spec.clusters` that has a client and is **connected** (others are skipped with a V(3) log), it finds the worker LocalQueues with the **same namespace and name**, takes the worker ClusterQueues they point at, and sums the `nominalQuota` of every resource across **all** their ResourceGroups and flavors. It sums across flavors because the manager's flavor assignment is not passed to workers. Both remote Lists go through the selectively caching client.
5. If a worker resource is missing from the manager's `coveredResources` → `UnsupportedConfiguration` ("manager-side coveredResources is missing resources configured on workers"). Otherwise the single flavor's quotas are rewritten for every covered resource (0 if no worker has it), with an `Update` only when they changed. The condition becomes `QuotaAutomated`.

## Incremental Dispatcher `stepSize` (KEP-9270)

The `IncrementalDispatcherReconciler` nominates worker clusters for a workload in **batches per round** (rather than all candidates at once). The batch size was previously hardcoded to 3. [[pr-11208]] adds the `multiKueue.incrementalDispatcherConfig.stepSize` config field (`*int32`, default 3, minimum 1) to make it configurable, behind the `MultiKueueIncrementalDispatcherConfig` gate (Beta, on by default). Defaulting only allocates the struct and sets `stepSize=3` when `dispatcherName` is the incremental dispatcher. The field was added to `apis/config/v1beta2` (and v1beta1 was deliberately not extended further, to nudge migration to v1beta2).

## AllAtOnce dispatcher correctness (eviction races)

The default **AllAtOnce** dispatcher nominates *all* candidate worker clusters at once (`wlReconciler.nominateAndSynchronizeWorkers` in `pkg/controller/admissionchecks/multikueue/workload.go`) and writes the set into `Workload.Status.NominatedClusterNames`. Two v0.17.4 / v0.16.9 fixes harden it against stale-cache and ordering bugs; both are specific to AllAtOnce — the Incremental and External dispatchers copy the existing nominated list verbatim and are unaffected.

- **Wait for eviction before re-nomination** ([[pr-11378]] on main; cherry-picked manually as [[pr-11472]]/0.17, [[pr-11473]]/0.16). A workload evicted from a worker cluster could fail to be re-admitted: a stale informer cache still showed `Status.ClusterName` set from the prior nomination (with `NominatedClusterNames == nil`), so the dispatcher skipped its guard and unconditionally created a remote workload on another worker; once that worker admitted, an SSA status update looped forever against webhook validation. The nomination guard was changed to skip entirely whenever `NominatedClusterNames` already equals the target set, so the dispatcher waits for the in-flight eviction to complete (which clears both `ClusterName` and `NominatedClusterNames`) before starting a fresh nomination/re-admission cycle.
- **Order-insensitive nomination compare** ([[pr-11497]] on main; cherry-picked as [[pr-11507]]/0.17, [[pr-11508]]/0.16, fixes [[issue-11453]]). The check deciding whether to patch `Status.NominatedClusterNames` used the order-sensitive `equality.Semantic.DeepEqual`. Because the nominated set could be produced in a different order across reconciles, AllAtOnce issued spurious status patches even when the set was unchanged. A new helper `nominatedClusterSetsEqual(...)` sorts both lists before comparing, so the status is updated only when the actual set changes.

## RBAC: RayService on worker clusters

RayService has been a MultiKueue-managed integration since v0.17.0, but the worker-cluster ClusterRole generated by `create-multikueue-kubeconfig.sh` (Hugo-included into the MultiKueue setup docs) lacked `rayservices` / `rayservices/status` rules, so dispatched RayService workloads failed at the API level on the worker. [[pr-11400]] adds those rules. If you maintain a hand-written worker kubeconfig/ClusterRole, add `rayservices` and `rayservices/status` to it.

- **Kubeconfigs.** The manager needs credentials to each worker. These live in a Secret referenced by `MultiKueueCluster`.
- **Version skew.** Worker clusters must run a Kueue version compatible with the manager — cross-version mirror-Workload fields can drift.
- **Observability.** Metrics expose both manager-side admission and mirror-side dispatch; both should be scraped for end-to-end visibility. See [[metrics]].
- **Plain Pods caveat.** Because plain Pods aren't owned by a controller the manager can suspend, enabling MultiKueue for plain Pods required extra glue ([[issue-2341]]).

## Clearing `status.nominatedClusterNames` via MutatingAdmissionPolicy

External dispatchers nominate worker clusters with their **own** Server-Side Apply field manager (e.g. `fieldManager: "my-external-dispatcher"`). SSA then tracks ownership of `.status.nominatedClusterNames` under that manager, and Kueue's attempt to clear the field to `nil` under the `kueue-admission` manager lost to a field-manager conflict, leaving a stale nomination behind.

[[pr-13749]] (fixes #6185; cherry-picks [[pr-14643]], [[pr-14659]]) solves this **inside kube-apiserver** with a static **MutatingAdmissionPolicy** (MAP v1) rather than a mutating webhook — deliberately, to avoid the extra API-server latency and out-of-process call an UPDATE webhook would add:

- manifests live in `config/components/map/` (Kustomize) and `charts/kueue/templates/map/` (Helm), enabled by default via `enableMutatingAdmissionPolicy: true` in `values.yaml`;
- CEL `matchConditions` clear `status.nominatedClusterNames` when `status.clusterName` is **newly set** (the Workload was admitted) or when an `Evicted: True` condition is **newly added**;
- the earlier attempt to extend the `mworkload.kb.io` mutating webhook to UPDATE was reverted; it keeps `verbs=create`.

GitOps note: rendering the MAP templates with `helm template` is not yet supported everywhere ([[issue-14592]], open).

## Preemption gates are local to each cluster

MultiKueue no longer considers `spec.preemptionGates` when deciding whether a manager Workload and its remote copy are in sync ([[pr-14258]], original #12587). Preemption gates on the manager and on a worker are **independent**: they are not copied manager → worker, and a difference is not treated as out-of-sync. Before the fix, creating a MultiKueue Workload that carried a preemption gate produced an infinite sync-and-delete loop on the worker clusters. See [[multikueue-orchestrated-preemption]].

## Worker Job TTL

MultiKueue used to copy `spec.ttlSecondsAfterFinished` from the manager Job onto the remote worker Job. The worker's TTL controller could then delete the completed remote Job **before** MultiKueue synced its terminal status back, so the manager saw the remote as missing and dispatched the completed Job again.

[[pr-14734]] omits the field when creating a remote Job, behind `MultiKueueBatchJobClearingTTLSecondsAfterFinishedOnWorkerCluster` (**Beta/on in v0.20**; **Alpha/off** in the release-0.18 / release-0.19 backports [[pr-14827]], [[pr-14828]]). Existing remote Jobs are not modified. With the gate on, the lifecycle is:

1. the manager Job keeps its configured `spec.ttlSecondsAfterFinished`;
2. the remote Job is created without it;
3. the worker TTL controller leaves the completed remote Job alone, so MultiKueue can sync terminal status back;
4. the manager Job completes and is deleted by its own TTL policy;
5. MultiKueue removes the remote Job as part of manager-side cleanup.

The general problem — worker-side self-cleanup policies across all MultiKueue integrations — is tracked in [[issue-14779]] (open), and preserving fields the manager's typed struct does not model is [[issue-14837]] (open).

## AdmissionCheck `observedGeneration` is refreshed on config change

The MultiKueue AdmissionCheck reconciler skipped the status update whenever the `Active` condition's status, reason and message were unchanged. Updating the check's parameters to a *different but equally healthy* MultiKueueConfig therefore left `observedGeneration` pointing at the old generation, even though the new configuration had been evaluated successfully. [[pr-14838]] refreshes it (cherry-picks [[pr-14914]], [[pr-14915]], [[pr-14931]], [[pr-14933]], [[pr-14934]]).

`cmpConditionState` was intentionally **not** changed: event handlers use the same helper to detect meaningful health-state transitions, and broadening it would trigger extra reconciles.

## Manager → worker clients: `clientConnection` QPS/Burst now applies (v0.20, Beta)

`newClientWithWatch` (`pkg/controller/admissionchecks/multikueue/multikueuecluster.go`) used to build each worker cluster's client from the kubeconfig without touching `restConfig.QPS`/`Burst`, so the manager→worker leg ran at client-go's defaults (**QPS 5 / Burst 10**) while Kueue's own client uses `clientConnection` (defaults 300/500). A burst of 1000 Workloads across 10 workers took ~15 minutes to admit; a PoC with QPS=Burst=500 brought it to ~1.5 minutes (source: issue-14973.md).

Gate **`MultiKueueReuseClientConnectionConfigForWorkers`** (**Beta, default on since v0.20**, depends on `MultiKueue`) makes `clientConfig.toRESTConfig()` copy the Configuration's `clientConnection.qps`/`burst` into each worker `rest.Config`. Because `rest.Config` ignores QPS/Burst when a `RateLimiter` is already set, the code clears any existing limiter and installs a fresh **per-cluster** token bucket (unset values fall back to `rest.DefaultQPS/DefaultBurst`); a negative QPS disables throttling. The direct client and the remote informer cache built from that config share the same per-cluster budget. Disable the gate to restore the old 5/10 behaviour (source: raw/kueue/pkg/controller/admissionchecks/multikueue/multikueuecluster.go, raw/kueue/pkg/features/kube_features.go). See [[performance-and-scale#Client-side rate limiting]].

Provenance and versions: [[pr-15280]] (fixes issue-14973) merged with the gate first written as `MultiKueueClientConnection` and renamed `MultiKueueReuseClientConnectionConfigForWorkers` in review. It is **Beta/on in v0.20.0**. The backports are **Alpha/off**: v0.19.4 and v0.18.8. The companion fix #15310 ("share one rate limiter across per-worker MultiKueue REST clients") makes the direct client and the remote informer cache of **one** worker draw from one token bucket, instead of each building its own. It shipped in v0.20.0, v0.19.4 (#15326) and v0.18.8 ([[pr-15387]]) (source: pr-15280.md, pr-15387.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, CHANGELOG-0.19.md, CHANGELOG-0.18.md). With the gate on, the budget is therefore **per worker cluster**, not one global budget across all workers.

## A worker-local WorkloadPriorityClass can overwrite a remote Workload's priority

The manager owns the priority of a dispatched Workload; a same-named class on the worker with a different value can silently re-price it. See [[workload-priority#Worker-cluster classes must not re-price MultiKueue remote Workloads]].

## Elastic RayCluster with in-tree autoscaling

By default an elastic RayCluster with `enableInTreeAutoscaling` is rejected under MultiKueue ([[elastic-jobs#MultiKueue rejects an autoscaling elastic RayCluster]], pr-14061).

**Why the rejection exists ([[pr-13244]]).** An earlier change (#12885) cleared `enableInTreeAutoscaling` on the *remote* copy, but `BuildPodSets` on the manager still counted the autoscaler sidecar in the head PodSet. The worker then derived PodSets **without** the sidecar and judged the prebuilt Workload `OutOfSync`, finishing it right after admission. The manager reacted by creating a replacement slice and deleting the remote Workload. #13244 resolves the inconsistency by keeping that combination out of the system. The webhook rejects it (`validateElasticJob`), `copyJobSpec` now copies the spec unchanged (**no strip**), and `syncWorkerReplicas` syncs only each worker group's `Replicas` and `NumOfHosts`. Manual manager → worker replica edits with autoscaling off still work. Shipped in v0.20.0, v0.19.1 (#13563) and v0.18.5 (source: pr-13244.md, raw/kueue/pkg/controller/jobs/raycluster/raycluster_multikueue_adapter.go, raw/kueue/CHANGELOG/CHANGELOG-0.19.md). **Correction (2026-10-21)**: this page used to say the adapter clears `enableInTreeAutoscaling` on the remote copy. That was true only before #13244.

**v0.20 adds an opt-in**: gate `MultiKueueRayInTreeAutoscaling` (**Alpha, off by default**, KEP-13243) allows worker-side Ray in-tree autoscaling for MultiKueue-managed elastic RayCluster/RayJob (#13435). Its dependencies are `MultiKueue`, `ElasticJobsViaWorkloadSlices` **and, since [[pr-16470]] (v0.20.1), `SkipChildJobSuspension`**. Kueue fails startup validation if the last one is disabled or unset, because the generic child-job suspension otherwise races with slice replacement and suspends the running child RayCluster (see [[job-framework-interface#Child jobs: `SkipChildJobSuspension`]]). Validation in the shared `raycluster` helper (source: raw/kueue/pkg/controller/jobs/raycluster/common.go):

- `enableInTreeAutoscaling` without workload slicing is rejected with "a kueue-managed job can use autoscaling only as an elastic job: enable the ElasticJobsViaWorkloadSlices feature gate and set the "kueue.x-k8s.io/elastic-job": "true" annotation". This wording is from [[pr-13996]], and it is built from `workloadslicing.EnabledAnnotationKey/Value`, so it cannot drift from the constant.
- A MultiKueue-managed elastic job with autoscaling and the gate off is rejected with "in-tree autoscaling for a MultiKueue-managed elastic job requires enabling the MultiKueueRayInTreeAutoscaling feature gate". **Correction (2026-10-21)**: this page quoted the message as "...elastic RayCluster requires...".
- In v0.20.0–v0.20.2, a MultiKueue-managed **RayService** with in-tree autoscaling is always forbidden ("...is not supported"), even with the gate on. #16260 (v0.20.0) extended the rejection to RayJob and RayService. [[pr-16259]] lifts it for RayService on `main` and release-0.20 (see the next section). Worker-side replica changes flow back to the manager as runtime annotations; for a RayJob the reverse sync is triggered directly by the worker-side child RayCluster (pr-16315), and evicted elastic slices have their remote objects removed (pr-15871). See [[elastic-jobs#MultiKueue and elastic slices]].

## RayService worker autoscaling

[[pr-16259]] extends worker-side Ray autoscaling to RayService when workload slicing and `MultiKueueRayInTreeAutoscaling` (**Alpha, off**; requires `MultiKueue`, `ElasticJobsViaWorkloadSlices`, `SkipChildJobSuspension`) are on (source: pr-16259.md, raw/kueue/pkg/controller/jobs/ray/ray_multikueue_adapter.go, raw/kueue/pkg/controller/jobs/rayservice/rayservice_multikueue_adapter.go):

- `workerOwnsReplicas` is true for an elastic job with autoscaling and the gate on. Then the manager never pushes replica counts to the worker.
- On each `SyncJob`, `reflectRuntimeState` reads the worker's state and writes it onto the manager copy as runtime annotations (`SetRuntimeWorkerStateAnnotations`). For RayService, `fetchActiveRayClusterWorkerState` reads `status.activeServiceStatus.rayClusterName` on the worker RayService and returns that RayCluster's `WorkerGroupPodCounts` plus a revision (`<UID>-<generation>`). It returns nothing while the RayService is suspended or has no active cluster. The lookup checks that the RayService controls the active RayCluster and that the cluster has only worker groups the service declares.
- A change in the runtime counts produces a new or updated workload slice on the manager. After the replacement slice is admitted, `repointPrebuiltWorkload` points the worker RayService's prebuilt-workload marker at it. If the counts did not change in this pass, the repoint happens at once; otherwise it waits for the next reconcile.
- Limit: only the **active** RayCluster is followed. A pending RayCluster during a zero-downtime upgrade, and the period when both exist, are not handled (issue-17099, open; TODO in `fetchActiveRayClusterWorkerState`).

**`serveConfigV2` during autoscaling ([[pr-17464]]).** In autoscaling mode the Ray adapter returned right after syncing runtime counts. So a `serveConfigV2` edit on the manager never reached the worker. Now the adapter continues to the `MultiKueueRemoteSpecSync` step after the runtime sync, and KubeRay updates the active RayCluster in place. The deferred repoint is kept when runtime counts change. The e2e test drives worker counts `0 → 2 → 0 → 1` by changing only `serveConfigV2`, with the RayService and active RayCluster UIDs unchanged (source: pr-17464.md).

Releases: `main` and release-0.20 only ([[pr-17466]] for #16259, [[pr-17513]] for #17464), merged 2026-10-20, after v0.20.2. Not on release-0.19. See [[integration-rayjob#MultiKueue: RayService worker autoscaling]].

## Manager-side gate `MultiKueueRemoteSpecSync`

**Beta, default on since v0.20.** Forwards manager-side spec changes made after admission onto the worker copy. Today the only such change is a RayService `serveConfigV2` edit. The gate also watches the manager job so the change propagates promptly rather than on the next periodic requeue (source: raw/kueue/pkg/features/kube_features.go).

How it works ([[pr-14036]]; source: pr-14036.md):

- Before this, a dispatched RayService was **create-once**. `SyncJob` copied status back but never re-applied the manager spec, so a `serveConfigV2` edit on the manager was silently dropped. KubeRay applies `serveConfigV2` *in place* to the existing RayCluster, moving deployments `UPDATING → HEALTHY`, with no new Pods.
- `RemoteSpecSyncer[PtrT]` (`NeedsSync` / `Apply`) plus the `WithRemoteSpecSync` option on the shared Ray MultiKueue adapter. The adapter owns the mechanism (detect on reconcile, patch the remote in place, keep the MultiKueue metadata). Each job type owns the policy. RayService forwards **only `serveConfigV2`**. Changes to `rayClusterConfig` and `upgradeStrategy` (zero-downtime upgrade) are **not** propagated; issue-17099 is open for that.
- Prompt trigger: the edit changes neither PodSets nor quota, so the Workload does not change and nothing would reconcile until the `workerLostTimeout` requeue (default 15 min). An optional adapter interface **`MultiKueueLocalJobWatcher`** (`NewEmptyLocalJob`; create-once adapters return `nil`) registers a watch on the manager job. `localJobHandler` enqueues the owning Workload, found through the owner-reference index, only when the job's `metadata.generation` changes, so status-only updates cannot cause a sync feedback loop.
- If the RayService CRD is not installed, the informer must not crash the manager. This was found during review.
- With worker-side autoscaling on, the spec sync now runs after the runtime-count sync instead of being skipped ([[pr-17464]]; see [[#RayService worker autoscaling]]).
- Versions: Beta/on in v0.20.0. Backported to v0.19.1 and v0.18.5 (source: raw/kueue/CHANGELOG/CHANGELOG-0.19.md, CHANGELOG-0.18.md).

## Recovering a replaced slice that was not finished (worker side)

When a workload slice scales, the scheduler reserves quota for the replacement and then finishes the old slice. If that finish fails, for example on an update conflict, the old slice keeps holding quota. The ordinary job reconcile recovers from this, but the **prebuilt-workload** path used by MultiKueue workers did not. [[pr-16473]] adds `FinishReplacedWorkloadSlices` to prebuilt job reconciliation. A slice is finished there when some replacement points at it via `replacement-for` and that replacement holds quota and is neither evicted nor finished. Ordinary slice normalization is unchanged. Shipped in **v0.20.1** ([[pr-16772]]) (source: pr-16473.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md). See [[elastic-jobs#MultiKueue and elastic slices]].

## Remote `OwnerNotFound` finishes are treated as sync failures

A remote Workload that finished with reason `OwnerNotFound` was mirrored back verbatim. That permanently finished the manager Workload and left the manager Pod's scheduling gates stuck. Such a finish is now treated like `OutOfSync`: the admission check is reset and the Workload is re-dispatched (#14997). Shipped in v0.20.0, v0.19.3 and v0.18.7 ([[pr-15092]]) (source: pr-15092.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md).

## `MultiKueueKubeConfigPathValidation` is Beta (v0.20)

[[pr-13706]] (fixes #13704) graduated the gate to **Beta, on by default in v0.20** (Alpha since 0.19). `MultiKueueCluster` kubeconfigs with `locationType: Path` must then live under **`/etc/multikueue/kubeconfigs/`**. Disabling the gate restores any file path, which can expose sensitive files readable by the manager (source: pr-13706.md, raw/kueue/pkg/features/kube_features.go). See [[security]].

## Metrics: `multikueue_workloads_evicted_total`

pr-15288 adds counter `multikueue_workloads_evicted_total{cluster_queue, cluster, reason, replica_role}`, next to `multikueue_workloads_dispatched_total` and `multikueue_workloads_admitted_total`, so operators can see Workloads that keep being admitted on a worker and bounced back for re-admission, and attribute the churn to a specific worker and eviction reason. As with `admitted_total`, a Workload can be counted repeatedly if evicted and re-admitted (source: pr-15288.md, raw/kueue/pkg/metrics/metrics.go). See [[metrics]].

## `observedGeneration` refresh on unchanged status (v0.20; MultiKueueCluster and manager ClusterQueue)

The same pattern behind the AdmissionCheck fix above was found in two more reconcilers: they skipped the status write whenever the condition's status/reason/message were unchanged, so an updated spec that was evaluated and left the condition `True` left `observedGeneration` stale.

- **`MultiKueueCluster`** `Active` condition: refreshed after configuration updates that keep the connection healthy (pr-15962; backports pr-15986, pr-15989).
- **Manager `ClusterQueue`** `MultiKueueManagerQuotaAutomation` condition: refreshed after a spec change that leaves the condition unchanged (pr-16140).

Clients that wait for `observedGeneration == metadata.generation` before trusting a condition depend on this. `cmpConditionState` (renamed `isConditionEqual` in pr-15985) is still used by event handlers to detect meaningful health transitions and must not be broadened.

## Beta: `MultiKueueOrchestratedPreemption`

Graduated to **Beta, on by default, in v0.20** (pr-16235, tracked by issue-13966.md). The KEP still notes that a concrete Configuration API for the preemption behaviour is planned under issue-9852. Details in [[multikueue-orchestrated-preemption]].

**Throughput regression fixed ([[pr-17157]]).** Workers no longer write a `Closed` state into `status.preemptionGates` for gates that were never opened, which removed two status writes per replicated Workload. A missing state still means closed. Backports pr-17468 / pr-17469, after v0.20.2 / v0.19.9. Details in [[multikueue-orchestrated-preemption]] (source: pr-17157.md).

## ClusterProfile (`MultiKueueClusterProfile`, Alpha)

- **No crash without the CRD ([[pr-17228]]).** With the `MultiKueueClusterProfile` gate (**Alpha, off**) on and the optional `clusterprofiles.multicluster.x-k8s.io` CRD not installed, the manager failed to start. `ConfigureClusterProfileCache` already skipped the cache entry, but the cluster controller registered the ClusterProfile watch based on the gate alone. The watch then synced against a cache entry that did not exist, and the manager exited. This also broke kubeconfig-based MultiKueue on such clusters. `cmd/kueue/main.go` now detects the CRD (`config.ClusterProfileCRDPresent`) and passes it through `multikueue.WithClusterProfileCRDPresent`. The watch is registered only if the gate is on **and** the CRD exists. Backports: pr-17360 (release-0.20), pr-17362 (release-0.19), merged 2026-10-16, after v0.20.2 / v0.19.9. This is the first step of the Beta work tracked in issue-17133 (source: pr-17228.md, raw/kueue/pkg/controller/admissionchecks/multikueue/controllers.go).
- **`v1alpha2` ClusterProfile (`main` only, [[pr-17331]]).** Kueue now builds on `sigs.k8s.io/cluster-inventory-api` v0.2.0 and reads `ClusterProfile` as `multicluster.x-k8s.io/v1alpha2`, not the deprecated `v1alpha1`. It no longer reads `status.credentialProviders`. It applies `tls-server-name`, `insecure-skip-tls-verify` and `disable-compression` from `status.accessProviders[].cluster`. **ACTION REQUIRED** if you use the gate: before upgrading Kueue, upgrade the ClusterProfile CRD to cluster-inventory-api v0.2.0 or later, and make sure your cluster manager sets `status.accessProviders` (source: pr-17331.md).

## Behaviours worth knowing (from open issues)

- **The manager's flavor assignment is not mirrored to the worker.** Kueue injects the admitted flavor's node labels into the manager's *local* copy; the mirrored Workload on the worker is admitted independently against the worker's own ClusterQueue and flavors. Manager-side per-flavor quota therefore need not describe where work ran (source: issue-16010.md, open feature/bug report).
- **A worker watch that reconnects does not replay missed events**, and there is no relist on reconnect; state changes during the gap (`Admitted`, `Finished`, `Evicted`) are normally picked up only by the `workerLostTimeout`-based requeue (source: issue-16172.md, open). Suspect this when the manager lags a worker after a network blip.
- **RayJob + external AdmissionCheck `Retry`** can leave a manager Workload `Admitted` (holding quota) after the worker mirror is deleted, because the worker RayJob's `Suspended` status was not mirrored back first (source: issue-15380.md, open).

## Related pages

- [[admission-check]] — MultiKueue is one.
- [[workload]] — mirror workloads exist on each worker.
- [[integrations]] — which job types can be dispatched.
- [[multikueue-orchestrated-preemption]] — **[Alpha]** serializes preemption across worker clusters to avoid duplicate disruption.
- [[job-framework-interface]]
- [[integration-rayjob]]
- [[elastic-jobs]]
