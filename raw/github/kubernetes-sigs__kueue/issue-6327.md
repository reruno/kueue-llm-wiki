# Issue #6327: [Flaky] E2E MultiKueue tests fails: when MultiKueue with Incremental mode Should run a job on worker if admitted

**Summary**: [Flaky] E2E MultiKueue tests fails: when MultiKueue with Incremental mode Should run a job on worker if admitted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6327

**Last updated**: 2025-07-31T14:12:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-07-31T13:31:57Z
- **Updated**: 2025-07-31T14:12:51Z
- **Closed**: 2025-07-31T14:12:50Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
E2E MultiKueue test failed

**What you expected to happen**:
No failure

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6322/pull-kueue-test-e2e-multikueue-main/1950904441649500160

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-07-31T13:32:03Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-31T14:12:45Z

/close 
duplicate of https://github.com/kubernetes-sigs/kueue/issues/6233

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-31T14:12:51Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6327#issuecomment-3140141955):

>/close 
>duplicate of https://github.com/kubernetes-sigs/kueue/issues/6233


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
