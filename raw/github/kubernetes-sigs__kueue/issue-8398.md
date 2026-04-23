# Issue #8398: Flaky Test: Failed to build images at main branch

**Summary**: Flaky Test: Failed to build images at main branch

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8398

**Last updated**: 2025-12-24T02:44:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-12-23T17:12:05Z
- **Updated**: 2025-12-24T02:44:32Z
- **Closed**: 2025-12-24T02:44:32Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Building images at the main branch is always failing after we merge https://github.com/kubernetes-sigs/kueue/pull/8369

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/post-kueue-push-images/2002021275274317824

```shell
go: downloading google.golang.org/genproto/googleapis/rpc v0.0.0-20250303144028-a0af3efb3deb
DEST_CHART_DIR= \
HELM="/workspace/bin/helm" YQ="/workspace/bin/yq" GIT_TAG="v0.16.0-devel-151-g4722f21b" IMAGE_REGISTRY="us-central1-docker.pkg.dev/k8s-staging-images/kueue" \
HELM_CHART_PUSH=true \
./hack/helm-chart-package.sh
rm: can't remove 'cmd/experimental/kueue-populator/charts/kueue-populator/charts': No such file or directory
make: *** [Makefile:319: helm-chart-package] Error 1
ERROR
ERROR: build step 0 "gcr.io/k8s-staging-test-infra/gcb-docker-gcloud:v20250513-9264efb079" failed: step exited with non-zero status: 2
--------------------------------------------------------------------------------
```

**What you expected to happen**:
No errors

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-12-23T17:13:03Z

cc @mbobrovskyi

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-12-23T17:13:38Z

/kind flake
