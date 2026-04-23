# Wiki operations log

Append-only. Most recent entries at the bottom.

---

## 2026-04-23 — Initial bulk ingest

**Source**: `raw/github/kubernetes-sigs__kueue/` — 2,427 issues + 8,229 pull requests scraped from `kubernetes-sigs/kueue` (through April 2026).

**Operator**: Claude Code, per the `/ultraplan` executed on 2026-04-23.

**What was created**:

- `wiki/index.md` — table of contents with 30+ entries, organized into seven sections (Start here, Core API objects, Admission and scheduling, Advanced scheduling, Integrations, Operator tooling, Lifecycle and performance).
- Core concept pages: `kueue-overview`, `architecture`, `cluster-queue`, `local-queue`, `cohort`, `resource-flavor`, `workload`.
- Admission and scheduling: `admission`, `admission-check`, `queueing-strategy`, `preemption`, `fair-sharing`, `borrowing-and-lending`, `workload-priority`, `gang-scheduling`, `elastic-jobs`.
- Advanced scheduling: `topology-aware-scheduling`, `multikueue`.
- Integrations: `integrations` + `integration-batchjob`, `integration-jobset`, `integration-kubeflow`, `integration-rayjob`, `integration-leaderworkerset`, `integration-appwrapper`, `integration-argo-workflow`, `integration-plain-pod`.
- Operator tooling: `kueuectl`, `visibility-api`, `metrics`, `dashboard`, `webhooks`, `importer`.
- Lifecycle: `feature-gates`, `release-process`, `performance-and-scale`.

**Method**: For each concept, representative issues and PRs were located by grepping title lines in `raw/github/kubernetes-sigs__kueue/*.md` (e.g. foundational KEPs, graduation trackers, and representative bug reports). Pages cite those files inline as Obsidian wiki-links — `[[issue-NNN]]` or `[[pr-NNN]]` — which resolve to the corresponding files under `raw/github/kubernetes-sigs__kueue/`.

**Out of scope**:

- The `raw/kueue/` submodule (Kueue Go source) was not initialized, so code-level detail (file paths, function names in `pkg/`) is not covered.
- The 10,656 raw issue/PR files are not individually summarized; they are cited only where they substantiate a conceptual claim.

---

## 2026-04-23 — Lint pass (citations + ProvisioningRequest page)

**Operator**: Claude Code, per the `/ultraplan` executed on 2026-04-23 (lint the wiki).

**What was changed**:

- `wiki/feature-gates.md` — corrected `LocalQueueDefaulting` GA citation from [[pr-3652]] (KEP design PR, merged 2024-12-03) to [[issue-9633]] (confirms v0.17 GA). Softened the `AdmissionCheckRetry` bullet: dropped the [[issue-10618]] citation (that issue is about surface-message improvements, not the feature gate), marked the retry-across-flavors semantics claim as needing verification.
- `wiki/admission-check.md` — rewrote the `Retry` bullet to accurately cite [[issue-10618]] as "improving the surfaced reason for Retry"; slimmed the ProvisioningRequest bullet and `admissionCheckStrategy` paragraph to summaries that link to the new `[[provisioning-request]]` page; added the new page to Related pages.
- `wiki/provisioning-request.md` — NEW concept page covering controller + API object, `ProvisioningRequestConfig` (with `managedResources`), per-flavor gating via `admissionCheckStrategy`, tolerations/nodeSelectors flow-through, DWS (Dynamic Workload Scheduler) mode, and Retry interaction. Cites [[issue-2572]], [[issue-2213]], [[issue-2260]], [[issue-10660]].
- `wiki/index.md` — added `[[provisioning-request]]` under "Admission and scheduling" after `[[admission-check]]`.

**Also flagged (not fixed)**:

- Weakly connected operator-tooling pages (`dashboard`, `importer`, `kueuectl`, `release-process`) each have only one non-index inbound link. They are not orphans per CLAUDE.md's definition; improvement deferred.
- DRA / `DynamicResourceAllocation` (KEP-2941) does not yet warrant its own page (3 references total, no dedicated source ingested into `raw/`). Deferred.

---

## 2026-04-23 — Convert citations to Obsidian wiki-link style

**Operator**: Claude Code, per a follow-up request to the `/ultraplan` lint pass.

**What was changed**:

Converted all 300 inline source citations across 36 wiki pages from `(source: issue-NNN.md)` / `(source: pr-NNN.md)` form to Obsidian wiki-links `[[issue-NNN]]` / `[[pr-NNN]]`. Descriptive text after the em-dash is preserved, e.g. `([[issue-9633]] — confirms v0.17 GA)`. Bare in-prose references like `issue-3450.md` were also converted. The style-description sentence on line 23 of this log was updated to reflect the new convention.

**Rationale**: Obsidian-style wiki-links render as clickable references in Obsidian (and compatible viewers), let the existing `[[wiki-page]]` convention extend uniformly to raw sources, and make it trivial to navigate from any claim to its source file under `raw/github/kubernetes-sigs__kueue/`.
