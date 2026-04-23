# Issue #946: Default support for MPI jobs causes a crashloop in the controller if the CRD is not installed

**Summary**: Default support for MPI jobs causes a crashloop in the controller if the CRD is not installed

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/946

**Last updated**: 2023-07-05T06:56:20Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@bh-tt](https://github.com/bh-tt)
- **Created**: 2023-07-04T14:00:47Z
- **Updated**: 2023-07-05T06:56:20Z
- **Closed**: 2023-07-04T15:35:03Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
After upgrading to the newest helm chart version, the controller ended up in a crashloop as we do have the MPI job installed but support for it is enabled by default.
**What you expected to happen**:
I expected the same configuration to continue working after an update, not a breaking change without even a Chart.yaml version increment. Using an actual helm repository instead of cloning this repository means the chart version can be incremented in a meaningful way.

I expect the chart to work by default on a standard kubeadm cluster without additional (except kueue's own) CRDs installed.

**How to reproduce it (as minimally and precisely as possible)**:
Install the controller on a cluster without MPIJob CRD installed. The crash only happens after approximately 2 minutes 20 seconds, which might mean the current unit tests do not catch it?

**Anything else we need to know?**:
Initially it logs some errors saying that for kind CRD they should be installed before the controller is started, after a while the controller crashes as it spends too long waiting for the MPI job cache to be initialized.

Commit 4599a19484070f0a239a66cc02b3fc3bccae68e0 introduces these changes to the chart and kustomize files.

**Environment**:
- Kubernetes version (use `kubectl version`): 1.27.3
- Kueue version (use `git describe --tags --dirty --always`): v0.3.2 controller, chart version 
- Cloud provider or hardware configuration: kubeadm 1.27.3
- OS (e.g: `cat /etc/os-release`): 
- Kernel (e.g. `uname -a`):
- Install tools: helm
- Others:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-04T15:28:17Z

@stuton PTAL

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-04T15:34:59Z

Oh I understand what is going on.

You are using a 0.3.2 controller with a chart from the main branch.

We haven't officially released helm charts yet, so you should treat the charts in the main branch as experimental and, in particular, no guaranteed to work with an older release of kueue.

We hope to have a 0.4 release of Kueue this week. We are also investigating how best to serve the helm charts given our infrastructure and the domain we have #745.
Feel free to leave some suggestions if you have any.

As it stands, this is not actionable for us.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-07-04T15:35:04Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/946#issuecomment-1620456708):

>Oh I understand what is going on.
>
>You are using a 0.3.2 controller with a chart from the main branch.
>
>We haven't officially released helm charts yet, so you should treat the charts in the main branch as experimental and, in particular, no guaranteed to work with an older release of kueue.
>
>We hope to have a 0.4 release of Kueue this week. We are also investigating how best to serve the helm charts given our infrastructure and the domain we have #745.
>Feel free to leave some suggestions if you have any.
>
>As it stands, this is not actionable for us.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@Borrelhapje](https://github.com/Borrelhapje) — 2023-07-05T06:56:20Z

Thanks for the quick response, for now the problem is fixable by simply overriding the integrations.
