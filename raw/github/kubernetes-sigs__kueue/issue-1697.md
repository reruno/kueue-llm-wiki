# Issue #1697: Kueue assumes Pods with different names of volumes belong to different pod groups

**Summary**: Kueue assumes Pods with different names of volumes belong to different pod groups

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1697

**Last updated**: 2024-02-07T17:30:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@nstogner](https://github.com/nstogner)
- **Created**: 2024-02-06T16:28:13Z
- **Updated**: 2024-02-07T17:30:58Z
- **Closed**: 2024-02-07T17:30:58Z
- **Labels**: `kind/bug`
- **Assignees**: [@nstogner](https://github.com/nstogner)
- **Comments**: 1

## Description

**What happened**:

Created 9 pods in a pod group of size 8. Kueue failed to a create the Workload object because it thought each pod was a different pod set. Kueue appears to have a max pod set size of 8: https://github.com/kubernetes-sigs/kueue/blob/892d85c35a94c875005d6b547710ad06704bccf9/pkg/controller/jobs/pod/pod_controller.go#L885

Each pod had a different role hash. It appears that this is due to each pod having a different PVC name specified in `.spec.volumes`.

**What you expected to happen**:

I would expect Kueue to ignore PVC volume names or volumes altogether and treat the 9 pods as having the same role (being in the same pod set). See: https://github.com/kubernetes-sigs/kueue/blob/892d85c35a94c875005d6b547710ad06704bccf9/pkg/controller/jobs/pod/pod_controller.go#L565

**How to reproduce it (as minimally and precisely as possible)**:

Follow the steps above, using a different PVC name in the volumes array for each pod. Make sure to use N > 8 for pod group size. Make sure Kueue is configured to support raw pods. Assert that the Workload never gets created. The pods should remain in a ScheduleGated state.

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): NA
- Kueue version (use `git describe --tags --dirty --always`): v0.6.0-rc.1
- Cloud provider or hardware configuration: NA
- OS (e.g: `cat /etc/os-release`): A
- Kernel (e.g. `uname -a`): NA
- Install tools: NA
- Others: NA

## Discussion

### Comment by [@nstogner](https://github.com/nstogner) — 2024-02-06T16:30:37Z

/assign
