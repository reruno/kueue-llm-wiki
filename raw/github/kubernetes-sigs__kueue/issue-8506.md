# Issue #8506: LWS RBACs are missing

**Summary**: LWS RBACs are missing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8506

**Last updated**: 2026-01-10T03:49:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2026-01-09T17:17:03Z
- **Updated**: 2026-01-10T03:49:39Z
- **Closed**: 2026-01-10T03:49:39Z
- **Labels**: `kind/bug`
- **Assignees**: [@kannon92](https://github.com/kannon92)
- **Comments**: 3

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**:

The released artifacts do not have RBACs for LWS:

- https://github.com/kubernetes-sigs/kueue/tree/main/config/components/rbac
- https://github.com/kubernetes-sigs/kueue/tree/main/charts/kueue/templates/rbac

**What you expected to happen**:

The same as other integrations, LWS RBAC manifests are published.

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-09T17:17:25Z

Thank you for reporting this problem @Huang-Wei 👍

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-09T17:39:37Z

Thank you for reporting! It would be great to fix for the next patch releases

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-09T20:52:45Z

/assign

Opened up #8513
