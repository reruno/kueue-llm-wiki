# Issue #8831: [Flaky Perf] TestScalability/CommandStats

**Summary**: [Flaky Perf] TestScalability/CommandStats

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8831

**Last updated**: 2026-01-27T16:17:54Z

---

## Metadata

- **State**: open
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-01-27T16:17:51Z
- **Updated**: 2026-01-27T16:17:54Z
- **Closed**: —
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake


**What happened**:

sigs.k8s.io/kueue/test/performance/scheduler/checker: TestScalability/CommandStats

```
{Failed  === RUN   TestScalability/WorkloadClasses/small
    checker_test.go:108: Average wait for admission 248062ms is more then expected 233000ms
--- FAIL: TestScalability/WorkloadClasses/small (0.00s)
}
```


sigs.k8s.io/kueue/test/performance/scheduler/checker: TestScalability/WorkloadClasses expand_less | 0s
```
{Failed  === RUN   TestScalability/WorkloadClasses
--- FAIL: TestScalability/WorkloadClasses (0.00s)
}
```

sigs.k8s.io/kueue/test/performance/scheduler/checker: TestScalability 

```
{Failed  === RUN   TestScalability
--- FAIL: TestScalability (0.01s)
}
```


```
=== Failed
=== FAIL: test/performance/scheduler/checker TestScalability/CommandStats (0.00s)
    checker_test.go:81: Wall time 493017ms is greater than maximum expected 425000ms
=== FAIL: test/performance/scheduler/checker TestScalability/WorkloadClasses/small (0.00s)
    checker_test.go:108: Average wait for admission 248062ms is more then expected 233000ms
=== FAIL: test/performance/scheduler/checker TestScalability/WorkloadClasses (0.00s)
=== FAIL: test/performance/scheduler/checker TestScalability (0.01s)
```

**What you expected to happen**:

No issue

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8825/pull-kueue-test-scheduling-perf-main/2016176842435727360

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:
