# Issue #9621: Kueue when Creating a Job With Queueing Should allow updating the workload's priority through the job

**Summary**: Kueue when Creating a Job With Queueing Should allow updating the workload's priority through the job

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9621

**Last updated**: 2026-03-04T18:32:20Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-02T08:58:44Z
- **Updated**: 2026-03-04T18:32:20Z
- **Closed**: 2026-03-04T18:32:20Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 1

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:
Kueue when Creating a Job With Queueing Should allow updating the workload's priority through the job
**Link to failed CI job or steps to reproduce locally**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9617/pull-kueue-test-e2e-main-1-33/2028383367677874176
**Failure message or logs**:
```
End To End Suite: kindest/node:v1.33.7: [It] Kueue when Creating a Job With Queueing Should allow updating the workload's priority through the job [area:singlecluster, feature:job] expand_less	14s
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/job_test.go:534 with:
Expected
    <bool>: true
to be false failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/job_test.go:534 with:
Expected
    <bool>: true
to be false
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/job_test.go:535 @ 03/02/26 08:40:19.903
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-03-03T03:21:33Z

/assign
