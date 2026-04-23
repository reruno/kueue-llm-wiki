# Issue #3957: ProvisioningRequest is created before its PodTemplates, what may cause Cluster Autoscaler to mark it as failed

**Summary**: ProvisioningRequest is created before its PodTemplates, what may cause Cluster Autoscaler to mark it as failed

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3957

**Last updated**: 2025-02-03T16:16:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@macsko](https://github.com/macsko)
- **Created**: 2025-01-10T14:47:58Z
- **Updated**: 2025-02-03T16:16:58Z
- **Closed**: 2025-02-03T16:16:58Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

When creating a ProvisioningRequest for workloads, Kueue creates the corresponding PodTemplates **after** provreq. Meanwhile, Cluster Autoscaler may try to process the ProvisioningRequest, but due to the lack of PodTemplates in the cluster, it marks the provreq as failed.

**What you expected to happen**:

Create PodTemplates first. Its ownerReference could be updated after creating a ProvisioningRequest.

**How to reproduce it (as minimally and precisely as possible)**:

Have OSS Cluster Autoscaler enabled in the cluster and create many provreq workloads using Kueue. Some of them could potentially be marked as failed.

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

### Comment by [@macsko](https://github.com/macsko) — 2025-01-10T14:48:06Z

cc @PBundyra

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-01-13T09:41:19Z

/assign @mbobrovskyi
