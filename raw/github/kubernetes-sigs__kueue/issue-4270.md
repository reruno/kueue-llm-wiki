# Issue #4270: TAS: Incorrect Topology Assignment when topology allocatable Pods count are less than number of requested Pods

**Summary**: TAS: Incorrect Topology Assignment when topology allocatable Pods count are less than number of requested Pods

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4270

**Last updated**: 2025-02-18T07:54:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-02-16T19:23:11Z
- **Updated**: 2025-02-18T07:54:15Z
- **Closed**: 2025-02-18T07:54:15Z
- **Labels**: `kind/bug`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
TAS assigned topologies with nodes without enough allocatable pods count to TAS Workloads.
After that, the kube-scheduler failed to schedule pods to TAS assignment nodes.

**What you expected to happen**:
TAS considers allocatable pods count in the topologies.

**How to reproduce it (as minimally and precisely as possible)**:
You can see the actual situation in fixing PR (#4271) test cases, `workload does not get scheduled as the node capacity (.status.allocatable['pods']) is already used by non-TAS and TAS workloads` in `pkg/scheduler/scheduler_test.go`.

**Anything else we need to know?**:
The nodes have a limitation of allocatable pods count in `.status.allocatable["pods"]`, which is defaults are 110, and can be replaced by kubelet configurations.
However, the current TAS implementation has never considered the number of allocatable pods since `TASFlavorSnapshot` does not record how many [TAS|NonTAS] pods are scheduled to nodes in [`addNonTASUsage`](https://github.com/kubernetes-sigs/kueue/blob/5b426e99efffc546c3b3bcd4d5dbdcfa07e922fb/pkg/cache/tas_flavor_snapshot.go#L207-L212) and [`addTASUsage`](https://github.com/kubernetes-sigs/kueue/blob/5b426e99efffc546c3b3bcd4d5dbdcfa07e922fb/pkg/cache/tas_flavor_snapshot.go#L214-L226).

So, `TASFlavorSnapshot` consider allocatable Pod counts only from computing resources like CPU and Memory in the following: https://github.com/kubernetes-sigs/kueue/blob/5b426e99efffc546c3b3bcd4d5dbdcfa07e922fb/pkg/cache/tas_flavor_snapshot.go#L511

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-16T19:23:28Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-16T19:23:39Z

cc: @mimowo
