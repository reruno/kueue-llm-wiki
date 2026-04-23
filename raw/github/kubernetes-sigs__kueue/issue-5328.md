# Issue #5328: [Flaky test] Should be stuck in termination until admitted workloads finished running

**Summary**: [Flaky test] Should be stuck in termination until admitted workloads finished running

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5328

**Last updated**: 2025-06-20T07:18:53Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-05-23T15:57:17Z
- **Updated**: 2025-06-20T07:18:53Z
- **Closed**: 2025-06-20T07:18:53Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mykysha](https://github.com/mykysha)
- **Comments**: 1

## Description

/kind flake

**What happened**:

failure on unrelated branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5276/pull-kueue-test-integration-baseline-main/1925940251549765632

**What you expected to happen**:

no failure

**How to reproduce it (as minimally and precisely as possible)**:

ci

**Anything else we need to know?**:


```
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:539 with:
local_queue_status with status=True
Expected
    <float64>: 1
to equal
    <float64>: 0 failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:539 with:
local_queue_status with status=True
Expected
    <float64>: 1
to equal
    <float64>: 0
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/core/clusterqueue_controller_test.go:919 @ 05/23/25 15:48:12.255
}
```

## Discussion

### Comment by [@mykysha](https://github.com/mykysha) — 2025-05-27T08:49:30Z

/assign
