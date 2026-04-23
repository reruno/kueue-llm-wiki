# Issue #148: Pending workloads not updated in ClusterQueue status at creation

**Summary**: Pending workloads not updated in ClusterQueue status at creation

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/148

**Last updated**: 2022-03-25T19:16:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-03-24T15:43:19Z
- **Updated**: 2022-03-25T19:16:01Z
- **Closed**: 2022-03-25T19:16:01Z
- **Labels**: `kind/bug`
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor)
- **Comments**: 1

## Description

**What happened**:

When workloads are created, we are not updating the corresponding CQ status.


**What you expected to happen**:


The status to be up to date

**How to reproduce it (as minimally and precisely as possible)**:

Repro: https://github.com/alculquicondor/kueue/commit/1ae8618cb687956bcc6fc361ea839490164faa29

**Anything else we need to know?**:

This is because we are only queueing the clusterqueue for admitted workloads in assignedWorkloadHandler https://github.com/kubernetes-sigs/kueue/blob/27b05145f94ac528ff92790efc70d62d8c9feafc/pkg/controller/core/clusterqueue_controller.go#L145

**Environment**:
- Kueue version (use `git describe --tags --dirty --always`): main

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-24T21:07:47Z

/assign
