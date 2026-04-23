# Issue #2708: Flaky Performance Test: checker_test

**Summary**: Flaky Performance Test: checker_test

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2708

**Last updated**: 2024-11-05T07:05:08Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@IrvingMg](https://github.com/IrvingMg)
- **Created**: 2024-07-26T16:09:38Z
- **Updated**: 2024-11-05T07:05:08Z
- **Closed**: 2024-11-05T07:05:06Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Flaky test for `test/performance/scheduler/checker TestScalability`.

```
=== Failed
=== FAIL: test/performance/scheduler/checker TestScalability/WorkloadClasses/large (0.00s)
    checker_test.go:117: Average wait for admission 11213ms is more then expected 11000ms
```

**What you expected to happen**:
Errors have never been seen.

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2642/pull-kueue-test-scheduling-perf-main/1816858084459417600

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

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2024-07-26T16:09:49Z

/kind flake

### Comment by [@trasc](https://github.com/trasc) — 2024-07-29T12:28:01Z

/assign

### Comment by [@trasc](https://github.com/trasc) — 2024-08-07T14:48:03Z

This looks to be caused just by a high load in the test infra.

We can keep it open for tracking purposes.

### Comment by [@trasc](https://github.com/trasc) — 2024-11-05T07:05:01Z

I believe we can close it for now as:

1. the issue was no longer observed
2. we have the retry mechanism: https://github.com/kubernetes-sigs/kueue/pull/3020 , able to retry the test and ignore infra cased flakes (eg. https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-scheduling-perf-main/1852546889136738304)
3. the board is clean for 2 months: https://testgrid.k8s.io/sig-scheduling#periodic-kueue-test-scheduling-perf-main

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-11-05T07:05:07Z

@trasc: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2708#issuecomment-2456392198):

>I believe we can close it for now as:
>
>1. the issue was no longer observed
>2. we have the retry mechanism: https://github.com/kubernetes-sigs/kueue/pull/3020 , able to retry the test and ignore infra cased flakes (eg. https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-scheduling-perf-main/1852546889136738304)
>3. the board is clean for 2 months: https://testgrid.k8s.io/sig-scheduling#periodic-kueue-test-scheduling-perf-main
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
