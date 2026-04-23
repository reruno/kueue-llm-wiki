# Issue #6763: [FairSharing] Preemption algorithm is non-deterministic leading to excessive preemption

**Summary**: [FairSharing] Preemption algorithm is non-deterministic leading to excessive preemption

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6763

**Last updated**: 2025-09-09T11:57:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-09-09T07:45:56Z
- **Updated**: 2025-09-09T11:57:30Z
- **Closed**: 2025-09-09T11:57:30Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
When there are two CQ that have equal DRS, FairSharing preemption algorithm picks one randomly ([based on the hash function in a set](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/cache/hierarchy/cohort.go#L45)). Since the algorithm is run over and over for the same preemptor until preemption actually executes this leads to excessive preemption, where a preemptor Workload preempts more Workloads than needed if they come from drawing ClusterQueues

**What you expected to happen**:
Make the preemption algorithm deterministic, ideally Workloads should be ordered by the same less function as across the codebase

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:
