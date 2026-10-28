# Visibility API

**Summary**: The Visibility API is an aggregated-apiserver extension at `visibility.kueue.x-k8s.io` that exposes pending-workload information per [[local-queue]] and [[cluster-queue]]. It lets tenants see their queue position without needing direct read access to the Workload CRD.

**Sources**: `raw/github/kubernetes-sigs__kueue/`, pr-14411.md, pr-16485.md, pr-16342.md, raw/kueue/apis/visibility/v1beta2/types.go, raw/kueue/pkg/visibility/storage/utils.go, raw/kueue/pkg/features/kube_features.go, raw/kueue/CHANGELOG/CHANGELOG-0.20.md

**Last updated**: 2026-10-28

---

## Why it's a separate API

Reading all Workloads to answer "where am I in line" is expensive at scale. The Visibility API exposes derived, aggregated views (pending list, position, counts) on top of Kueue's in-memory queues — serving them from the kueue-controller-manager directly. Tenants query `kubectl get --raw /apis/visibility.kueue.x-k8s.io/v1beta2/namespaces/<ns>/localqueues/<lq>/pendingworkloads` or `/apis/visibility.kueue.x-k8s.io/v1beta2/clusterqueues/<cq>/pendingworkloads` instead of listing all Workloads. **Correction (2026-10-21)**: this page previously showed a `v1beta1` path; `visibility.kueue.x-k8s.io/v1beta1` is unserved from v0.20 and its package was deleted on main by pr-16485, so only `v1beta2` exists (source: pr-16485.md, raw/kueue/apis/visibility/v1beta2/types.go). The serving gate is `VisibilityOnDemand` (Alpha 0.6, Beta/on since 0.9).

## Evolution

- The feature started as alpha under the `QueueVisibility` feature gate ([[issue-1102]] — Add `QueueVisibility` to featureGate).
- Position-in-queue report was added ([[issue-1657]]).
- Integration tests landed ([[issue-1377]]) and HA of the extension apiserver was considered ([[issue-1510]]).
- Cohort-level visibility was proposed ([[issue-2272]]) but closed as not planned.
- "Deprecate the `QueueVisibility` feature gate and corresponding API" ([[issue-2256]]) marks the transition from the older aggregated approach to the new server implementation.
- Cross-namespace / cross-LocalQueue visibility fetches were extended ([[issue-10575]]).

## Caveats

- **Snapshot locking.** The snapshot that serves the API is shared with the scheduler's cache. Holding the lock for long while serving a large cohort was a performance concern ([[issue-1098]] — Release the lock as soon as possible when computing the snapshot for CQ visibility).
- **Port collision.** Visibility and pprof endpoints both landed on 8082 originally ([[issue-2226]]).
- **Staleness.** A deleted Workload could still appear as pending until the next snapshot refresh ([[issue-1555]]).
- **Discovery failures.** "Failed to get resource list for visibility.kueue.x-k8s.io/v1alpha1" ([[issue-1519]]) is the canonical "apiserver can't reach the extension" symptom, usually a Service/Endpoints misconfiguration.

## Configuration: bind port and address (`--visibility-server-port` removed)

The visibility server's bind port and address are configured through the Kueue Configuration API under `visibilityServer` (`bindPort`, default `configapi.DefaultVisibilityBindPort`; `bindAddress`), read in `pkg/visibility/server.go`.

- **`--visibility-server-port` flag removed (action-required).** [[pr-11309]] deletes the deprecated controller-manager flag. Installations that still pass `--visibility-server-port` must drop it and set `visibilityServer.bindPort` in the Configuration instead before upgrading.
- **`bindAddress` regression fixed.** During the port-defaulting refactor in #11323 the `o.SecureServing.BindAddress = net.ParseIP(*cfg.VisibilityServer.BindAddress)` assignment was accidentally dropped, so a configured `visibilityServer.bindAddress` (e.g. `127.0.0.1`) was silently ignored and the server kept binding to the default `0.0.0.0`. [[pr-11341]] restores it. Gotcha: the bug only manifested when `visibilityServer.bindPort` was *also* set — with `bindPort` left default, the address was applied correctly.

## Response shape (v1beta2)

`GET .../pendingworkloads` returns a `PendingWorkloadsSummary` whose `items` are `PendingWorkload{metadata, priority, localQueueName, positionInClusterQueue, positionInLocalQueue}` (positions start at 0). Query parameters (`PendingWorkloadOptions`): `offset` (default 0) and `limit` (default 1000) (source: raw/kueue/apis/visibility/v1beta2/types.go).

## Fixes in v0.20

- **Nil priority panicked the endpoint (pr-14411, v0.20.0; cherry-picks requested for 0.19/0.18).** `newPendingWorkload` (`pkg/visibility/storage/utils.go`) dereferenced `*wlInfo.Obj.Spec.Priority`. `Workload.Spec.Priority` is a `*int32` that is legitimately nil for a Workload created with no global default priority class and no pod priority class — in practice a user-supplied prebuilt Workload ("BYOW"), since Kueue-created Workloads get a priority. The apiserver panic filter turned it into a `500`/`ServiceUnavailable`, so **one such pending Workload broke the CQ and LQ endpoints for every caller** until it was admitted or deleted. Now uses `priority.Priority(wl)`, which resolves nil to `constants.DefaultPriority`, like the rest of the codebase. Rule: never dereference `Spec.Priority` directly (source: pr-14411.md).
- **`positionInLocalQueue` inflated across namespaces (#14431, v0.20.0).** On the ClusterQueue endpoint, two LocalQueues in different namespaces with the same name (for example the auto-created `default` LocalQueue) were counted as one queue, inflating positions. LocalQueue identity must be namespace+name (source: CHANGELOG-0.20.md).

The cert-manager visibility e2e test no longer deletes the first Job's Workload by hand: since #11596 deleting a Job with orphan propagation releases quota on its own (pr-16342, test-only).


## Model revisit

"Revisit the model for cache management and visibility server" ([[issue-10553]]) — an open thread about whether the cache needs reshaping to serve visibility cheaply at larger cluster scales.

## Related pages

- [[cluster-queue]] — where pending queues live.
- [[cohort]] — cohort-scoped views.
- [[local-queue]] — tenant-facing view.
- [[metrics]] — complementary Prometheus surface.
- [[api-versions]] — v1beta1 removal.
- [[kueuectl]] — `kueuectl list workload`/pending views built on this API.
