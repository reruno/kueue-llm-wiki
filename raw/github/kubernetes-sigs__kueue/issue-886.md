# Issue #886: Flaky test TestWaitForPodsReadyCancelled

**Summary**: Flaky test TestWaitForPodsReadyCancelled

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/886

**Last updated**: 2023-07-06T16:23:06Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@bh-tt](https://github.com/bh-tt)
- **Created**: 2023-06-22T07:52:51Z
- **Updated**: 2023-07-06T16:23:06Z
- **Closed**: 2023-07-06T16:23:06Z
- **Labels**: `kind/bug`, `priority/important-soon`
- **Assignees**: [@stuton](https://github.com/stuton)
- **Comments**: 3

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Test failed during PR #878, retry worked.
**What you expected to happen**:
The test to succeed.
**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/878/pull-kueue-test-unit-main/1671583007175086080
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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-22T12:34:36Z

/assign @trasc

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-22T12:35:00Z

/priority important-soon

### Comment by [@stuton](https://github.com/stuton) — 2023-06-23T13:49:08Z

/assign
