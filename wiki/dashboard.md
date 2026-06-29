# Dashboard (KueueViz)

**Summary**: KueueViz is a web UI for Kueue: it reads the Kueue API (and, partially, the [[visibility-api]]) to show per-[[cluster-queue]] usage, pending workloads, cohort utilization, and per-namespace quotas. It's a separate component (backend + frontend) deployed alongside Kueue, not part of the controller-manager.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-06-29

---

## Components

- **Backend** — service account with read access to Kueue CRDs and Workloads; exposes a JSON API consumed by the frontend.
- **Frontend** — a web UI for cluster admins and tenants.

## Scope

KueueViz is oriented at operational visibility, not management actions — edits happen through [[kueuectl]] or plain `kubectl`. The UI covers:

- Cluster-queue list with usage vs. nominal quota.
- Cohort-level views.
- Per-namespace / per-LocalQueue pending workloads.
- Resource utilization plots ([[issue-10072]] — UI improvements).

## Known issues / evolution

- "Kueueviz backend fails to list cohorts due to missing permissions" ([[issue-10091]]) — the backend ServiceAccount needed an RBAC update when cohorts became a first-class CRD.
- "KueueViz: add e2e tests for the resource utilization feature" ([[issue-10132]]) — test coverage catching up to features.

## LocalQueue details: filter by `spec.queueName`

The LocalQueue details page used to list **every** Workload in the namespace regardless of which LocalQueue was selected: the backend `fetchLocalQueueWorkloads` (`cmd/kueueviz/backend/handlers/local_queue_workloads.go`) accepted a `queueName` parameter but never applied it ([[pr-11199]], fixes [[issue-6613]]; cherry-picked to 0.16/0.17 in [[pr-11212]]/[[pr-11213]]). The fix filters `wql.Items` client-side on `item.Spec.QueueName == queueName`. A server-side field selector was rejected because `spec.queueName` is not registered as a selectable field on the Workload CRD — so client-side filtering is used, consistent with `kueuectl list workload localqueue`.

## MultiKueue stats

"Support worker resource stats visibility in MultiKueue manager cluster" ([[issue-10105]]) — KueueViz historically couldn't reach into worker clusters; this opened the path.

## Related pages

- [[visibility-api]] — underlying API surface for some views.
- [[metrics]] — alternate Prometheus-based visibility.
- [[cluster-queue]], [[cohort]] — core entities shown.
