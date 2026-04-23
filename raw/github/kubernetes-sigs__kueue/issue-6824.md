# Issue #6824: Flaky Integration Test: Scheduler when Preemption is enabled in fairsharing and there are large values of quota and weights Queue can reclaim its nominal quota

**Summary**: Flaky Integration Test: Scheduler when Preemption is enabled in fairsharing and there are large values of quota and weights Queue can reclaim its nominal quota

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6824

**Last updated**: 2025-10-03T13:01:07Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-09-15T05:49:12Z
- **Updated**: 2025-10-03T13:01:07Z
- **Closed**: 2025-10-03T13:01:07Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@pajakd](https://github.com/pajakd)
- **Comments**: 7

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

`Scheduler Fair Sharing Suite: [It] Scheduler when Preemption is enabled in fairsharing and there are large values of quota and weights Queue can reclaim its nominal quota [slow]` failed in release-0.12 periodic Job.

```shell
{Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util_scheduling.go:67 with:
Not enough workloads evicted
Expected
    <int>: 0
to equal
    <int>: 3 failed [FAILED] Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util_scheduling.go:67 with:
Not enough workloads evicted
Expected
    <int>: 0
to equal
    <int>: 3
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/scheduler/fairsharing/fair_sharing_test.go:499 @ 09/13/25 07:51:18.383
}
```

**What you expected to happen**:

No errors.

**How to reproduce it (as minimally and precisely as possible)**:

<img width="3168" height="482" alt="Image" src="https://github.com/user-attachments/assets/7259e200-1e88-4336-b761-da6a3d415555" />

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-12/1966767439517585408

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-15T05:49:43Z

/kind flake

IIUC, we added this case in https://github.com/kubernetes-sigs/kueue/pull/6617

cc @pajakd @PBundyra

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-22T07:52:32Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-12/1969848044652335104

### Comment by [@pajakd](https://github.com/pajakd) — 2025-09-22T07:54:30Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-10-01T16:09:38Z

It also happens in main: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7122/pull-kueue-test-integration-extended-main/1973390165825032192.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-10-01T16:13:18Z

/retitle Flaky Integration Test: Scheduler when Preemption is enabled in fairsharing and there are large values of quota and weights Queue can reclaim its nominal quota

### Comment by [@pajakd](https://github.com/pajakd) — 2025-10-03T11:20:55Z

I looked at the logs and I think there is the following race condition:
https://github.com/kubernetes-sigs/kueue/blob/0d6a4aee95cb221f172cb82b88d6ebb68f1c57e0/test/integration/singlecluster/scheduler/fairsharing/fair_sharing_test.go#L837-L846

- The last of the 10 workloads in queue "a" is created and reserves the quota.
- Before it gets admitted, the workload in queue "b" gets created. 
- I can see in the logs that the workload in "b" evicts 2 workloads (for some reason the error in the test failure says 0 evictions).

IMO to deflake the test we should wait for the actual admission of the 10 workloads.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-03T11:41:10Z

Is it becuase the metric `ReservingActiveWorkloadsMetric` is bumped before the workloads are actually reserving the quota? 

If this is the case, then it looks like an issue on its own, as we try to bump metrics only once the transition happens. 

Still, the metrics fix may not be trivial and the issue is likely low priority. Finally, testing the metric is not the intention of the test.

So, +1 on the pragmatic flakiness fix.
