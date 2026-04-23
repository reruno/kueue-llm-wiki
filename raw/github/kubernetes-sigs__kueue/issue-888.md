# Issue #888: Flaky job for unit tests

**Summary**: Flaky job for unit tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/888

**Last updated**: 2023-06-22T12:34:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-06-22T12:30:48Z
- **Updated**: 2023-06-22T12:34:32Z
- **Closed**: 2023-06-22T12:34:31Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 2

## Description

**What happened**:

I've seen a couple of instances where we run out of time in the bot for running unit tests https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/878/pull-kueue-test-unit-main/1671583007175086080

We could of course increase the timeout. But we could also take the opportunity to check what are the most time consuming tests and see what we can do.

**What you expected to happen**:

Tests should succeed.

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-22T12:34:26Z

Actually, no, we can see that this is happening specifically with the `cache` package:

```
✓  pkg/webhooks (190ms)
✓  pkg/workload (210ms)
✖  pkg/cache (10m0.148s)
```

/close


because this was already reported in #886

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-06-22T12:34:31Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/888#issuecomment-1602559337):

>Actually, no, we can see that this is happening specifically with the `cache` package:
>
>```
>✓  pkg/webhooks (190ms)
>✓  pkg/workload (210ms)
>✖  pkg/cache (10m0.148s)
>```
>
>/close
>
>
>because this was already reported in #886 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
