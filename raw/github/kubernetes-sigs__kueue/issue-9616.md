# Issue #9616: Terminate forever pending pods for node replacement

**Summary**: Terminate forever pending pods for node replacement

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9616

**Last updated**: 2026-03-18T10:16:38Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@j-skiba](https://github.com/j-skiba)
- **Created**: 2026-03-02T07:31:37Z
- **Updated**: 2026-03-18T10:16:38Z
- **Closed**: 2026-03-18T10:16:38Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 0

## Description

**What happened**:

After pods are assigned to some node by topology assignment and before are ungated (and given `nodeSelector` for that specific node) it might happen that in between these two events a node can be tainted or become `NotReady`. In such scenario these pods would be stuck in `Pending` state as they are bound to a node by `nodeSelector` but will not be scheduled on a node because of a taint or `NotReady` condition.

 Pods would be stuck like this and replacement pods would not be created because the existing pending pods are still waiting to be scheduled.

That is necessary for node replacement mechanism to work as expected. Currently topology assignment for a workload will be updated but the pods will stay `Pending` forever until deleted manually.

**What you expected to happen**:

We should handle such pods as described here - https://github.com/kubernetes-sigs/kueue/blob/main/keps/2724-topology-aware-scheduling/README.md#tainted-nodes-treatment

**How to reproduce it (as minimally and precisely as possible)**:

https://github.com/kubernetes-sigs/kueue/pull/9615 - shown here as an e2e test

**Anything else we need to know?**:
---

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:
