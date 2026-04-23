# Issue #2051: Add the ProvisioningRequest's classname annotation to pods

**Summary**: Add the ProvisioningRequest's classname annotation to pods

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2051

**Last updated**: 2024-04-25T15:54:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-04-24T09:54:42Z
- **Updated**: 2024-04-25T15:54:37Z
- **Closed**: 2024-04-25T15:54:37Z
- **Labels**: `kind/feature`
- **Assignees**: [@PBundyra](https://github.com/PBundyra)
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Pods created by Kueue that use ProvisioningRequest lack the `cluster-autoscaler.kubernetes.io/provisioning-class-name` annotation

**What you expected to happen**:
Pods created by Kueue that use ProvisioningRequest to have the `cluster-autoscaler.kubernetes.io/provisioning-class-name` annotation

**How to reproduce it (as minimally and precisely as possible)**:
Create a Job that uses a ProvisioningRequest

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-04-24T10:05:13Z

/assign @PBundyra

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-24T16:35:03Z

Why is this necessary? Or is it just for information completeness?

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-04-25T12:24:24Z

It' ll be necessary to distinguish different ProvReq classes

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-25T15:16:52Z

From offline discussion, this is something that will be necessary as cluster-autoscaler is adding more engines

/remove-kind bug
/kind feature
