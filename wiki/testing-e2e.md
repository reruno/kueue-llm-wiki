# E2E tests

**Summary**: E2E tests run Kueue against a real (Kind-based) Kubernetes cluster, with any external operators (JobSet, KubeRay, Kubeflow Training, LeaderWorkerSet, AppWrapper, cert-manager, Prometheus Operator) installed alongside. This page covers the per-suite matrix, the dev-mode Kind lifecycle (`E2E_MODE=dev`), the full MultiKueue invocation recipe, and flake patterns specific to e2e.

**Sources**: `raw/kueue/Makefile-test.mk`, `raw/kueue/hack/testing/e2e-common.sh`, `raw/kueue/hack/testing/e2e-test.sh`, `raw/kueue/hack/testing/e2e-multikueue-test.sh`, `raw/kueue/test/e2e/`, `raw/kueue/site/content/en/docs/contribution_guidelines/testing.md`; `raw/github/kubernetes-sigs__kueue/` — [[issue-3044]], [[issue-6525]], [[issue-10200]], [[pr-5414]].

**Last updated**: 2026-04-23

---

## What e2e covers that integration doesn't

- Real `kubelet` + real `kube-scheduler`. Pod placement actually happens.
- External operator reconciliation — JobSet, KubeRay, Kubeflow Training, LeaderWorkerSet, AppWrapper, cert-manager, Prometheus Operator are installed and run.
- Image loading, RBAC, CRD apply paths — things that are bypassed by envtest.
- Upgrade / downgrade behavior (the `upgrade` suite installs a prior release, then upgrades to the current build).

Because each e2e suite spins up its own Kind cluster(s), each suite is expensive. The MultiKueue suite was ~19 min sequential / ~22 min parallel when it was last benchmarked ([[issue-10200]]).

## Suite matrix

Every target below is in `Makefile-test.mk`. All of them run via `hack/testing/e2e-test.sh` or `hack/testing/e2e-multikueue-test.sh`.

| Make target | E2E folder | What it covers |
|---|---|---|
| `test-e2e` | `test/e2e/singlecluster/` | Baseline singlecluster e2e. |
| `test-multikueue-e2e-main` | `test/e2e/multikueue/` | Manager + worker Kind clusters; [[multikueue]] dispatch flow. The site-docs form `test-multikueue-e2e` is not defined in the current `Makefile-test.mk`; use `-main` explicitly. |
| `test-multikueue-e2e-sequential` | `test/e2e/multikueuesequential/` | Disruptive MultiKueue specs that cannot run in parallel ([[issue-10200]]). |
| `test-e2e-multikueue-dra` | `test/e2e/multikueuedra/` | MultiKueue + DynamicResourceAllocation. |
| `test-tas-e2e` | `test/e2e/tas/` | Topology-aware scheduling end-to-end; uses `kind-cluster-tas.yaml`. |
| `test-e2e-dra` | `test/e2e/dra/` | DRA support path. |
| `test-e2e-certmanager` | `test/e2e/certmanager/` | cert-manager-backed webhooks. |
| `test-e2e-certmanager-upgrade` | `test/e2e/upgrade/` | cert-manager + upgrade. |
| `test-e2e-sequential-baseline` | `test/e2e/sequential/baseline/` | Non-default `configuration.kueue.x-k8s.io` Kueue configurations (baseline set). |
| `test-e2e-sequential-extended` | `test/e2e/sequential/extended/` | The same, extended set (includes Spark). |
| `test-e2e-customconfigs` | — | Aggregate target; runs the two `sequential-*` targets above. |
| `test-e2e-upgrade` | `test/e2e/upgrade/` | Install `KUEUE_UPGRADE_FROM_VERSION` (default `v0.14.8`) first, then upgrade to the current build. |
| `test-e2e-kueueviz` / `test-e2e-kueueviz-local` | `test/e2e/kueueviz/` | KueueViz UI end-to-end; runs Cypress against a real browser. See [[dashboard]]. |
| `test-e2e-k8s-main-was` | `test/e2e/singlecluster/` | Same as `test-e2e` but against a kind node image built from k/k `main` with `WAS_ENABLED=true`. |

Add `-helm` to any supported target (`test-e2e-helm`, `test-tas-e2e-helm`, `test-multikueue-e2e-helm`, `test-e2e-sequential-baseline-helm`, `test-e2e-sequential-extended-helm`) to install via Helm instead of kustomize. Or set `E2E_USE_HELM=true`.

## Running an e2e suite

Typical first-time singlecluster run:

```shell
make kind-image-build   # build the controller image with the current source
make test-e2e           # creates cluster, runs tests, deletes cluster
```

Pick a k8s version (from `E2E_K8S_VERSIONS` — currently `1.33.7 1.34.3 1.35.0`):

```shell
E2E_K8S_FULL_VERSION=1.34.3 make test-e2e
```

Use a released image instead of rebuilding:

```shell
IMAGE_TAG=registry.k8s.io/kueue/kueue:v0.16.0 make test-e2e
# or a staging image from a PR
IMAGE_TAG=us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:main make test-e2e
```

To reproduce a bug against an exact release, also `git checkout v0.16.0` first — CRDs and deployment manifests come from the checkout, only the controller image is overridden by `IMAGE_TAG`.

Focus a subset:

```shell
GINKGO_ARGS="--label-filter=feature:jobset" make test-e2e
GINKGO_ARGS="--label-filter=feature:jobset,feature:trainjob" make test-e2e
GINKGO_ARGS="--focus='Creating a Pod requesting TAS'" make test-tas-e2e
GINKGO_ARGS="--label-filter=feature:admissionfairsharing" make test-e2e-sequential-baseline
GINKGO_ARGS="--label-filter=feature:spark" make test-e2e-sequential-extended
```

### E2E singlecluster label taxonomy

`appwrapper, certs, deployment, job, fairsharing, jaxjob, jobset, kuberay, kueuectl, leaderworkerset, metrics, pod, pytorchjob, statefulset, tas, trainjob, visibility, e2e_v1beta1` (source: `Makefile-test.mk`).

### E2E customconfigs label taxonomy

- Baseline: `admissionfairsharing, certs, failurerecoverypolicy, localqueuemetrics, objectretentionpolicies, podintegrationautoenablement, reconcile, visibility, waitforpodsready`.
- Extended: `managejobswithoutqueuename, spark`.

## E2E_MODE — cluster lifecycle

`E2E_MODE` controls whether the suite runner creates, reuses, and/or deletes Kind clusters (defined in `hack/testing/e2e-common.sh`).

| `E2E_MODE` | Before the test | After the test |
|---|---|---|
| `ci` (default) | Create Kind cluster(s). | Delete Kind cluster(s). |
| `dev` | Create if missing, **reuse if existing**. | **Keep running.** |

`dev` is the mode contributors use locally. The canonical dev loop:

```shell
# First time — builds image, creates cluster, runs tests, keeps cluster
E2E_MODE=dev make kind-image-build test-e2e

# Subsequent iterations — rebuild image, redeploy Kueue, rerun tests, keep cluster
E2E_MODE=dev make kind-image-build test-e2e

# Repeat the run until it fails (for flake-hunting)
E2E_MODE=dev GINKGO_ARGS="--until-it-fails" make kind-image-build test-e2e

# Focus one spec, fast iteration
E2E_MODE=dev GINKGO_ARGS="--focus='MultiKueue should dispatch'" make kind-image-build test-multikueue-e2e-main
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
KIND_CLUSTER_NAME=kueue-dev E2E_MODE=dev make kind-image-build test-e2e
```

### Debugging metrics

To bring up a Kind cluster with Prometheus already wired in for metrics debugging:

```shell
E2E_MODE=dev GINKGO_ARGS="--label-filter=feature:prometheus" make kind-image-build test-e2e
```

See [[metrics]] for what's exposed.

### Legacy: interactive attach mode

Before `E2E_MODE=dev`, the way to keep a cluster for manual investigation was:

```shell
E2E_RUN_ONLY_ENV=true make kind-image-build test-multikueue-e2e-main
# ...wait for "Do you want to cleanup? [Y/n]" prompt to appear...
# Now, from another terminal, run the specs you care about:
./bin/ginkgo --json-report ./ginkgo.report \
    -focus "MultiKueue when Creating a multikueue admission check Should run a jobSet on worker if admitted" \
    -r ./test/e2e/multikueue
```

Prefer `E2E_MODE=dev` for new workflows; `E2E_RUN_ONLY_ENV=true` remains available for the VSCode Ginkgo Test Explorer attach pattern.

## The full MultiKueue invocation

`make test-multikueue-e2e-main` expands (via `run-test-multikueue-e2e-%` in `Makefile-test.mk`) into `hack/testing/e2e-multikueue-test.sh` with a specific environment. The exact invocation at the time of [[issue-10200]]:

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

In practice you don't call the script directly — `make test-multikueue-e2e-main` fills in the versions from `Makefile-deps.mk`. Reach for the raw invocation when you need to pin a non-default version of a dependency (e.g. reproduce a bug with JobSet `v0.10.x`).

## Parallelization

`E2E_NPROCS` controls Ginkgo `-procs`. Defaults in `Makefile-test.mk`:

- `test-e2e` (singlecluster): `E2E_NPROCS=4`.
- `test-multikueue-e2e-main`: `E2E_NPROCS=5`.
- Everything else: `E2E_NPROCS=1` (sequential).

Cluster-scoped object names are suffixed per parallel worker; namespaces are created per spec. Tests that *cannot* safely run in parallel (disruptive operator restarts, controller re-deploys) live under `test/e2e/multikueuesequential/` and run via `make test-multikueue-e2e-sequential` ([[issue-10200]]).

## Parallel builds for multi-image suites

MultiKueue e2e needs both a Ray-mini image and the secretreader plugin image. `test-multikueue-e2e-parallel-builds` builds them concurrently:

```shell
make test-multikueue-e2e-parallel-builds   # kind-ray-project-mini-image-build + kind-secretreader-plugin-image-build in parallel
```

This runs automatically as a dependency of `test-multikueue-e2e-main`.

## Flake patterns

### 10-second `Eventually` too tight

The e2e analogue of the integration pattern. [[issue-6525]] — "MultiKueue when Incremental mode Should run a job on worker if admitted" flaked on a 10-s timeout for an `AdmissionCheckState` transition. Fix: bump to `LongTimeout` (90 s). Quote from the incident: *"This failed on 10s timeout, which often isn't enough for e2e tests when the machines are under load. So, I would probably suggest to just bump timeout to LongTimeout and see if this repeats."*

### Visibility server race on small polls

[[issue-3044]] — `pull-kueue-test-e2e-main-1-31`: "Should allow fetching information about pending workloads in LocalQueue" timed out on a 5-s `Eventually`. Visibility API has its own latency profile; assertions on it should use `MediumTimeout` at minimum.

### Disruptive specs in a parallel suite

[[issue-10200]] — When new MultiKueue specs were added to the parallel suite without awareness of disruptive ones, total runtime climbed and flake rate rose. Disruptive specs go to `test/e2e/multikueuesequential/`. Mark a new spec with `Disruptive` (and add a label filter) if it restarts operators, reconfigures webhooks, or otherwise mutates shared state.

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
- [[topology-aware-scheduling]] — exercised by `test-tas-e2e`.
- [[dashboard]] — the KueueViz UI exercised by `test-e2e-kueueviz`.
- [[feature-gates]] — what the customconfigs suites toggle.
