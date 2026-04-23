# Issue #601: New controller-runtime broke support for FieldOwner in status updates

**Summary**: New controller-runtime broke support for FieldOwner in status updates

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/601

**Last updated**: 2023-03-03T16:46:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-03-02T22:25:22Z
- **Updated**: 2023-03-03T16:46:59Z
- **Closed**: 2023-03-03T16:46:59Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 1

## Description

**What happened**:

https://github.com/kubernetes-sigs/controller-runtime/issues/2204

**What you expected to happen**:



**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

This is blocking #532, which moves the admission field to the status.
Maybe we need to revert #588, but that sounds big.
Maybe a patch to controller-runtime isn't that big.

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-02T22:26:09Z

cc @kerthcet
