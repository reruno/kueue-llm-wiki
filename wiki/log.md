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

**Method**: For each concept, representative issues and PRs were located by grepping title lines in `raw/github/kubernetes-sigs__kueue/*.md` (e.g. foundational KEPs, graduation trackers, and representative bug reports). Pages cite those files inline with `(source: issue-NNN.md)` or `(source: pr-NNN.md)`.

**Out of scope**:

- The `raw/kueue/` submodule (Kueue Go source) was not initialized, so code-level detail (file paths, function names in `pkg/`) is not covered.
- The 10,656 raw issue/PR files are not individually summarized; they are cited only where they substantiate a conceptual claim.
