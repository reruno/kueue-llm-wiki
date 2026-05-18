# Issue #8834: End To End MultiKueue Suite: kindest/node:v1.34.3: [BeforeSuite]

**Summary**: End To End MultiKueue Suite: kindest/node:v1.34.3: [BeforeSuite]

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8834

**Last updated**: 2026-05-11T07:26:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-01-27T16:39:23Z
- **Updated**: 2026-05-11T07:26:29Z
- **Closed**: 2026-05-11T07:26:28Z
- **Labels**: `kind/bug`, `kind/flake`, `area/multikueue`
- **Assignees**: _none_
- **Comments**: 3

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-05-11T07:26:22Z

/close
Closing stale tickets which haven't re-occur in 2 months, because maybe some of them are already fixed along the way. We will re-open when they re-occur again.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-05-11T07:26:29Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8834#issuecomment-4418416390):

>/close
>Closing stale tickets which haven't re-occur in 2 months, because maybe some of them are already fixed along the way. We will re-open when they re-occur again.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
