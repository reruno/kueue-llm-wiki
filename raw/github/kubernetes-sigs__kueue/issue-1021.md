# Issue #1021: Flaky test: Kueue when Creating a Job With Queueing [It] Should unsuspend a job and set nodeSelectors

**Summary**: Flaky test: Kueue when Creating a Job With Queueing [It] Should unsuspend a job and set nodeSelectors

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1021

**Last updated**: 2023-10-02T19:08:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@BinL233](https://github.com/BinL233)
- **Created**: 2023-07-28T02:32:55Z
- **Updated**: 2023-10-02T19:08:31Z
- **Closed**: 2023-10-02T19:08:30Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 7

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
`Kueue when Creating a Job With Queueing [It] Should unsuspend a job and set nodeSelectors` is flaky.

e2e test failed link: 
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1018/pull-kueue-test-e2e-main-1-26/1684507556703113216

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

### Comment by [@BinL233](https://github.com/BinL233) — 2023-07-28T09:12:06Z

`apimeta.IsStatusConditionTrue` in line 142 of kueue/test/e2e/e2e_test.go, always run for more than 15 seconds. I think this is because the pod needs time to pull image and run sleep. There is a risk that the job reaches `util.Timeout`.

### Comment by [@BinL233](https://github.com/BinL233) — 2023-07-28T09:22:02Z

Can we just extend the time limit like `util.Timeout * 1.5`?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-28T12:23:10Z

That sounds plausible.
We can introduce another constant `LongTimeout` and put a comment that is meant for E2E tests when waiting for complex operations such as running pods to completion.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-08-03T13:56:28Z

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1014/pull-kueue-test-e2e-main-1-24/1687045071767080960
/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-08-03T13:56:33Z

@alculquicondor: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1021#issuecomment-1664031756):

>https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1014/pull-kueue-test-e2e-main-1-24/1687045071767080960
>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-02T19:08:26Z

Not sure if it's reproducible in 1.25

Let's reopen if we see it again.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-10-02T19:08:31Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1021#issuecomment-1743603980):

>Not sure if it's reproducible in 1.25
>
>Let's reopen if we see it again.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
