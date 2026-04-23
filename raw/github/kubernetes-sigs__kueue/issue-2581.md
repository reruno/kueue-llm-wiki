# Issue #2581: Flaky e2e: Kueue visibility server when There are pending workloads due to capacity maxed by the admitted job

**Summary**: Flaky e2e: Kueue visibility server when There are pending workloads due to capacity maxed by the admitted job

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2581

**Last updated**: 2024-07-15T11:59:10Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-07-11T11:39:16Z
- **Updated**: 2024-07-15T11:59:10Z
- **Closed**: 2024-07-15T11:59:10Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 3

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
```
{Timed out after 5.001s.
The matcher passed to Eventually returned the following error:
    <*errors.errorString | 0xc000916e80>: 
    NotFoundError expects an error
    {
        s: "NotFoundError expects an error",
    } failed [FAILED] Timed out after 5.001s.
The matcher passed to Eventually returned the following error:
    <*errors.errorString | 0xc000916e80>: 
    NotFoundError expects an error
    {
        s: "NotFoundError expects an error",
    }
In [AfterEach] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/visibility_test.go:133 @ 07/10/24 20:52:49.276
}
```

**What you expected to happen**:
No issue

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2553/pull-kueue-test-e2e-main-1-27/1811140041414545408
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2579/pull-kueue-test-e2e-main-1-29/1811357227194257408

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-11T13:53:27Z

cc @PBundyra

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-07-11T16:53:32Z

/kind flake

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-07-15T06:05:57Z

/assign
