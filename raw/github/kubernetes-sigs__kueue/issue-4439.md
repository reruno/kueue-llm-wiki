# Issue #4439: TAS with Preemption: Failed to preempt workloads when the the sum of admitted and waiting pods count exceeds Node limit

**Summary**: TAS with Preemption: Failed to preempt workloads when the the sum of admitted and waiting pods count exceeds Node limit

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4439

**Last updated**: 2025-02-28T15:34:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-02-28T12:30:26Z
- **Updated**: 2025-02-28T15:34:58Z
- **Closed**: 2025-02-28T15:34:58Z
- **Labels**: `kind/bug`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Preemptor with TAS failed to preempt candidates when sum of Pods count (admitted and head worklod pods) exceeds Node Pods count limit (`.status.allocatablePods["pods"]`).

The `FindTopologyAssitnmentForWorkload` with empty usage mode failed to find preemptees since the preemptor does not consider pod count (`"pods": X`) when it temporarily removes candidated workloads in the following:

**What you expected to happen**:
The preemptee is preempted by head higher priority workloads.

**How to reproduce it (as minimally and precisely as possible)**:
If we use the `.status.Allocatable["pods"]=1` in the following UT case, the test fails.
The test should succeed since the admitted workload, waiting workload, and node allocatable Pods have one pod.
The replacement from admitted and waiting workloads should happen since the node has enough pods allocatable count and waiting pod has higher priority than admitted one.

https://github.com/kubernetes-sigs/kueue/blob/690e9762b796d28b057e31ec8298b09f9ede0e0d/pkg/scheduler/scheduler_test.go#L5187

**Anything else we need to know?**:
The root cause is `cq.removeUsage(wl.Usage())` does not consider the pods count (`{"pods": 1}`) since `wl.Usage()` takes TAS usage from `TASUsage()`. The only `TASFlavorCashe` knows completely TAS usage including pods count `{"pods": xx}`.

- https://github.com/kubernetes-sigs/kueue/blob/690e9762b796d28b057e31ec8298b09f9ede0e0d/pkg/cache/snapshot.go#L44-L48
- https://github.com/kubernetes-sigs/kueue/blob/690e9762b796d28b057e31ec8298b09f9ede0e0d/pkg/workload/workload.go#L243-L248
- https://github.com/kubernetes-sigs/kueue/blob/690e9762b796d28b057e31ec8298b09f9ede0e0d/pkg/workload/workload.go#L292-L297

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-28T12:34:49Z

/assign
/cc @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-28T12:49:38Z

> The root cause is cq.removeUsage(wl.Usage()) does not consider the pods count ({"pods": 1}) since wl.Usage() takes TAS usage from TASUsage()

Is it correct though? TASUsage is using underneath TopologyDomainRequests which knows about the pod count for each domain. So the information is there.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-28T12:53:55Z

> > The root cause is cq.removeUsage(wl.Usage()) does not consider the pods count ({"pods": 1}) since wl.Usage() takes TAS usage from TASUsage()
> 
> Is it correct though? TASUsage is using underneath TopologyDomainRequests which knows about the pod count for each domain. So the information is there.

Because we add pods count as requests only in `TASFlavorCache.updateUsage` https://github.com/kubernetes-sigs/kueue/blob/690e9762b796d28b057e31ec8298b09f9ede0e0d/pkg/cache/tas_flavor.go#L155

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-28T12:56:50Z

I think this is expected.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-28T12:59:10Z

> I think this is expected.

In the current impl, preemptor failed to check preemption candidates since the candidates worklod pods count resource is not removed here: https://github.com/kubernetes-sigs/kueue/blob/690e9762b796d28b057e31ec8298b09f9ede0e0d/pkg/scheduler/preemption/preemption.go#L289

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-28T13:20:36Z

I see what you mean now, we synced on slack, and indeed there is another place requiring taking ResourcePods into account. One way of doing is to extend the `updateTASUsage` function with the number of Pods and then extend the Resources.
