# Issue #1265: Flaky -  Job controller when the queue has admission checks [It] labels and annotations should be propagated from admission check to job

**Summary**: Flaky -  Job controller when the queue has admission checks [It] labels and annotations should be propagated from admission check to job

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1265

**Last updated**: 2023-10-26T13:09:14Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@trasc](https://github.com/trasc)
- **Created**: 2023-10-26T09:55:09Z
- **Updated**: 2023-10-26T13:09:14Z
- **Closed**: 2023-10-26T13:09:14Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

[FAIL] Job controller when the queue has admission checks [It] labels and annotations should be propagated from admission check to job

**What you expected to happen**:

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/directory/pull-kueue-test-integration-main/1717459094870167552

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

### Comment by [@trasc](https://github.com/trasc) — 2023-10-26T09:55:24Z

/assign
