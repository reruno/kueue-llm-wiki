# Release process

**Summary**: Kueue cuts minor releases on a regular cadence; recent minors are v0.14, v0.15, v0.16, v0.17, v0.18. Patch releases pick fixes into release branches. Release artifacts include container images, a signed manifest bundle, and Helm charts; SLSA attestations are generated for releases.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-05-08

---

## Branching

Each minor version has a `release-0.X` branch. `main` is the trunk for the next minor. Patch releases go out from the release branch.

Representative release tracking issues:

- v0.4.1 ([[issue-1056]]), v0.4.2 ([[issue-1200]]).
- v0.5.0 ([[issue-1256]]), v0.5.1 ([[issue-1368]]), v0.5.2 ([[issue-1539]]).
- v0.15.8 ([[issue-10054]]), v0.16.5 ([[issue-10053]]), v0.16.6 ([[issue-10476]]), v0.17.1 ([[issue-10477]]).
- v0.16.7 ([[issue-10706]]), v0.17.2 ([[issue-10705]]) — paired patch releases on 2026-04-30 carrying CQ-finalizer fix ([[pr-10821]]), TAS stateWithLeader / NodeHotSwap fixes, FailureRecovery terminal-pod handling ([[pr-10853]]), and Helm/KueueViz fixes (#10977 / #10978 / #10979).
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

## Related pages

- [[feature-gates]] — graduation happens alongside releases.
- [[performance-and-scale]] — scale fixes land via patch releases.
