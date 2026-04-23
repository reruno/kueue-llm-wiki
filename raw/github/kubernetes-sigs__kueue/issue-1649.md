# Issue #1649: Flaky E2E test for MultiKueue

**Summary**: Flaky E2E test for MultiKueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1649

**Last updated**: 2024-01-26T20:58:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@B1F030](https://github.com/B1F030)
- **Created**: 2024-01-26T08:32:49Z
- **Updated**: 2024-01-26T20:58:31Z
- **Closed**: 2024-01-26T20:58:30Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->
/kind flake

**What happened**:
```
Internal error occurred: failed calling webhook "vclusterqueue.kb.io": failed to call webhook:
Post "https://kueue-webhook-service.kueue-system.svc:443/validate-kueue-x-k8s-io-v1beta1-clusterqueue?timeout=10s":
dial tcp 10.96.212.22:443: connect: connection refused
```
**What you expected to happen**:

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1385/pull-kueue-test-e2e-main-1-28/1750699242197880832
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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-26T10:25:35Z

cc: @trasc

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-26T20:58:26Z

/close
in favor of #1658

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-01-26T20:58:31Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1649#issuecomment-1912687310):

>/close
>in favor of #1658


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
