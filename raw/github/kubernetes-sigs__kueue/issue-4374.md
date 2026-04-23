# Issue #4374: [Flaky test] LeaderWorkerSet created should allow to scale down LeaderReadyStartupPolicy

**Summary**: [Flaky test] LeaderWorkerSet created should allow to scale down LeaderReadyStartupPolicy

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4374

**Last updated**: 2025-02-26T08:40:33Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-02-24T10:53:42Z
- **Updated**: 2025-02-26T08:40:33Z
- **Closed**: 2025-02-26T08:40:33Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 1

## Description

/kind flake 

**What happened**:

The test failed on unrelated PR: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4368/pull-kueue-test-e2e-main-1-32/1893968484795158528

**What you expected to happen**:

No random failures

**How to reproduce it (as minimally and precisely as possible)**:

Run on CI

**Anything else we need to know?**:

```
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:103 with:
Error matcher expects an error.  Got:
    <nil>: nil failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:103 with:
Error matcher expects an error.  Got:
    <nil>: nil
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:425 @ 02/24/25 10:28:43.548
}
```
This is e2e test `pull-kueue-test-e2e-main-1-32` so maybe the timeout of 10s is not enough, I would suggest to try incrementing it.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-24T10:53:54Z

/assign @mbobrovskyi 
PTAL
