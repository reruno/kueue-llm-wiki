# Issue #929: Workload yaml in documentation doesn't work

**Summary**: Workload yaml in documentation doesn't work

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/929

**Last updated**: 2023-06-29T15:15:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-06-29T14:42:14Z
- **Updated**: 2023-06-29T15:15:39Z
- **Closed**: 2023-06-29T15:15:39Z
- **Labels**: `kind/bug`
- **Assignees**: [@stuton](https://github.com/stuton)
- **Comments**: 1

## Description

**What happened**:

https://kueue.sigs.k8s.io/docs/concepts/workload/

The `spec` field doesn't exist. It should be inside `template`

**What you expected to happen**:

Example to pass validation

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

Users are not expected to create Workload objects, but this could confuse anybody trying to integrate with kueue.

When updating this, make sure the yaml passes validation

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@stuton](https://github.com/stuton) — 2023-06-29T14:47:55Z

/assign
