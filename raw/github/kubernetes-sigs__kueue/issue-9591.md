# Issue #9591: Scheduler when Requeueing Inadmissible Workloads Should collapse requeue requests to ClusterQueue

**Summary**: Scheduler when Requeueing Inadmissible Workloads Should collapse requeue requests to ClusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9591

**Last updated**: 2026-03-02T18:52:54Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-27T17:06:43Z
- **Updated**: 2026-03-02T18:52:54Z
- **Closed**: 2026-03-02T18:52:54Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 2

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:
 Scheduler when Requeueing Inadmissible Workloads Should collapse requeue requests to ClusterQueue
**Link to failed CI job or steps to reproduce locally**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9528/pull-kueue-test-integration-baseline-release-0-15/2027424372553158656
**Failure message or logs**:
```
Scheduler Inadmissible Requeueing Suite: [It] Scheduler when Requeueing Inadmissible Workloads Should collapse requeue requests to ClusterQueue expand_less	15s
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:577 with:
pending_workloads with status=inadmissible
Expected
    <int>: 3
to be <=
    <int>: 2 failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:577 with:
pending_workloads with status=inadmissible
Expected
    <int>: 3
to be <=
    <int>: 2
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/scheduler/inadmissible/requeueing_test.go:83 @ 02/27/26 16:59:55.868
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-27T17:08:04Z

cc @gabesaba @sohankunkerkar @Sebastianhayashi

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-02-28T07:24:21Z

/assign
