# Issue #2117: It seems like the wrong function is being used when a multiKueueCluster is created

**Summary**: It seems like the wrong function is being used when a multiKueueCluster is created

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2117

**Last updated**: 2024-05-08T18:48:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@leprode](https://github.com/leprode)
- **Created**: 2024-05-03T00:45:30Z
- **Updated**: 2024-05-08T18:48:55Z
- **Closed**: 2024-05-08T18:48:55Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
when a multiKueueCluster is created, the function named **queueReconcileForConfigUsers** is used directly in admissioncheck.go#L270

**What you expected to happen**:
the function named **queue**(admissioncheck.go#L313) should be used, then the function named **queueReconcileForConfigUsers** used in queue function.

**How to reproduce it (as minimally and precisely as possible)**:
when a multiKueueCluster is created

**Anything else we need to know?**:
https://github.com/kubernetes-sigs/kueue/blob/43e5eb8ee19fe69d3dd3f03c13f4ad46b77dd094/pkg/controller/admissionchecks/multikueue/admissioncheck.go#L264-L273

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2024-05-08T16:40:26Z

Thanks @leprode 

/assign
