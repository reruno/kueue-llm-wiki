# Issue #9610: [release-0.15] Flaky Test: Scheduler when Requeueing Inadmissible Workloads Should collapse requeue requests to ClusterQueue

**Summary**: [release-0.15] Flaky Test: Scheduler when Requeueing Inadmissible Workloads Should collapse requeue requests to ClusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9610

**Last updated**: 2026-03-03T06:14:50Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2026-03-02T05:36:18Z
- **Updated**: 2026-03-03T06:14:50Z
- **Closed**: 2026-03-02T13:46:17Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:

Scheduler Suite: [It] Scheduler when Requeueing Inadmissible Workloads Should collapse requeue requests to ClusterQueue

**Link to failed CI job or steps to reproduce locally**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-15/2027016273371598848

**Failure message or logs**:
```shell
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:577 with:
pending_workloads with status=inadmissible
Expected
    <int>: 10
to be <=
    <int>: 5 failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:577 with:
pending_workloads with status=inadmissible
Expected
    <int>: 10
to be <=
    <int>: 5
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/scheduler/scheduler_test.go:3065 @ 02/26/26 14:02:39.634
}
```

**Anything else we need to know?**:

This might be sibling issue with https://github.com/kubernetes-sigs/kueue/issues/9591

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-02T13:46:17Z

the failure is from Thursday, and refers to lines which were moved in https://github.com/kubernetes-sigs/kueue/pull/9531/ to solve this specific problem. So, I believe this is already solved.
Let me close, and let's open a new one if this remains an issue.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-03T06:14:50Z

> the failure is from Thursday, and refers to lines which were moved in [#9531](https://github.com/kubernetes-sigs/kueue/pull/9531) to solve this specific problem. So, I believe this is already solved. Let me close, and let's open a new one if this remains an issue.

That sounds reasonable, thank you for investigating that 👍
