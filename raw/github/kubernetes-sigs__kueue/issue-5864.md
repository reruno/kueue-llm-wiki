# Issue #5864: [Flake] Preemption integration test failed due to invalid cleanup

**Summary**: [Flake] Preemption integration test failed due to invalid cleanup

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5864

**Last updated**: 2025-07-03T12:39:27Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-07-03T11:23:02Z
- **Updated**: 2025-07-03T12:39:27Z
- **Closed**: 2025-07-03T12:39:27Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**:
Integration test failed:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5861/pull-kueue-test-integration-baseline-main/1940724672173707264

**What you expected to happen**:
No failure

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-07-03T11:23:08Z

/kind flake
