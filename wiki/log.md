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

**Rationale**: Obsidian-style wiki-links render as clickable references in Obsidian (and compatible viewers), let the existing `[[wiki-page]]` (placeholder) convention extend uniformly to raw sources, and make it trivial to navigate from any claim to its source file under `raw/github/kubernetes-sigs__kueue/`.

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

---

## 2026-04-28 — Gap analysis and bulk wiki expansion (19 new pages)

**Data-collection commit**: `663bb2a2f206bf7f721aebef491d25ac8efb21ee`

**Operator**: Claude Code, driven by a gap analysis of KEPs in `raw/kueue/keps/` and job types in `raw/kueue/pkg/controller/jobs/` that lacked wiki coverage.

**What was created** (19 new pages):

### Features and scheduling
- `wiki/dra.md` — **Alpha** DRA support (KEP-2941): ResourceClaimTemplate and extended-resource paths, `deviceClassMappings` config, feature gates `DynamicResourceAllocation` + `DRAExtendedResources`.
- `wiki/resource-transformer.md` — **GA** Configurable resource transformers (KEP-2937): Replace/Retain modes, MIG GPU slicing, budget credits use case, `multiplyBy` field.
- `wiki/admission-fair-sharing.md` — **Beta** Admission fair sharing (KEP-4136): usage-decay, entry penalty, AdmissionScope, weight config; distinct from preemption-based fair sharing.
- `wiki/concurrent-admission.md` — **Alpha** Concurrent admission (KEP-8691): Parent/Variant Workload model, flavor racing, migration policies.
- `wiki/admission-gated-by-annotation.md` — **Alpha** `kueue.x-k8s.io/admission-gated-by` annotation (KEP-6915): delay admission for external controllers patching resource requests.
- `wiki/preemption-cost.md` — **Alpha** `kueue.x-k8s.io/priority-boost` annotation (KEP-7990): dynamic effective priority for scheduling and preemption candidate ordering.
- `wiki/multikueue-orchestrated-preemption.md` — **Alpha** MultiKueue orchestrated preemption (KEP-8303): PreemptionGate API, serialized ungating, 5-min timeout.
- `wiki/failure-recovery.md` — **Alpha** Failure recovery (KEP-6757): zombie pod force-delete, `safe-to-forcefully-delete` annotation, `FailureRecovery` gate.
- `wiki/workload-max-execution-time.md` — **Beta** Maximum execution time (KEP-3125): `spec.maximumExecutionTimeSeconds`, accumulation across preemption cycles, deactivation outcome.

### Operator tooling
- `wiki/workload-garbage-collection.md` — **Stable** GC of finished/deactivated Workloads (KEP-1618): `objectRetentionPolicies` config, cascade deletion warning.
- `wiki/local-queue-defaulting.md` — **Stable** LocalQueue defaulting (KEP-2936): auto-inject `queue-name: default` when a `default` LQ exists in the namespace.
- `wiki/manage-jobs-selectively.md` — **Stable** Selective job management (KEP-3589): `manageJobsWithoutQueueName` + `managedJobsNamespaceSelector`, namespace-selector patterns.

### New integrations
- `wiki/integration-spark.md` — **Alpha** SparkApplication (Spark Operator v2): driver+executor PodSets, no dynamic allocation, no MultiKueue support.
- `wiki/integration-statefulset.md` — **Beta** StatefulSet: pod scheduling gates (no spec.suspend), MultiKueue adapter with limited status sync.
- `wiki/integration-trainjob.md` — **Alpha** TrainJob (Training Operator v2): delegates PodSets to child JobSet, reclaimable pods, full MultiKueue status sync.

### Developer and debugging
- `wiki/job-framework-interface.md` — **Stable** GenericJob interface (KEP-369): all required methods, optional interfaces, base reconciler, webhook scaffolding, integration registration.
- `wiki/debugging-guide.md` — Synthesized from source code and GitHub issues: workload condition table, 6 root cause categories (quota, flavor mismatch, admission check, PodsReady timeout, TAS, deactivation), kueuectl commands, Prometheus metrics.
- `wiki/scheduler-internals.md` — The 6-phase scheduling cycle (Heads → Snapshot → Nominate → Iterator → processEntry → Requeue), FlavorAssigner modes (Fit/Preempt/NoFit), quota tiers, fair-sharing iterator.
- `wiki/cache-architecture.md` — Scheduler cache vs queue manager, per-cycle snapshot, `hierarchy.Manager`, cycle detection, informer-based consistency model.

**Also changed**:
- `wiki/index.md` — 19 new entries added under existing and new subsections; alpha/beta/stable labels added to relevant entries.
- `wiki/dra.md` — added prominent alpha callout block after the stage reminder from user.

**Sources**: `raw/kueue/keps/` (KEPs 2941, 2937, 4136, 8691, 6915, 7990, 8303, 6757, 3125, 1618, 2936, 3589, 369), `raw/kueue/pkg/scheduler/`, `raw/kueue/pkg/cache/`, `raw/kueue/pkg/controller/jobframework/`, `raw/kueue/pkg/controller/jobs/{sparkapplication,statefulset,trainjob}/`, `raw/kueue/pkg/dra/`, `raw/github/kubernetes-sigs__kueue/` (selected issues for debugging patterns).

---

## 2026-04-28 — Lint pass on the bulk-expansion entry

**Operator**: Claude Code, follow-up to the same-day gap-analysis ingest.

**What changed**:

- Inline source citations on the 19 new pages stripped of the redundant `raw/kueue/` prefix; paths are now repo-relative (e.g. `(source: keps/4136-admission-fair-sharing/README.md)`), matching the convention already in use on the testing pages.
- Stage labels normalized: every new page that documents a single feature now carries a top-of-page `> **Stage: X** — feature-gate \`Name\`, …` blockquote. Pages that previously held a separate `## Stage` or `## Feature gate` section have had it folded into the top callout. Pages without a single owning feature (`scheduler-internals`, `cache-architecture`, `debugging-guide`) intentionally have no callout.
- `wiki/index.md` — `**[Stable/GA]**` on `[[resource-transformer]]` collapsed to `**[Stable]**`; `Last updated` bumped.
- `wiki/feature-gates.md` — extended the "Gates that have shipped" list to cover `AdmissionFairSharing`, `ConcurrentAdmission`, `MultiKueueOrchestratedPreemption`, `AdmissionGatedBy`, `WorkloadPriorityBoost`, `FailureRecovery`, `MaxExecTime`, `ManagedJobsNamespaceSelectorAlwaysRespected`, `DRAExtendedResources`, `SparkApplicationIntegration`. Existing `LocalQueueDefaulting` bullet repointed at `[[local-queue-defaulting]]`. Added a config-only-knobs callout for `objectRetentionPolicies` and `integrations.frameworks`.
- Wired the eight orphan pages: `[[concurrent-admission]]` from `admission-check`, `scheduler-internals`, `workload`; `[[debugging-guide]]` from `architecture`, `kueuectl`, `metrics`, `scheduler-internals`; `[[integration-spark]]`, `[[integration-statefulset]]`, `[[integration-trainjob]]` from `integrations`; `[[multikueue-orchestrated-preemption]]` from `multikueue`, `preemption`; `[[preemption-cost]]` from `preemption`, `workload-priority`; `[[workload-garbage-collection]]` and `[[workload-max-execution-time]]` from `workload`.
- `[[kueue-overview]]` cross-linked from `integrations`, `kueuectl`, `debugging-guide` (it was previously only linked from `architecture`).
- `wiki/dra.md` — Related-pages list now includes `[[provisioning-request]]`. The duplicated DRA-vs-resource-transformer comparison was collapsed to a one-line cross-link to the canonical version on `[[resource-transformer]]`.
- `wiki/log.md` — annotated the `[[wiki-page]]` literal (line 58) as a placeholder so readers don't mistake it for a broken link.

**Not changed**: the `**Sources**:` headers on individual pages still carry the full `raw/kueue/...` paths, since those serve as a self-contained "where this came from" reference and the redundancy is one-line, not per-paragraph.

---

## 2026-04-30 — Reviewer profile: mimowo

**Data-collection commit**: `663bb2a2f206bf7f721aebef491d25ac8efb21ee`

**Operator**: Claude Code, driven by user request to analyze maintainer review style for LLM code-review agents.

**What was created**:

- `wiki/reviewer-mimowo.md` — NEW page profiling @mimowo's review philosophy, patterns, communication style, and a checklist for LLM reviewers. Drawn from analysis of review comments across 6,000+ PRs where @mimowo participated, with representative deep reads of [[pr-4444]], [[pr-8082]], [[pr-8151]], [[pr-8186]], [[pr-8341]], [[pr-8464]], [[pr-8530]], [[pr-8805]], [[pr-9311]], [[pr-9619]].

**What changed**:

- `wiki/index.md` — added "Reviewer profiles" section at the bottom; linked [[reviewer-mimowo]].

**Scope and method**:

Grepped all 8,241 PR files for `@mimowo` comments; identified PRs with 5+ comments from them; read 10 representative PRs spanning 2025-03 through 2026-04 to collect inline review comments, prose feedback, and approval patterns. Synthesized into categories: backwards compatibility, naming, API design, test requirements, log verbosity, helper extraction, communication vocabulary, approval workflow.

---

## 2026-05-06 — MultiKueueCluster reconnect mechanics

**Source**: `pkg/controller/admissionchecks/multikueue/multikueuecluster.go` (read directly), prompted by user question about a multikueue e2e log showing two `setting client config` errors 6 ms apart with `retryAfter: 5s` and `retryAfter: 10s`.

**What changed**:

- `wiki/multikueue.md` — added "MultiKueueCluster reconnect mechanics" section documenting the `2^(n-1) * 5s` backoff (capped at ~5m20s, `retryMaxSteps=7`), the `failedConnAttempts` / `connecting` state, and why the condition flip `True/Connected → False/ClientConnectionFailed` causes a self-triggered second reconcile (status-update event re-enqueues the cluster before `RequeueAfter` fires; the cascade stops after one extra cycle because the second status write is a no-op via `cmpConditionState`).

**Why it's worth a wiki entry**: not visible from the [[multikueue]] high-level flow; the "double error in the same second" pattern is a real operational footgun when reading manager logs.

---

## 2026-05-11 — v0.16.7 / v0.17.2 / v0.18.0 ingest

**Data-collection commit**: `b8776e3175da41ba110c3213e5b7aebdd7f5422e`

**Operator**: Claude Code, per the standing wiki ingest workflow.

**Source files analysed** (283 new + 184 updated raw files in this collection run; the new files are listed in full below):

- Issues (61): `issue-10705`, `issue-10706`, `issue-10750`, `issue-10751`, `issue-10759`, `issue-10773`, `issue-10777`, `issue-10778`, `issue-10802`, `issue-10807`, `issue-10812`, `issue-10813`, `issue-10814`, `issue-10815`, `issue-10816`, `issue-10822`, `issue-10824`, `issue-10827`, `issue-10831`, `issue-10847`, `issue-10848`, `issue-10852`, `issue-10861`, `issue-10865`, `issue-10866`, `issue-10872`, `issue-10876`, `issue-10880`, `issue-10897`, `issue-10901`, `issue-10902`, `issue-10904`, `issue-10911`, `issue-10912`, `issue-10913`, `issue-10918`, `issue-10920`, `issue-10926`, `issue-10929`, `issue-10932`, `issue-10933`, `issue-10934`, `issue-10938`, `issue-10939`, `issue-10942`, `issue-10946`, `issue-10953`, `issue-10960`, `issue-10965`, `issue-10968`, `issue-10986`, `issue-10988`, `issue-10991`, `issue-10995`, `issue-11000`, `issue-11003`, `issue-11006`, `issue-11024`, `issue-11029`, `issue-11055`, `issue-11061`.
- PRs (222): `pr-10686`, `pr-10707`, `pr-10723`, `pr-10744`, `pr-10745`, `pr-10747`, `pr-10754`, `pr-10755`, `pr-10779`, `pr-10784`, `pr-10785`, `pr-10797`–`pr-10801`, `pr-10803`–`pr-10806`, `pr-10808`–`pr-10811`, `pr-10817`–`pr-10821`, `pr-10823`, `pr-10825`, `pr-10826`, `pr-10828`–`pr-10830`, `pr-10832`–`pr-10846`, `pr-10849`–`pr-10851`, `pr-10853`–`pr-10860`, `pr-10862`–`pr-10864`, `pr-10867`–`pr-10871`, `pr-10873`–`pr-10875`, `pr-10877`–`pr-10895`, `pr-10898`–`pr-10900`, `pr-10903`, `pr-10905`–`pr-10910`, `pr-10914`–`pr-10917`, `pr-10919`, `pr-10921`–`pr-10925`, `pr-10927`, `pr-10928`, `pr-10930`, `pr-10931`, `pr-10935`–`pr-10937`, `pr-10940`, `pr-10941`, `pr-10943`–`pr-10945`, `pr-10947`–`pr-10952`, `pr-10954`–`pr-10959`, `pr-10961`–`pr-10964`, `pr-10966`, `pr-10967`, `pr-10969`–`pr-10985`, `pr-10987`, `pr-10989`, `pr-10990`, `pr-10992`–`pr-10994`, `pr-10996`–`pr-10999`, `pr-11001`, `pr-11002`, `pr-11004`, `pr-11005`, `pr-11007`–`pr-11023`, `pr-11025`–`pr-11028`, `pr-11030`–`pr-11054`, `pr-11056`–`pr-11060`.

**Triage outcome**: of the 283 new files, ~75 carry merged behaviour worth documenting. The remainder are open issues, open/draft PRs, KEPs, flaky-test reports, release-tracking issues, dependency bumps, and test-infra cleanups — all excluded by the "merged, shipped behaviour only" rule from CLAUDE.md.

**Wiki pages updated** (no new pages — depth on existing pages favoured per the prompt):

- `wiki/cluster-queue.md` — NEW sections: "Finalizer (`kueue.x-k8s.io/cluster-queue`)" documenting the scheduler-cleanup race and its fix in [[pr-10821]] (cherry-picked to release-0.16, release-0.17 in v0.16.7 / v0.17.2; tracked in [[issue-10759]]); "Configuration: `quotaCheckStrategy` (alpha, v0.18)" covering the new field gated by the `QuotaCheckStrategy` feature gate, with `IgnoreUndeclared` mode (v0.18.0 release note from [[issue-10861]]).
- `wiki/concurrent-admission.md` — NEW "Implementation details (v0.18 hardening)" section covering: scheduling-equivalence hash for Variants ([[pr-10910]]), parent → Variant indexer ([[pr-10921]] / [[issue-10904]]), skip-less-favorable-Variant guard ([[pr-10917]] / [[issue-10913]]), Variant lifecycle Events ([[pr-10951]]), comma-separated annotation parsing cleanup ([[pr-10957]]), `preemption.Target` wrapping cleanup ([[pr-10954]]); also updated the StrictFIFO constraint to note the new webhook rejection in [[pr-11022]].
- `wiki/failure-recovery.md` — NEW "Pods already in a terminal phase" subsection: terminal-phase (Failed/Succeeded) pods on unreachable nodes are now also force-deleted when annotated, fixing JobSet cascade-deletion deadlocks ([[pr-10853]] cherry-picked in v0.16.7 / v0.17.2, KEP follow-up [[pr-10854]], tracked in [[issue-10847]]).
- `wiki/fair-sharing.md` — NEW: "Where you can set `fairSharing.weight` — CQ vs Cohort" clarifying the per-level semantics and the documentation gap in [[issue-10872]]; "`SubtreeQuota` invalidation on cohort deletion" describing the cache-staleness fix in [[pr-10797]]; "Nil-pointer panic on cohort-less CQs" describing the [[pr-10891]] fix.
- `wiki/feature-gates.md` — Three new bullets (`FinishOrphanedWorkloads` downgrade with full root-cause writeup citing [[pr-11010]] / [[pr-11014]] / [[issue-10901]]; new alpha `QuotaCheckStrategy`; new alpha action-required `RejectUpdatesToCQWithInvalidOnFlavors`); new "v0.18 graduations" subsection listing `MultiKueueRedoAdmissionOnEvictionInWorker`, `MultiKueueWaitForWorkloadAdmitted`, `SkipFinalizersForPodsSuspendedByParent`.
- `wiki/integration-appwrapper.md` — NEW "AppWrapper version pin" section: v0.18.0 ships against AppWrapper v1.2.1 ([[pr-10898]]); dependency-only patch.
- `wiki/integration-leaderworkerset.md` — NEW "v0.18.0 behaviour changes" with four subsections: `nodeSelector` mutability on running LWS (#10275, cherry-picks [[pr-10944]] / [[pr-10930]]), `queue-name` mutable while idle (#4932), `WorkloadKeyForLeaderWorkerSet` helper unification (#8843, cherry-pick [[pr-10945]]), PodTemplate metadata propagation (#10330, closes [[issue-10326]]).
- `wiki/integration-rayjob.md` — NEW "Ray version pin (v0.18.0)" section: Ray bumped 2.41.0 → 2.53.0 ([[pr-10707]] with cherry-picks [[pr-10958]] / [[pr-10959]]) due to opencensus SIGABRT in 2.41.0; resource baseline implications.
- `wiki/integration-trainjob.md` — NEW "Mutating webhook scope (v0.18.0)" section: webhook no longer patches the referenced TrainingRuntime, only the TrainJob itself ([[pr-10829]] / fixes #10099); avoids race when one runtime is shared across namespaces.
- `wiki/metrics.md` — NEW "Cohort CPU unit fix" subsection ([[pr-10747]] / [[issue-10746]]) explaining the `kueue_cohort_subtree_*` milliCPU-vs-CPU-units bug; "Stale cohort metrics after subtree change" cross-link to [[fair-sharing]]; new "v0.18.0 metric changes" listing `workload_eviction_latency_seconds` (new histogram, #10323) and the `evicted_workloads_once_total` `detailed_reason` → `underlying_cause` rename (#10637, action-required).
- `wiki/release-process.md` — Updated representative release tracking with v0.16.7 ([[issue-10706]]), v0.17.2 ([[issue-10705]]), v0.18.0 ([[issue-10861]]); NEW "v0.18.0 highlights" section summarising the action-required items, new features, stable graduations, and notable bug fixes from the v0.18.0 changelog.
- `wiki/scheduler-internals.md` — NEW "Inadmissible-workload requeue guard" subsection covering [[pr-11014]] and the `FinishOrphanedWorkloads` regression motivation; NEW "Second-pass seeding (multi-resource workloads)" subsection covering [[pr-11005]] / fixes #9048 (multi-resource second-pass double-counting bug).
- `wiki/topology-aware-scheduling.md` — NEW "Snapshot internals (`tas_flavor_snapshot.go`)" with three deep subsections: empty-children over-estimation in `stateWithLeader` ([[pr-10841]] cherry-pick of #10783, prep [[pr-10843]], tracked in [[issue-10778]] and [[issue-10812]]); negative state propagation into `TopologyAssignment.podCounts.individual` ([[pr-10949]]); multi-resource second-pass double-counting ([[pr-11005]]); NEW "Performance: incremental non-TAS usage cache" describing the per-node aggregation cache in #10366 (cherry-pick [[pr-11041]]); NEW "NodeHotSwap 'late pods'" subsection covering #10760 (cherry-picks [[pr-10837]] / [[pr-10838]]).

**Excluded items of note** (not documented; visible in this batch but not yet shipped behaviour):

- Open ConcurrentAdmission proposals: `HoldFirstAdmission` mode ([[issue-10911]]), mutable `concurrentAdmissionPolicy` API ([[issue-10912]]), reaction to ClusterQueue `resourceGroups` changes ([[issue-10918]]), single-Variant-eviction policy ([[issue-10920]]).
- Open TAS/preemption bug reports: TAS preemption skipped for Deployment-backed workloads ([[issue-10929]]), `flavorFungibility: TryNextFlavor` ghost-quota deadlock ([[issue-10824]]), FairSharing + TAS conflict ([[issue-10815]]), TAS `preferredDuringSchedulingIgnoredDuringExecution` support ([[issue-10902]] / open [[pr-10903]]), Decouple non-leader TAS from `stateWithLeader` ([[issue-10812]]).
- Open MultiKueue / admission bugs: Workload `Admitted` condition not flipped on AdmissionCheck Rejection ([[issue-10807]]), MultiKueue Prebuilt Preemption Event clarity ([[issue-10968]]), FeatureGates not validated on configMap/CLI input ([[issue-10866]] / open fix [[pr-10931]]).
- Open features/proposals: scheduling-goodput metric ([[issue-10813]] / WIP [[pr-10987]]), per-Workload metrics ([[issue-10876]]), Inadmissible-Workloads metrics ([[issue-10852]] / open [[pr-10899]]), pending-resource metric for head-of-queue ([[issue-10897]]), workload/job dependencies API ([[issue-11024]]), Kueue + Grove integration ([[issue-10831]]), `WorkloadPriorityClassDefaulting` (open [[pr-10798]]), composable MultiKueue dispatcher (open [[pr-10784]] / [[pr-10937]]), TAS LFC fragmentation reduction ([[pr-10878]]), DRA → Beta ([[pr-10996]]), Extended Resources → Beta ([[pr-10973]]).
- Documentation/skills/test-infra/release plumbing: numerous merged docs (ConcurrentAdmission docs, Quick Start guide, KubeCon talk update, multikueue-e2e docs), agent-skills additions and skill-tooling work, Helm-test deduplication, test wrappers / labels (`GroupNameLabel`, `PrebuiltWorkloadLabel`), Eventually-wrapping for flake reduction, e2e timeout/recovery bumps, Dockerfile multi-arch fixes, controller-runtime Event Recorder migration ([[pr-10971]] open), HA follower-cache regression test ([[pr-10811]] — test only; the underlying fix was #10518/#10529, already shipped).

**Note for future ingests**: many of the open items above are in active development and will likely land in a future patch or v0.19; revisit when their PRs merge. In particular [[pr-10996]] (DRA → Beta), [[pr-10973]] (Extended Resources → Beta), [[pr-10798]] (WorkloadPriorityClassDefaulting), [[pr-10878]] (TAS fragmentation), and the open MultiKueue dispatcher refactors will each warrant page updates when shipped.

---

## 2026-05-12 — Reviewers and code-quality pages

**Source**: `raw/github/kubernetes-sigs__kueue/` review comments across multiple PRs; `raw/kueue/OWNERS`, `OWNERS_ALIASES`, `CONTRIBUTING.md`, `.golangci.yaml`, `Makefile-verify.mk`.

**Operator**: Claude Code.

**Data-collection commit this analysis is based on**: `b8776e3` (`[data-collection] 283 new,184 updated items from kubernetes-sigs/kueue, kueue@f23b3bf06`).

**What was created**:

- `wiki/reviewers.md` — NEW: overview of OWNERS structure (top-level approvers, path-filter overrides for dependency/test/agent paths, emeritus approvers, security/release contacts), reviewer roster table, Prow command reference (`/lgtm`, `/approve`, `/hold`, `/cherrypick`, `/release-note-edit`, etc.), division-of-responsibility matrix across the five most active reviewers, and a "how to get a PR reviewed quickly" checklist.
- `wiki/code-quality.md` — NEW: synthesized cross-reviewer quality bar in 12 themes (upgrade safety, integration tests, naming, API versioning, scope/hygiene, scheduler performance, logging verbosity, helper extraction, release notes, feature-gate lifecycle, tooling, and a pre-flight checklist). Quotes from mimowo (pr-8530, pr-8186, pr-9619, pr-8341, pr-8151, pr-8082, pr-6297, pr-10013, pr-8805), tenzen-y (pr-10282), gabesaba (pr-10082, pr-8709, pr-9359), mbobrovskyi (pr-10595, pr-10323), and PBundyra (pr-10244).
- `wiki/reviewer-tenzen-y.md` — NEW: profile of @tenzen-y as the project's de-facto release manager; release-branch thinking, semantic correctness on annotation pairs, release-note rewriting, conflict-resolution discipline; representative PRs pr-10145, pr-10282, pr-10623, pr-10668, pr-10674, pr-10677, pr-10684.
- `wiki/reviewer-gabesaba.md` — NEW: profile of @gabesaba focused on scheduler invariants, preemption-loop avoidance, cache coherency, performance regressions in event/workqueue paths, MultiKueue manager-worker disconnect scenarios; representative PRs pr-7392, pr-8484, pr-8658, pr-8709, pr-9359, pr-10082, pr-10422, pr-10510, pr-10524.
- `wiki/reviewer-mbobrovskyi.md` — NEW: profile of @mbobrovskyi as test-approver and dependency-approver; "do we need this?" pattern, duplication/helper extraction, multi-concern PR splitting, suggestion-block Go idioms, delegation to top approvers via `/assign`; representative PRs pr-10244, pr-10294, pr-10323, pr-10388, pr-10595.
- `wiki/reviewer-pbundyra.md` — NEW: profile of @PBundyra focused on API design and Kubernetes versioning practices (no in-place removal of beta fields, `+required` vs `omitempty` markers, deprecation migration paths, KEP-first workflow); representative PRs pr-8861, pr-10244, pr-10388.

**Index updates**:

- Renamed "Reviewer profiles" section to "Reviewers and code quality" with entries for all new pages.
- Bumped `Last updated` to 2026-05-12.

**Method**: parallel research agents extracted recurring patterns and direct quotes from PR comment threads per reviewer; `OWNERS_ALIASES` consulted to confirm roles and path-filter responsibilities; `CONTRIBUTING.md` and `.golangci.yaml` checked to ground the formal-tooling sections in code-quality.md.

**Cross-linking**: each reviewer page links to the others, to `reviewers.md`, and to `code-quality.md`. `code-quality.md` links into the technical pages (`testing`, `feature-gates`, `scheduler-internals`, `preemption`, `cache-architecture`, `multikueue`, `job-framework-interface`, `release-process`). Pre-existing `reviewer-mimowo.md` is referenced but not modified.

**Out of scope**: dedicated profile pages for the second-tier reviewers (kannon92, pajakd, olekzabl, kshalot, sohankunkerkar) — listed in `reviewers.md` only with focus areas.
