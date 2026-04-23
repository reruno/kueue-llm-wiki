# Issue #840: Preemption should prioritize removing more recently admitted workloads first

**Summary**: Preemption should prioritize removing more recently admitted workloads first

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/840

**Last updated**: 2023-06-12T12:31:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-06-08T20:48:01Z
- **Updated**: 2023-06-12T12:31:51Z
- **Closed**: 2023-06-12T12:31:51Z
- **Labels**: `kind/bug`
- **Assignees**: [@stuton](https://github.com/stuton)
- **Comments**: 1

## Description

**What happened**:

Preemption is prioritizing jobs that were admitted earlier to be removed first.

**What you expected to happen**:

Jobs that were admitted later to be preempted.

**How to reproduce it (as minimally and precisely as possible)**:

setup two clusterqueues (A & B) with the same CPU nominalquota=40 as the limiting factor. I submit 40 jobs (workflow 1) into partition A to saturate its CPU nominalquota, then submit 10 jobs (workflow 2) to partition A to see the borrowing behavior. \
Then I submit 40 jobs (workflow 3) to partition B, saturating its nominal quota, and expecting Kueue to preempt 10 jobs from workflow 2 since it is the more recently admitted (than workflow 1)

**Anything else we need to know?**:

The intention was:

https://github.com/kubernetes-sigs/kueue/blob/2a74cb034e3e3adb6403444d6566d3d8ab2acf36/pkg/scheduler/preemption/preemption.go#L359

But the implementation is reversed:

https://github.com/kubernetes-sigs/kueue/blob/2a74cb034e3e3adb6403444d6566d3d8ab2acf36/pkg/scheduler/preemption/preemption.go#L374

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@stuton](https://github.com/stuton) — 2023-06-09T07:06:03Z

/assign
