# Issue #6323: [ProvReq] Kueue doesnt recreate a ProvReq after second failed attempt

**Summary**: [ProvReq] Kueue doesnt recreate a ProvReq after second failed attempt

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6323

**Last updated**: 2025-07-31T14:59:20Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-07-31T11:22:59Z
- **Updated**: 2025-07-31T14:59:20Z
- **Closed**: 2025-07-31T14:59:20Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
When a ProvisioningRequest fails for the second time, Kueue doesnt recreate the ProvisioningRequest even with a large BackoffLimit

**What you expected to happen**:
Kueue to create a ProvisioningRequest as many times as configured

**How to reproduce it (as minimally and precisely as possible)**:
Is it reproduced by an integration test in the PR #6322  

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:
