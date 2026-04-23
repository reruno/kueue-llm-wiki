# Issue #2208: Deleted Pending Pods count as active in Pod Groups

**Summary**: Deleted Pending Pods count as active in Pod Groups

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2208

**Last updated**: 2024-05-17T14:54:22Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-05-15T20:29:24Z
- **Updated**: 2024-05-17T14:54:22Z
- **Closed**: 2024-05-17T14:54:22Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 1

## Description

**What happened**:

A Pending Pod (a Pod that doesn't have a scheduling gate, but it never got scheduled) is still considered as an "active" pod that cannot yet be replaced.

https://github.com/kubernetes-sigs/kueue/blob/eaa43d3f81050913826fa341b976e00b92832337/pkg/controller/jobs/pod/pod_controller.go#L731

**What you expected to happen**:

A replacement Pod for a Pod that never got scheduled should be allowed to run

**How to reproduce it (as minimally and precisely as possible)**:

1. Create a Pod, part of a pod group, with an unsatisfiable node-selector
2. Wait for the group to be admitted.
3. Delete the Pod manually
4. Create a replacement Pod (this Pod should not be deleted)

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-15T20:29:38Z

/assign @trasc
