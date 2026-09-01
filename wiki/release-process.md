# Release process

**Summary**: Kueue cuts minor releases on a regular cadence; recent minors are v0.14, v0.15, v0.16, v0.17, v0.18. Patch releases pick fixes into release branches. Release artifacts include container images, a signed manifest bundle, and Helm charts; SLSA attestations are generated for releases.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-09-01

---

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

Follow-on patch releases v0.18.7 ([[issue-14694]]) and v0.19.3 ([[issue-14693]]) were open at the time of this ingest.

## v0.20: action required

- **`v1beta1` is no longer served.** Run `hack/migrate-to-v1beta2.sh` before upgrading. See [[api-versions]] ([[pr-14558]]).
- **`TASRecomputeAssignmentWithinSchedulingCycle` now requires `TopologyAwareScheduling`.** If TAS is disabled, set the gate to `false` before upgrading ([[pr-14256]]).
- **A Configuration that names `pods`** as a DRA `deviceClassMappings[].name` or in a resource transformation will now stop the manager at startup (`os.Exit`). Rename it, or set `ReservedResourceNameValidation=false` for one release ([[pr-13989]], [[pr-14778]]). Renaming an `outputs` key also requires updating the matching ClusterQueue resource name.
- **`kueue_pod_scheduling_gate_removal_seconds` gained a `replica_role` label**, changing that metric's series identity ([[pr-14488]]).
- **`RejectUpdatesToCQWithInvalidOnFlavors` is Beta/on** — fix invalid `AdmissionCheckStrategy.OnFlavors` references first ([[pr-14776]]).

## Cherry-pick mechanics worth knowing

Feature-gate specs generally **cannot** be cherry-picked verbatim. Kueue never sets an emulation version, so the effective version is Kubernetes' `DefaultKubeBinaryVersion`; `featureSpecAtEmulationAndMinCompatVersion` therefore still selects a spec written as `{0.20, Default: true, Beta}` on a release-0.19 build, silently enabling the gate there. A backport that must stay opt-in has to rewrite the spec as `{0.19, Default: false, Alpha}`, and gate *dependencies* move from `main`'s `defaultFeatureGateDependencies` map to the branch's `validateFeatureGateDependency` in `pkg/config/validation.go`. ([[pr-14804]])

A manual cherry-pick is also required whenever the bot's automated pick fails on a diverged `go.mod` — see [[pr-14531]] for a worked example (dependency resolution to the branch's own versions, plus test-fixture adaptation to the branch's older internal API).

## Related pages

- [[feature-gates]] — graduation happens alongside releases.
- [[performance-and-scale]] — scale fixes land via patch releases.
