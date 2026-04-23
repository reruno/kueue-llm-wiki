# Issue #1654: Restarting controller manager admits all workloads

**Summary**: Restarting controller manager admits all workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1654

**Last updated**: 2024-02-07T16:09:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kchopra456](https://github.com/kchopra456)
- **Created**: 2024-01-26T14:12:17Z
- **Updated**: 2024-02-07T16:09:32Z
- **Closed**: 2024-02-07T16:09:32Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 2

## Description

**What happened**:
- Restarting Kueue controller (_common occurence when leader election fails_), admits all previously **finished workloads**.

**What you expected to happen**:
- `Finished workloads`, must not be queued and admitted to Q and CQ.

**How to reproduce it (as minimally and precisely as possible)**:
1. Submit 2 jobs, with `sleep 5; exit 0` and `sleep 5; exit 1`, one job suceeds and other fails.
2. Both the workloads are marked as `Finished`.
3. Rollout restart to the Kueue controller, and both the workloads will be re-admitted, though the workloads are marked `Finished`.
4. Q resources are never released, until the workloads are deleted.

**Anything else we need to know?**:
Log attached.
[manager-001.log](https://github.com/kubernetes-sigs/kueue/files/14065802/manager-001.log)

**Environment**:
- Kubernetes version (use `kubectl version`): 1.27.0
- Kueue version (use `git describe --tags --dirty --always`): v0.5.0, v0.5.1, v0.5.2, v0.6.0-rc.1
- Cloud provider or hardware configuration: minikube
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@kchopra456](https://github.com/kchopra456) — 2024-01-26T14:17:00Z

Related comment - https://github.com/kubernetes-sigs/kueue/issues/1450#issuecomment-1887308576
Helped but does not solve the issue - https://github.com/kubernetes-sigs/kueue/pull/1572

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-05T14:48:49Z

/assign @trasc
