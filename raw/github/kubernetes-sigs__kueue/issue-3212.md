# Issue #3212: Flaky test: Scheduler with WaitForPodsReady Suite

**Summary**: Flaky test: Scheduler with WaitForPodsReady Suite

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3212

**Last updated**: 2024-10-17T06:37:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-10-10T07:45:33Z
- **Updated**: 2024-10-17T06:37:04Z
- **Closed**: 2024-10-17T06:37:04Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Flaky testing on "Scheduler with WaitForPodsReady Suite: [It] SchedulerWithWaitForPodsReadyNonblockingMode Long PodsReady timeout Should not block admission of one new workload if two are considered in the same scheduling cycle".

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
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/scheduler/podsready/scheduler_test.go:635 @ 10/10/24 06:15:45.64
}
```

https://prow.k8s.io/view/gs/kubernetes-jenkins/logs/periodic-kueue-test-integration-main/1844256892138819584

**What you expected to happen**:
No errors happened

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/logs/periodic-kueue-test-integration-main/1844256892138819584

<img width="1196" alt="Screenshot 2024-10-10 at 16 44 47" src="https://github.com/user-attachments/assets/c2fcdb02-30ec-45c7-b733-c1c15e1ae370">

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-10T07:45:41Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-11T11:21:20Z

/cc @IrvingMg @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-11T11:33:56Z

/assign

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2024-10-11T15:48:05Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-11T15:48:25Z

/unassign
