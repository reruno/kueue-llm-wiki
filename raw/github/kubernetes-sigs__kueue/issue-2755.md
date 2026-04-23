# Issue #2755: Flaky Test: TestScalability/CommandStats

**Summary**: Flaky Test: TestScalability/CommandStats

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2755

**Last updated**: 2024-08-02T07:28:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-08-02T06:22:05Z
- **Updated**: 2024-08-02T07:28:51Z
- **Closed**: 2024-08-02T07:28:51Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Flaky test for `TestScalability/CommandStats`.

```shell
{Failed  === RUN   TestScalability/CommandStats
    checker_test.go:87: Average CPU usage 516mCpu is greater than maximum expected 515mCPU
--- FAIL: TestScalability/CommandStats (0.00s)
}
```

**What you expected to happen**:

It never happened. 

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/logs/periodic-kueue-test-scheduling-perf-main/1819194281240301568

<img width="1052" alt="Screenshot 2024-08-02 at 15 21 12" src="https://github.com/user-attachments/assets/d0a3f99d-d4c8-48bd-accb-7ff7370bf722">

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-02T06:22:17Z

/assign
/kinf flake

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-02T06:22:23Z

/kind flake
