# Issue #1352: Removing the pod leads to stucking

**Summary**: Removing the pod leads to stucking

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1352

**Last updated**: 2023-11-20T14:52:26Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@stuton](https://github.com/stuton)
- **Created**: 2023-11-20T14:29:14Z
- **Updated**: 2023-11-20T14:52:26Z
- **Closed**: 2023-11-20T14:52:26Z
- **Labels**: `kind/bug`
- **Assignees**: [@stuton](https://github.com/stuton)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
For single pod support in v0.5, we create a Pod pointing to a queue that didn't exist. Pod status is in status SchedulingGated. When we remove the Pod, the finalizer is not cleared. In other words, it was stuck.

**What you expected to happen**:

**How to reproduce it (as minimally and precisely as possible)**:
Install kueue-controller, set pod integration in configuration, create a pod with a queue that didn't exist

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

### Comment by [@stuton](https://github.com/stuton) — 2023-11-20T14:29:21Z

/assign

### Comment by [@stuton](https://github.com/stuton) — 2023-11-20T14:52:26Z

closed is duplicate #1339
