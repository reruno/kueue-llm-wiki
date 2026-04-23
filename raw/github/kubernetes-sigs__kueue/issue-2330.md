# Issue #2330: Unknown fields in the Configuration API are silently ignored

**Summary**: Unknown fields in the Configuration API are silently ignored

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2330

**Last updated**: 2024-06-06T18:46:22Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-05-30T14:28:53Z
- **Updated**: 2024-06-06T18:46:22Z
- **Closed**: 2024-06-06T18:46:22Z
- **Labels**: `kind/bug`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 1

## Description

**What happened**:

If you start Kueue with a Configuration containing fields that don't exist, Kueue starts normally.

**What you expected to happen**:

Kueue startup to fail, guarding users from typos.

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-30T14:29:03Z

/assign @IrvingMg
