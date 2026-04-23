# Issue #3149: [Flaky integration test] SchedulerWithWaitForPodsReady Long PodsReady timeout Should block admission of one new workload if two are considered in the same scheduling cycle

**Summary**: [Flaky integration test] SchedulerWithWaitForPodsReady Long PodsReady timeout Should block admission of one new workload if two are considered in the same scheduling cycle

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3149

**Last updated**: 2024-09-30T15:34:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-09-27T07:42:17Z
- **Updated**: 2024-09-30T15:34:05Z
- **Closed**: 2024-09-30T15:34:05Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 3

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Scheduler with WaitForPodsReady Suite: [It] SchedulerWithWaitForPodsReady Long PodsReady timeout Should block admission of one new workload if two are considered in the same scheduling cycle

```
{Timed out after 5.001s.
Not enough workloads are pending
Expected
    <int>: 1
to equal
    <int>: 2 failed [FAILED] Timed out after 5.001s.
Not enough workloads are pending
Expected
    <int>: 1
to equal
    <int>: 2
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/scheduler/podsready/scheduler_test.go:177 @ 09/26/24 16:12:49.608
}
```

**What you expected to happen**:
No random failure.

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/3148/pull-kueue-test-integration-main/1839333717571538944

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-27T10:49:06Z

/kind flake

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-27T17:23:20Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-30T06:51:40Z

Looks like another occurrence: https://prow.k8s.io/view/gs/kubernetes-jenkins/logs/periodic-kueue-test-integration-main/1840270117556981760
