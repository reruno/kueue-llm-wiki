# Testing

**Summary**: How to run, focus, and debug Kueue's three test tiers (unit, integration, e2e) on a local dev machine, which make targets and env vars each tier honors, how CI exercises them, and where to look when a test goes flaky. Entry point for the developer-workflow section.

**Sources**: `raw/kueue/Makefile-test.mk`, `raw/kueue/hack/testing/`, `raw/kueue/site/content/en/docs/contribution_guidelines/testing.md`, `raw/kueue/test/util/constants.go`; `raw/github/kubernetes-sigs__kueue/` — [[issue-9952]], [[issue-9954]], [[issue-3044]], [[issue-6525]], [[issue-10200]], [[pr-2415]], [[pr-5414]], [[pr-6906]].

**Last updated**: 2026-04-23

---

## The test pyramid

Kueue has three tiers. Each tier's make targets live in `Makefile-test.mk`.

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
- `make envtest` pulls the kubebuilder assets; integration targets set `KUBEBUILDER_ASSETS` automatically via `ENVTEST_K8S_VERSION` (default `1.35`, set in `Makefile-test.mk`).

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

`make test` excludes `./test/` and writes a coverage profile to `$ARTIFACTS/cover.out` (`Makefile-test.mk`).

### Integration

```shell
make test-integration                 # full singlecluster suite
make test-multikueue-integration      # multikueue integration suite
make test-integration-baseline        # --label-filter="!slow && !redundant"
make test-integration-extended        # --label-filter="slow || redundant"
```

Knobs (all read by `Makefile-test.mk`):

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
- `E2E_K8S_VERSION` (default `1.35`) — picks the Kind node image. Valid values live in `E2E_K8S_VERSIONS` (currently `1.33.7 1.34.3 1.35.0` in `Makefile-test.mk`).
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

Taxonomies come from `Makefile-test.mk`:

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

The `Makefile-test.mk` targets whose CI jobs are not individually cited in the raw corpus — `test-tas-e2e`, `test-e2e-dra`, `test-e2e-certmanager`, `test-e2e-sequential-baseline`, `test-e2e-sequential-extended`, `test-e2e-upgrade`, `test-e2e-kueueviz`, `test-performance-scheduler`, `test-tas-performance-scheduler` — exist as make targets today but their exact Prow job names are not verified from raw/github/. Dashboard: `https://testgrid.k8s.io/sig-scheduling` ([[issue-9954]]).

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

Ginkgo suites under `test/integration/`. Shared fixtures live in `test/util/` ([[pr-2415]]). Common patterns:

- `var _ = ginkgo.Describe("...", ginkgo.Ordered, ginkgo.ContinueOnFailure, func() { ... })`.
- `ginkgo.DescribeTable("Should ...", func(args...) { ... }, ginkgo.Entry(...))`.
- `ginkgo.DeferCleanup(...)` over manual teardown.
- `gomega.Eventually(func(g gomega.Gomega) { ... }, util.Timeout, util.Interval).Should(gomega.Succeed())` rather than `time.Sleep`.
- Builders from `pkg/util/testing` (e.g. `testing.MakeLocalQueue(name, ns).StopPolicy(p).Obj()`); delete-helpers from `test/util/util.go` (e.g. `util.ExpectLocalQueueToBeDeleted`, `util.ExpectAdmittedWorkloadsTotalMetric`).

Timeout constants (from `test/util/constants.go`):

| Name | Value |
|---|---|
| `TinyTimeout` | 10 ms |
| `ShortTimeout` | 1 s |
| `Timeout` | 10 s (default for `Eventually`) |
| `MediumTimeout` | 45 s |
| `LongTimeout` | 90 s |
| `VeryLongTimeout` | 5 min |
| `ShortInterval` | 10 ms |
| `Interval` | 250 ms (default poll) |
| `LongInterval` | 1 s |

Reach for `LongTimeout` or higher when asserting on things that cross envtest boundaries slowly under CI load ([[issue-6525]]).

### E2E

Same Ginkgo + Gomega patterns, but every assertion crosses a real apiserver over the network and external operators. Timeouts used with `Eventually` are already more generous than integration defaults; bumping to `LongTimeout` is the standard flake fix ([[issue-6525]]). See [[testing-e2e]] for the e2e-specific cluster lifecycle and operator installation flow.

## Debugging flakes

Flakes are tracked with the `kind/flake` label ([[issue-9952]], [[issue-3044]], [[issue-6525]]). The recurring patterns:

- **10-second `Eventually` too tight.** The default `util.Timeout` is 10 s; under Prow load the sequence "Delete Sticky → Sync Cache → Finish Eviction → Reclaim Resources → Admit Next" often does not fit in 10 s ([[issue-9952]]). Usual fix: bump to `MediumTimeout`/`LongTimeout`, or add an explicit synchronization step (e.g. wait for `NotFound` before starting the next timer).
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

## Related pages

- [[testing-integration]] — envtest-based integration suites.
- [[testing-e2e]] — Kind-based e2e: dev mode, MultiKueue recipe, per-suite matrix.
- [[testing-performance]] — scheduler benchmarks.
- [[architecture]] — what the integration tests are actually testing.
- [[feature-gates]] — baseline vs extended integration variants exercise different feature-gate combinations.
- [[release-process]] — how release branches (`release-0-16`, …) map to CI jobs.
- [[performance-and-scale]] — what perf tests are measuring.
- [[metrics]] — signals you will look at during test runs.
