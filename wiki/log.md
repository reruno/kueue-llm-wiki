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

---

## 2026-04-23 — Developer-workflow (testing) section

**Operator**: Claude Code, per the `/ultraplan` executed on 2026-04-23 (developer testing wiki).

**What was created**:

- `wiki/testing.md` — landing page for the new Developer-workflow section. Test pyramid (unit / integration / e2e), prerequisites, `make kind-image-build` vs `make image-build` ([[pr-5414]]), per-tier run commands, four focus strategies (label filter, `--focus`, `ginkgo.FIt`, narrowed package), CI job map (attested subset), `TEST_LOG_LEVEL`, bot commands (`/retest`, `/test <job>`, `/retitle`), flake-debugging playbook, `make verify` / `make lint-fix` / `make update-helm` / `make generate manifests` notes.
- `wiki/testing-integration.md` — `envtest` suites under `test/integration/`; directory map (singlecluster, multikueue, framework); four CI variants (main/baseline/extended/multikueue); label taxonomy (controllers, jobs, features, areas, slow/redundant); Ginkgo conventions (`Ordered`, `ContinueOnFailure`, `DescribeTable`, `DeferCleanup`, builders in `pkg/util/testing`, helpers in `test/util/util.go`); timeout-constant table from `test/util/constants.go`; three flake patterns citing [[issue-9952]] and [[issue-9954]].
- `wiki/testing-e2e.md` — full suite matrix (singlecluster, multikueue, multikueue-sequential, multikueue-dra, tas, dra, certmanager, sequential/baseline, sequential/extended, upgrade, kueueviz, k8s-main-was); `E2E_MODE=ci|dev` lifecycle from `hack/testing/e2e-common.sh`; dev-mode speedup vars (`E2E_SKIP_REINSTALL`, `E2E_SKIP_IMAGE_RELOAD`, `E2E_ENFORCE_OPERATOR_UPDATE`); the verbatim MultiKueue invocation from [[issue-10200]]; parallelization defaults; legacy `E2E_RUN_ONLY_ENV` attach mode; flake patterns from [[issue-6525]], [[issue-3044]], [[issue-10200]].
- `wiki/testing-performance.md` — scheduler perf targets and configs (baseline, TAS); `SCALABILITY_*` env vars; `hack/testing/compare-performance.sh`; primary metric signals; explicit note that Prow job names for perf are not individually attested in the raw/github corpus.

**Also changed**:

- `wiki/index.md` — added a "Developer workflow" section after "Lifecycle and performance" with the four new pages.
- `wiki/performance-and-scale.md` — reciprocal link to [[testing-performance]] under Related pages.

**Sources cited inline**: [[issue-9952]], [[issue-9954]], [[issue-3044]], [[issue-6525]], [[issue-10200]], [[pr-2415]], [[pr-5414]], [[pr-6906]]. Authoritative repo files cited by path: `Makefile-test.mk`, `hack/testing/e2e-common.sh`, `hack/testing/e2e-test.sh`, `hack/testing/e2e-multikueue-test.sh`, `hack/testing/performance-test.sh`, `hack/testing/compare-performance.sh`, `test/util/constants.go`, `test/util/util.go`, `site/content/en/docs/contribution_guidelines/testing.md`, and the `test/integration/`, `test/e2e/`, `test/performance/` trees.

**Correction noted**: The 2026-04-23 bulk-ingest entry above stated that `raw/kueue/` was uninitialized. That is no longer true — the submodule is populated, so this section could cite `Makefile-test.mk`, the `hack/testing/*.sh` runners, and the `test/` tree directly.

---

## 2026-04-27 — Triage-only batch (no wiki changes)

**Data-collection commit**: `663bb2a2f206bf7f721aebef491d25ac8efb21ee`

**Source files reviewed**:

- Issues: `issue-10766.md`, `issue-10786.md`, `issue-10792.md`, `issue-10795.md`
- PRs: `pr-10725.md`, `pr-10752.md`, `pr-10753.md`, `pr-10760.md`, `pr-10775.md`, `pr-10780.md`, `pr-10782.md`, `pr-10783.md`, `pr-10788.md`, `pr-10793.md`, `pr-10794.md`, `pr-10796.md`

**Outcome**: No wiki pages created or updated. All items fall under the exclusion rules:

- `issue-10766` — KEP discussion ("Composable dispatcher" for MultiKueue); proposal-stage.
- `issue-10786`, `issue-10792` — flaky-test report and E2E cleanup task; admin/test-infra.
- `issue-10795` — open RayService bug ("Redis cleanup jobs enter Suspended"); not yet fixed.
- `pr-10725` — open MultiKueue past-execution-time bug fix; unmerged.
- `pr-10752` — open TAS test fix; unmerged + test-infra.
- `pr-10753` — merged but `kind/flake` only; the bug analysis surfaced a real CQ-cleanup race (CQ may stick around if last evicting workloads + LQ are deleted in a narrow window) which the maintainers explicitly deferred to a separate issue rather than fixing in shipped code. No behaviour change to record.
- `pr-10760` — open TAS NodeHotSwap "late pods" UnhealthyNodes pollution fix; unmerged.
- `pr-10775` — open Dockerfile multi-arch fix; release/build infra.
- `pr-10780` — open additional perf tests; test infra.
- `pr-10782` — open indexer-test addition; test infra.
- `pr-10783` — open TAS `stateWithLeader` aggregation fix for grouped PodSets; unmerged.
- `pr-10788` — merged backport (release-0.17) of an MK e2e flake timeout bump; admin/test-infra.
- `pr-10793`, `pr-10794` — zh-CN doc translations; localization, no behaviour.
- `pr-10796` — open KEP-10765 (`WorkloadPriorityClassDefaulting` feature gate proposal); proposal-stage.

**Note for future ingests**: PR #10725 (MultiKueue past-execution-time), #10760 (TAS late-pods/UnhealthyNodes), #10783 (TAS grouped-PodSet `stateWithLeader`), and the KEP-10765 implementation should be revisited once merged — they each refine non-obvious controller invariants worth documenting in `[[multikueue]]`, `[[topology-aware-scheduling]]`, or `[[workload-priority]]`.
