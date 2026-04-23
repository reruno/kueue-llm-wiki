# Issue #8362: KueuePopulator lock for helm charts complicates the release steps

**Summary**: KueuePopulator lock for helm charts complicates the release steps

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8362

**Last updated**: 2025-12-19T14:20:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-19T10:53:48Z
- **Updated**: 2025-12-19T14:20:41Z
- **Closed**: 2025-12-19T14:20:41Z
- **Labels**: `kind/bug`, `priority/important-soon`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

When following the release script I hit this issue:

```
❯ make artifacts IMAGE_REGISTRY=registry.k8s.io/kueue GIT_TAG=$VERSION
if [ -d artifacts ]; then rm -rf artifacts; fi
DEST_CHART_DIR="artifacts" \
HELM="/usr/local/google/home/michalwozniak/go/src/sigs.k8s.io/kueue/bin/helm" YQ="/usr/local/google/home/michalwozniak/go/src/sigs.k8s.io/kueue/bin/yq" GIT_TAG="v0.15.2" IMAGE_REGISTRY="registry.k8s.io/kueue" \
HELM_CHART_PUSH= \
./hack/helm-chart-package.sh
Successfully packaged chart and saved it to: artifacts/kueue-0.15.2.tgz
Error: the lock file (Chart.lock) is out of sync with the dependencies file (Chart.yaml). Please update the dependencies
make: *** [Makefile:317: helm-chart-package] Error 1

```
and I need to manually remove the Chart.lock file


**What you expected to happen**:

No need to manually remove it

**How to reproduce it (as minimally and precisely as possible)**:

Follow the release steps.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:54:03Z

/priority important-soon
cc @mbobrovskyi @j-skiba
