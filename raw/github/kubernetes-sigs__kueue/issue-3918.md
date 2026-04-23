# Issue #3918: Make the visibility server lightweight

**Summary**: Make the visibility server lightweight

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3918

**Last updated**: 2025-01-03T18:46:17Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@varshaprasad96](https://github.com/varshaprasad96)
- **Created**: 2025-01-02T11:27:28Z
- **Updated**: 2025-01-03T18:46:17Z
- **Closed**: 2025-01-03T18:46:16Z
- **Labels**: `kind/bug`
- **Assignees**: [@varshaprasad96](https://github.com/varshaprasad96)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

Follow up from: https://github.com/kubernetes-sigs/kueue/pull/3908#issue-2756645658

Remove the default APIs enabled in the visibility server and keep it lightweight. The ones that would be required are - NamespaceLifecycle, ServiceAccount plugins. 

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@varshaprasad96](https://github.com/varshaprasad96) — 2025-01-02T11:27:38Z

/assign @varshaprasad96
