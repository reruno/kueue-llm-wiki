# Issue #9526: [flaky test] Scheduler when Handling clusterQueue events Should re-enqueue by the update event of ClusterQueue

**Summary**: [flaky test] Scheduler when Handling clusterQueue events Should re-enqueue by the update event of ClusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9526

**Last updated**: 2026-02-27T17:08:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-26T14:37:37Z
- **Updated**: 2026-02-27T17:08:16Z
- **Closed**: 2026-02-27T09:54:04Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:
Scheduler when Handling clusterQueue events Should re-enqueue by the update event of ClusterQueue 
and
Scheduler Suite: [It] Scheduler when Requeueing Inadmissible Workloads Should collapse requeue requests to ClusterQueue

**Link to failed CI job or steps to reproduce locally**:

**Failure message or logs**:
```
Scheduler Suite: [It] Scheduler when Handling clusterQueue events Should re-enqueue by the update event of ClusterQueue expand_less	11s
{Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:577 with:
pending_workloads with status=inadmissible
Expected
    <int>: 3
to be <=
    <int>: 2 failed [FAILED] Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:577 with:
pending_workloads with status=inadmissible
Expected
    <int>: 3
to be <=
    <int>: 2
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/scheduler/scheduler_test.go:901 @ 02/26/26 14:02:14.99
}
[open stderropen_in_new](https://prow.k8s.io/spyglass/lens/junit/iframe?req=%7B%22artifacts%22%3A%5B%22artifacts%2Fjunit.xml%22%5D%2C%22index%22%3A2%2C%22src%22%3A%22gs%2Fkubernetes-ci-logs%2Flogs%2Fperiodic-kueue-test-integration-release-0-15%2F2027016273371598848%22%7D&topURL=https%3A//prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-15/2027016273371598848&lensIndex=2#)
Scheduler Suite: [It] Scheduler when Requeueing Inadmissible Workloads Should collapse requeue requests to ClusterQueue expand_less	13s
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
[open stderropen_in_new](https://prow.k8s.io/spyglass/lens/junit/iframe?req=%7B%22artifacts%22%3A%5B%22artifacts%2Fjunit.xml%22%5D%2C%22index%22%3A2%2C%22src%22%3A%22gs%2Fkubernetes-ci-logs%2Flogs%2Fperiodic-kueue-test-integration-release-0-15%2F2027016273371598848%22%7D&topURL=https%3A//prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-15/2027016273371598848&lensIndex=2#)
```

**Anything else we need to know?**:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-26T14:38:04Z

cc @gabesaba @sohankunkerkar  , maybe just a bit more that 10s is needed one a busy CI ?

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-02-26T15:11:39Z

The 1st one is surprising. The 2nd one, less so. Increasing the timeout won't help. For the 2nd one, bumping the batch window from 100ms to something like 1-2 seconds would help (but I don't know if we can target that just for that test, or if we'll need an entirely new suite)

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-26T15:15:10Z

I think bumping to 2s  just for the test sgtm. We can open a dedicated test suite when we have more test cases requiring large batch period. For now Iiuc this is only one

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-26T16:35:31Z

Looks like the failures come in pairs: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9528/pull-kueue-test-integration-baseline-release-0-15/2027053478857150464

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-02-27T06:21:55Z

I think the cherry-pick of #9531 fixes the collapse requeue requests test by moving it into a dedicated suite with a 2s batch period. However, the first failure `Should re-enqueue by the update event of ClusterQueue` is still present on release-0.15.

With async requeueing (#9508), an inadmissible workload can observe up to 3 pending admission attempts before it settles. The test currently asserts <= 2, which was correct with synchronous requeueing but is now too strict.

Relaxing both assertions from <= 2 to <= 3 may fix the issue. This test isn't about batching collapse (that's test 2's job). It's about verifying that a CQ update re-enqueues an inadmissible workload. Whether it takes 2 or 3 attempts to settle is a timing detail that depends on the requeuer implementation.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-27T17:08:16Z

Looks like there is one more flaky site: https://github.com/kubernetes-sigs/kueue/issues/9591
