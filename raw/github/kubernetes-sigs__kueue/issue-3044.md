# Issue #3044: Flaky: Should allow fetching information about pending workloads in LocalQueue.

**Summary**: Flaky: Should allow fetching information about pending workloads in LocalQueue.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3044

**Last updated**: 2024-09-16T07:07:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-09-13T17:14:11Z
- **Updated**: 2024-09-16T07:07:15Z
- **Closed**: 2024-09-16T07:07:15Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Flaky test on `pull-kueue-test-e2e-main-1-31`:

End To End Suite: kindest/node:v1.31.0: [It] Kueue visibility server when There are pending workloads due to capacity maxed by the admitted job Should allow fetching information about pending workloads in LocalQueue

Kueue visibility server when There are pending workloads due to capacity maxed by the admitted job Should allow fetching information about pending workloads in LocalQueue.

```
{Timed out after 5.000s.
Expected
    <int>: 1
to equal
    <int>: 0 failed [FAILED] Timed out after 5.000s.
Expected
    <int>: 1
to equal
    <int>: 0
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/visibility_test.go:307 @ 09/13/24 16:50:11.318
}
```

**What you expected to happen**:
Any errors have never been seen.

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/3043/pull-kueue-test-e2e-main-1-31/1834633751506718720

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-13T17:14:53Z

/kind flake
