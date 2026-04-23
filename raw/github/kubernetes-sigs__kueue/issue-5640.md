# Issue #5640: [flaky test] LeaderWorkerSet integration when LeaderWorkerSet created should admit group with leader onl

**Summary**: [flaky test] LeaderWorkerSet integration when LeaderWorkerSet created should admit group with leader onl

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5640

**Last updated**: 2025-07-03T10:01:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-13T07:43:35Z
- **Updated**: 2025-07-03T10:01:28Z
- **Closed**: 2025-07-03T10:01:28Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mykysha](https://github.com/mykysha)
- **Comments**: 2

## Description


**What happened**:

failed https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-release-0-12-1-32/1933255326035873792

**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:
```
{Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/leaderworkerset_test.go:103 with:
Expected
    <int32>: 0
to equal
    <int32>: 1 failed [FAILED] Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/leaderworkerset_test.go:103 with:
Expected
    <int32>: 0
to equal
    <int32>: 1
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/leaderworkerset_test.go:105 @ 06/12/25 20:26:33.793
}
```

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-17T11:29:34Z

/kind flake

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-23T10:30:31Z

/assign @mykysha 

Who already working on https://github.com/kubernetes-sigs/kueue/issues/5639 and the problem looks like the same.
