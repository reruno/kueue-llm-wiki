# Issue #4160: [Flaky E2E] StatefulSet integration when StatefulSet created should allow to change queue name if ReadyReplicas=0

**Summary**: [Flaky E2E] StatefulSet integration when StatefulSet created should allow to change queue name if ReadyReplicas=0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4160

**Last updated**: 2025-02-10T13:39:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-02-06T11:10:37Z
- **Updated**: 2025-02-10T13:39:59Z
- **Closed**: 2025-02-10T13:39:59Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake

**What happened**:

End To End Suite: kindest/node:v1.32.0: [It] StatefulSet integration when StatefulSet created should allow to change queue name if ReadyReplicas=0 

```
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:366 with:
Expected
    <int32>: 0
to equal
    <int32>: 3 failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:366 with:
Expected
    <int32>: 0
to equal
    <int32>: 3
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:367 @ 02/06/25 10:58:59.115
}
```

**What you expected to happen**:
No failures

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4159/pull-kueue-test-e2e-main-1-32/1887452310766882816

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-02-06T11:14:05Z

/assign
