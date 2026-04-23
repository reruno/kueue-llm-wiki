# Issue #7390: [flaky test]  StatefulSet integration when StatefulSet created should allow to scale up after scale down to zer

**Summary**: [flaky test]  StatefulSet integration when StatefulSet created should allow to scale up after scale down to zer

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7390

**Last updated**: 2025-11-03T08:00:06Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-24T16:28:56Z
- **Updated**: 2025-11-03T08:00:06Z
- **Closed**: 2025-11-03T08:00:06Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 5

## Description

/kind flake


**What happened**:
failures 

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7389/pull-kueue-test-e2e-main-1-32/1981745144096886784
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7205/pull-kueue-test-e2e-main-1-34/1975862374690721792

**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:


```
End To End Suite: kindest/node:v1.32.8: [It] StatefulSet integration when StatefulSet created should allow to scale up after scale down to zero expand_less	58s
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:339 with:
Expected
    <int32>: 0
to equal
    <int32>: 3 failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:339 with:
Expected
    <int32>: 0
to equal
    <int32>: 3
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:340 @ 10/24/25 15:46:46.084
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-24T16:29:03Z

cc @mszadkow

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-27T06:37:52Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-main-1-34/1982173434930532352

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-27T06:37:58Z

cc @mbobrovskyi

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-29T14:37:29Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7420/pull-kueue-test-e2e-main-1-31/1983533293143855104

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-10-29T14:45:24Z

/assign
