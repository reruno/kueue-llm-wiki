# Issue #2240: scalability: "Average CPU usage" flakes

**Summary**: scalability: "Average CPU usage" flakes

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2240

**Last updated**: 2024-05-21T10:26:45Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-05-20T18:10:19Z
- **Updated**: 2024-05-21T10:26:45Z
- **Closed**: 2024-05-21T10:26:45Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake
**What happened**:
The scalability test failed on the "Average CPU usage 504mCpu is greater than maximum expected 500mCPU".

```shell
{Failed  === RUN   TestScalability/CommandStats
    checker_test.go:87: Average CPU usage 504mCpu is greater than maximum expected 500mCPU
--- FAIL: TestScalability/CommandStats (0.00s)
}
```

**What you expected to happen**:
No error happened.

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2235/pull-kueue-test-scheduling-perf-main/1792493875051368448

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-20T18:10:40Z

cc: @trasc @mimowo

### Comment by [@trasc](https://github.com/trasc) — 2024-05-21T07:24:17Z

/assign
