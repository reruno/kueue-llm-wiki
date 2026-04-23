# Issue #3679: Flaky scheduler integration test

**Summary**: Flaky scheduler integration test

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3679

**Last updated**: 2024-12-04T10:20:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-11-28T14:18:18Z
- **Updated**: 2024-12-04T10:20:02Z
- **Closed**: 2024-12-04T10:20:00Z
- **Labels**: `kind/bug`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Scheduler integration test failed

**What you expected to happen**:
No failure

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3677/pull-kueue-test-integration-main/1862134281669709824

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-11-28T14:18:38Z

/cc @gabesaba

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-12-04T07:34:38Z

/assign

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-12-04T10:19:55Z

/close
duplicate of #3633

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-12-04T10:20:01Z

@gabesaba: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3679#issuecomment-2516859830):

>/close
>duplicate of #3633


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
