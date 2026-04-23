# Issue #1392: Admitted event reported when only quota is reserved

**Summary**: Admitted event reported when only quota is reserved

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1392

**Last updated**: 2023-12-14T19:55:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-12-01T21:26:57Z
- **Updated**: 2023-12-14T19:55:23Z
- **Closed**: 2023-12-14T19:55:21Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 8

## Description

**What happened**:

When using admission checks, and the Workload gets the QuotaReserved, we get an event:

```
Normal  Admitted  5m57s  kueue-admission  Admitted by ClusterQueue dws-cluster-queue, wait time was 0s
```

This is not accurate, as at this point the workload is not admitted.

https://github.com/kubernetes-sigs/kueue/blob/0385c104ce0dc98011a4bbd28836a9fdb466a173/pkg/scheduler/scheduler.go#L454

**What you expected to happen**:

Two events, one for when the workload gets the quota reservation and one when it gets admitted.
If admission checks are not configured (or in other words, admission happens instantly, prefer to have just one event for Admitted)

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-01T21:27:05Z

/assign @stuton

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-04T15:01:36Z

/assign @achernevskii

### Comment by [@trasc](https://github.com/trasc) — 2023-12-11T09:18:02Z

/assign

### Comment by [@trasc](https://github.com/trasc) — 2023-12-11T09:19:05Z

/unassign @achernevskii
/unassign @stuton

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-14T16:58:22Z

/reopen
@trasc please prepare a cherry-pick for release-0.5

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-12-14T16:58:27Z

@alculquicondor: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1392#issuecomment-1856209861):

>/reopen
>@trasc please prepare a cherry-pick for release-0.5


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@trasc](https://github.com/trasc) — 2023-12-14T19:55:16Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-12-14T19:55:22Z

@trasc: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1392#issuecomment-1856492057):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
