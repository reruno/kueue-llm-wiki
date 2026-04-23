# Visibility API

**Summary**: The Visibility API is an aggregated-apiserver extension at `visibility.kueue.x-k8s.io` that exposes pending-workload information per [[local-queue]], [[cluster-queue]], and [[cohort]]. It lets tenants see their queue position and wait estimate without needing direct read access to the Workload CRD.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

---

## Why it's a separate API

Reading all Workloads to answer "where am I in line" is expensive at scale. The Visibility API exposes derived, aggregated views (pending list, position, counts) on top of Kueue's in-memory queues — serving them from the kueue-controller-manager directly. Tenants query `kubectl get --raw /apis/visibility.kueue.x-k8s.io/v1beta1/namespaces/<ns>/localqueues/<lq>/pendingworkloads` (or similar) instead of listing all Workloads.

## Evolution

- The feature started as alpha under the `QueueVisibility` feature gate (source: issue-1102.md — Add `QueueVisibility` to featureGate).
- Position-in-queue report was added (source: issue-1657.md).
- Integration tests landed (source: issue-1377.md) and HA of the extension apiserver was considered (source: issue-1510.md).
- Cohort-level visibility was added (source: issue-2272.md).
- "Deprecate the `QueueVisibility` feature gate and corresponding API" (source: issue-2256.md) marks the transition from the older aggregated approach to the new server implementation.
- Cross-namespace / cross-LocalQueue visibility fetches were extended (source: issue-10575.md).

## Caveats

- **Snapshot locking.** The snapshot that serves the API is shared with the scheduler's cache. Holding the lock for long while serving a large cohort was a performance concern (source: issue-1098.md — Release the lock as soon as possible when computing the snapshot for CQ visibility).
- **Port collision.** Visibility and pprof endpoints both landed on 8082 originally (source: issue-2226.md).
- **Staleness.** A deleted Workload could still appear as pending until the next snapshot refresh (source: issue-1555.md).
- **Discovery failures.** "Failed to get resource list for visibility.kueue.x-k8s.io/v1alpha1" (source: issue-1519.md) is the canonical "apiserver can't reach the extension" symptom, usually a Service/Endpoints misconfiguration.

## Model revisit

"Revisit the model for cache management and visibility server" (source: issue-10553.md) — an open thread about whether the cache needs reshaping to serve visibility cheaply at larger cluster scales.

## Related pages

- [[cluster-queue]] — where pending queues live.
- [[cohort]] — cohort-scoped views.
- [[local-queue]] — tenant-facing view.
- [[metrics]] — complementary Prometheus surface.
