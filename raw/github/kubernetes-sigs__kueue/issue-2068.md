# Issue #2068: Support for sidecar containers

**Summary**: Support for sidecar containers

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2068

**Last updated**: 2024-05-07T15:11:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-04-25T17:15:39Z
- **Updated**: 2024-05-07T15:11:51Z
- **Closed**: 2024-05-07T15:11:50Z
- **Labels**: `kind/bug`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg), [@trasc](https://github.com/trasc)
- **Comments**: 3

## Description

**What happened**:

We are currently treating sidecar containers as regular initContainers. However, sidecar containers continue running until the pod completes https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/

Note that this feature is beta since kubernetes v1.29

**What you expected to happen**:

To account for the usage of sidecar containers.

**Anything else we need to know?**:

The function should look similar to this: https://github.com/kubernetes/kubernetes/blob/ae02f87bb47cd3e10e702ffe19225ff2dba73578/pkg/api/v1/resource/helpers.go#L50

However, we should not directly use that function, as it doesn't have stability guarantees and the kubernetes module might have non-trivial dependencies.

We could, in parallel, start a different effort to move this function to some other place more reusable, like https://github.com/kubernetes/kubernetes/tree/master/staging/src/k8s.io/component-helpers/scheduling

**Environment**:
- Kubernetes version (use `kubectl version`): v.129
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-25T17:15:56Z

/assign @trasc

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-25T17:26:10Z

I opened the issue upstream https://github.com/kubernetes/kubernetes/issues/124537

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2024-04-26T11:52:06Z

/assign
