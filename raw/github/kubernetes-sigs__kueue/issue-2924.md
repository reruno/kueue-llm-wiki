# Issue #2924: Flaky: Kueue visibility server when There are pending workloads due to capacity maxed by the admitted job Should allow fetching information about pending workloads in ClusterQueue

**Summary**: Flaky: Kueue visibility server when There are pending workloads due to capacity maxed by the admitted job Should allow fetching information about pending workloads in ClusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2924

**Last updated**: 2024-08-28T12:08:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-08-28T12:04:59Z
- **Updated**: 2024-08-28T12:08:05Z
- **Closed**: 2024-08-28T12:08:03Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 3

## Description

**What happened**:

Flaky test on `periodic-kueue-test-e2e-main-1-29`:
`Kueue visibility server when There are pending workloads due to capacity maxed by the admitted job Should allow fetching information about pending workloads in ClusterQueue`

**What you expected to happen**:

To pass consistently

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/logs/periodic-kueue-test-e2e-main-1-29/1828542136862117888

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-08-28T12:07:01Z

Is it duplicate for https://github.com/kubernetes-sigs/kueue/issues/2920?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-08-28T12:08:00Z

Yes, thanks!

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-08-28T12:08:04Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2924#issuecomment-2315147888):

>Yes, thanks!
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
