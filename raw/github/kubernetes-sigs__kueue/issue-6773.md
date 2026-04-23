# Issue #6773: [flaky test] Scheduler when Preemption is enabled in fairsharing and there are best effort and guaranteed workloads Guaranteed workloads cause preemption of a single best effort workload

**Summary**: [flaky test] Scheduler when Preemption is enabled in fairsharing and there are best effort and guaranteed workloads Guaranteed workloads cause preemption of a single best effort workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6773

**Last updated**: 2025-11-12T07:48:47Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@pajakd](https://github.com/pajakd)
- **Created**: 2025-09-09T13:49:20Z
- **Updated**: 2025-11-12T07:48:47Z
- **Closed**: 2025-11-12T07:48:46Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

failure https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6769/pull-kueue-test-integration-baseline-main/1965399536276869120

**What you expected to happen**:

no failure :)

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-12T07:48:42Z

/close
Duplicate of https://github.com/kubernetes-sigs/kueue/issues/7004 which has more comments

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-12T07:48:47Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6773#issuecomment-3520501222):

>/close
>Duplicate of https://github.com/kubernetes-sigs/kueue/issues/7004 which has more comments


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
