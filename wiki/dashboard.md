# Dashboard (KueueViz)

**Summary**: KueueViz is a web UI for Kueue: it reads the Kueue API (and, partially, the [[visibility-api]]) to show per-[[cluster-queue]] usage, pending workloads, cohort utilization, and per-namespace quotas. It's a separate component (backend + frontend) deployed alongside Kueue, not part of the controller-manager.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

---

## Components

- **Backend** — service account with read access to Kueue CRDs and Workloads; exposes a JSON API consumed by the frontend.
- **Frontend** — a web UI for cluster admins and tenants.

## Scope

KueueViz is oriented at operational visibility, not management actions — edits happen through [[kueuectl]] or plain `kubectl`. The UI covers:

- Cluster-queue list with usage vs. nominal quota.
- Cohort-level views.
- Per-namespace / per-LocalQueue pending workloads.
- Resource utilization plots (source: issue-10072.md — UI improvements).

## Known issues / evolution

- "Kueueviz backend fails to list cohorts due to missing permissions" (source: issue-10091.md) — the backend ServiceAccount needed an RBAC update when cohorts became a first-class CRD.
- "KueueViz: add e2e tests for the resource utilization feature" (source: issue-10132.md) — test coverage catching up to features.

## MultiKueue stats

"Support worker resource stats visibility in MultiKueue manager cluster" (source: issue-10105.md) — KueueViz historically couldn't reach into worker clusters; this opened the path.

## Related pages

- [[visibility-api]] — underlying API surface for some views.
- [[metrics]] — alternate Prometheus-based visibility.
- [[cluster-queue]], [[cohort]] — core entities shown.
