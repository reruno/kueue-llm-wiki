# Issue #7961: [flaky test] Fair Sharing when the cluster queue starts borrowing should update the ClusterQueue.status.fairSharing.weightedShare

**Summary**: [flaky test] Fair Sharing when the cluster queue starts borrowing should update the ClusterQueue.status.fairSharing.weightedShare

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7961

**Last updated**: 2025-11-28T01:28:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-27T13:44:53Z
- **Updated**: 2025-11-28T01:28:23Z
- **Closed**: 2025-11-28T01:28:23Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 1

## Description

/kind flake

**What happened**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7953/pull-kueue-test-e2e-main-1-34/1994032552188317696

**What you expected to happen**:
no fail
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:

```
End To End Suite: kindest/node:v1.34.0: [It] Fair Sharing when the cluster queue starts borrowing should update the ClusterQueue.status.fairSharing.weightedShare expand_less	11s
{Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/fair_sharing_test.go:114 with:
Expected
    <int32>: 0
to equal
    <int32>: 4 failed [FAILED] Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/fair_sharing_test.go:114 with:
Expected
    <int32>: 0
to equal
    <int32>: 4
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/fair_sharing_test.go:125 @ 11/27/25 13:32:09.589
}
```

## Discussion

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-11-27T15:06:25Z

/assign @sohankunkerkar
