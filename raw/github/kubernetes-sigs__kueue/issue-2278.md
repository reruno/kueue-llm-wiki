# Issue #2278: Provisioning Admission Check doesn't consider limits

**Summary**: Provisioning Admission Check doesn't consider limits

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2278

**Last updated**: 2024-05-28T15:16:44Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-05-24T19:42:37Z
- **Updated**: 2024-05-28T15:16:44Z
- **Closed**: 2024-05-28T15:16:44Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

In k8s, requests is equal to limits when unset.

However, this check only considers the requests:

https://github.com/kubernetes-sigs/kueue/blob/fab6cfe507a3c91659d93355383f1c98fc7a7635/pkg/controller/admissionchecks/provisioning/controller.go#L419

**What you expected to happen**:

To consider the limits.

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-24T19:42:43Z

/assign @trasc
