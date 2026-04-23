# Issue #1389: Flaky: Job controller interacting with scheduler Should schedule jobs with partial admission

**Summary**: Flaky: Job controller interacting with scheduler Should schedule jobs with partial admission

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1389

**Last updated**: 2023-12-01T01:12:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2023-12-01T01:08:38Z
- **Updated**: 2023-12-01T01:12:32Z
- **Closed**: 2023-12-01T01:12:30Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Failed "Job Controller Suite: [It] Job controller interacting with scheduler Should schedule jobs with partial admission"

**What you expected to happen**:
No error happens.

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1252/pull-kueue-test-integration-main/1730371464466534400

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-01T01:12:26Z

Ah, this is duplicated with #1369 
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-12-01T01:12:31Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1389#issuecomment-1835242041):

>Ah, this is duplicated with #1369 
>/close
>
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
