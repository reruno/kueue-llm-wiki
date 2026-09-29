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

---

## 2026-05-18 — Security ingest from CVE corpus

**Source**: `raw/cve/` — 515 CVE files (2018-2026) covering Kubernetes, kubernetes-sigs, Flux, Argo, Jenkins, Red Hat, Fedora, etc. Each file has a fixed structure with a `Category` field and a `Security Code Patterns` checklist that repeats per category.

**Data-collection commit**: `a5d7eec [data-collection] 736 new,219 updated items from kubernetes-sigs/kueue, kueue@a7ba93ed4` (most recent `[data-collection]` commit; the `raw/cve/` files were added in `6a83ef2 Add collect cve` / `6a3d3f6 update collect_cve`).

**Operator**: Claude Code, in response to "based on these please create wiki pages dedicated to code security and best practices".

**What was created**:

- `wiki/security.md` — NEW: landing page. Threat model for Kueue, CVE corpus shape (counts by Category and severity), and pointer index to the six topic pages.
- `wiki/security-code-patterns.md` — NEW: master checklist of patterns to flag in code review, grouped by Category and cross-referenced by CWE. Single-pane reference distilling the `Security Code Patterns` block that repeats across the corpus.
- `wiki/security-denial-of-service.md` — NEW: DoS-class patterns from 83 CVEs. CWE-400/770/476/1284 with Kueue-specific mappings to the scheduler, webhooks, cache, and workqueue.
- `wiki/security-authn-authz.md` — NEW: combined Authentication Bypass (23), RBAC Misconfiguration (7), Privilege Escalation (48), Unauthorized Write Access (30). Covers Kueue controller SA, webhook handlers, and MultiKueue manager→worker credential boundary.
- `wiki/security-information-disclosure.md` — NEW: 110 Info-Disclosure CVEs. Log hygiene (CWE-532), exposure (CWE-200), credentials (CWE-522), file/dir access (CWE-552). Concrete `git grep` checks for review.
- `wiki/security-injection-and-input-validation.md` — NEW: combined Injection (11), Path Traversal (7), Code Execution (139). CWE-20/22/74/77/78/89/94/502/918/79/352/601. Kueue surface is narrow (no `os/exec`) but constructed API requests and dashboard XSS apply.
- `wiki/security-supply-chain.md` — NEW: 6 Supply-Chain CVEs plus CWE-295/494. Image digest pinning, signature verification, `go.mod` hygiene, CI action SHA pinning.
- `wiki/security-best-practices.md` — NEW: actionable checklist for Kueue contributors and reviewers, organized by topic (input handling, resource bounds, errors/logs, authn/RBAC, nil-safety, supply chain) with suggested `git grep` commands.

**Index updates**:

- Added new "Code security" section in `index.md` after "Reviewers and code quality" with one-line blurbs for all eight new pages.
- Bumped `Last updated` to 2026-05-18.

**Method**: read a stratified sample of CVEs across all 11 categories to confirm the corpus is template-driven (per-category `Security Code Patterns` and `Mitigation` blocks repeat verbatim). The eight pages are therefore organized by *vulnerability class*, not per-CVE — each page synthesizes one or more categories and grounds patterns in Kueue's actual code surface (scheduler, webhooks, controller SA, MultiKueue, dashboard).

**Cross-linking**: every page links back to `security.md` and `security-code-patterns.md`; topic pages link to the relevant existing concept pages (`scheduler-internals`, `webhooks`, `admission`, `multikueue`, `metrics`, `visibility-api`, `dashboard`, `cache-architecture`, `release-process`); `security-best-practices.md` links to all six topic pages and to `code-quality.md` and `testing.md`.

**Out of scope**:

- No per-CVE wiki pages — 515 entries with templated content would not add information beyond the category synthesis. The `raw/cve/` files remain the authoritative per-CVE source.
- Code-level grounding in `pkg/` requires the `raw/kueue/` Go-source submodule (not initialized at the time of this ingest, per the 2026-04-23 entry above). The new pages reference Kueue's design surface by name but do not cite specific files or line numbers. A follow-up ingest with the submodule available could resolve the suggested `git grep` checks into concrete file references.
- No Kueue-specific CVE exists as of 2026-05; the corpus is used to teach patterns, not to document Kueue history.

---

## 2026-06-29 — GitHub PR ingest (v0.18 behaviour) + CVE corpus refresh

**Data-collection commit**: `a5d7eec57cd66cb48f85db72e9dad6a78557e706`

**Operator**: Claude Code, "wiki ingest workflow" for the latest data-collection batch.

**Source files analysed**:

- `raw/github/kubernetes-sigs__kueue/` — issue-10761 and issues 11062–11279; PRs 11064–11281 (~220 PR files, ~50 issue files). Only **merged** PRs with shipped behaviour were used; open KEPs/proposals (e.g. pr-11064 WorkloadDependency, pr-11242), draft PRs, dependency bumps, agent-skill changes, doc reorgs, and CI/test-infra/release-bookkeeping PRs were read but excluded as out-of-scope.
- `raw/cve/CVE-*.md` — full corpus, now **569** entries (was 515 at the 2026-05-18 ingest; ~54 new files in this batch). Templated, per-category teaching material; no new vulnerability classes. Used only to refresh the counts on the existing security pages.

**Wiki pages updated** (no new pages — favoured depth on existing pages):

- `feature-gates.md` — DRA gate **rename** (`DynamicResourceAllocation`→`KueueDRAIntegration`, `DRAExtendedResources`→`KueueDRAIntegrationExtendedResource`; old gates deprecated+LockToDefault in v0.18, migration helper) (pr-11255); added `SchedulingEquivalenceHashing` (Beta, v0.18, pr-11097), `TASHandleOverlappingFlavors` (Alpha, pr-11210), `TASReplaceNodeOnNodeTaints` (pr-11185), `MultiKueueManagerQuotaAutomation` (Alpha, pr-11141), `MultiKueueIncrementalDispatcherConfig` (Beta, pr-11208), `KubeRayAccountForRedisCleanup` (Beta, pr-11260).
- `concurrent-admission.md` — new "Migration policy" section: `TryPreferredFlavors` vs new `RetainFirstAdmission` mode (pr-11236), `minPreferredFlavorName`/`lastAcceptableFlavor` flavor floor + `isMigrationAllowed` (pr-11125) and its webhook validation (pr-11126); noted SchedulingEquivalenceHashing beta graduation.
- `topology-aware-scheduling.md` — Balanced-placement → BestFit fallback (pr-11136); NodeHotSwap node-taint relocation now uses *effective* tolerations (pr-11185); overlapping-ResourceFlavor usage aggregation behind `TASHandleOverlappingFlavors` (pr-11210, resolves issue-10659); non-TAS terminal-Pod cache-cleanup fix (pr-11145/11146).
- `multikueue.md` — manager quota automation KEP-9988 (pr-11141); Incremental Dispatcher `stepSize` KEP-9270 (pr-11208); hung-remote-watch establish-timeout (pr-11207); reconnect-backoff guardrail (pr-11275/10990); `clustersReconciler` predicate + replica-role logging (pr-11153).
- `scheduler-internals.md` — WorkloadSlice "admit-first, finish-old-after" ordering in processEntry (pr-11195); SchedulingEquivalenceHashing requeue-reason narrowing in Phase 6 (pr-11097); new "Quota arithmetic and integer-overflow safety" section (pr-11137/11139/11182, points to Amount).
- `cache-architecture.md` — new "Quota amount type and overflow safety" section: `resources.Amount` + `Unlimited` sentinel, `ResourceQuota` field migration, DeepEqual panic gotcha (pr-11156).
- `elastic-jobs.md` — WorkloadSlice replacement correctness: admit-then-finish (pr-11195) and sort-comparator antisymmetry fix (pr-11198).
- `webhooks.md` — integration webhooks now default-exclude `kube-system` + install namespace (pr-11192, action-required).
- `dashboard.md` — KueueViz LocalQueue page filters by `spec.queueName` (pr-11199).
- `job-framework-interface.md` — new optional `JobWithCustomQueueNameChange` interface for serving workloads (pr-11191/11215), queue-name-change logging (pr-11148).
- `integration-leaderworkerset.md` — **corrected**: the "relaxed PodSpec validation / mutable nodeSelector" entry was the #10275 change that pr-11214 **reverted**; strict PodSpec equality is restored. Added manual-queue-name-edit race fix (pr-11191).
- `integration-rayjob.md` — KubeRay Redis-cleanup Job quota accounting folded into the head PodSet (pr-11260, `KubeRayAccountForRedisCleanup`).
- `resource-flavor.md` — toleration dedup bug when `Operator:""` vs `Operator:"Equal"` (pr-11147).
- `workload-garbage-collection.md` — WorkloadSlices stuck after retention because the scheduler-set Finished condition didn't drop the finalizer; new `workload.Delete` helper (pr-11181).
- `manage-jobs-selectively.md` — webhook namespace-exclusion default (pr-11192) and kueue-populator inheriting `managedJobsNamespaceSelector` (pr-11218).
- `security-authn-authz.md` — per-resource ClusterRole aggregation label `rbac.kueue.x-k8s.io/role` (pr-11205); refreshed category counts.
- `security.md` + `security-{denial-of-service,information-disclosure,injection-and-input-validation,supply-chain}.md` — refreshed corpus totals/category counts to 569 (recomputed from `raw/cve/`).
- `index.md` — bumped Last updated and broadened the Sources note to include the CVE corpus.

**Confirmed latest patch releases** from this batch: v0.17.3 and v0.16.8 (both 2026-05-15; pr-11233/pr-11234).

**Out of scope**: pr-11064 (WorkloadDependency KEP — proposal/open), pr-11242 (KEP graduation-criteria doc), pure refactors with no behaviour change (pr-11144 ClusterQueueReference wrappers, pr-11179 constants alias, pr-11217 jobframework package reorg, pr-11156's mechanics beyond the Amount summary), test-infra/e2e-split/flake-timeout PRs, dependency bumps, and agent-skill/website PRs. No per-CVE pages (templated corpus).

---

## 2026-06-29 — GitHub ingest (v0.17.4 / v0.16.9 patch fixes) + CVE corpus check

**Data-collection commit**: `4c9f1d12da22d98ddb568b46d6e82ee779226f40`

**Operator**: Claude Code, standing wiki ingest workflow for the 224-file data-collection batch (189 PRs + 33 issues + 2 CVEs).

**Source files analysed**:

- `raw/github/kubernetes-sigs__kueue/` — PRs `pr-10688` and `pr-11282`–`pr-11502` (189 merged/closed PR files); issues `issue-11283`, `issue-11287`, `issue-11297`, `issue-11303`, `issue-11311`, `issue-11315`, `issue-11321`, `issue-11330`, `issue-11335`, `issue-11340`, `issue-11346`, `issue-11351`, `issue-11354`, `issue-11359`, `issue-11360`, `issue-11366`, `issue-11369`, `issue-11372`, `issue-11374`, `issue-11375`, `issue-11377`, `issue-11379`, `issue-11414`, `issue-11426`, `issue-11452`, `issue-11453`, `issue-11458`, `issue-11470`, `issue-11480`, `issue-11491`, `issue-11493`, `issue-11495`, `issue-11496` (33 issue files). All four PR chunks + the issue set were read in full by parallel sub-agents; only **merged, shipped** behaviour was carried into the wiki.
- `raw/cve/CVE-2026-27173.md` (Apache Airflow JWT-token exposure → Information Disclosure, CWE-538) and `raw/cve/CVE-2026-45760.md` (Apache Camel K user-controlled Build resource → Authentication Bypass, CWE-610/639). Both are ecosystem CVEs with the standard templated per-category content; neither introduces a new vulnerability class.

**Triage outcome**: of the 189 PRs, ~20 carry documentable merged behaviour (the rest are `ginkgo.Ordered` test-cleanup / e2e-split, flake fixes, dependency bumps, OWNERS/governance, website/docs, agent-skills, WIP/closed-unmerged, or pure refactors). Of the 33 issues, four document confirmed-fixed bugs worth invariants (`issue-11287`, `issue-11297`+`issue-11303`, `issue-11480`) plus the PodSet-limit feature (`issue-11379`); the rest are flaky-test fixes, release-tracking issues, open feature requests/proposals, or CI/tooling.

**Wiki pages updated** (no new pages — depth on existing pages favoured):

- `multikueue.md` — extended the hung-remote section with the **per-cluster reconcile lock** (one slow remote no longer stalls all clusters; `findOrCreateRemoteClient` + per-cluster `setConfigLock`; [[pr-11305]]/[[pr-11332]]/[[pr-11333]], issue-11297) and the **exponential watch-establish timeout** (1m→10m, detect a hung remote in 1 min; [[pr-11304]]/[[pr-11328]]/[[pr-11329]], issue-11303); new "AllAtOnce dispatcher correctness" section (wait-for-eviction-before-re-nomination [[pr-11378]]/[[pr-11472]]/[[pr-11473]]; order-insensitive `nominatedClusterSetsEqual` [[pr-11497]]/[[pr-11507]]/[[pr-11508]], issue-11453); new "RBAC: RayService on worker clusters" ([[pr-11400]]).
- `scheduler-internals.md` — new "Admitted workloads must leave `preemptionExpectations`" subsection (the SSA-admission-overwrites-eviction race causing head-of-line blocking / quota oversubscription; [[pr-11502]]/[[pr-11648]]/[[pr-11647]], issue-11480); Phase-2 note that `Snapshot()` is read-only; updated the FinishOrphanedWorkloads paragraph to record the structural fix [[pr-11296]] (re-graduated to Beta/default-on).
- `preemption.md` — new "The `preemptionExpectations` store" section (issue-11480 / [[pr-11502]]); bumped date.
- `cache-architecture.md` — new "Snapshot is strictly read-only" subsection: `skipInactiveCQReason()` + `inactiveCQReasonTASUsageNotSynced`, TAS sync moved off the read-lock path ([[pr-11286]]).
- `topology-aware-scheduling.md` — new "Cumulative Pod-count across PodSets (`addAssumedUsage`)" subsection: per-node `pods` capacity now respected across all PodSets of one Workload ([[pr-11293]]/[[pr-11326]]/[[pr-11331]], issue-11287).
- `feature-gates.md` — `FinishOrphanedWorkloads` re-graduated to **Beta/default-on** via [[pr-11296]]; `ElasticJobsViaWorkloadSlices` Beta-graduation webhook validations ([[pr-11300]]) + slice normalization ([[pr-11327]]); new **`WorkloadIdentifierAnnotations`** gate ([[pr-11409]]); `SchedulingEquivalenceHashing` effective-requests refinement for DRA ([[pr-11399]]); new "User-specified gate parameters are validated" section ([[pr-11288]]/[[pr-11291]]).
- `elastic-jobs.md` — annotation-keyed enablement + immutability path fix ([[pr-11342]]); third replacement-correctness bullet `normalizeActiveSlices` ([[pr-11327]]).
- `workload.md` — max PodSets per Workload raised 8→10 ([[pr-11388]], issue-11379 requested 16); bumped date.
- `concurrent-admission.md` — flavor-floor field renamed `minPreferredFlavorName` → `lastAcceptableFlavorName` ([[pr-11317]]).
- `dra.md` — gate names updated to `KueueDRAIntegration` / `KueueDRAIntegrationExtendedResource`; new "Startup safety: DeviceClass index is conditional" ([[pr-11405]]) and "Scheduling-equivalence hash and DRA" ([[pr-11399]]) sections; bumped date.
- `visibility-api.md` — new "Configuration: bind port and address" section: `--visibility-server-port` flag removed ([[pr-11309]], action-required) and `bindAddress` regression fix ([[pr-11341]]); bumped date.
- `job-framework-interface.md` — signature-change callout: `RunWithPodSetsInfo` / `PodSets` / `PodsReady` / `ReclaimablePods` now take a `client.Client` argument ([[pr-11310]], action-required for out-of-tree integrations).
- `integration-leaderworkerset.md` — expanded "Name length": >39-char LWS names failed because PodGroup identifiers were labels; `WorkloadIdentifierAnnotations` raises the limit to 52 ([[pr-11409]]).
- `integration-rayjob.md` — worker-group cap up to 9 (PodSet limit 8→10, [[pr-11388]]); RayService worker RBAC ([[pr-11400]]).
- `workload-garbage-collection.md` — patch-release delivery of the finalizer-GC fix ([[pr-11307]]/[[pr-11308]]); new "don't *finish* a Workload right after creation" note ([[pr-11296]]).
- `release-process.md` — added paired patch releases **v0.16.9** ([[issue-11360]]) / **v0.17.4** ([[issue-11359]]) with their headline fixes; bumped date.

**CVE corpus**: no security-page change. The two new CVE files are already within the 569-file corpus total recorded at the 2026-05-18 / a5d7eec ingests; both map to already-covered categories (Information Disclosure / Authentication Bypass) and add no new pattern.

**Out of scope** (read, excluded): the large `ginkgo.Ordered`/e2e-split and flake-fix test-infra wave (≈100 PRs across the batch), dependency bumps (containerd, k8s.io, vite/vitest, ginkgo, gomega, appwrapper v1.2.2), Helm v3→v4 tooling, OWNERS/infra-approvers governance, website/Hugo/Netlify CI, KueueViz navbar UI, agent-skill PRs, WIP/closed-unmerged PRs, pure refactors (pr-11355 RayJob global-state, pr-11356 SetMultiKueueMeta, pr-11367 MK adapter signature, pr-11323 visibility port refactor), pr-11334 (priority-booster Helm packaging), and pr-11460/pr-11490 ("Unblock ray version update" #11184 — no release note/body in the batch; low-confidence). Open items to revisit when fixed: issue-11372 (orphaned gated Pod when Workload creation fails), issue-11366 (`waitForPodsReady` default-on proposal), issue-11375 (MultiKueue cross-cluster preemption KEP).

---

## 2026-09-01 — GitHub ingest (v0.18.6 / v0.19.2 / v0.20 pre-release) + CVE corpus refresh

**Data-collection commit**: `8714655e810262a1913b044ad88ceaaf2fe2cf52` (`[data-collection] 579 new,141 updated items from kubernetes-sigs/kueue, kueue@80042b1a0`)

**Operator**: Claude Code, standing wiki ingest workflow.

**Source files analysed** (the 579-item new set: 467 GitHub files + 112 CVE files):

- `raw/github/kubernetes-sigs__kueue/` — **371 PR files** spanning `pr-12645` … `pr-14934`, and **96 issue files** spanning `issue-12692` … `issue-14935`. Every PR was triaged by state, labels, changed-file count and `release-note` block; the 223 merged PRs were deduplicated by release note (main PR + its cherry-picks collapsed into one entry), and the ~45 carrying documentable merged behaviour were read in full together with the closed/completed issues they fix.
- `raw/cve/` — **112 new CVE files**: `CVE-2026-8590`, `CVE-2026-8715`, `CVE-2026-9165`, `CVE-2026-9181`, `CVE-2026-9182`, `CVE-2026-10059`, `CVE-2026-10079`, `CVE-2026-10090`, `CVE-2026-12564`, `CVE-2026-13019`, `CVE-2026-13020`, `CVE-2026-14450`, `CVE-2026-15228`, `CVE-2026-15378`, `CVE-2026-15416`, `CVE-2026-15687`, `CVE-2026-16543`, `CVE-2026-16745`, `CVE-2026-17107`, `CVE-2026-18381`, `CVE-2026-18608`, `CVE-2026-18942`, `CVE-2026-18951`, `CVE-2026-18982`, `CVE-2026-20770`, `CVE-2026-32637`, `CVE-2026-41579`, `CVE-2026-44180`–`44182`, `CVE-2026-44949`, `CVE-2026-45737`, `CVE-2026-45738`, `CVE-2026-46680`, `CVE-2026-47237`, `CVE-2026-47262`, `CVE-2026-49478`, `CVE-2026-50149`, `CVE-2026-50195`, `CVE-2026-50516`, `CVE-2026-53487`–`53489`, `CVE-2026-53492`, `CVE-2026-53572`, `CVE-2026-53657`, `CVE-2026-54526`, `CVE-2026-54680`, `CVE-2026-54725`, `CVE-2026-54745`, `CVE-2026-54765`, `CVE-2026-55723`, `CVE-2026-55761`, `CVE-2026-55765`, `CVE-2026-55769`, `CVE-2026-55848`, `CVE-2026-55882`–`55884`, `CVE-2026-55997`, `CVE-2026-56163`, `CVE-2026-56743`, `CVE-2026-59269`, `CVE-2026-59818`, `CVE-2026-60401`–`60410`, `CVE-2026-61459`, `CVE-2026-62246`, `CVE-2026-62290`, `CVE-2026-62440`, `CVE-2026-62845`, `CVE-2026-62994`, `CVE-2026-64378`, `CVE-2026-65601`, `CVE-2026-65602`, `CVE-2026-65834`, `CVE-2026-65835`, `CVE-2026-65956`, `CVE-2026-66297`, `CVE-2026-66781`–`66783`, `CVE-2026-66787`, `CVE-2026-66793`, `CVE-2026-66794`, `CVE-2026-67309`, `CVE-2026-69129`, `CVE-2026-71208`, `CVE-2026-71327`, `CVE-2026-72640`, `CVE-2026-72648`, `CVE-2026-73263`, `CVE-2026-73298`, `CVE-2026-73499`, `CVE-2026-73500`, `CVE-2026-73666`, `CVE-2026-73667`, `CVE-2026-73834`, `CVE-2026-73840`–`73843`, `CVE-2026-75485`, `CVE-2026-75889`.

**Pages created (1)**

- `api-versions.md` — **new**. `v1beta1` set `served: false` in v0.20 and v1beta1 conversion support removed ([[pr-14558]], part of #13957, `+42/−9114` across 58 files); the `hack/migrate-to-v1beta2.sh` no-op-update migration script and what else has to change (Helm values, GitOps repos, CI fixtures, scheme registration); the "deprecate on promotion boundaries, not in place" policy; the cross-version CEL gotcha.

**Pages updated (33, plus 8 security pages below)**

- `feature-gates.md` — new "Gates added or changed in v0.19/v0.20" section covering `PrioritizePreemptorWorkloads`, `RecomputeAssignmentUponPreemptionTargetsOverlap`, `TASRecomputeAssignmentWithinSchedulingCycle` (now depends on TAS, action required), `FairSharingReevaluatePreemptionCandidates`, `SchedulingEquivalenceHashingIgnorePodSetName`, `TASCacheTopologyTree`, `ValidateRayAndSparkJobUpdates`, `MultiKueueBatchJobClearingTTLSecondsAfterFinishedOnWorkerCluster`, `ElasticJobsViaWorkloadSlicesWithPartialReplicaScaleUp`, `ReservedResourceNameValidation`, `RejectUpdatesToCQWithInvalidOnFlavors`→Beta, `LendingLimit` removed, and the `SchedulerLibraryIntegration` (WAS) pieces; plus a new "Registering a gate on a release branch" section documenting the **emulation-version trap** (a `{0.20, Beta, Default:true}` spec is still selected on a 0.19 build) and the main-vs-branch gate-dependency mechanisms.
- `scheduler-internals.md` — new sections: preemptor prioritization (`preemptorWorkload` + strict generation match, iterator ordering, `cq.AddUsage` snapshot and TAS-domain locking); recompute-on-overlapping-preemption-targets; popped heads surviving a snapshot failure (`SnapshotFailed`, inflight cleanup moved into `RequeueWorkload`, accepted tight-retry trade-off); what the scheduling-equivalence hash excludes; the shipped WAS pieces.
- `fair-sharing.md` — strategies restated in terms of **`AlmostLCA`** rather than "the preempting ClusterQueue" (wrong for hierarchies deeper than two levels); `fsStrategyUnsatisfiable` `+Inf` tournament skip and why zero-vs-zero is *not* skipped; `ZeroWeightBorrows` reuse; the reevaluate-candidates gate and its documented preemption-loop caveat; per-CQ log collapse.
- `topology-aware-scheduling.md` — cached topology trees + benchmark table; elastic leader-assignment preservation on scale-up/same-count/scale-down; `ComputeTASNetUsage` shrinking-domain guard; cross-cycle topology-domain locking for preemptors; TAS gate dependency; node-health delegation under `SchedulerLibraryIntegration`.
- `preemption.md` — preemptor tracking on the ClusterQueue; pointers to the fair-sharing and rejected-check changes.
- `admission-fair-sharing.md` — LocalQueue identity must be namespace-qualified (`team-a/default` vs `team-b/default`).
- `cluster-queue.md` — "shrinking capacity never evicts admitted Workloads" (four pinned scenarios); `RejectUpdatesToCQWithInvalidOnFlavors` Beta; the new `scheduling.quotaReleaseStrategy` Configuration field (`OnTermination` vs `OnTerminalBestEffort`, API-only scope so far).
- `borrowing-and-lending.md` — `LendingLimit` gate removed; capacity-shrink invariant.
- `admission.md` — when quota is released; the two "Admitted ≠ checks passed" fixes.
- `workload.md` — `minCount >= 0`; `priorityClassRef` frozen once quota is reserved; prefix matching for derived `DeactivatedDueTo<Cause>` reactivation; extended resources declared only in `limits` are now indexed.
- `workload-priority.md` — the refused-transition skip and its `V(4)` demotion; bounded/cancellable `parallelize.Until` sweep (≤8 workers, one error).
- `admission-check.md` — `Rejected` check during an in-flight eviction (before/after table, why the guard moved rather than being deleted); `observedGeneration` refresh.
- `multikueue.md` — `MutatingAdmissionPolicy` clearing of `status.nominatedClusterNames` (why MAP and not a webhook); preemption gates treated independently; worker Job TTL clearing and its 5-step lifecycle; AdmissionCheck `observedGeneration`.
- `metrics.md` — new recovery-wait histograms; readiness metrics no longer emitted after recovery; the two `kueue_pod_scheduling_gate_removal_seconds` fixes (negative clamp — including *why* a negative observation breaks `rate()` — and the `replica_role` label, a series-identity change); overflow/`+Inf`.
- `dra.md` — the reserved `pods` resource name: the `Set`-overwrites-in-`assignFlavors` mechanism, the four refused Configuration positions and why two of them are operands, why only the mapping-name check sits behind `KueueDRAIntegration`, and the `ReservedResourceNameValidation` upgrade escape hatch; stale DRA names after DeviceClass deletion.
- `resource-transformer.md` — `pods` refused in `input` / `multiplyBy` / `outputs`.
- `integration-plain-pod.md` — the pod-group **quota-bypass** in full (`Load` → `finalize` → `ListChildWorkloads` → `FinalizeOrphanedWorkload`, reachability via unmanaged Pods, the two-condition `is-group-workload` + controller-reference predicate and why the marker alone would regress prebuilt Workloads); finalizer removal on non-deletion eviction for serving groups and why batch groups keep the old behaviour; `role-hash` → PodSet name.
- `integration-rayjob.md` — queue-name-removal rejection (`ValidateRayAndSparkJobUpdates`); KubeRay v1.7.0 and what derives from the module version; elastic RayCluster specifics.
- `integration-spark.md` — same webhook validation.
- `integration-leaderworkerset.md` — queue-name backfill on adoption (full failure chain to deactivation); the `||`/`&&` precedence bug in the revision guard and why narrowing it is safe.
- `integration-statefulset.md` — `wlName` resolved once; why its legacy name fallback is *not* exploitable like the pod-group one; same-name replacement deadlock pointer.
- `integration-trainjob.md` — merge patch instead of `Update`, and the unmodelled-field data-loss class.
- `integration-batchjob.md` — MultiKueue does not copy `spec.ttlSecondsAfterFinished`.
- `job-framework-interface.md` — merge-patch rule for integrations vendoring third-party CRDs; "ownership markers, not names" rule for Workload lookup.
- `local-queue.md` — stale pending accounting when a LocalQueue moves; LocalQueue identity is `namespace/name`.
- `cache-architecture.md` — cached TAS topology trees; `RequeueWorkload` owns inflight cleanup.
- `elastic-jobs.md` — `minCount` 0; ungater counts admitted pods; Alpha partial scale-up gate + `elastic-job-scale-up-strategy` annotation; MultiKueue autoscaling rejection.
- `kueuectl.md` — UID delete precondition; `list clusterqueue` chunking.
- `webhooks.md` — MAP as a new mechanism alongside webhooks; the update-rejection webhooks added in v0.19/v0.20.
- `dashboard.md` — WebSocket closed with a status; KueueViz cluster RBAC namespace omission.
- `debugging-guide.md` — four new symptom→cause entries: permanently `SchedulingGated` Pods under `Admitted=True`; Pod stuck `Terminating` / missing replacement; Workload that stays inactive after reactivation; ClusterQueue that stops admitting after a snapshot error; plus the `V(4)` priority-skip log.
- `release-process.md` — v0.18.6 / v0.19.2 paired patch releases and their contents; a consolidated "v0.20: action required" list; cherry-pick mechanics (feature-gate specs cannot be picked verbatim; manual picks on diverged `go.mod`).
- `index.md` — added `api-versions`; refreshed the sources line and date.

**Security pages** — corpus recomputed from `raw/cve/` (**682** files, up from 569): category table, severity distribution (Medium 264 / High 251 / Critical 102 / Low 24 / Unknown 38 / None 3) and per-page counts refreshed on `security.md`, `security-code-patterns.md`, `security-denial-of-service.md` (94), `security-information-disclosure.md` (137), `security-injection-and-input-validation.md` (Injection 22 / Path Traversal 11 / Code Execution 194), `security-authn-authz.md` (34/13/67/37), `security-supply-chain.md` (7, unchanged), `security-best-practices.md`. New content:

- `security.md` — "The first confirmed instance in Kueue's own code": the pod-group quota bypass ([[pr-13960]]) plus three sibling fixes with the same shape (kueuectl UID precondition, AFS namespace qualification, role-hash-derived PodSet name).
- `security-code-patterns.md` — new "Tenant-controlled identifiers as lookup keys" table pairing each ecosystem CVE with its Kueue counterpart (`CVE-2026-15228` Kong KIC ↔ pod-group name; `CVE-2026-65601` Traefik namespace confusion ↔ AFS LocalQueue identity; `CVE-2026-72640` ECK annotation confused-deputy; `CVE-2026-71208` / `CVE-2026-73263` CR-supplied endpoint SSRF ↔ MultiKueue kubeconfig; `CVE-2026-53572` KEDA connection-string injection; `CVE-2026-75889` Alloy CR-named file read; `CVE-2026-65834` regex `MustCompile` webhook panic; `CVE-2026-65835` incomplete-fix shape ↔ the #13014 gap).
- `security-authn-authz.md` — namespace confusion / confused deputy / tenant-reachable hijack-by-name write-ups, plus the over-broad operator ClusterRole entries.
- `security-denial-of-service.md` — admin-writable regex compiled with `MustCompile` inside a webhook.
- `security-injection-and-input-validation.md` — connection strings and file paths built from CR fields.

**Out of scope** (read, excluded): the very large test-infra wave in this batch (e2e stabilization, `ginkgo` restructuring, MultiKueue integration-spec splits, flake fixes, integration teardown bounding, indexer test refactors), all dependency bumps (Kubernetes group, containerd, Helm v4, Hugo, oras, vite/cypress, ray/redis/debian/distroless images, golangci-lint v2.13.2), release bookkeeping and CI/ChatOps automation, website/Hugo/Netlify and KueueViz UI-only work, OWNERS/governance, and every open or closed-unmerged PR. Notable **proposals/KEPs deliberately excluded**: `pr-13163` (KEP-10076 Quota Release Strategy — only the merged API surface from `pr-13224` is documented), `pr-14310` (KEP PartialScaleUp — only the merged Alpha gate from `pr-14909` is documented), `pr-12776` (waitForPodsReady-per-workload KEP), `pr-12645` / `pr-13028` (WIP POCs). Closed-as-not-a-bug: `issue-14846` (`validateQualifiedName` multi-slash — already fixed by the earlier `IsLabelKey` refactor) and `issue-14785` (reported Kustomize RBAC misname — reporter's own porting error).

**Open items to revisit when fixed**: `issue-14543` (FairSharing infinite preemption loop — explicitly called out in the `FairSharingReevaluatePreemptionCandidates` release note), `issue-14736` and `issue-14935` (MultiKueue: manager Workload strands after a remote `OutOfSync` / `OwnerNotFound` finish), `issue-14811` (`waitForPodsReady` recovery eviction leaves admission populated so quota is never released), `issue-14802` (client-set role-hash controls PodSet order and therefore flavor assignment), `issue-14792` (fully reclaimed elastic Workload can switch ResourceFlavor at count zero), `issue-14563` (DeviceClass change never reaches a quota-reserved Workload), `issue-14231` (equivalence hashing vs `UsageBasedAdmissionFairSharing`), `issue-14917` and `issue-14304` (TAS node-replacement bugs), `issue-14698` (controller restart overwrites `.spec.priority`).

**Coverage note**: two earlier data-collection commits — `b3ed9c2` and `f929f80` — have no corresponding entry in this log, so the wiki has a gap between `pr-11502` (the last PR of the 2026-06-29 ingest) and `pr-12645` (the first of this batch). This batch is a sparse sample of the `12645`–`14934` range; behaviour introduced by PRs in the gap is documented here only where a PR in this batch describes it.

---

## 2026-09-01 — GitHub ingest (v0.18/0.19 backports + config validation) + one CVE

**Data-collection commit**: `700ae3f74bacd01011799a9345b5c2c415c6f332` (`[data-collection] 52 new,86 updated items from kubernetes-sigs/kueue, kueue@6617ee8a5`)

**Operator**: Claude Code, standing wiki ingest workflow.

**Source files analysed** (52 files): `raw/cve/CVE-2025-15613.md`; `raw/github/kubernetes-sigs__kueue/` issues `12927`, `13414`, `13982`, `14105`, `14673`, `14936`, `14964`, `14965`, `14969`, `14973`; PRs `13571`, `14078`, `14149`, `14181`, `14442`, `14519`, `14562`, `14937`, `14938`, `14939`, `14940`, `14941`, `14942`, `14943`, `14944`, `14945`, `14946`, `14947`, `14948`, `14949`, `14950`, `14951`, `14952`, `14953`, `14954`, `14955`, `14956`, `14957`, `14958`, `14959`, `14960`, `14961`, `14962`, `14963`, `14966`, `14967`, `14968`, `14970`, `14971`, `14972`, `14974`.

A small batch dominated by cherry-picks and CI-flake retries. Only four merged changes carry behaviour (two of them backports of already-documented fixes), so most of the new depth below comes from bug reports that *describe shipped code* precisely enough to be worth recording as gotchas — each is marked as an open bug where that is the case.

**Created**

- `workload-resource-adjustment.md` — new page on `workload.AdjustResources`: where the adjustment happens (`handlePodLimitRange` consumes only LimitRange `Default`/`DefaultRequest`; `mergeResourceList`; saturating `totalRequestsFromPodSets`), the deep-copy requirement, the raw-vs-adjusted consumer table with all seven call paths (DRA vs validation vs `NewInfo`/`Info.Update`), `ValidateAdmissibility` → `ValidateLimitRange` and its `RequeueReasonGeneric`, and the two LimitRange gotchas.

**Updated**

- `cache-architecture.md` — new "Workload usage can reach the `Unlimited` sentinel" section: the `Amount` invariant is enforced on the quota boundary only, saturating `Mul`/`AddInt64` make `math.MaxInt64` reachable from a Workload's own requests, and the resulting add/sub asymmetry drifts ClusterQueue usage *below* reality (measured `MaxInt64 → 0 → -7`); plus the hierarchy-manager ordering invariant that a part-way-failed `updateClusterQueue` leaves a nil `NamespaceSelector` and panics `MatchingClusterQueues`.
- `workload-priority.md` — sweep fix backported to release-0.19/0.18; the unpaginated `List` + one-error-per-Workload signature of the old shape; the sweep does **not** filter terminal Workloads and is the only Workload-keyed writer that skips `workloadfinish.IsFinished` (with the list of writers that do check); and the MultiKueue hazard where a same-named worker-cluster `WorkloadPriorityClass` re-prices manager-owned remote Workloads.
- `multikueue.md` — manager→worker clients are built without touching `restConfig.QPS`/`Burst`, so they run at client-go's QPS 5 / Burst 10 while Kueue's own client defaults to 300/500; measured 1000-Workload burst ~15 min vs ~1.5 min with the limit raised. Pointer to the priority-overwrite hazard.
- `performance-and-scale.md` — new "Client-side rate limiting" section: `clientConnection` defaults, negative `qps` disables the limiter, MultiKueue's separate leg, and the unvalidated-zero gotcha (`burst: 0` fails every request; `qps: 0` grants the burst then blocks).
- `dra.md` — `validateQualifiedName` silently accepted names with more than one slash (`switch` covered only 1 and 2 parts); fixed by `pr-14951` (+ `pr-14953` on 0.19), with the ratcheting argument for failing fast on a Configuration field and a **correction**: `issue-14846` was logged in the previous ingest as closed-not-a-bug, and the merged fix shows the gap was real.
- `feature-gates.md` — the gate-cleanup umbrella (`issue-12927`) with a done/not-done table (`ManagedJobsNamespaceSelectorAlwaysRespected` Stable; `MultiKueueBatchJobWithManagedBy` / `HierarchicalCohorts` / `ObjectRetentionPolicies` removed; `MultiKueueKubeConfigPathValidation`, `QuotaCheckStrategy`, `WorkloadPriorityClassDefaulting` Beta; `PriorityBoost` deliberately deferred), plus when batching graduations is and is not appropriate.
- `scheduler-internals.md` — snapshot-failure requeue backported to release-0.19 (`pr-14938`) and release-0.18 (`pr-14939`); regression test relocated to `scheduler_afs_test.go`.
- `debugging-guide.md` — three new symptom→cause entries: Workload still pending after a LimitRange is raised; slow MultiKueue dispatch under a burst; ClusterQueue usage drifting below what is admitted.
- `admission.md`, `workload.md` — `ValidateAdmissibility`/LimitRange rejection listed among the reasons a Workload cannot be admitted; cross-links to the new page.
- `security-code-patterns.md`, `security-injection-and-input-validation.md` — `CVE-2025-15613` (Kyverno < 1.13.4 Service Call SSRF, CWE-918, CVSS 6.5, `PR:L`): a low-privilege `(Cluster)Policy` author points `apiCall`/`service` at an external URL and the policy context — Secrets included — is exfiltrated with the request. Rules drawn: an "in-cluster only" endpoint field must be enforced rather than documented, and object context must never ride on a request whose destination the requester chose.
- `index.md` — added `workload-resource-adjustment`.

**Out of scope** (read, excluded): the CI-flake wave that makes up most of this batch — e2e image-pull and `docker manifest inspect` retries (`pr-14940`, `pr-14941`, `pr-14946`–`pr-14948`), image-build oauth 502 retries (`pr-14942`, `pr-14949`, `pr-14950`), `GOTRACEBACK=system` for e2e (`pr-14181`), the kind-cluster-join flake `issue-14673`, and the WAS retention-test flake `pr-14974`; test-only moves (`pr-14956`, `pr-14959`, `pr-14960`); Helm chart work (`pr-14955` configurable controller-manager `affinity` — merged but no chart page exists to hold it; `pr-14957`, `pr-14961`, `pr-14962` doc-comment fixes); WAS cleanup umbrellas `issue-14936`, `issue-14969`; the `PriorityBoost`-scoping KEP `issue-13414`; `pr-14970` (KueueViz authorization KEP); and every open or closed-unmerged PR as *shipped* content — `pr-13571`, `pr-14078`, `pr-14149`, `pr-14442`, `pr-14519`, `pr-14562`, `pr-14937`, `pr-14943`, `pr-14952`, `pr-14954`, `pr-14958`, `pr-14963`, `pr-14966`–`pr-14968`, `pr-14971`, `pr-14972` — of which only `pr-13571`, `pr-14442`, `pr-14958` and `pr-14963` were mined for the *existing* behaviour they describe.

**Open items to revisit when fixed**: `issue-14105` (workload usage reaching the `Unlimited` sentinel; `pr-14519` was the closed-unmerged first attempt), `issue-14965` / `pr-14967` (LimitRange relaxation never requeues), `issue-14964` (consolidate `AdjustResources` into one effective-resource view), `issue-14973` (configurable MultiKueue QPS/Burst), `pr-14442` (validate `clientConnection` `qps`/`burst`), `#13553` / `pr-13571` (nil `NamespaceSelector` panic on cyclic cohorts), `pr-14963` (worker-cluster priority sweep touching MultiKueue remote Workloads), `pr-14952` (JobSet TTL propagation, the JobSet counterpart of the shipped batch/v1 fix), `pr-14954` (parent/variant cleanup when `ConcurrentAdmission` is disabled), `pr-14078` (stale Workload on TAS second-pass retries).

---

## 2026-09-29 — CVE wave, v0.20 configurable preemptions, TAS/DRA/elastic-job fixes

**Data-collection commit**: `7a43850b8c91f2edf7645739eea2b3b61d643e14` (`[data-collection] 983 new,155 updated items from kubernetes-sigs/kueue, kueue@e60e95121`)

**Operator**: Claude Code, standing wiki ingest, run as four parallel slices (TAS/WAS/DRA, integrations, core scheduling, CVEs).

**Source files analysed** (983 new files): 67 CVE files in `raw/cve/` (CVE-2025-71422, CVE-2025-71423, CVE-2025-71424, CVE-2025-71425, CVE-2025-71426, CVE-2026-100704, CVE-2026-100833, CVE-2026-100838, CVE-2026-100839, CVE-2026-15140, CVE-2026-19274, CVE-2026-19283, CVE-2026-19444, CVE-2026-44300, CVE-2026-44778, CVE-2026-45720, CVE-2026-45723, CVE-2026-45726, CVE-2026-47680, CVE-2026-47701, CVE-2026-50125, CVE-2026-50166, CVE-2026-52724, CVE-2026-52831, CVE-2026-53493, CVE-2026-53495, CVE-2026-53713, CVE-2026-53714, CVE-2026-53715, CVE-2026-53716, CVE-2026-53717, CVE-2026-53718, CVE-2026-53719, CVE-2026-53941, CVE-2026-54246, CVE-2026-54247, CVE-2026-55225, CVE-2026-55226, CVE-2026-55636, CVE-2026-59341, CVE-2026-61549, CVE-2026-61672, CVE-2026-61682, CVE-2026-61794, CVE-2026-61795, CVE-2026-77180, CVE-2026-78600, CVE-2026-78609, CVE-2026-79754, CVE-2026-79767, CVE-2026-80352, CVE-2026-84721, CVE-2026-85594, CVE-2026-85596, CVE-2026-85781, CVE-2026-86332, CVE-2026-86464, CVE-2026-86503, CVE-2026-86590, CVE-2026-88877, CVE-2026-91164, CVE-2026-92568, CVE-2026-92574, CVE-2026-93537, CVE-2026-93539, CVE-2026-93991, CVE-2026-94611); 230 issues in `raw/github/kubernetes-sigs__kueue/` (`issue-N`: 12763, 13149, 13237, 13243, 13277, 13356, 13359, 13363, 13396, 13501, 13502, 13534, 13602, 13625, 13746, 13911, 13966, 13969, 14004, 14204, 14229, 14230, 14255, 14393, 14409, 14478, 14541, 14574, 14591, 14596, 14608, 14609, 14615, 14994, 15057, 15062, 15136, 15221, 15340, 15380, 15399, 15401, 15422, 15424, 15431, 15450, 15455, 15458, 15463, 15500, 15504, 15507, 15537, 15544, 15547, 15552, 15563, 15564, 15566, 15570, 15572, 15613, 15614, 15618, 15621, 15625, 15629, 15630, 15631, 15636, 15637, 15638, 15650, 15658, 15669, 15674, 15681, 15685, 15691, 15692, 15702, 15705, 15709, 15722, 15730, 15731, 15732, 15733, 15735, 15740, 15742, 15746, 15747, 15752, 15753, 15756, 15757, 15765, 15766, 15767, 15769, 15771, 15777, 15782, 15784, 15785, 15786, 15787, 15788, 15789, 15790, 15791, 15812, 15817, 15835, 15838, 15843, 15846, 15873, 15874, 15880, 15883, 15890, 15891, 15892, 15893, 15895, 15896, 15898, 15911, 15920, 15921, 15932, 15934, 15936, 15937, 15947, 15948, 15950, 15953, 15957, 15958, 15965, 15968, 15969, 15975, 15978, 15979, 15981, 16007, 16008, 16010, 16013, 16018, 16021, 16025, 16026, 16027, 16029, 16030, 16038, 16043, 16045, 16048, 16049, 16052, 16058, 16068, 16073, 16075, 16083, 16092, 16095, 16109, 16112, 16115, 16116, 16118, 16119, 16120, 16131, 16141, 16142, 16143, 16147, 16155, 16159, 16160, 16172, 16176, 16185, 16203, 16205, 16207, 16210, 16211, 16212, 16213, 16214, 16215, 16226, 16227, 16232, 16233, 16234, 16238, 16239, 16245, 16265, 16266, 16272, 16274, 16275, 16276, 16283, 16285, 16291, 16295, 16297, 16301, 16302, 16304, 16305, 16310, 16322, 16330, 16331, 16333, 16337, 16338); 686 PRs (`pr-N`: 12636, 12756, 13015, 13111, 13114, 13168, 13299, 13646, 13691, 13713, 13714, 13793, 13800, 13912, 14113, 14198, 14199, 14200, 14247, 14367, 14384, 14396, 14397, 14432, 14578, 14579, 14582, 14589, 14999, 15000, 15001, 15002, 15026, 15034, 15035, 15036, 15048, 15049, 15056, 15065, 15116, 15117, 15142, 15146, 15154, 15157, 15200, 15205, 15227, 15235, 15236, 15242, 15247, 15257, 15262, 15263, 15278, 15284, 15288, 15290, 15293, 15307, 15319, 15327, 15335, 15354, 15358, 15366, 15384, 15412, 15417, 15435, 15436, 15444, 15446, 15447, 15456, 15457, 15466, 15467, 15492, 15497, 15499, 15503, 15505, 15526, 15527, 15531, 15533, 15534, 15536, 15538, 15543, 15545, 15553, 15554, 15555, 15561, 15562, 15567, 15568, 15571, 15573, 15574, 15576, 15577, 15578, 15579, 15584, 15586, 15591, 15596, 15597, 15598, 15599, 15600, 15601, 15602, 15603, 15604, 15605, 15606, 15607, 15608, 15609, 15610, 15611, 15612, 15615, 15616, 15617, 15619, 15620, 15622, 15623, 15624, 15626, 15627, 15628, 15632, 15633, 15634, 15635, 15639, 15640, 15641, 15642, 15643, 15644, 15645, 15646, 15647, 15648, 15649, 15651, 15652, 15653, 15654, 15655, 15656, 15657, 15659, 15660, 15661, 15662, 15663, 15664, 15665, 15666, 15667, 15668, 15670, 15671, 15672, 15673, 15675, 15676, 15677, 15678, 15679, 15680, 15682, 15683, 15684, 15686, 15687, 15688, 15689, 15690, 15693, 15694, 15695, 15696, 15697, 15698, 15699, 15700, 15701, 15703, 15704, 15706, 15707, 15708, 15710, 15711, 15712, 15713, 15714, 15715, 15716, 15717, 15718, 15719, 15720, 15721, 15723, 15724, 15725, 15726, 15727, 15728, 15729, 15734, 15736, 15737, 15738, 15739, 15741, 15743, 15744, 15745, 15748, 15749, 15750, 15751, 15754, 15755, 15758, 15759, 15760, 15761, 15762, 15763, 15764, 15768, 15770, 15772, 15773, 15774, 15775, 15776, 15778, 15779, 15780, 15781, 15783, 15792, 15793, 15794, 15795, 15796, 15797, 15798, 15799, 15800, 15801, 15802, 15803, 15804, 15805, 15806, 15807, 15808, 15809, 15810, 15811, 15813, 15814, 15815, 15816, 15818, 15819, 15820, 15821, 15822, 15823, 15824, 15825, 15826, 15827, 15828, 15829, 15830, 15831, 15832, 15833, 15834, 15836, 15837, 15839, 15840, 15841, 15842, 15844, 15845, 15847, 15848, 15849, 15850, 15851, 15852, 15853, 15854, 15855, 15856, 15857, 15858, 15859, 15860, 15861, 15862, 15863, 15864, 15865, 15866, 15867, 15868, 15869, 15870, 15871, 15872, 15875, 15876, 15877, 15878, 15879, 15881, 15882, 15884, 15885, 15886, 15887, 15888, 15889, 15894, 15897, 15899, 15900, 15901, 15902, 15903, 15904, 15905, 15906, 15907, 15908, 15909, 15910, 15912, 15913, 15914, 15915, 15916, 15917, 15918, 15919, 15922, 15923, 15924, 15925, 15926, 15927, 15928, 15929, 15930, 15931, 15933, 15935, 15938, 15939, 15940, 15941, 15942, 15943, 15944, 15945, 15946, 15949, 15951, 15952, 15954, 15955, 15956, 15959, 15960, 15961, 15962, 15963, 15964, 15966, 15967, 15970, 15971, 15972, 15973, 15974, 15976, 15977, 15980, 15982, 15983, 15984, 15985, 15986, 15987, 15988, 15989, 15990, 15991, 15992, 15993, 15994, 15995, 15996, 15997, 15998, 15999, 16000, 16001, 16002, 16003, 16004, 16005, 16006, 16009, 16011, 16012, 16014, 16015, 16016, 16017, 16019, 16020, 16022, 16023, 16024, 16028, 16031, 16032, 16033, 16034, 16035, 16036, 16037, 16039, 16040, 16041, 16042, 16044, 16046, 16047, 16050, 16051, 16053, 16054, 16055, 16056, 16057, 16059, 16060, 16061, 16062, 16063, 16064, 16065, 16066, 16067, 16069, 16070, 16071, 16072, 16074, 16076, 16077, 16078, 16079, 16080, 16081, 16082, 16084, 16085, 16086, 16087, 16088, 16089, 16090, 16091, 16093, 16094, 16096, 16097, 16098, 16099, 16100, 16101, 16102, 16103, 16104, 16105, 16106, 16107, 16108, 16110, 16111, 16113, 16114, 16117, 16121, 16122, 16123, 16124, 16125, 16126, 16127, 16128, 16129, 16130, 16132, 16133, 16134, 16135, 16136, 16137, 16138, 16139, 16140, 16144, 16145, 16146, 16148, 16149, 16150, 16151, 16152, 16153, 16154, 16156, 16157, 16158, 16161, 16162, 16163, 16164, 16165, 16166, 16167, 16168, 16169, 16170, 16171, 16173, 16174, 16175, 16177, 16178, 16179, 16180, 16181, 16182, 16183, 16184, 16186, 16187, 16188, 16189, 16190, 16191, 16192, 16193, 16194, 16195, 16196, 16197, 16198, 16199, 16200, 16201, 16202, 16204, 16206, 16208, 16209, 16216, 16217, 16218, 16219, 16220, 16221, 16222, 16223, 16224, 16225, 16228, 16229, 16230, 16231, 16235, 16236, 16237, 16240, 16241, 16242, 16243, 16244, 16246, 16247, 16248, 16249, 16250, 16251, 16252, 16253, 16254, 16255, 16256, 16257, 16258, 16259, 16260, 16261, 16262, 16263, 16264, 16267, 16268, 16269, 16270, 16271, 16273, 16277, 16278, 16279, 16280, 16281, 16282, 16284, 16286, 16287, 16288, 16289, 16290, 16292, 16293, 16294, 16296, 16298, 16299, 16300, 16303, 16306, 16307, 16308, 16309, 16311, 16312, 16313, 16314, 16315, 16316, 16317, 16318, 16319, 16320, 16321, 16323, 16324, 16325, 16326, 16327, 16328, 16329, 16332, 16334, 16335, 16336, 16339). Most PRs were triaged by title/labels; about 300 merged PRs and about 60 issues were read closely, the rest are cherry-picks, CI/test/dependency/KEP/open items (cited only as backports or known gaps). The slices also cross-checked claims against `raw/kueue/` source.

**Created**
- `configurable-preemptions.md` — PreemptionConfig API, triggers, evaluator, candidate filters, eviction reasons, RBAC (Alpha).
- `dynamic-quota-orchestration.md` — DQO / CapacityProvider (Alpha).
- `wait-for-pods-ready.md` — config, defaults, per-workload override, unscheduled timeout, succeeded pods ready.
- `unadmitted-workloads-observability.md` — tiered `QuotaReserved` reasons, gauges, gate stages.

**Updated**
- TAS/DRA: `topology-aware-scheduling.md` (gate table, spreading, partial slices, leader/worker groups, elastic-slice fixes, simulator/Planner), `dra.md` (per-node device feasibility, taints, charge fixes; gate-stage corrections).
- Integrations: `elastic-jobs`, `integration-plain-pod`, `-statefulset`, `-leaderworkerset`, `-rayjob`, `-spark`, `-trainjob`, `-batchjob`, `-kubeflow`, `-jobset`, `job-framework-interface`, `integrations`, `workload-priority`, `local-queue-defaulting`, `provisioning-request`, `kueuectl`, `dashboard`, `importer` — partial scale-up model, group finalization, TAS validation, Ray/Spark fixes, `RestorePodSetsInfo` context, namespace-selector-aware priority defaulting, kueuectl fixes.
- Core: `preemption`, `fair-sharing`, `admission-fair-sharing`, `concurrent-admission`, `multikueue`, `multikueue-orchestrated-preemption`, `cluster-queue`, `admission`, `workload`, `webhooks`, `borrowing-and-lending`, `api-versions`, `scheduler-internals`, `metrics`, `debugging-guide`, `performance-and-scale`, `failure-recovery`, `preemption-cost`, `feature-gates`, `cache-architecture`, `workload-resource-adjustment`, `resource-transformer`. Corrections: exact quota amounts (no `Unlimited` sentinel), `Info.EffectivePodSpecs` replaces `AdjustResources`, transformation-vs-`excludeResourcePrefixes` ordering, feature-gate stage table.
- Security: `security`, `security-code-patterns`, `-injection-and-input-validation`, `-authn-authz`, `-denial-of-service`, `-information-disclosure`, `-supply-chain`, `-best-practices` — 67 non-Kueue CVEs distilled into guard-coverage / derived-identity / SSRF / operator-trusts-CR-author rules.
- `gang-scheduling.md`, `index.md` — link to and list the new pages.

**Contradictions flagged**: `dra.md` Alpha banner vs Beta gates in code; `TASHandleOverlappingFlavors` / `TASPartialSlices` stage (PR text says Alpha, code says Beta); LimitRange-requeue gotcha appears fixed in code while issue-14965 / pr-14967 still show open; `MaxExecTime` and `KubeRayAccountForRedisCleanup` missing from generated gate list (marked needs verification).

**Open items**: some PR numbers cited in integration pages (14703, 15056, 13375, 13025, 7663, 15565) come from other PR descriptions and were not checked against raw files; `pr-16089` diff not verified.
