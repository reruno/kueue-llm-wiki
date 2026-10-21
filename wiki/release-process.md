# Release process

**Summary**: Kueue cuts a minor release roughly every eight weeks (recent minors: v0.18, v0.19, v0.20) and keeps patching the two previous minors. Patch releases pick fixes into release branches. Release artifacts include container images, a signed manifest bundle, and Helm charts; SLSA attestations are generated for releases.

**Sources**: `raw/github/kubernetes-sigs__kueue/`; pr-14150.md, pr-16442.md, pr-16917.md, pr-16916.md, pr-16440.md, pr-16439.md, pr-16456.md, pr-16476.md, pr-16502.md, pr-16505.md, pr-16690.md, pr-16711.md, pr-16714.md, pr-16850.md; `raw/kueue/RELEASE.md`, `raw/kueue/release-timelines/`, `raw/kueue/.github/ISSUE_TEMPLATE/NEW_RELEASE.md`, `raw/kueue/CHANGELOG/CHANGELOG-0.20.md`, `CHANGELOG-0.19.md`, `CHANGELOG-0.18.md`.

**Last updated**: 2026-10-21

---

## Release cycle and milestones

From `RELEASE.md` as restructured by pr-14150.md (merged 2026-08-11, fixes #14147):

- One minor release about **every two months**, so every second Kueue minor lines up with a Kubernetes minor. The "aligned" Kueue minor ships about a month after the Kubernetes release, once its first patch release exists. A release may slip (the aim is no more than two weeks), and a slip does not move the next minor's target date.
- Each minor normally uses an **eight-week cycle**, with the public release planned for the middle of W8:

| Milestone | Timing | Meaning |
|---|---|---|
| D1 Planning opens | W1–W2 | Scope discussed at WG Batch, a planning meeting, or asynchronously in the issue |
| D2 Larger KEP review | W1–W4 | Larger KEPs should become visible early |
| D3 Scope cooldown | W5 | Maintainers fix the scope in terms of larger KEPs; small KEPs/KEP updates stay eligible until D4 |
| D4 KEP publication | W6 | Accepted KEPs published |
| C1 Code cooldown | W6 | All big feature PRs open, substantially complete and reviewable |
| C2 Code freeze | W7 | Feature PRs merged or deferred; only bug fixes or approved exceptions |
| R Public release | W8 | Release published |

- **Exceptions** are agreed between maintainers and the feature owner in a dedicated Slack group, and the decision is recorded in the feature tracking issue. Maintainers decide scope (based on their review capacity), approve feature PRs and exceptions, and may update the tentative schedule. The release team runs the publication.
- **Tentative timelines** live in `release-timelines/`: v0.20 had scope finalization on 4 Sep, code freeze on 17 Sep and release on 24 Sep (2026); v0.21 has scope on 5 Nov, freeze on 19 Nov and release on 25 Nov; v0.22 treats W3–W4 (late December) as a holiday window, with scope on 8 Jan, freeze on 21 Jan and release on 28 Jan. v0.20.0 was prepared on 2026-09-30, about a week after its tentative date (source: pr-16442.md).
- **Patch releases**: while working on minor N, the project keeps maintaining N-1 and N-2. Their release branches are tested by CI.

## Branching

Each minor version has a `release-0.X` branch. `main` is the trunk for the next minor. Patch releases go out from the release branch.

Representative release tracking issues:

- v0.4.1 ([[issue-1056]]), v0.4.2 ([[issue-1200]]).
- v0.5.0 ([[issue-1256]]), v0.5.1 ([[issue-1368]]), v0.5.2 ([[issue-1539]]).
- v0.15.8 ([[issue-10054]]), v0.16.5 ([[issue-10053]]), v0.16.6 ([[issue-10476]]), v0.17.1 ([[issue-10477]]).
- v0.16.7 ([[issue-10706]]), v0.17.2 ([[issue-10705]]) — paired patch releases on 2026-04-30 carrying CQ-finalizer fix ([[pr-10821]]), TAS stateWithLeader / NodeHotSwap fixes, FailureRecovery terminal-pod handling ([[pr-10853]]), and Helm/KueueViz fixes (#10977 / #10978 / #10979).
- v0.16.9 ([[issue-11360]]), v0.17.4 ([[issue-11359]]) — paired patch releases carrying the MultiKueue connection-health fixes (per-cluster reconcile lock [[pr-11332]]/[[pr-11333]]; exponential watch-establish timeout [[pr-11328]]/[[pr-11329]]), the MultiKueue AllAtOnce eviction-race fixes ([[pr-11472]]/[[pr-11473]] and [[pr-11507]]/[[pr-11508]]), the TAS multi-PodSet pod-count fix ([[pr-11326]]/[[pr-11331]]), the finished-Workload GC finalizer fix ([[pr-11307]]/[[pr-11308]]), and the scheduler `preemptionExpectations` race fix ([[pr-11648]]/[[pr-11647]]).
- v0.18 plan ([[issue-10261]] — "☂️ Release 0.18 plan" umbrella issue); v0.18.0 release tracking ([[issue-10861]]).

## v0.18.0 highlights (released 2026-05; RC1 on 2026-05-06)

From the changelog in [[issue-10861]]:

**Action required before upgrading**:

- Alpha `RejectUpdatesToCQWithInvalidOnFlavors` feature gate (off by default). When enabling it, fix any invalid `AdmissionCheckStrategy.OnFlavors` references first (#10384).
- The `evicted_workloads_once_total` metric's `detailed_reason` label was renamed to `underlying_cause` for consistency. Migrate dashboards and alerts.

**New features**:

- `quotaCheckStrategy` configuration for [[cluster-queue]] (#9808) — new `IgnoreUndeclared` mode admits Workloads that ask for resources the CQ does not list.
- Concurrent Admission introduced as an Alpha feature (#10610) — see [[concurrent-admission]].
- LWS `nodeSelector` mutability while running (#10275); `queue-name` mutable on idle LWS (#4932) — see [[integration-leaderworkerset]].
- `workload_eviction_latency_seconds` metric (#10323) — see [[metrics]].
- Improved Retry-state AdmissionCheck eviction message (#10623).
- Aggregate Kueue read-only ClusterRoles into the `view` ClusterRole (#10482).
- Stable graduations: `MultiKueueRedoAdmissionOnEvictionInWorker` (#10695), `MultiKueueWaitForWorkloadAdmitted` (#10656), `SkipFinalizersForPodsSuspendedByParent` (#10645).

**Notable bug fixes** (selected — see [[feature-gates]], [[topology-aware-scheduling]], [[fair-sharing]], [[multikueue]] for details):

- FailureRecovery: force-delete Failed/Succeeded pods on unreachable nodes ([[pr-10853]]).
- FairSharing nil-pointer panic on cohort-less CQs ([[pr-10891]]).
- CQ finalizer race after admission failure ([[pr-10821]]).
- TAS `stateWithLeader` over-estimation (#10783, cherry-pick [[pr-10841]]); empty `count=0` PodSets infinite loop (#10478); NodeHotSwap "late pods" pollution (#10760).
- Cohort subtree-quota refresh on cohort deletion ([[pr-10797]]).
- Cohort CPU metrics in CPU units (not milli) ([[pr-10747]]).
- MultiKueue: workload after eviction-on-worker incorrectly marked Admitted (#9670); deferred dispatch when other AdmissionChecks pending (#9866).
- TrainJob webhook no longer patches the TrainingRuntime ([[pr-10829]]).
- Multi-arch image builds for importer/populator/kueueviz-backend (#10775).
- Helm probe periodSeconds bug (#10978); FlowSchema fullname template (#10979); KueueViz plural workloadpriorityclasses (#10977).
- `FinishOrphanedWorkloads` downgraded to Alpha to fix the "Workloads marked Finished immediately after creation" regression ([[pr-11010]], [[issue-10901]]); requeue guard added ([[pr-11014]]).

## Release automation

### The release issue checklist (ChatOps)

A release is tracked by an issue opened from the **New Release** template (`.github/ISSUE_TEMPLATE/NEW_RELEASE.md`). The steps run as ChatOps commands on that issue: `/sync-release-notes`, optional `/create-release-candidate` (minor/major), `/create-release-branch`, `/tag-release`, `/create-draft-release` (changelog, artifacts, OpenVEX, SBOM), `/wait-for-images`, `/wait-for-prod-images`, `/publish-release`, `/update-krew-index`, `/merge-main-into-website`, `/create-devel-tag` and `/create-milestone`. Local scripts remain for PRs that need a personal fork: `prepare_pull.sh --target release|main`, `promote_pull.sh`, `milestone_pull.sh`, `ci_pull.sh`. OWNERS must LGTM the release proposal: at least two for a minor or major release, one for a patch.

Changes in this window:

- `/update-krew-index` submits the krew plugin release for the latest published release (source: pr-16476.md, fixes #16475).
- `/create-milestone` creates the next minor's milestone after a major or minor release. It skips milestones that already exist and rejects patch versions (source: pr-16502.md). `milestone_pull.sh` therefore no longer creates the milestone by default: release managers run it from forks without upstream write access, which returned 404. Set `CREATE_MILESTONE` to opt in; `SKIP_MILESTONE` was removed (source: pr-16714.md, fixes #16454).
- A successful ChatOps command ticks its own checklist item, matched by a `<!-- step:<command> -->` marker. Only the `Report Success` steps pass `mark-done`, so a failed command leaves its item unchecked (source: pr-16711.md, fixes #13359).
- The release-tag action distinguishes "no release" from a lookup error (one GraphQL query for published and draft releases) and stops on errors. It builds the replacement annotated tag locally and updates the remote with `--force-with-lease` instead of deleting the remote tag first. Before, a failure in between could leave a draft release without its tag (source: pr-16690.md, fixes #13501).
- Members of `kueue-approvers` (not only `release-team`) may use `/set-release-note` (source: pr-16505.md, fixes #16131). Gotcha: `/set-release-note` takes **everything after it** in the comment as the note, so put other Prow commands in a separate comment (source: pr-16850.md).

### Versioned docs

The site at kueue.sigs.k8s.io publishes from the `website` branch, which tracks `main`. Docs are versioned **by path in one deploy**: development docs are under `site/content/<locale>/docs` (`/docs/`), and each release is a frozen copy under `site/content/<locale>/v0.X/docs` (`/v0.X/docs/`), chosen from a header dropdown. The dropdown keeps `main` plus the current and previous release. The `main`-update PR from `prepare_pull.sh` runs `hack/releasing/snapshot-docs.py`. It copies each locale's docs from the release branch, rewrites `/docs/` links, prunes old snapshots and prepends a `[[params.versions]]` entry in `site/hugo.toml`. Patch releases re-freeze the existing snapshot (source: `raw/kueue/RELEASE.md`, `NEW_RELEASE.md`; updated by pr-16456.md).

### Older automation notes

- **Cherry-pick automation** lifts fixes from main to release branches; "Cherry-picker should copy release notes" ([[issue-1715]]) addressed the release-note-propagation gap.
- **Promotion PR automation** was hardened to always rebase onto latest main ([[issue-10535]] — ensure the promotion PR is created on top of the latest main branch).
- **SLSA attestations** are generated for release artifacts ([[issue-1466]]).
- **Signing** — release artifacts are signed; an early gap was "Release artifacts are not signed" ([[issue-1477]]).
- **OLM listing** — images are packaged for OperatorHub ([[issue-1101]]).
- **Helm chart sync** — webhook configs auto-sync to helm ([[issue-1461]]).

## Kubernetes version support

Kueue supports a rolling window of Kubernetes minor versions (typically the current and previous two). `manager` tests run against multiple kind versions. Kubernetes 1.30 changed scheduling-gate behavior and Kueue had to track ([[issue-2029]]).

## Dependency management

Kueue depends on `cluster-autoscaler/apis` for the ProvisioningRequest types; historically these were sometimes pinned to unreleased commits ([[issue-1194]], [[issue-1896]] — use a released cluster-autoscaler/apis module). Similar for KubeRay ([[issue-1634]]).

## v0.18.6 and v0.19.2 (paired patch releases, 2026-08)

Prepared by [[pr-14685]] ([[issue-14322]]) and [[pr-14686]] ([[issue-14323]]); `main` and the website were re-synced by [[pr-14690]], [[pr-14691]], [[pr-14692]], [[pr-14696]]. Headline content carried by these two branches in this window:

- the pod-group foreign-Workload adoption fix ([[pr-14617]], [[pr-14630]]) — see [[integration-plain-pod]];
- the reserved `pods` resource-name refusal plus its `ReservedResourceNameValidation` escape-hatch gate ([[pr-14756]], [[pr-14758]], [[pr-14773]], [[pr-14774]]) — see [[dra]];
- TAS elastic leader-assignment preservation ([[pr-14064]], [[pr-14076]]) and the `TASCacheTopologyTree` gate at Alpha/off ([[pr-14639]], [[pr-14644]]);
- MultiKueue `nominatedClusterNames` MAP clearing ([[pr-14643]], [[pr-14659]]) and AdmissionCheck `observedGeneration` refresh ([[pr-14914]], [[pr-14915]], [[pr-14933]], [[pr-14934]]);
- observability fixes on `kueue_pod_scheduling_gate_removal_seconds` ([[pr-14731]], [[pr-14530]]) and the metrics overflow / `+Inf` fix ([[pr-14050]]);
- LeaderWorkerSet queue-name backfill ([[pr-14602]], [[pr-14603]]) and the revision-guard precedence fix ([[pr-14892]], [[pr-14893]]);
- `kueuectl` UID-precondition delete ([[pr-14882]], [[pr-14883]]) and clusterqueue list chunking ([[pr-14880]], [[pr-14881]]).

Follow-on patch releases v0.18.7 ([[issue-14694]]) and v0.19.3 ([[issue-14693]]) followed. The most recent patch releases at this snapshot are listed below.

## Releases in this window

Dates are when the release-prep PR merged into the release branch.

| Release | Prepared | Prep PR | Headline changes |
|---|---|---|---|
| **v0.20.0** | 2026-09-30 | pr-16442.md | New minor; `v1beta1` no longer served; see the action-required list below |
| **v0.19.7** | 2026-09-30 | pr-16440.md | `HighMaxParallelismWithinReconcile` (8 → 32 concurrent API updates per reconcile); AFS fair-sharing vs priority order fix; Cohort-cycle hang fix (`CohortCycleDetected`); LWS/StatefulSet rolling-update ungating without quota fixed; `kueue_cohort_subtree_admitted_active_workloads` after hierarchy changes; Admitted events reporting 0s; TAS requeue only for CQs using the changed flavor; KueueViz empty Workloads page crash; `kueuectl list pods --for pod/NAME` fixes; fair-sharing preemption up to 20% faster |
| **v0.18.11** | 2026-09-30 | pr-16439.md | Same set as v0.19.7 backported to 0.18, plus the ConcurrentAdmission panic on Workload names without `-` |
| **v0.20.1** | 2026-10-08 | pr-16917.md | FairSharing weighted-share overflow / zero-weight / huge-weight fixes and `kueue_cohort_weighted_share` NaN; int64-overflow admission fixes; pending-workload metric refresh on LocalQueue/ClusterQueue lifecycle; `kueue_replaced_workload_slices_total` exposed; TAS second-pass and elastic PodSet-group fixes; Workloads no longer inherit Kueue-internal labels via `labelKeysToCopy`; new Alpha `KubeRayServiceUsingTopLevelSuspend`; `MultiKueueRayInTreeAutoscaling` now requires `SkipChildJobSuspension`; kueuectl `create clusterqueue` ordering and `delete workload` propagation fixes; KueueViz detail-page fixes |
| **v0.19.8** | 2026-10-08 | pr-16916.md | Mostly the same fixes as v0.20.1; also adds the Alpha `SkipChildJobSuspension` gate (off by default) to 0.19 |

(source: CHANGELOG-0.20.md, CHANGELOG-0.19.md, CHANGELOG-0.18.md at kueue@8922c563e). Each patch changelog starts with an "Actions Required Before Upgrading" section telling users to read the `.0` notes of every minor they cross and the earlier patch notes of their own minor line.

## v0.20: action required

- **`v1beta1` is no longer served.** Run `hack/migrate-to-v1beta2.sh` before upgrading. See [[api-versions]] ([[pr-14558]]).
- **`TASRecomputeAssignmentWithinSchedulingCycle` now requires `TopologyAwareScheduling`.** If TAS is disabled, set the gate to `false` before upgrading ([[pr-14256]]).
- **A Configuration that names `pods`** as a DRA `deviceClassMappings[].name` or in a resource transformation will now stop the manager at startup (`os.Exit`). Rename it, or set `ReservedResourceNameValidation=false` for one release ([[pr-13989]], [[pr-14778]]). Renaming an `outputs` key also requires updating the matching ClusterQueue resource name.
- **`kueue_pod_scheduling_gate_removal_seconds` gained a `replica_role` label**, changing that metric's series identity ([[pr-14488]]).
- **`RejectUpdatesToCQWithInvalidOnFlavors` is Beta/on** — fix invalid `AdmissionCheckStrategy.OnFlavors` references first ([[pr-14776]]).

Further action-required items from the v0.20.0 changelog (source: CHANGELOG-0.20.md):

- **AFS:** `AdmissionFairSharingAnchorAtQuotaReservation` is Beta/on (LocalQueue usage counts from quota reservation). If you explicitly disable `AdmissionFairSharing`, disable this gate too, or startup validation rejects the configuration. Remove it from the configuration before rolling back to a release that does not know it (#15000).
- **KueueViz:** with authentication enabled, every request is checked with a SubjectAccessReview. Users need get/list/watch; custom RBAC must let the backend SA create `subjectaccessreviews` (#13810; see [[dashboard]]).
- **LeaderWorkerSet:** `spec.leaderWorkerTemplate.size` is immutable while Kueue manages the LWS (gate `LWSImmutableGroupSize`), which closes a quota bypass. Recreate the LWS to resize (#13279).
- **Observability:** an invalid `metrics.localQueueMetrics.localQueueSelector` is rejected at startup; before, it silently exposed all LocalQueues (#16379).
- **RayService:** `RayServiceValidateUpgradeStrategy` is Beta/on. Zero-downtime upgrades need `ElasticJobsViaWorkloadSlices` plus the `kueue.x-k8s.io/elastic-job: "true"` annotation, or `spec.upgradeStrategy.type: None` (#16094).
- **SparkApplication:** Workloads now reserve `cores` as CPU and Spark's memory overhead (at least 384Mi per Pod). Raise quotas if needed (#15833).
- **TAS:** slice sizes must be positive, and `podSetSliceRequiredTopology` and `podSetSliceSize` must be set together (#12728).
- **TrainJob:** Trainer v2.3 is required; v2.2 is API-incompatible (#14504).
- **Custom integrations:** `ComposableJob.Load` now returns `(*jobframework.LoadResult, error)`; use `jobframework.NewLoadResult(shouldFinalize, found)` (#12849).

## Cherry-pick mechanics worth knowing

Feature-gate specs generally **cannot** be cherry-picked verbatim. Kueue never sets an emulation version, so the effective version is Kubernetes' `DefaultKubeBinaryVersion`; `featureSpecAtEmulationAndMinCompatVersion` therefore still selects a spec written as `{0.20, Default: true, Beta}` on a release-0.19 build, silently enabling the gate there. A backport that must stay opt-in has to rewrite the spec as `{0.19, Default: false, Alpha}`, and gate *dependencies* move from `main`'s `defaultFeatureGateDependencies` map to the branch's `validateFeatureGateDependency` in `pkg/config/validation.go`. ([[pr-14804]])

**Go language version on release branches.** `release-0.19` pins `-lang=go1.26` in `go.mod`. Test code on `main` that uses promoted fields in composite literals (for example `&kueue.WorkloadList{Continue: "page2"}` or `&batchv1.Job{Name: ..., UID: ...}`, described in review as a Go 1.27+ language feature) does not compile there. The manual cherry-pick must spell out the embedded struct: `ListMeta: metav1.ListMeta{Continue: ...}`, `ObjectMeta: metav1.ObjectMeta{...}` (source: pr-16850.md, which hit this on its release-0.19 pick).

A manual cherry-pick is also required whenever the bot's automated pick fails on a diverged `go.mod` — see [[pr-14531]] for a worked example (dependency resolution to the branch's own versions, plus test-fixture adaptation to the branch's older internal API).

## Related pages

- [[feature-gates]] — graduation happens alongside releases.
- [[performance-and-scale]] — scale fixes land via patch releases.
