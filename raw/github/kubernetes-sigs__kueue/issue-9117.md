# Issue #9117: [Flaky E2E] Kuberay Should run a rayjob with InTreeAutoscaling

**Summary**: [Flaky E2E] Kuberay Should run a rayjob with InTreeAutoscaling

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9117

**Last updated**: 2026-02-12T19:30:10Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-02-11T11:01:36Z
- **Updated**: 2026-02-12T19:30:10Z
- **Closed**: 2026-02-12T19:30:10Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@ikchifo](https://github.com/ikchifo)
- **Comments**: 1

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:

End To End Suite: kindest/node:v1.33.7: [It] Kuberay Should run a rayjob with InTreeAutoscaling [area:singlecluster, feature:kuberay] 

**Link to failed CI job or steps to reproduce locally**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9114/pull-kueue-test-e2e-main-1-33/2021532576509857792

**Failure message or logs**:
```
{Timed out after 300.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/kuberay_test.go:314 with:
Expected exactly 5 pods with 'workers' in the name
Expected
    <[]string | len:0, cap:0>: nil
to have length 5 failed [FAILED] Timed out after 300.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/kuberay_test.go:314 with:
Expected exactly 5 pods with 'workers' in the name
Expected
    <[]string | len:0, cap:0>: nil
to have length 5
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/kuberay_test.go:322 @ 02/11/26 10:56:27.07
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@ikchifo](https://github.com/ikchifo) — 2026-02-11T16:05:53Z

/assign

Looks like different failure mode than #9058 - the test is timing out during scale-up (expecting 5 workers, finding 0) rather than scale-down. Will investigate some more
