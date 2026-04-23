# Issue #6738: Workload re-evaluation

**Summary**: Workload re-evaluation

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6738

**Last updated**: 2025-10-23T06:54:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ravisantoshgudimetla](https://github.com/ravisantoshgudimetla)
- **Created**: 2025-09-07T03:38:06Z
- **Updated**: 2025-10-23T06:54:40Z
- **Closed**: 2025-10-23T06:54:40Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Existing workloads are not re-evaluated
when new clusters are added to MultiKueueConfig. 

**What you expected to happen**:
When new clusters are added, existing workloads should be evaluated.

**How to reproduce it (as minimally and precisely as possible)**:
https://github.com/kubernetes-sigs/kueue/pull/6732

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:
