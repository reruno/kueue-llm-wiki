# Issue #3486: Installing 0.9.0 has some warnings around multikueue

**Summary**: Installing 0.9.0 has some warnings around multikueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3486

**Last updated**: 2024-11-07T16:44:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2024-11-07T16:40:15Z
- **Updated**: 2024-11-07T16:44:28Z
- **Closed**: 2024-11-07T16:44:28Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
I ran `kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.9.0/manifests.yaml` and I see the following warnings:

```
Error from server (Invalid): CustomResourceDefinition.apiextensions.k8s.io "multikueueclusters.kueue.x-k8s.io" is invalid: status.storedVersions[0]: Invalid value: "v1alpha1": must appear in spec.versions
Error from server (Invalid): CustomResourceDefinition.apiextensions.k8s.io "multikueueconfigs.kueue.x-k8s.io" is invalid: status.storedVersions[0]: Invalid value: "v1alpha1": must appear in spec.versions
```
**What you expected to happen**:

I don't expect to see this warnings.

**How to reproduce it (as minimally and precisely as possible)**:
Install Kueue 0.9.0 (ie kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.9.0/manifests.yaml)
**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): 1.31
- Kueue version (use `git describe --tags --dirty --always`): 0.9.0
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2024-11-07T16:44:28Z

/close

This may have been a user error.
