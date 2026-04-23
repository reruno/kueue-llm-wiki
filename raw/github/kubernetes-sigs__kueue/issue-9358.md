# Issue #9358: Flaky Test: Workload controller with resource retention when manager is setup with long retention period should not delete the workload before retention period elapses [slow]

**Summary**: Flaky Test: Workload controller with resource retention when manager is setup with long retention period should not delete the workload before retention period elapses [slow]

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9358

**Last updated**: 2026-02-20T20:41:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-19T08:45:52Z
- **Updated**: 2026-02-20T20:41:41Z
- **Closed**: 2026-02-20T20:41:41Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 1

## Description

**Which test is flaking?**:
Flaky Test: Workload controller with resource retention when manager is setup with long retention period should not delete the workload before retention period elapses [slow]

**Link to failed CI job or steps to reproduce locally**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9321/pull-kueue-test-integration-extended-main/2023776846776111104

**Failure message or logs**:
```
Core Controllers Suite: [It] Workload controller with resource retention when manager is setup with long retention period should not delete the workload before retention period elapses [slow] expand_less	15s
{Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/metrics.go:293 with:
Expected
    <float64>: 1
to equal
    <float64>: 0 failed [FAILED] Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/metrics.go:293 with:
Expected
    <float64>: 1
to equal
    <float64>: 0
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/core/workload_controller_test.go:1043 @ 02/17/26 15:17:39.147
}
```

## Discussion

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-02-19T21:44:14Z

/assign
