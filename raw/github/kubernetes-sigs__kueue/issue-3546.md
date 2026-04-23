# Issue #3546: [Flaky e2e] StatefulSet integration when StatefulSet created should allow to scale up after scale down to zero.

**Summary**: [Flaky e2e] StatefulSet integration when StatefulSet created should allow to scale up after scale down to zero.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3546

**Last updated**: 2024-11-15T17:38:53Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-11-15T13:12:22Z
- **Updated**: 2024-11-15T17:38:53Z
- **Closed**: 2024-11-15T17:38:53Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 0

## Description

/kind flake

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
End To End Suite: kindest/node:v1.30.0: [It] StatefulSet integration when StatefulSet created should allow to scale up after scale down to zero

**What you expected to happen**:
No random failures

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3539/pull-kueue-test-e2e-main-1-30/1857384106699001856

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:
