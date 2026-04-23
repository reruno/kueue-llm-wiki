# Issue #8834: End To End MultiKueue Suite: kindest/node:v1.34.3: [BeforeSuite]

**Summary**: End To End MultiKueue Suite: kindest/node:v1.34.3: [BeforeSuite]

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8834

**Last updated**: 2026-02-16T10:49:29Z

---

## Metadata

- **State**: open
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-01-27T16:39:23Z
- **Updated**: 2026-02-16T10:49:29Z
- **Closed**: —
- **Labels**: `kind/bug`, `kind/flake`, `area/multikueue`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake 

**What happened**:

End To End MultiKueue Suite: kindest/node:v1.34.3: [BeforeSuite]

```
{Timed out after 300.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/e2e.go:278 with:
Expected
    <int32>: 0
to equal
    <int32>: 2 failed [FAILED] Timed out after 300.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/e2e.go:278 with:
Expected
    <int32>: 0
to equal
    <int32>: 2
In [BeforeSuite] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/suite_test.go:282 @ 01/27/26 16:05:53.36
}
```

**What you expected to happen**:

no issue

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8827/pull-kueue-test-e2e-multikueue-release-0-16/2016176664433659904

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

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-02-16T10:49:27Z

/area multikueue
