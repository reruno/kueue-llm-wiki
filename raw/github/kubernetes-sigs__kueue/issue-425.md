# Issue #425: Don't misappropriate ResourceFlavor labels for nodeSelector

**Summary**: Don't misappropriate ResourceFlavor labels for nodeSelector

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/425

**Last updated**: 2023-02-16T02:54:49Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@SammyA](https://github.com/SammyA)
- **Created**: 2022-11-10T13:09:49Z
- **Updated**: 2023-02-16T02:54:49Z
- **Closed**: 2022-11-28T14:34:12Z
- **Labels**: `kind/bug`, `help wanted`
- **Assignees**: [@kerthcet](https://github.com/kerthcet)
- **Comments**: 14

## Description

**What happened**:
Kueue was deployed via ArgoCD. Jobs that were ready to run produced Pods that stayed "Pending" because k8s could not find any nodes to satisfy the nodeSelector restriction. The nodeSelectors were put there by Kueue and taken from the ResourceFlavor labels.

Systems like ArgoCD and Helm add labels to objects under their control to select all objects belonging to a certain app/chart. This makes ResourceFlavors incompatible with any system that add their own labels.

**What you expected to happen**:
Don't use the ResourceFlavor labels for node selection. Define an explicit field in the ResourceFlavor definition for nodeSelector.

**How to reproduce it (as minimally and precisely as possible)**:
Add a label like `app.kubernetes.io/managed-by: Helm` to a ResourceFlavor. This is one of several labels Helm adds to every object it controls. ArgoCd works in a similar fashion. Jobs using this ResourceFlavor wil have the same label added as a nodeSelector. If you don't have nodes with this label (you probably won't), this job can never run, and will stay pending indefinately.

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): v1.25.3
- Kueue version (use `git describe --tags --dirty --always`): v0.2.1
- Cloud provider or hardware configuration: on-premise 
- OS (e.g: `cat /etc/os-release`): Debian GNU/Linux 11 (bullseye)
- Kernel (e.g. `uname -a`): 5.10.0-19-amd64
- Install tools: kubeadm
- Others:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-11-10T15:03:03Z

We used to have a separate labels field, but we removed it because it caused confusion #334.

But your use case seems like a good justification to revert. Although it's probably better to have a different name for the field, like `matchingLabels`.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-11-10T15:03:18Z

cc @ahg-g

### Comment by [@SammyA](https://github.com/SammyA) — 2022-11-10T15:09:50Z

May I suggest `nodeSelector` as the field name? It conveys very explicity what it's purpose is, thereby avoiding any confusion with the earlier `labels` implementation (which sounds too generic to me). It also nicely coincides with the `nodeSelector` field in Pods where the values should ultimately end up.

### Comment by [@inossidabile](https://github.com/inossidabile) — 2022-11-11T17:50:48Z

Just hit exactly the same issue. Apparently there's no workaround? Helm states having such label there is a must. So there seem to be no way to create ResourceFlavors via helm as of now?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-11-11T18:13:11Z

I don't think there is a workaround, besides downgrading to kueue 0.1.1

I agree with the `nodeSelector` name. Can someone work on it? We can have it for the 0.3.0 release.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-11-11T18:40:28Z

Sounds good, too bad we went ahead and removed the explicit parameter in the first place! But, the good thing is that we can add it back without needing to bump the api version.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-11-23T21:37:22Z

/help

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-11-23T21:37:23Z

@alculquicondor: 
	This request has been marked as needing help from a contributor.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- Does this issue have zero to low barrier of entry?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://git.k8s.io/community/contributors/guide/help-wanted.md) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-help` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/425):

>/help


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-11-24T02:39:06Z

Also meet this problem in our cluster, we use argocd. I'd like to fix this.
/assign

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-11-24T02:43:51Z

And also, maybe we should provide a helm chart for installation besides kustomize, we depends a lot on helm charts in CI/CD, I guess it's true for some other uses as well. 

Created a issue here https://github.com/kubernetes-sigs/kueue/issues/436

### Comment by [@maaft](https://github.com/maaft) — 2023-02-15T15:31:02Z

Just hit the same issue. Are there any workarounds currently?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-15T16:02:29Z

You can use a development version. We didn't backport this to 0.2 as it's not a backwards compatible change.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-15T16:03:00Z

https://github.com/kubernetes-sigs/kueue/blob/main/docs/setup/install.md#install-the-latest-development-version

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-02-16T02:54:49Z

Is the advice helpful and solved your problem? @maaft
