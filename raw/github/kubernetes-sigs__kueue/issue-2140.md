# Issue #2140: [scalability] The asserts for "Average wait for admission" flakes

**Summary**: [scalability] The asserts for "Average wait for admission" flakes

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2140

**Last updated**: 2024-05-06T13:52:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-05-06T09:42:53Z
- **Updated**: 2024-05-06T13:52:59Z
- **Closed**: 2024-05-06T13:52:59Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 3

## Description

**What happened**:

The scalability test failed on the assert ` checker_test.go:117: Average wait for admission 9303ms is more then expected 9000ms`:  https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2070/pull-kueue-test-scheduling-perf-main/1786492813098094592

```
{Failed  === RUN   TestScalability/WorkloadClasses/large
    checker_test.go:117: Average wait for admission 9303ms is more then expected 9000ms
--- FAIL: TestScalability/WorkloadClasses/large (0.00s)
}
```

**What you expected to happen**:

Not to flake.

**How to reproduce it (as minimally and precisely as possible)**:

Repeat the build

**Anything else we need to know?**:

The assert was recently bumped to 9s, but it shows as not enough: https://github.com/kubernetes-sigs/kueue/pull/2067/files.

The estimations [here](https://github.com/kubernetes-sigs/kueue/issues/2066#issuecomment-2079053502) suggest 10s might be needed.

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-06T09:44:07Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-06T11:25:11Z

/cc @tenzen-y @alculquicondor

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-06T13:49:48Z

In the future, I would like to see a test for the 65 or 99th percentile instead, which would remove the outliers that are affected by load in the nodes.
