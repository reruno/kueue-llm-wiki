# Integration tests

**Summary**: Integration tests run Kueue's controllers and webhooks against a controller-runtime `envtest` (an etcd + kube-apiserver pair; no kubelet, no kube-scheduler). They are Ginkgo + Gomega suites under `test/integration/`. This page covers the suites, the CI variants (main / baseline / extended / multikueue), how to write one, and the flake patterns that recur.

**Sources**: `raw/kueue/Makefile-test.mk`, `raw/kueue/test/integration/`, `raw/kueue/test/util/constants.go`, `raw/kueue/test/util/util.go`, `raw/kueue/site/content/en/docs/contribution_guidelines/testing.md`; `raw/github/kubernetes-sigs__kueue/` — [[issue-9952]], [[issue-9954]], [[pr-2415]], [[pr-6906]].

**Last updated**: 2026-04-23

---

## What envtest gives you

`envtest` downloads a real etcd binary and a real `kube-apiserver` binary and runs them locally. Kueue's controllers and webhooks then run in-process against that apiserver. What you get:

- Real CRD validation and admission webhook execution.
- Real watch/reconcile loops.
- Real conditions races between reconcilers.

What you don't get:

- **No kubelet** — Pods never start; `.status.phase` stays where you put it.
- **No kube-scheduler** — nothing assigns Nodes.
- **No external operators** — JobSet, KubeRay, Kubeflow, AppWrapper controllers are not running. You create the CRs, but nothing reconciles them except Kueue's own integration shims.

This is why integration tests are fast (~minutes) but cannot catch everything e2e does. Anything Pod-scheduling-sensitive has to go to [[testing-e2e]].

## Directory layout

Under `test/integration/`:

```
test/integration/
├── framework/              # shared suite bootstrap
├── singlecluster/
│   ├── controller/
│   ├── conversion/
│   ├── importer/
│   ├── kueuectl/
│   ├── scheduler/
│   │   ├── delayedadmission/
│   │   ├── excluderesources/
│   │   ├── fairsharing/     # e.g. fair_sharing_test.go — see [[issue-9952]]
│   │   ├── inadmissible/
│   │   ├── podsready/
│   │   ├── resourcetransformations/
│   │   ├── preemption_test.go
│   │   ├── scheduler_test.go
│   │   └── workload_controller_test.go
│   ├── tas/
│   └── webhook/
└── multikueue/
    ├── scheduler/           # scheduler_test.go — see [[issue-9954]]
    └── ...
```

`INTEGRATION_TARGET` (default `./test/integration/singlecluster/...`) selects which subtree runs. `INTEGRATION_TARGET_MULTIKUEUE` (default `./test/integration/multikueue/...`) is used by `make test-multikueue-integration`.

## CI variants

Four flavors exist in `Makefile-test.mk`. They differ only by label filter:

| Target | Label filter | Purpose |
|---|---|---|
| `make test-integration` | (none) | Full singlecluster suite. |
| `make test-integration-baseline` | `!slow && !redundant` | What pre-submit blocks on. Same assertions as `main`, with slow/redundant specs excluded. Runs on release branches too, e.g. `pull-kueue-test-integration-baseline-release-0-16` ([[issue-9952]]). |
| `make test-integration-extended` | `slow \|\| redundant` | Catches specs marked `slow` or `redundant` that `baseline` skips. |
| `make test-multikueue-integration` | (none) | Two envtest instances — one acting as the MultiKueue manager, one as a worker. Has its own CI jobs `pull-kueue-test-integration-multikueue-main` (presubmit) and `periodic-kueue-test-integration-multikueue-main` (periodic) ([[issue-9954]]). |

There is no separate `feature-gates` integration variant in `Makefile-test.mk` — feature-gate combinations are exercised by enabling them inside specific specs rather than by a dedicated target.

## Running

```shell
make test-integration
make test-multikueue-integration
make test-integration-baseline
make test-integration-extended

# Narrow to one directory
INTEGRATION_TARGET='test/integration/singlecluster/scheduler' make test-integration

# Label filter
INTEGRATION_FILTERS="--label-filter=controller:localqueue" make test-integration
INTEGRATION_FILTERS="--label-filter=area:core && !slow" make test-integration

# Focus on a spec description
GINKGO_ARGS="--focus=Scheduler" make test-integration

# Parallelism (default 4; multikueue default 3)
INTEGRATION_NPROCS=1 make test-integration
INTEGRATION_NPROCS_MULTIKUEUE=1 make test-multikueue-integration

# Verbosity
TEST_LOG_LEVEL=-5 INTEGRATION_API_LOG_LEVEL=4 make test-integration
```

### Label taxonomy

From `Makefile-test.mk`:

- **Controllers**: `controller:workload`, `controller:localqueue`, `controller:clusterqueue`, `controller:admissioncheck`, `controller:resourceflavor`, `controller:provisioning`.
- **Job types**: `job:batch`, `job:pod`, `job:jobset`, `job:pytorch`, `job:tensorflow`, `job:mpi`, `job:paddle`, `job:xgboost`, `job:jax`, `job:train`, `job:ray`, `job:appwrapper`, `job:sparkapplication`.
- **Features**: `feature:tas`, `feature:multikueue`, `feature:provisioning`, `feature:fairsharing`, `feature:admissionfairsharing`.
- **Areas**: `area:core`, `area:jobs`, `area:admissionchecks`, `area:multikueue`.
- **Gating**: `slow`, `redundant` — excluded by `baseline`, selected by `extended`.

Label filters combine with Ginkgo's boolean syntax: `"area:core && !slow"`, `"feature:tas,feature:multikueue"` (comma = OR).

### Debugging with VSCode

Integration tests can be debugged in VSCode's Go extension (`run test | debug test` gutters), but envtest needs two env vars set in `settings.json`:

```json
"go.testEnvVars": {
    "KUBEBUILDER_ASSETS": "<path from `./bin/setup-envtest use $ENVTEST_K8S_VERSION -p path`>",
    "KUEUE_BIN": "<absolute path to your kueue checkout>/bin"
}
```

Get `KUBEBUILDER_ASSETS` by running `ENVTEST_K8S_VERSION=1.35 make envtest && ./bin/setup-envtest use $ENVTEST_K8S_VERSION -p path`.

## Writing an integration test

The conventions in the current codebase (see e.g. `test/integration/singlecluster/kueuectl/resume_test.go`; the pattern was established in [[pr-2415]]):

### Suite skeleton

```go
var _ = ginkgo.Describe("Kueuectl Resume", ginkgo.Ordered, ginkgo.ContinueOnFailure, func() {
    ginkgo.When("Resuming a LocalQueue", func() {
        ginkgo.DescribeTable("Should resume a LocalQueue",
            func(name string, wantInitialStopPolicy v1beta1.StopPolicy) {
                lq := testing.MakeLocalQueue(name, ns.Name).StopPolicy(wantInitialStopPolicy).Obj()

                ginkgo.By("Create a LocalQueue", func() {
                    gomega.Expect(k8sClient.Create(ctx, lq)).To(gomega.Succeed())
                })

                gomega.Eventually(func(g gomega.Gomega) {
                    g.Expect(k8sClient.Get(ctx, client.ObjectKeyFromObject(lq), createdLocalQueue)).To(gomega.Succeed())
                    g.Expect(ptr.Deref(createdLocalQueue.Spec.StopPolicy, v1beta1.None)).Should(gomega.Equal(wantInitialStopPolicy))
                }, util.Timeout, util.Interval).Should(gomega.Succeed())
            },
            ginkgo.Entry("stop-policy=Hold", "lq-hold", v1beta1.Hold),
        )
    })
})
```

### Conventions worth internalizing

- **`ginkgo.Ordered` + `ginkgo.ContinueOnFailure`** on `Describe` blocks when later specs depend on earlier setup. Used throughout the kueuectl suite.
- **`ginkgo.DescribeTable` + `ginkgo.Entry`** for parameterized tests. The Go-level `testcases := []struct{}{}` table-test pattern is also used in unit tests ([[pr-6906]]).
- **`ginkgo.DeferCleanup(...)`** for per-spec teardown. Prefer over manual `AfterEach`.
- **Builders from `pkg/util/testing`**: `testing.MakeClusterQueue(...)`, `testing.MakeLocalQueue(...)`, `testing.MakeWorkload(...)`, chained with fluent setters and closed with `.Obj()`.
- **Assertion helpers from `test/util/util.go`**: `util.ExpectLocalQueueToBeDeleted`, `util.ExpectAdmittedWorkloadsTotalMetric`, `util.ExpectWorkloadToFinish`, `util.ExpectWorkloadsToBePending`, etc. These wrap `Eventually` with the right timeout/interval already.
- **Never `time.Sleep`.** Use `gomega.Eventually(..., util.Timeout, util.Interval).Should(...)` or `gomega.Consistently(...)`.
- **Label your spec**. `ginkgo.It("...", ginkgo.Label("feature:fairsharing"), func(){})` lets baseline/extended pickups work.

### Timeout constants

From `test/util/constants.go`:

| Name | Value | When to use |
|---|---|---|
| `TinyTimeout` | 10 ms | Only for synchronous expectations. |
| `ShortTimeout` | 1 s | Fast reconcile loops. |
| `Timeout` | 10 s | Default. Most assertions. |
| `MediumTimeout` | 45 s | Preemption + re-admission chains. |
| `LongTimeout` | 90 s | Cross-cluster flows (MultiKueue), or specs that flake at default under CI load ([[issue-6525]]). |
| `VeryLongTimeout` | 5 min | Scale-oriented specs. |
| `ShortInterval` | 10 ms | Rarely needed. |
| `Interval` | 250 ms | Default poll interval. |
| `LongInterval` | 1 s | Use when the reconcile cadence is slow. |

## Flake patterns (learned from real incidents)

### 10-second `Eventually` too tight

[[issue-9952]] — "Scheduler ... sticky workload deleted, next workload can admit" timed out after 10 s in CI. Timestamp autopsy showed the sequence **Delete Sticky → Sync Cache → Finish Eviction → Reclaim Resources → Admit Next** completed ~70 ms *after* the test failed. The scheduler was actually correct; the timeout just didn't fit under CI load.

Fixes that actually work:

1. Bump the timeout on the final assertion from `util.Timeout` to `util.MediumTimeout` or `util.LongTimeout`.
2. Add an explicit synchronization step: wait for the deleted object to be `NotFound` *before* starting the timer for the final admission. This gives the final `Eventually` a clean window.

### `Consistently` racing with cleanup

[[issue-9954]] — A MultiKueue spec used `Consistently` to assert that a Workload never transitioned; it flaked with `"workloads.kueue.x-k8s.io \"...\" not found"` because the cleanup path beat the assertion. Fix was structural: align the integration spec with what the e2e version already did.

### Missing ResourceFlavor during test setup

The [[issue-9952]] Prow logs showed `ResourceFlavor "on-demand" not found` causing the Job reconciler to burn 7 cycles in 72 ms before the test timed out. If your suite creates flavors conditionally or in a non-obvious order, create them in `BeforeAll`/`BeforeEach` explicitly and assert creation succeeded, so missing-flavor paths fail fast instead of consuming the `Eventually` budget.

### Parallel-spec state bleed

With `INTEGRATION_NPROCS=4`, specs run in parallel within a suite. Cluster-scoped objects (ClusterQueue, Cohort, ResourceFlavor) need unique names per spec (use a `ginkgo.NodeName`-derived suffix or `rand.String(...)`), and namespaces need to be created per spec. The builders in `pkg/util/testing` handle this if you use them consistently.

## Reproducing and stressing

```shell
# Repeat until failure
GINKGO_ARGS="--until-it-fails" make test-integration

# Repeat N times
GINKGO_ARGS="--repeat=10" INTEGRATION_TARGET='test/integration/singlecluster/scheduler/fairsharing' make test-integration

# Unit-level stress (go stress loops the compiled test binary)
go install golang.org/x/tools/cmd/stress@latest
go test ./pkg/scheduler/preemption/ -c
stress ./preemption.test -test.run TestPreemption

# Add CPU pressure in a separate shell to emulate Prow
sudo apt install stress
/usr/bin/stress --cpu 80
```

## Related pages

- [[testing]] — the landing page; tiers, prerequisites, CI map.
- [[testing-e2e]] — when integration can't cover it.
- [[architecture]] — the controllers these tests exercise.
- [[feature-gates]] — gates that alter behavior across baseline/extended.
- [[admission]] — the subsystem most scheduler integration tests cover.
