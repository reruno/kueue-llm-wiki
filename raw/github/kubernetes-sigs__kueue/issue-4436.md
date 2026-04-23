# Issue #4436: TAS with Preemption: Unexpected Pods count requests in findTopologyAssignment()

**Summary**: TAS with Preemption: Unexpected Pods count requests in findTopologyAssignment()

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4436

**Last updated**: 2025-02-28T15:34:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-02-28T09:35:02Z
- **Updated**: 2025-02-28T15:34:57Z
- **Closed**: 2025-02-28T15:34:57Z
- **Labels**: `kind/bug`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 8

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
In the `findTopologyAssignment()`, `requests` should have `{"pods": 1}` since requests is referenced to [`SinglePodRequests`](https://github.com/kubernetes-sigs/kueue/blob/690e9762b796d28b057e31ec8298b09f9ede0e0d/pkg/cache/tas_flavor_snapshot.go#L322).

https://github.com/kubernetes-sigs/kueue/blob/690e9762b796d28b057e31ec8298b09f9ede0e0d/pkg/cache/tas_flavor_snapshot.go#L317-L320

However, as I described in https://github.com/kubernetes-sigs/kueue/pull/4355#issuecomment-2685761682, when TAS with preemption, `SinglePodRequests` has `{"pods": 2}` in the following UT cases

- https://github.com/kubernetes-sigs/kueue/blob/690e9762b796d28b057e31ec8298b09f9ede0e0d/pkg/scheduler/scheduler_test.go#L5187
- https://github.com/kubernetes-sigs/kueue/blob/cfed6f3fd7f0fa7394b5f3be79af8a8138a54650/pkg/scheduler/scheduler_test.go#L5248
- https://github.com/kubernetes-sigs/kueue/blob/cfed6f3fd7f0fa7394b5f3be79af8a8138a54650/pkg/scheduler/scheduler_test.go#L5334

**What you expected to happen**:
The `SinglePodRequests` has `{"pods": 1}` every time.

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4355/pull-kueue-test-unit-main/1894775753115963392

**Anything else we need to know?**:
The root cause is the unintended reuse of `tasPodSetRequests.SinglePodRequests` within a single schedulingCycle. We should use it as read-only objects. The reason why this happens only in the case of preemption is that `FindTopologyAssignmentsForWorkload()` is called twice only for the TAS with Preemption in the following:

- https://github.com/kubernetes-sigs/kueue/blob/690e9762b796d28b057e31ec8298b09f9ede0e0d/pkg/scheduler/flavorassigner/flavorassigner.go#L407
- https://github.com/kubernetes-sigs/kueue/blob/690e9762b796d28b057e31ec8298b09f9ede0e0d/pkg/scheduler/preemption/preemption.go#L586

Otherwise, `FindTopologyAssignmentsForWorkload()` is called only once within a single scheduling cycle.

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-28T09:36:21Z

/assign @tenzen-y 
cc: @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-28T10:12:43Z

Right, I think the bug is user-facing on the current main. Ideally, along with the fix we would add a unit test in `TestScheduleForTASPreemption` which reproduces that scenario.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-28T10:15:14Z

> Right, I think the bug is user-facing on the current main. Ideally, along with the fix we would add a unit test in `TestScheduleForTASPreemption` which reproduces that scenario.

I think so too. Non-existence test case brought this missed edge case.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-28T12:35:05Z

Blocked by #4439

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-28T12:40:53Z

Why blocked? Isn't it enough to Clone the SinglePodRequests here: https://github.com/kubernetes-sigs/kueue/blob/690e9762b796d28b057e31ec8298b09f9ede0e0d/pkg/cache/tas_flavor_snapshot.go#L322?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-28T12:43:03Z

> Why blocked? Isn't it enough to Clone the SinglePodRequests here:
> 
> [kueue/pkg/cache/tas_flavor_snapshot.go](https://github.com/kubernetes-sigs/kueue/blob/690e9762b796d28b057e31ec8298b09f9ede0e0d/pkg/cache/tas_flavor_snapshot.go#L322)
> 
> Line 322 in [690e976](/kubernetes-sigs/kueue/commit/690e9762b796d28b057e31ec8298b09f9ede0e0d)
> 
>  requests := tasPodSetRequests.SinglePodRequests 
> ?

If we do not fix #4439 first, we can not implement tests for this bug fix since #4439 blocks all preemption UT impls for Pods count.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-28T12:44:23Z

If you are ok, I will submit this bug fix PR without tests.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-28T12:51:02Z

I prefer with a test, but I'm not sure I understand the other issue, left a comment there.
