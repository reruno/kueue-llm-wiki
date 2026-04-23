# Issue #7964: [flaky test]  Pod groups when Single CQ should admit group that fits

**Summary**: [flaky test]  Pod groups when Single CQ should admit group that fits

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7964

**Last updated**: 2025-11-28T02:08:21Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-27T15:22:23Z
- **Updated**: 2025-11-28T02:08:21Z
- **Closed**: 2025-11-28T02:08:21Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 3

## Description

**What happened**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7938/pull-kueue-test-e2e-main-1-32/1994057749700284416

**What you expected to happen**:

no failure
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:
```
End To End Suite: kindest/node:v1.32.8: [It] Pod groups when Single CQ should admit group that fits expand_less	11s
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:317 with:
Not enough workloads were admitted
Expected
    <int>: 0
to equal
    <int>: 1 failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:317 with:
Not enough workloads were admitted
Expected
    <int>: 0
to equal
    <int>: 1
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:98 @ 11/27/25 15:09:46.256
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-27T15:22:46Z

cc @sohankunkerkar

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-11-27T15:57:14Z

/assign @sohankunkerkar

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-27T17:23:19Z

/kind flake
