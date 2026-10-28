# E2E tests

**Summary**: E2E tests run Kueue against a real (Kind-based) Kubernetes cluster, with any external operators (JobSet, KubeRay, Kubeflow Training, LeaderWorkerSet, AppWrapper, cert-manager, Prometheus Operator) installed alongside. This page covers the per-suite matrix, the dev-mode Kind lifecycle (`E2E_MODE=dev`), the full MultiKueue invocation recipe, and flake patterns specific to e2e.

**Sources**: `raw/kueue/hack/make/test.mk`, `raw/kueue/hack/testing/e2e-common.sh`, `raw/kueue/hack/testing/e2e-test.sh`, `raw/kueue/hack/testing/e2e-multikueue-test.sh`, `raw/kueue/test/e2e/`, `raw/kueue/site/content/en/community/contribution_guidelines/testing.md`; `raw/github/kubernetes-sigs__kueue/` — [[issue-3044]], [[issue-6525]], [[issue-10200]], [[pr-5414]]; pr-16348.md, pr-17050.md, pr-16753.md, pr-16723.md.

**Last updated**: 2026-10-28

---

## What e2e covers that integration doesn't

- Real `kubelet` + real `kube-scheduler`. Pod placement actually happens.
- External operator reconciliation — JobSet, KubeRay, Kubeflow Training, LeaderWorkerSet, AppWrapper, cert-manager, Prometheus Operator are installed and run.
- Image loading, RBAC, CRD apply paths — things that are bypassed by envtest.
- Upgrade / downgrade behavior (historical: an `upgrade` suite installed a prior release, then upgraded to the current build; there is no upgrade make target or `test/e2e/upgrade/` folder at kueue@3bbb8cce4, although `pull-kueue-test-e2e-upgrade-main` and `pull-kueue-test-e2e-certmanager-upgrade-main` appear in the CI corpus, e.g. issue-12444.md, issue-11792.md).

Because each e2e suite spins up its own Kind cluster(s), each suite is expensive. The MultiKueue suite was ~19 min sequential / ~22 min parallel when it was last benchmarked ([[issue-10200]]).

## Suite matrix

Every target below is in `hack/make/test.mk` (formerly `Makefile-test.mk`). All of them run via `hack/testing/e2e-test.sh` or `hack/testing/e2e-multikueue-test.sh`.

| Make target | E2E folder | What it covers |
|---|---|---|
| `test-e2e-baseline` | `test/e2e/singlecluster/baseline/` | Core singlecluster e2e: certs, batch Job, Pod, Deployment, StatefulSet, fair sharing, kueuectl, metrics, visibility, HA. |
| `test-e2e-extended` (+ `-shard-0/1/2`) | `test/e2e/singlecluster/extended/` | Job-framework integrations against real operators: AppWrapper, JAX, JobSet, KubeRay, LeaderWorkerSet, PyTorch, TrainJob, MPI. The shards split KubeRay (shards 0 and 2) from the other operators (shard 1). |
| `test-multikueue-e2e-baseline` | `test/e2e/multikueue/baseline/` | Manager + worker Kind clusters; [[multikueue]] dispatch flow. |
| `test-multikueue-e2e-extended` (+ `-shard-0/1`, `-ray-autoscaling`) | `test/e2e/multikueue/extended/` | MultiKueue with external job integrations; shard 1 is KubeRay, `-ray-autoscaling` is KubeRay autoscaling. |
| `test-multikueue-e2e-sequential` (+ `-shard-0/1`) | `test/e2e/multikueue/sequential/` | Disruptive MultiKueue specs that cannot run in parallel ([[issue-10200]]). |
| `test-e2e-multikueue-dra` | `test/e2e/multikueue/dra/` | MultiKueue + DynamicResourceAllocation. |
| `test-tas-e2e-baseline` / `test-tas-e2e-extended` (+ `-shard-0/1`) | `test/e2e/singlecluster/tasapi/{baseline,extended}/` | Topology-aware scheduling end-to-end; uses `kind-cluster-tas.yaml`. `test-e2e-tas-*` are aliases; `test-e2e-was-tas-*` run the same suites with `WAS_ENABLED=true`. |
| `test-tas-e2e-deepintegration` | `test/e2e/singlecluster/tasapi/deepintegration/` | TAS deep-integration specs (used by `test-e2e-was-deep-tas-baseline-basic-fit`). |
| `test-e2e-dra-baseline` / `test-e2e-dra-counter` / `test-e2e-dra-capacity` | `test/e2e/dra/{whole-device,counter,capacity}/` | DRA support path. |
| `test-e2e-certmanager` | `test/e2e/certmanager/` | cert-manager-backed webhooks. |
| `test-e2e-sequential-baseline` (+ `-shard-0/1`) | `test/e2e/sequential/baseline/` | Non-default `configuration.kueue.x-k8s.io` Kueue configurations (baseline set). |
| `test-e2e-sequential-extended` (+ `-shard-0/1`) | `test/e2e/sequential/extended/` | The same, extended set (includes Spark). |
| `test-e2e-kueueviz` / `test-e2e-kueueviz-local` | `test/e2e/kueueviz/` | KueueViz UI end-to-end; runs Cypress against a real browser. See [[dashboard]]. |
| `test-e2e-k8s-main-was` | `test/e2e/singlecluster/wasapi/` | WAS API suite against a kind node image built from k/k `main` with `WAS_ENABLED=true`. `test-e2e-was-api` (alias `test-e2e-was`) runs the same folder on a released Kubernetes version. |

There is no `test-e2e`, `test-multikueue-e2e-main`, `test-tas-e2e`, `test-e2e-dra`, `test-e2e-upgrade`, `test-e2e-certmanager-upgrade` or `test-e2e-customconfigs` target at kueue@3bbb8cce4; use the baseline/extended targets above.

Add `-helm` to any supported target (`test-e2e-baseline-helm`, `test-e2e-extended-helm`, `test-tas-e2e-baseline-helm`, `test-tas-e2e-extended-helm`, `test-e2e-sequential-baseline-helm`, `test-e2e-sequential-extended-helm`) to install via Helm instead of kustomize. Or set `E2E_USE_HELM=true`. `test-multikueue-e2e-helm` is still defined but depends on the undefined `test-multikueue-e2e`, so it does not run (`hack/make/test.mk`).

**Helm and kustomize e2e now test the same configuration.** The Helm path used to carry its own copy of the manager configuration in `test/e2e/config/{default,certmanager}/values.yaml`. Nobody kept it in sync, so Helm e2e ran with **no feature gates enabled** and some settings missing. `helm_install` in `hack/testing/e2e-common.sh` now takes the kustomization directory as a third argument (`test/e2e/config/${E2E_CONFIG_FOLDER:-default}` or `test/e2e/config/certmanager`), runs `kustomize build`, and derives the manager configuration and replica count from it. Edit only the kustomize config (source: pr-16348.md). It also sets the chart's `enableAlphaAPIs` to `true` exactly when the kustomize build contains a CRD from `config/components/crd/alpha`. Without this, the 4 PreemptionConfig RBAC specs failed under Helm because the chart skipped the alpha CRDs (source: pr-17050.md).

**WAS deep-integration TAS targets.** `test-e2e-was-deep-tas-*` (baseline, extended, and two shards) run the `singlecluster/tasapi` suites with `SchedulerLibraryIntegration=true` and `SchedulerLibraryDeepIntegration=true` passed via `E2E_EXTRA_KUEUE_FEATURE_GATES` (source: pr-16753.md, part of #15333).

**When to write an e2e test at all.** Per the writing-tests guide, only when the behaviour needs real kubelets, kube-scheduler, kube-controller-manager or a real operator. Specs that change shared Kueue configuration belong in a sequential suite (source: pr-16723.md; see [[testing#Community test-writing guidelines]]).

## Running an e2e suite

Typical first-time singlecluster run:

```shell
make kind-image-build   # build the controller image with the current source
make test-e2e-baseline  # creates cluster, runs tests, deletes cluster
```

Pick a k8s version (from `E2E_K8S_VERSIONS` — currently `1.34.11 1.35.8 1.36.4 1.37.0`; default `E2E_K8S_VERSION=1.36`):

```shell
E2E_K8S_FULL_VERSION=1.35.8 make test-e2e-baseline
```

Use a released image instead of rebuilding:

```shell
IMAGE_TAG=registry.k8s.io/kueue/kueue:v0.16.0 make test-e2e-baseline
# or a staging image from a PR
IMAGE_TAG=us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:main make test-e2e-baseline
```

To reproduce a bug against an exact release, also `git checkout v0.16.0` first — CRDs and deployment manifests come from the checkout, only the controller image is overridden by `IMAGE_TAG`.

Focus a subset:

```shell
GINKGO_ARGS="--label-filter=feature:jobset" make test-e2e-extended
GINKGO_ARGS="--label-filter=feature:jobset,feature:trainjob" make test-e2e-extended
GINKGO_ARGS="--focus='Creating a Pod requesting TAS'" make test-tas-e2e-baseline
GINKGO_ARGS="--label-filter=feature:admissionfairsharing" make test-e2e-sequential-baseline
GINKGO_ARGS="--label-filter=feature:spark" make test-e2e-sequential-extended
```

### E2E singlecluster label taxonomy

- Baseline (`test-e2e-baseline`): `certs, deployment, job, fairsharing, kueuectl, metrics, pod, statefulset, visibility, ha`.
- Extended (`test-e2e-extended`): `appwrapper, jaxjob, jobset, kuberay, leaderworkerset, pytorchjob, trainjob, mpijob`.

(source: `hack/make/test.mk`)

### E2E customconfigs label taxonomy

- Baseline (`test-e2e-sequential-baseline`): `admissionfairsharing, certs, failurerecoverypolicy, localqueuemetrics, managejobswithoutqueuename, objectretentionpolicies, podintegrationautoenablement, reconcile, visibility, waitforpodsready`.
- Extended (`test-e2e-sequential-extended`): `managejobswithoutqueuename, workloadidentifierannotations, spark`.

## E2E_MODE — cluster lifecycle

`E2E_MODE` controls whether the suite runner creates, reuses, and/or deletes Kind clusters (defined in `hack/testing/e2e-common.sh`).

| `E2E_MODE` | Before the test | After the test |
|---|---|---|
| `ci` (default) | Create Kind cluster(s). | Delete Kind cluster(s). |
| `dev` | Create if missing, **reuse if existing**. | **Keep running.** |

`dev` is the mode contributors use locally. The canonical dev loop:

```shell
# First time — builds image, creates cluster, runs tests, keeps cluster
E2E_MODE=dev make kind-image-build test-e2e-baseline

# Subsequent iterations — rebuild image, redeploy Kueue, rerun tests, keep cluster
E2E_MODE=dev make kind-image-build test-e2e-baseline

# Repeat the run until it fails (for flake-hunting)
E2E_MODE=dev GINKGO_ARGS="--until-it-fails" make kind-image-build test-e2e-baseline

# Focus one spec, fast iteration
E2E_MODE=dev GINKGO_ARGS="--focus='MultiKueue should dispatch'" make kind-image-build test-multikueue-e2e-baseline
```

### Dev-mode-only speedups

These env vars are ignored in `ci` mode. They only take effect with `E2E_MODE=dev`:

- **`E2E_SKIP_REINSTALL=true`** — if the Kueue controller Deployment already exists in the cluster, skip reinstalling it. Useful when you're only changing test code and the controller image is fine as-is. Does not skip reinstall if the Deployment is missing.
- **`E2E_SKIP_IMAGE_RELOAD=true`** — skip `docker pull` for dependency images (JobSet controller, KubeRay, etc.) that are already in your local Docker cache, and skip loading an image into Kind worker nodes when the image reference is already present in the node's containerd store. Big speedup on multi-node clusters.
- **`E2E_ENFORCE_OPERATOR_UPDATE=true`** — invert the usual behavior: force re-installing external operators (MPI, KubeRay, JobSet, Kubeflow Trainer, LeaderWorkerSet, AppWrapper, cert-manager) on every run. Default in dev mode is to install operators only once per cluster lifetime.

Note: the Kueue controller image *is* always reloaded into the cluster unless `E2E_SKIP_REINSTALL=true`, because you may rebuild it with `make kind-image-build` under the same tag.

### Tear down dev-mode clusters

```shell
# Regular e2e
kind delete clusters kind

# MultiKueue (manager + two workers)
kind delete clusters kind kind-manager kind-worker1 kind-worker2
```

### Avoid deleting your default `kind` cluster

If you use `kind` for other work, set `KIND_CLUSTER_NAME=kueue-dev` (or similar) so the suite doesn't manage your default cluster.

```shell
KIND_CLUSTER_NAME=kueue-dev E2E_MODE=dev make kind-image-build test-e2e-baseline
```

### Debugging metrics

To bring up a Kind cluster with Prometheus already wired in for metrics debugging:

```shell
E2E_MODE=dev GINKGO_ARGS="--label-filter=feature:prometheus" make kind-image-build test-e2e-baseline
```

See [[metrics]] for what's exposed.

### Legacy (historical): interactive attach mode

Before `E2E_MODE=dev`, the way to keep a cluster for manual investigation was the following. This is historical: neither `E2E_RUN_ONLY_ENV` nor `test-multikueue-e2e-main` is wired up at kueue@3bbb8cce4.

```shell
E2E_RUN_ONLY_ENV=true make kind-image-build test-multikueue-e2e-main
# ...wait for "Do you want to cleanup? [Y/n]" prompt to appear...
# Now, from another terminal, run the specs you care about:
./bin/ginkgo --json-report ./ginkgo.report \
    -focus "MultiKueue when Creating a multikueue admission check Should run a jobSet on worker if admitted" \
    -r ./test/e2e/multikueue
```

`E2E_RUN_ONLY_ENV` is still documented in the site guide but is not read by any `hack/testing` script at kueue@3bbb8cce4; use `E2E_MODE=dev`.

## The full MultiKueue invocation

`make test-multikueue-e2e-baseline` / `-extended` expand (via `run-test-multikueue-e2e-baseline-%` / `run-test-multikueue-e2e-extended-%` in `hack/make/test.mk`) into `hack/testing/e2e-multikueue-test.sh` with a specific environment; today the recipe also passes `E2E_TARGET_FOLDER` and `E2E_CONFIG_FOLDER` (e.g. `multikueue/baseline`). The exact invocation at the time of [[issue-10200]], when MultiKueue was still one suite:

```shell
E2E_KIND_VERSION="kindest/node:v1.35.0" KIND_CLUSTER_NAME=kind \
  ARTIFACTS="/logs/artifacts/run-test-multikueue-e2e-1.35.0" \
  IMAGE_TAG=us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.18.0-devel-6-gf973c9168 \
  GINKGO_ARGS="" \
  E2E_MODE=ci \
  E2E_SKIP_REINSTALL=false \
  E2E_ENFORCE_OPERATOR_UPDATE=false \
  APPWRAPPER_VERSION=v1.2.0 \
  JOBSET_VERSION=v0.11.1 KUBEFLOW_VERSION=v1.9.3 \
  KUBEFLOW_MPI_VERSION=v0.8.0 \
  KUBERAY_VERSION=v1.6.0 RAY_VERSION=2.41.0 RAYMINI_VERSION=0.0.1 USE_RAY_FOR_TESTS="raymini" \
  KUBEFLOW_TRAINER_VERSION=v2.2.0 \
  LEADERWORKERSET_VERSION=v0.8.0 \
  CLUSTERPROFILE_VERSION=v0.0.0-20251124125836-445319b6307a \
  CLUSTERPROFILE_PLUGIN_IMAGE_VERSION=0.0.1 \
  TEST_LOG_LEVEL=-3 \
  E2E_RUN_ONLY_ENV=false \
  E2E_USE_HELM=false \
  ./hack/testing/e2e-multikueue-test.sh
```

Which eventually runs:

```shell
./bin/ginkgo run --junit-report=junit.xml --json-report=e2e.json \
  --output-dir=/logs/artifacts/run-test-multikueue-e2e-1.35.0 \
  -v ./test/e2e/multikueue/...
```

In practice you don't call the script directly — `make test-multikueue-e2e-baseline` fills in the versions from `hack/make/deps.mk`. Reach for the raw invocation when you need to pin a non-default version of a dependency (e.g. reproduce a bug with JobSet `v0.10.x`).

## Parallelization

`E2E_NPROCS` controls Ginkgo `-procs`. Defaults in `hack/make/test.mk`:

- `test-e2e-baseline` / `test-e2e-extended`: `E2E_NPROCS=4` (`test-e2e-extended-shard-2`: 2).
- `test-multikueue-e2e-baseline` / `-extended`: `E2E_NPROCS=5` (`-extended-ray-autoscaling`: 3).
- Everything else: `E2E_NPROCS=1` (sequential).

Cluster-scoped object names are suffixed per parallel worker; namespaces are created per spec. Tests that *cannot* safely run in parallel (disruptive operator restarts, controller re-deploys) live under `test/e2e/multikueue/sequential/` and run via `make test-multikueue-e2e-sequential` ([[issue-10200]]).

## Extra images for MultiKueue suites

`test-multikueue-e2e-sequential` depends on `kind-secretreader-plugin-image-build`, which builds the secretreader plugin image. The Ray-mini image is built by `kind-ray-project-mini-image-build` (top-level `Makefile`). There is no `test-multikueue-e2e-parallel-builds` target at kueue@3bbb8cce4.

## Flake patterns

### 10-second `Eventually` too tight

The e2e analogue of the integration pattern. [[issue-6525]] — "MultiKueue when Incremental mode Should run a job on worker if admitted" flaked on a 10-s timeout for an `AdmissionCheckState` transition. Fix: bump to `LongTimeout` (90 s). Quote from the incident: *"This failed on 10s timeout, which often isn't enough for e2e tests when the machines are under load. So, I would probably suggest to just bump timeout to LongTimeout and see if this repeats."*

### Visibility server race on small polls

[[issue-3044]] — `pull-kueue-test-e2e-main-1-31`: "Should allow fetching information about pending workloads in LocalQueue" timed out on a 5-s `Eventually`. Visibility API has its own latency profile; assertions on it should use `MediumTimeout` at minimum.

### Disruptive specs in a parallel suite

[[issue-10200]] — When new MultiKueue specs were added to the parallel suite without awareness of disruptive ones, total runtime climbed and flake rate rose. Disruptive specs go to `test/e2e/multikueue/sequential/`. Mark a new spec with `Disruptive` (and add a label filter) if it restarts operators, reconfigures webhooks, or otherwise mutates shared state.

## Reproducing CI failures locally

1. **Copy the CI invocation.** Open the Prow URL (`https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/<PR>/<job>/<run>`) and scroll down to find the exact env vars passed to `./hack/testing/e2e-*.sh`. Reproduce locally with the same versions.
2. **Collect controller logs.** In e2e, Kueue runs as two controller replicas. Logs are at `kind-worker/pods/kueue-system_kueue-controller-manager*/manager/` and `kind-worker2/...`. Each log line includes `file:line`, e.g. `core/clusterqueue_controller.go:341`.
3. **Add CPU pressure.** `sudo apt install stress && /usr/bin/stress --cpu 80` alongside the test emulates Prow's resource pressure and surfaces timeout issues faster.
4. **Repeat.** `GINKGO_ARGS="--repeat=10"` or `--until-it-fails`.

Bot rerun commands (in the PR):

- `/test pull-kueue-test-e2e-main-1-35` — rerun one job ([[pr-5414]]).
- `/retest` — rerun all failed required.
- `/retest-required` — same, gated.

## Related pages

- [[testing]] — the landing page.
- [[testing-integration]] — the cheaper tier.
- [[multikueue]] — the feature exercised by the multikueue e2e suites.
- [[topology-aware-scheduling]] — exercised by `test-tas-e2e-baseline` / `test-tas-e2e-extended`.
- [[dashboard]] — the KueueViz UI exercised by `test-e2e-kueueviz`.
- [[feature-gates]] — what the sequential (customconfigs) suites toggle.
