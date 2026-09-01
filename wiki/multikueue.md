# MultiKueue

**Summary**: MultiKueue dispatches [[workload]]s from a **manager cluster** to one of several **worker clusters**. Users submit jobs on the manager as usual; MultiKueue (implemented as an [[admission-check]]) picks a worker cluster with capacity, forwards the job, and mirrors status back. It's how one Kueue installation governs a fleet of clusters.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-09-01

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

- **Opt-in is per-config**: `MultiKueueConfig.spec.quotaAutomation.mode` is an enum (`Manual` | `Automated`); when unset the default depends on the feature gate.
- A new `CQReconciler` (`pkg/controller/admissionchecks/multikueue/clusterqueue.go`) watches manager ClusterQueues, finds the MultiKueue AdmissionCheck, resolves the `MultiKueueConfig`, and writes the summed `nominalQuota` into the CQ's single flavor (only when changed).
- **Constraint**: the manager CQ must have **exactly one ResourceGroup with exactly one Flavor**, else the CQ gets condition `MultiKueueManagerQuotaAutomation=False` with reason `UnsupportedConfiguration`. Worker clusters that are still `connecting` are skipped in the sum.
- New CQ status **condition** `MultiKueueManagerQuotaAutomation` (reasons: `QuotaAutomated`, `NotRequested`, `UnsupportedConfiguration`). Remote ClusterQueue/LocalQueue reads use a new `SelectivelyCachingClient` + informers so reconciles fire only on relevant remote changes.

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

## Manager → worker clients run at client-go's default rate limit

`newClientWithWatch` (`pkg/controller/admissionchecks/multikueue/multikueuecluster.go`) builds each worker cluster's `client.WithWatch` from the kubeconfig **without touching `restConfig.QPS` / `restConfig.Burst`**, so the manager→worker connection falls back to client-go's `rest.Config` defaults of **QPS 5 / Burst 10**. Kueue's *own* API client is far more generous — `clientConnection` defaults to **QPS 300 / Burst 500** — so the remote leg is the throttled one, and there is no configuration field to raise it.

Measured impact (source: issue-14973.md, open feature request): a burst of **1000 Workloads** across 10 worker clusters took **~15 minutes** to be fully admitted; hard-coding `QPS = Burst = 500` on `restConfig` in a PoC brought the same burst down to **~1.5 minutes**. The number of worker clusters was not the significant variable. If you are diagnosing slow MultiKueue dispatch under bursty load, client-side throttling on the remote clients is the first thing to rule out — see [[performance-and-scale#Client-side rate limiting]].

## A worker-local WorkloadPriorityClass can overwrite a remote Workload's priority

The manager owns the priority of a dispatched Workload; a same-named class on the worker with a different value can silently re-price it. See [[workload-priority#Worker-cluster classes must not re-price MultiKueue remote Workloads]].

## Elastic RayCluster with in-tree autoscaling is rejected

See [[elastic-jobs#MultiKueue rejects an autoscaling elastic RayCluster]] ([[pr-14061]]).

## Related pages

- [[admission-check]] — MultiKueue is one.
- [[workload]] — mirror workloads exist on each worker.
- [[integrations]] — which job types can be dispatched.
- [[multikueue-orchestrated-preemption]] — **[Alpha]** serializes preemption across worker clusters to avoid duplicate disruption.
