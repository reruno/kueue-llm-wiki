# Issue #1557: Pod group: Replacement Pods should be added as Workload owners

**Summary**: Pod group: Replacement Pods should be added as Workload owners

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1557

**Last updated**: 2024-02-06T14:34:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-01-08T19:06:27Z
- **Updated**: 2024-02-06T14:34:16Z
- **Closed**: 2024-02-06T14:34:16Z
- **Labels**: `kind/bug`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 3

## Description

**What happened**:

When a Pod fails, it can be replaced with a new pod. However, the new pod doesn't become an owner of the Workload.

This could lead to a Workload from disappearing before all the Pod finalizers have been removed.

**What you expected to happen**:

The replacement Pod should be owner of the Workload. Excess pods should not be owners.

**How to reproduce it (as minimally and precisely as possible)**:

1. Create pod group
2. Fail one pod
3. Create replacement pod

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-08T19:06:32Z

cc @achernevskii

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-25T15:27:07Z

From @mimowo:

re-admitted workload gets deleted after completing. This is because the replacement pods don't become owners of the workload. So the workload gets deleted by garbage-collector very quickly

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-26T17:32:24Z

/assign
I would like to give it a try, continuing tasks related to pod groups
