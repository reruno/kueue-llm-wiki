# Issue #2638: Flaky Performance Test: Usage 55.19% is less then expected 56.00%

**Summary**: Flaky Performance Test: Usage 55.19% is less then expected 56.00%

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2638

**Last updated**: 2024-07-18T14:58:10Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-07-18T12:52:52Z
- **Updated**: 2024-07-18T14:58:10Z
- **Closed**: 2024-07-18T14:58:10Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
```
{Failed  === RUN   TestScalability/ClusterQueueClasses/cq
    checker_test.go:103: Usage 55.19% is less then expected 56.00%
--- FAIL: TestScalability/ClusterQueueClasses/cq (0.00s)
}
```

**What you expected to happen**:
Errors never has been seen.

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2636/pull-kueue-test-scheduling-perf-main/1813914677910966272

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-07-18T13:57:44Z

/assign
