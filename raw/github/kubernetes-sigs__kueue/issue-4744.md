# Issue #4744: Flaky Test: End To End Suite: LeaderWorkerSet created with WorkloadPriorityClass should allow to update the PodTemplate in LeaderWorkerSet

**Summary**: Flaky Test: End To End Suite: LeaderWorkerSet created with WorkloadPriorityClass should allow to update the PodTemplate in LeaderWorkerSet

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4744

**Last updated**: 2025-03-21T14:14:33Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-03-21T13:39:20Z
- **Updated**: 2025-03-21T14:14:33Z
- **Closed**: 2025-03-21T14:14:33Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

End To End Suite: kindest/node:v1.29.14: [It] LeaderWorkerSet integration when LeaderWorkerSet created with WorkloadPriorityClass should allow to update the PodTemplate in LeaderWorkerSet

```
{Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:763 with:
Expected
    <int32>: 1
to equal
    <int32>: 0 failed [FAILED] Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:763 with:
Expected
    <int32>: 1
to equal
    <int32>: 0
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:776 @ 03/21/25 12:34:07.615
}
```

**What you expected to happen**:
No errors

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4059/pull-kueue-test-e2e-main-1-29/1903059880458063872

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-21T13:42:58Z

Let;s use LongTimeout here

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-21T13:45:57Z

/assign
