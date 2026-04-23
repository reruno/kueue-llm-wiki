# Issue #3718: Flaky e2e MultiKueue test

**Summary**: Flaky e2e MultiKueue test

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3718

**Last updated**: 2024-12-03T10:58:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-12-03T10:40:47Z
- **Updated**: 2024-12-03T10:58:31Z
- **Closed**: 2024-12-03T10:58:30Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
E2e MultiKueue test failed

**What you expected to happen**:
No failure

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3708/pull-kueue-test-multikueue-e2e-main/1863892287004610560

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-12-03T10:40:58Z

cc @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-03T10:58:25Z

/close

Duplicate of https://github.com/kubernetes-sigs/kueue/issues/3581.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-12-03T10:58:30Z

@mbobrovskyi: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3718#issuecomment-2514220046):

>/close
>
>Duplicate of https://github.com/kubernetes-sigs/kueue/issues/3581.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
