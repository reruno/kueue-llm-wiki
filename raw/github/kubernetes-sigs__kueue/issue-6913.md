# Issue #6913: [TAS] Unhealthy node replacement with TAS podset slice can lead to empty replacement topology assignment

**Summary**: [TAS] Unhealthy node replacement with TAS podset slice can lead to empty replacement topology assignment

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6913

**Last updated**: 2025-09-22T14:46:06Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-09-18T13:34:55Z
- **Updated**: 2025-09-22T14:46:06Z
- **Closed**: 2025-09-22T14:46:06Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Using TAS PodSet slice and deleting an assigned Node led to empty replacement topology assignment which was invalid

**What you expected to happen**:

**How to reproduce it (as minimally and precisely as possible)**:

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-19T14:31:43Z

/reopen
TO make sure the cherrypick of https://github.com/kubernetes-sigs/kueue/pull/6914 is done

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-19T14:31:49Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6913#issuecomment-3312443362):

>/reopen
>TO make sure the cherrypick of https://github.com/kubernetes-sigs/kueue/pull/6914 is done


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-09-22T14:46:00Z

The cherrypick is done: https://github.com/kubernetes-sigs/kueue/pull/6927
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-22T14:46:06Z

@PBundyra: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6913#issuecomment-3319506601):

>The cherrypick is done: https://github.com/kubernetes-sigs/kueue/pull/6927
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
