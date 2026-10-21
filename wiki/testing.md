# Testing

**Summary**: How to run, focus, and debug Kueue's three test tiers (unit, integration, e2e) on a local dev machine, which make targets and env vars each tier honors, how CI exercises them, and where to look when a test goes flaky. Entry point for the developer-workflow section.

**Sources**: `raw/kueue/hack/make/test.mk`, `raw/kueue/hack/testing/`, `raw/kueue/site/content/en/docs/contribution_guidelines/testing.md`, `raw/kueue/test/util/constants.go`; `raw/github/kubernetes-sigs__kueue/` — [[issue-9952]], [[issue-9954]], [[issue-3044]], [[issue-6525]], [[issue-10200]], [[pr-2415]], [[pr-5414]], [[pr-6906]]; pr-16723.md, pr-16481.md, pr-16781.md, pr-16791.md, pr-16823.md, pr-16996.md, pr-16923.md; 2026-10-21 batch: pr-17136.md, pr-17163.md, pr-17206.md, pr-17391.md, pr-17283.md, pr-17304.md, pr-17352.md, pr-17431.md, pr-17477.md, pr-17487.md, pr-17377.md, pr-17148.md, `raw/kueue/hack/make/verify.mk`, `raw/kueue/hack/make-failure-summary.sh`; `raw/kueue/site/content/en/community/contribution_guidelines/writing_tests.md`.

**Last updated**: 2026-10-21

---

## The test pyramid

Kueue has three tiers. Each tier's make targets live in `hack/make/test.mk`. **Correction (2026-10-21)**: the Makefile system was refactored (#14127). The test targets now live in `hack/make/test.mk`, and verify targets in `hack/make/verify.mk`, both included from the top-level `Makefile`. References to `hack/make/test.mk` on this page mean `hack/make/test.mk` (verified against `raw/kueue` at kueue@8922c563e).

| Tier | What it exercises | Runtime | Where |
|---|---|---|---|
| **Unit** | Pure Go packages. No API server. `-race` by default. | Seconds | `make test`, `go test ./pkg/...` |
| **Integration** | Controllers + webhooks against a controller-runtime `envtest` (etcd + kube-apiserver binaries, no kubelet, no kube-scheduler). Ginkgo suites. | Minutes | `make test-integration`, `make test-multikueue-integration` |
| **E2E** | A real (Kind-based) cluster with Kueue installed, plus whichever external operators the suite needs (JobSet, KubeRay, Kubeflow Training, LeaderWorkerSet, AppWrapper, cert-manager, Prometheus Operator). | Tens of minutes per suite. MultiKueue e2e was ~19 min sequential / 22 min parallel at the time it was last measured ([[issue-10200]]). | `make test-e2e`, `make test-multikueue-e2e-main`, `make test-tas-e2e`, others below |

Three companion pages go deep on the heavier tiers:

- [[testing-integration]] — envtest suites, writing integration tests, label filters, flake patterns.
- [[testing-e2e]] — Kind lifecycle, `E2E_MODE=dev`, the full MultiKueue invocation recipe, per-suite matrix.
- [[testing-performance]] — scheduler perf benchmarks and related CI jobs.

## Prerequisites

For unit + integration:

- Go toolchain matching `go.mod`.
- `make envtest` pulls the kubebuilder assets; integration targets set `KUBEBUILDER_ASSETS` automatically via `ENVTEST_K8S_VERSION` (default `1.35`, set in `hack/make/test.mk`).

For e2e (any suite):

- Docker (Kind needs it).
- Kind — `make kind` fetches the pinned version.
- `kubectl`, `kustomize`, `yq`, `helm`, `ginkgo` — all vendored into `./bin/` by `make setup-e2e-env`, so you do not need global installs.
- For `E2E_USE_HELM=true` flow, Helm is used to install Kueue instead of kustomize-rendered manifests.

## Build loop

Two image-build targets, for different purposes ([[pr-5414]]):

- `make kind-image-build` — native-arch image, loaded into the Kind cluster. This is the one you want for local e2e iteration.
- `make image-build` — multi-arch build via Docker Buildx. Parameterized by `PLATFORMS` (e.g. `PLATFORMS=linux/s390x,linux/ppc64le`). Used by release pipelines, not by local dev loops.

The standard local dev loop is:

```shell
make kind-image-build          # (re)build the controller image for Kind
E2E_MODE=dev make test-e2e     # create-or-reuse the cluster, run e2e, keep cluster running
```

See [[testing-e2e]] for the full dev-mode flow including `E2E_SKIP_REINSTALL`, `E2E_SKIP_IMAGE_RELOAD`, and `E2E_ENFORCE_OPERATOR_UPDATE`.

## Running each tier

### Unit

```shell
make test                                         # all unit tests, -race, gotestsum + coverage
GO_TEST_TARGET=./pkg/scheduler make test          # restrict to one package tree
go test ./pkg/webhooks                            # single package, no gotestsum
go test ./pkg/webhooks -run TestValidateClusterQueue   # regex on test name
go test ./pkg/scheduler/preemption/ -race         # explicit race detector
```

`make test` excludes `./test/` and writes a coverage profile to `$ARTIFACTS/cover.out` (`hack/make/test.mk`).

### Integration

```shell
make test-integration                 # full singlecluster suite
make test-multikueue-integration      # multikueue integration suite
make test-integration-baseline        # --label-filter="!slow && !redundant"
make test-integration-extended        # --label-filter="slow || redundant"
```

Knobs (all read by `hack/make/test.mk`):

- `INTEGRATION_NPROCS` (default `4`) — parallel specs within a suite. Suites still run sequentially.
- `INTEGRATION_NPROCS_MULTIKUEUE` (default `3`).
- `INTEGRATION_TARGET` (default `./test/integration/singlecluster/...`) — narrow to a directory.
- `INTEGRATION_FILTERS` — Ginkgo `--label-filter` expression.
- `INTEGRATION_API_LOG_LEVEL` — apiserver log verbosity (`0` = off).

See [[testing-integration]] for the full label taxonomy and Ginkgo conventions.

### E2E

The common targets, all backed by `hack/testing/e2e-test.sh` or `hack/testing/e2e-multikueue-test.sh`:

```shell
make kind-image-build          # (once per code change)

make test-e2e                  # singlecluster
make test-multikueue-e2e-main  # manager + worker Kind clusters
make test-tas-e2e              # topology-aware scheduling
make test-e2e-certmanager      # cert-manager-backed webhooks
make test-e2e-sequential-baseline    # customconfigs baseline
make test-e2e-sequential-extended    # customconfigs extended
make test-e2e-upgrade          # version-skew upgrade
make test-e2e-dra              # DynamicResourceAllocation path
make test-e2e-kueueviz         # KueueViz dashboard ([[dashboard]])
```

Add `-helm` to install via Helm instead of kustomize (e.g. `make test-e2e-helm`, `make test-tas-e2e-helm`, `make test-multikueue-e2e-helm`), or set `E2E_USE_HELM=true`.

Per-suite folder layout under `test/e2e/`: `singlecluster`, `multikueue`, `multikueuesequential`, `multikueuedra`, `tas`, `dra`, `certmanager`, `sequential/{baseline,extended}`, `upgrade`, `kueueviz`. See [[testing-e2e]] for what each covers.

Knobs most contributors touch:

- `E2E_MODE=dev` — keep Kind cluster across runs (see [[testing-e2e]]).
- `E2E_K8S_VERSION` (default `1.35`) — picks the Kind node image. Valid values live in `E2E_K8S_VERSIONS` (currently `1.33.7 1.34.3 1.35.0` in `hack/make/test.mk`).
- `KIND_CLUSTER_NAME` (default `kind`) — set this if you do not want the suite's teardown to delete your personal default cluster.
- `IMAGE_TAG` — point at a released or staging image to skip `kind-image-build` entirely, e.g. `IMAGE_TAG=registry.k8s.io/kueue/kueue:v0.16.0`.
- `GINKGO_ARGS` — passed through to Ginkgo.

## Running a subset of tests

Four mechanisms, in order of preference.

### 1. Label filter

Preferred when the suite defines labels. Integration uses `INTEGRATION_FILTERS`; e2e uses `GINKGO_ARGS`.

```shell
# integration
INTEGRATION_FILTERS="--label-filter=controller:localqueue" make test-integration
INTEGRATION_FILTERS="--label-filter=area:core && !slow" make test-integration
INTEGRATION_FILTERS="--label-filter=feature:tas" make test-integration

# e2e singlecluster
GINKGO_ARGS="--label-filter=feature:appwrapper" make test-e2e
GINKGO_ARGS="--label-filter=feature:jobset,feature:trainjob" make test-e2e

# e2e customconfigs
GINKGO_ARGS="--label-filter=feature:admissionfairsharing" make test-e2e-sequential-baseline
GINKGO_ARGS="--label-filter=feature:spark" make test-e2e-sequential-extended
```

Taxonomies come from `hack/make/test.mk`:

- Integration controllers: `controller:{workload,localqueue,clusterqueue,admissioncheck,resourceflavor,provisioning}`.
- Integration jobs: `job:{batch,pod,jobset,pytorch,tensorflow,mpi,paddle,xgboost,jax,train,ray,appwrapper,sparkapplication}`.
- Integration features: `feature:{tas,multikueue,provisioning,fairsharing,admissionfairsharing}`.
- Integration areas: `area:{core,jobs,admissionchecks,multikueue}`.
- E2E singlecluster features: `appwrapper, certs, deployment, job, fairsharing, jaxjob, jobset, kuberay, kueuectl, leaderworkerset, metrics, pod, pytorchjob, statefulset, tas, trainjob, visibility, e2e_v1beta1`.
- E2E customconfigs features (baseline): `admissionfairsharing, certs, failurerecoverypolicy, localqueuemetrics, objectretentionpolicies, podintegrationautoenablement, reconcile, visibility, waitforpodsready`. Extended: `managejobswithoutqueuename, spark`.

### 2. Ginkgo `--focus`

Regex match on spec description.

```shell
GINKGO_ARGS="--focus=Scheduler" make test-integration
GINKGO_ARGS="--focus='Creating a Pod requesting TAS'" make test-e2e
```

### 3. `ginkgo.FIt` / `FDescribe`

Flip `ginkgo.It(...)` → `ginkgo.FIt(...)` (or `Describe` → `FDescribe`) on specs you want, then run the suite normally. Everything else is skipped. Don't commit the `F`.

### 4. Narrow the package

```shell
INTEGRATION_TARGET='test/integration/singlecluster/scheduler' make test-integration
GO_TEST_TARGET=./pkg/scheduler/preemption make test
```

## Verbosity

`TEST_LOG_LEVEL` (default `-3`) controls test logging uniformly across unit, integration, and e2e targets. Lower (more negative) is louder. `INTEGRATION_API_LOG_LEVEL=N` additionally controls envtest's apiserver logs (`0` = off).

```shell
TEST_LOG_LEVEL=-5 make test-integration    # more verbose
TEST_LOG_LEVEL=-1 make test                # quieter
```

## CI surface

CI is Prow. Logs and artifacts are at `https://prow.k8s.io/view/gs/kubernetes-ci-logs/...`. Job names you actually see as PR checks follow the pattern `pull-kueue-test-<tier>-<variant>[-<k8s-version>]`. Attested in the raw corpus:

| Job | Tier / suite | Source |
|---|---|---|
| `pull-kueue-test-integration-baseline-release-0-16` | Integration baseline, release-0.16 branch | [[issue-9952]] |
| `pull-kueue-test-integration-multikueue-main` | Integration multikueue, main | [[issue-9954]] |
| `periodic-kueue-test-integration-multikueue-main` | Periodic (not PR-gating) multikueue integration | [[issue-9954]] |
| `pull-kueue-test-e2e-main-1-31` | E2E singlecluster against k8s 1.31 | [[issue-3044]] |
| `pull-kueue-test-e2e-main-1-35` | E2E singlecluster against k8s 1.35 | [[pr-5414]] |
| `pull-kueue-test-e2e-multikueue-main` | E2E multikueue, main | [[issue-6525]] |

The `hack/make/test.mk` targets whose CI jobs are not individually cited in the raw corpus — `test-tas-e2e`, `test-e2e-dra`, `test-e2e-certmanager`, `test-e2e-sequential-baseline`, `test-e2e-sequential-extended`, `test-e2e-upgrade`, `test-e2e-kueueviz`, `test-performance-scheduler`, `test-tas-performance-scheduler` — exist as make targets today but their exact Prow job names are not verified from raw/github/. Dashboard: `https://testgrid.k8s.io/sig-scheduling` ([[issue-9954]]).

Bot commands (k8s-ci-robot) you will use on PRs:

- `/retest` — rerun all failed required jobs ([[pr-5414]]).
- `/retest-required` — same, limited to required ([[pr-5414]]).
- `/test <job-name>` — rerun a single job, e.g. `/test pull-kueue-test-e2e-main-1-35` ([[pr-5414]]).
- `/retitle <new-title>` — change the PR/issue title; commonly used on flakes to paste the full spec path for search ([[issue-9954]]).
- `/close` — close the issue/PR.

## Writing tests

### Unit

Normal `go test`. Table tests in the codebase-standard form use `testingutil.MakeClusterQueue(...)` builders and assertion helpers from `pkg/util/testing`; see e.g. the webhook tests adjusted in [[pr-6906]] for the current pattern (`testcases := []struct{...}{}` with `t.Run(tc.name, ...)`).

### Integration

Ginkgo suites under `test/integration/`. Shared fixtures live under `test/util/behavioral/` ([[pr-2415]] started the shared-helper pattern; see the layout note below). Common patterns:

- `var _ = ginkgo.Describe("...", ginkgo.Ordered, ginkgo.ContinueOnFailure, func() { ... })`.
- One `ginkgo.It` per independent scenario. `ginkgo.DescribeTable` still appears in older suites, but the writing-tests guide keeps table-driven style for unit tests only, and CodeRabbit no longer suggests converting `It` blocks to `DescribeTable` (source: pr-16481.md).
- `ginkgo.DeferCleanup(...)` over manual teardown.
- `gomega.Eventually(func(g gomega.Gomega) { ... }, behavioral.Timeout, behavioral.Interval).Should(gomega.Succeed())` rather than `time.Sleep`.
- Builders from `pkg/util/testing` and the versioned `pkg/util/testing/v1beta2` (imported as `utiltestingapi`, e.g. `utiltestingapi.MakeClusterQueue("cq").Obj()`), plus `pkg/util/testingjobs`; assertion helpers from `test/util/behavioral` (e.g. `behavioral.ExpectAdmittedWorkloadsTotalMetric`, `behavioral.ExpectWorkloadsToBePending`, `behavioral.ExpectObjectToBeDeleted`).

**Correction (2026-10-21)**: earlier text named `test/util/util.go`, `test/util/constants.go` and the `util.` prefix. Helpers were reorganized in October 2026 (source: pr-16626.md, pr-16781.md, fixes #15172; pr-16791.md; pr-16823.md):

- `test/util/behavioral/`: helpers valid in **both** integration and e2e tests (constants, workloads, queues, metrics, events, objects, pods, jobs, namespaces, MultiKueue).
- `test/util/behavioral/integration/`: helpers that **simulate** kubelet or controller behaviour, valid only against envtest (for example faking Pod readiness or eviction completion).
- `test/util/behavioral/e2e/`: e2e-only helpers (clients, cluster components, images, kubelet/node control, restarts, KubeRay, metrics scraping).
- Log verification moved into the integration framework (`test/integration/framework`).
- Every Ginkgo helper calls `ginkgo.GinkgoHelper()`, so failures point at the caller. Explicit Gomega offsets were dropped (source: pr-16996.md, fixes #16896; release-0.19 got the same change as a manual pick, pr-17136). Exception: a function that only **returns** a closure (for example the diagnostic message builder `AssertMsgForMk`) needs `GinkgoHelper()` inside the closure, not in the outer function, which has already returned when the closure runs (pr-17163, fixes issue-17138).
- Shared helpers added or merged in this window: `SetLocalQueueStopPolicy(ctx, c, lq, policy)` in `test/util/behavioral/queues.go` sets `spec.stopPolicy` to any value with the usual get/update `Eventually` retry, and `UnholdLocalQueue` is a wrapper over it with `kueue.None` (pr-17391, fixes issue-16876). `DeleteAllPodsInNamespace` in `test/util/behavioral/pods.go` is now the single Pod-deletion helper, used by `DeleteNamespace` (pr-17206, fixes issue-17139). Both were backported to release-0.20/0.19. Reuse them instead of hand-written patch loops.

Timeout constants (from `test/util/behavioral/constants.go`):

| Name | Value |
|---|---|
| `TinyTimeout` | 10 ms |
| `ShortTimeout` | 1 s |
| `Timeout` | 10 s (default for `Eventually`) |
| `MediumTimeout` | 45 s (e2e: complex operations such as running Pods to completion) |
| `LongTimeout` | 90 s (e2e: Pod lifecycle including container/sandbox teardown) |
| `VeryLongTimeout` | 5 min (Kueue startup including cert propagation) |
| `ShortConsistentDuration` / `ConsistentDuration` / `LongConsistentDuration` | 100 ms / 300 ms / 2 s (for `Consistently`) |
| `ShortInterval` | 10 ms |
| `Interval` | 250 ms (default poll) |
| `LongInterval` | 1 s |

Reach for `LongTimeout` or higher when asserting on things that cross envtest boundaries slowly under CI load ([[issue-6525]]).

### E2E

Same Ginkgo + Gomega patterns, but every assertion crosses a real apiserver over the network and external operators. Timeouts used with `Eventually` are already more generous than integration defaults; bumping to `LongTimeout` is the standard flake fix ([[issue-6525]]). See [[testing-e2e]] for the e2e-specific cluster lifecycle and operator installation flow.

## Community test-writing guidelines

`site/content/en/community/contribution_guidelines/writing_tests.md` (pr-16723.md, merged 2026-10-07, cherry-picked to release-0.19/0.20) is the reference reviewers and the reviewer agent skills now cite. It builds on Go Test Comments, the Google Go Style Guide and the Kubernetes testing and e2e best-practice guides.

**Common**

- Choose the **lowest test level that can prove the behaviour**. Cover relevant branches, edge cases and errors. Test **both feature-gate states** when the gate changes the result. A bug fix needs a case that **fails without the fix**.
- Build fixtures with the wrappers in `pkg/util/testing` and `pkg/util/testingjobs`, not ad-hoc helper functions or closures. Declare objects per test case, or clone a shared base per case. Extend the wrappers when needed, but keep them to constructing objects and setting fields, without complex fallback logic.
- Integration and e2e tests use Ginkgo/Gomega with the shared suite setup. Keep independent scenarios in **separate `ginkgo.It` blocks**. Table-driven style is for unit tests only.

**Unit**

- Prefer testing complete operations (`Reconcile`, a scheduling cycle) or established logic layers. Test all exported functions; avoid testing unexported helpers directly.
- Use Go's `testing` package with plain checks and `cmp`, not assertion libraries.
- Extend an existing **map-based** table and reuse its runner. Add a runner setting rather than a separate setup, and start a new table only when setup really differs.
- Assert on the error details that matter (type or structure), not just a boolean "error/no error".
- Use the existing fake clocks for deadlines, and hooks or channels to coordinate concurrency. No fixed sleeps and no repeated attempts to win a race.

**Integration (envtest)**

- Let event handlers trigger the work. Do not call `Reconcile` directly.
- Use `Eventually` to retry transient errors (update conflicts) and fail on anything else.
- Use `Consistently` only for "stays unchanged over time". To check the outcome of an operation, prefer a single assertion (for example on a counter metric), and only after all relevant asynchronous processing has finished.
- Clean up explicitly with the suite's helpers, so the test can run in a loop.

**E2E**

- Use e2e only when real components beyond envtest are needed (kubelet, kube-scheduler, kube-controller-manager, real operators such as KubeRay, JobSet or LWS). These tests catch regressions when Kubernetes or an operator changes behaviour. They are expensive and the hardest to debug, so add them only when necessary.
- Tests that change shared Kueue configuration go in a **sequential** suite.

Related maintainer hygiene seen in this window: many tests were converted to the wrappers and to declarative table cases (pr-16648, pr-16654, pr-16655, pr-16961). The performance-tool unit tests moved from `make verify` into the regular unit-test shards, and `verify-checks` now runs with `GOMAXPROCS=2` to reduce CPU contention (source: pr-16923.md).

## Debugging flakes

Flakes are tracked with the `kind/flake` label ([[issue-9952]], [[issue-3044]], [[issue-6525]]). The recurring patterns:

- **10-second `Eventually` too tight.** The default `behavioral.Timeout` (formerly `util.Timeout`) is 10 s; under Prow load the sequence "Delete Sticky → Sync Cache → Finish Eviction → Reclaim Resources → Admit Next" often does not fit in 10 s ([[issue-9952]]). Usual fix: bump to `MediumTimeout`/`LongTimeout`, or add an explicit synchronization step (e.g. wait for `NotFound` before starting the next timer).
- **`Consistently` racing with deletion.** A `Consistently` that asserts a resource's state can fail with `NotFound` if the cleanup path races the assertion ([[issue-9954]]).
- **State race across parallel specs.** MultiKueue e2e runs disruptive tests sequentially for a reason; adding new specs into a parallel suite can surface order-dependent failures ([[issue-10200]]).

When a test flakes in CI:

1. Open the Prow link and scroll down to the `kind-worker/pods/kueue-system_kueue-controller-manager*/manager/` logs (there are two replicas in e2e; check both).
2. Grep for the affected controller and the timestamps just before the failed `Eventually`. Each log line includes `file:line`, e.g. `core/clusterqueue_controller.go:341` ([[issue-9952]]).
3. Reproduce locally with `--until-it-fails` or `--repeat=N`:
   ```shell
   GINKGO_ARGS="--until-it-fails" make test-integration
   GINKGO_ARGS="--repeat=10" make test-e2e
   ```
4. For unit-level timing races: compile the test and run `stress` on it.
   ```shell
   go install golang.org/x/tools/cmd/stress@latest
   go test ./pkg/scheduler/preemption/ -c
   stress ./preemption.test -test.run TestPreemption
   ```
5. File a `kind/flake` issue linking the failed Prow URL and the failure message. The `/retitle` bot command is conventionally used to paste the full spec path into the title for future de-dup searches ([[issue-9954]]).

Add external CPU pressure with `stress` to reproduce CI-load patterns locally (`sudo apt install stress && /usr/bin/stress --cpu 80`), alongside the test run.

## Presubmit verification (not tests, but co-gated)

`make verify` runs the presubmit linters and generator-freshness checks. On failure:

- `make lint-fix` — auto-applies `golangci-lint` rules (including `gci` import ordering). Running `go fmt` alone is not enough because the repo uses custom `.golangci.yaml` ([[pr-6906]]).
- `make update-helm` — regenerates Helm charts after CRD changes ([[pr-6906]]).
- `make generate manifests` — regenerates CRDs and RBAC after API changes ([[pr-6906]]).

If a PR's `verify` job fails for import ordering, run `make lint-fix` locally and recommit.

**Reading a failed `make verify` (2026-10).** Changes merged to main and both release branches:

- `verify-checks` runs through `hack/make-failure-summary.sh`. On failure, the `make[N]: ***` lines are repeated at the **end** of the log under `ERROR: failed make targets:`, with the exit status kept. Under `make -j`, the real failure used to sit hundreds of lines up (line 946 of 1262 in one case). Covered by the `verify-make-failure-summary` target (source: pr-17304.md).
- `verify-e2e-common-test` (`hack/testing/e2e-common_test.sh`, which fakes `docker` and `kind`) prints its output only when it fails. Its expected `net/http: TLS handshake timeout` for `registry.example.com` used to appear in **every** verify log and was repeatedly mistaken for a registry flake while the real failure was a lint or typecheck error (source: pr-17283.md, fixes issue-16959). If you see a TLS timeout in a verify log now, it is real.
- `verify-skills-lint` runs skillsaw (0.22.0+) with `-q`: a clean run prints nothing; the full report is in `$ARTIFACTS/skillsaw-summary.html`. Its config is `cmd/experimental/skills/.skillsaw.yaml`, owned by the skills sub-approvers, and the container runs with rootless-Podman user-namespace options (source: pr-17352.md, pr-17477.md, pr-17487.md).
- The standalone `make skills-lint` and `make ray-version-verify` targets were removed; use `make verify-skills-lint` and `make verify-ray-version`. Convention: a separate `X` target exists next to `verify-X` only when `verify-X` depends on `verify-tree-prereqs` (source: pr-17431.md).
- golangci-lint is pinned to **v2.14.0** in `hack/tools/go.mod`. Go 1.27.2 writes export data v5, which v2.13.x cannot read, so every package failed with `typecheck` (source: pr-17148.md). The custom API linter (`make golangci-lint-kal`) is built with `GOTOOLCHAIN=$(go env GOVERSION)`; otherwise an older local Go could build it and it refused to analyse Kueue (`built with go1.26.x`) (source: pr-17377.md).

## Related pages

- [[testing-integration]] — envtest-based integration suites.
- [[testing-e2e]] — Kind-based e2e: dev mode, MultiKueue recipe, per-suite matrix.
- [[testing-performance]] — scheduler benchmarks.
- [[architecture]] — what the integration tests are actually testing.
- [[feature-gates]] — baseline vs extended integration variants exercise different feature-gate combinations.
- [[release-process]] — how release branches (`release-0-16`, …) map to CI jobs.
- [[performance-and-scale]] — what perf tests are measuring.
- [[metrics]] — signals you will look at during test runs.
