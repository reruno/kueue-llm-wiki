# Issue #951: Flaky test: Reclaimed resources are not accounted during admission

**Summary**: Flaky test: Reclaimed resources are not accounted during admission

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/951

**Last updated**: 2023-07-06T11:59:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-07-05T21:12:21Z
- **Updated**: 2023-07-06T11:59:05Z
- **Closed**: 2023-07-06T11:59:05Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 1

## Description

**What happened**:

The test `Scheduler when Scheduling workloads on clusterQueues Reclaimed resources are not accounted during admission ` is flaky

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/949/pull-kueue-test-integration-main/1676696996531933184

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-05T21:12:29Z

/assign @trasc
