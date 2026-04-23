# Issue #2149: Nil pointer dereference when handling the ProvisioningRequest's Accepted condition

**Summary**: Nil pointer dereference when handling the ProvisioningRequest's Accepted condition

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2149

**Last updated**: 2024-05-07T15:40:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-05-07T10:34:50Z
- **Updated**: 2024-05-07T15:40:58Z
- **Closed**: 2024-05-07T15:40:58Z
- **Labels**: `kind/bug`
- **Assignees**: [@pajakd](https://github.com/pajakd)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Kueue paniced because of nil pointer dereference. It tried to [dereference a nil pointer](https://github.com/kubernetes-sigs/kueue/blob/bd42edb21408a70d8e52c76ddc8713b78aedd966/pkg/controller/admissionchecks/provisioning/controller.go#L540), as the `autoscaling.Provisioned` condition was not present.

**What you expected to happen**:
Not panic

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-05-07T10:35:12Z

@pajakd  Could you take a look please?

### Comment by [@pajakd](https://github.com/pajakd) — 2024-05-07T12:45:29Z

/assign
