# Issue #6969: [ElasticJobs] scale-up workload stuck pending: preemption not triggered.

**Summary**: [ElasticJobs] scale-up workload stuck pending: preemption not triggered.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6969

**Last updated**: 2025-09-24T17:14:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2025-09-23T17:06:55Z
- **Updated**: 2025-09-24T17:14:16Z
- **Closed**: 2025-09-24T17:14:16Z
- **Labels**: `kind/bug`
- **Assignees**: [@ichekrygin](https://github.com/ichekrygin)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**:
When scaling up an ElasticJob (via WorkloadSlices), the scaled-up workload slice does not preempt or evict other workloads as expected. Instead, it remains in a "pending" (unadmitted) state.

**What you expected to happen**:
The scaled-up workload slice should preempt/evict lower-priority workloads as necessary and be successfully admitted.

**How to reproduce it (as minimally and precisely as possible)**:

1. Create a ClusterQueue and two WorkloadPriorityClasses: `low` and `high`.
2. Submit a regular `batchv1.Job` with low priority.
3. Submit an ElasticJob with high priority, still within the ClusterQueue quota capacity.
4. Scale up the ElasticJob so that it requires preemption/eviction of the low-priority job.

**Anything else we need to know?**:
N/A

**Environment**:

* Kubernetes version (use `kubectl version`):
* Kueue version (use `git describe --tags --dirty --always`): `v0.13.4`
* Cloud provider or hardware configuration:
* OS (e.g. `cat /etc/os-release`):
* Kernel (e.g. `uname -a`):
* Install tools:
* Others:

## Discussion

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-23T17:12:33Z

**Root cause analysis:**

Kueue’s scheduler simulates workload preemption during flavor assignment. However, the flavor assignment itself does not produce preemption targets. Instead, preemption targets are generated in a separate step, after flavor assignment completes in `Preempt` mode.

When scheduling a scaled-up workload slice, the scheduler correctly computes the *additional capacity* required to place the remaining (delta) pods during flavor assignment. The problem is that this additional capacity is not considered during the preemption-target generation step. As a result, the flavor assignment may succeed in `Preempt` mode, but the corresponding preemption target list is empty.

**Consequence:**
This leaves scaled-up workloads stuck in a pending state, even though preemption should have occurred to free the necessary capacity.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-23T17:16:55Z

/assign
