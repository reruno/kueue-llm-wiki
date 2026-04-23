# Issue #2876: [Flaky test] Unit test for pkg/scheduler/preemption fails

**Summary**: [Flaky test] Unit test for pkg/scheduler/preemption fails

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2876

**Last updated**: 2024-08-26T15:23:54Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-08-22T08:47:37Z
- **Updated**: 2024-08-26T15:23:54Z
- **Closed**: 2024-08-26T15:23:54Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 1

## Description

/kind flake

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Flaky unit test for `pkg/scheduler/preemption` `TestPreemption/preempt_newer_workloads_with_the_same_priority`.

```
=== Failed
=== FAIL: pkg/scheduler/preemption TestPreemption/preempt_newer_workloads_with_the_same_priority (0.10s)
    preemption_test.go:1467: Issued preemptions (-want,+got):
          sets.Set[string](
        - 	{"/wl2:InClusterQueue": {}},
        + 	{"/wl3:InClusterQueue": {}},
          )
=== FAIL: pkg/scheduler/preemption TestPreemption (3.38s)
```

**What you expected to happen**:
It never happened.

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2875/pull-kueue-test-unit-main/1826529623073099776

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-08-24T00:33:35Z

/assign
