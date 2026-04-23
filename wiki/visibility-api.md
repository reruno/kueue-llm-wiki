# Visibility API

**Summary**: The Visibility API is an aggregated-apiserver extension at `visibility.kueue.x-k8s.io` that exposes pending-workload information per [[local-queue]], [[cluster-queue]], and [[cohort]]. It lets tenants see their queue position and wait estimate without needing direct read access to the Workload CRD.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

---

## Why it's a separate API

Reading all Workloads to answer "where am I in line" is expensive at scale. The Visibility API exposes derived, aggregated views (pending list, position, counts) on top of Kueue's in-memory queues — serving them from the kueue-controller-manager directly. Tenants query `kubectl get --raw /apis/visibility.kueue.x-k8s.io/v1beta1/namespaces/<ns>/localqueues/<lq>/pendingworkloads` (or similar) instead of listing all Workloads.

## Evolution

- The feature started as alpha under the `QueueVisibility` feature gate ([[issue-1102]] — Add `QueueVisibility` to featureGate).
- Position-in-queue report was added ([[issue-1657]]).
- Integration tests landed ([[issue-1377]]) and HA of the extension apiserver was considered ([[issue-1510]]).
- Cohort-level visibility was added ([[issue-2272]]).
- "Deprecate the `QueueVisibility` feature gate and corresponding API" ([[issue-2256]]) marks the transition from the older aggregated approach to the new server implementation.
- Cross-namespace / cross-LocalQueue visibility fetches were extended ([[issue-10575]]).

## Caveats

- **Snapshot locking.** The snapshot that serves the API is shared with the scheduler's cache. Holding the lock for long while serving a large cohort was a performance concern ([[issue-1098]] — Release the lock as soon as possible when computing the snapshot for CQ visibility).
- **Port collision.** Visibility and pprof endpoints both landed on 8082 originally ([[issue-2226]]).
- **Staleness.** A deleted Workload could still appear as pending until the next snapshot refresh ([[issue-1555]]).
- **Discovery failures.** "Failed to get resource list for visibility.kueue.x-k8s.io/v1alpha1" ([[issue-1519]]) is the canonical "apiserver can't reach the extension" symptom, usually a Service/Endpoints misconfiguration.

## Model revisit

"Revisit the model for cache management and visibility server" ([[issue-10553]]) — an open thread about whether the cache needs reshaping to serve visibility cheaply at larger cluster scales.

## Related pages

- [[cluster-queue]] — where pending queues live.
- [[cohort]] — cohort-scoped views.
- [[local-queue]] — tenant-facing view.
- [[metrics]] — complementary Prometheus surface.
