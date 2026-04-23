# Issue #2237: support deployment object

**Summary**: support deployment object

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2237

**Last updated**: 2024-06-25T21:00:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@inforly](https://github.com/inforly)
- **Created**: 2024-05-20T12:49:15Z
- **Updated**: 2024-06-25T21:00:29Z
- **Closed**: 2024-06-25T21:00:28Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Can Kueue add the support to K8s deployment object, so that the online services (deployments) can work together with the offline jobs together under one namespace. 

**Why is this needed**:
Usually, one namespace has both online services and offline jobs running, so needs a unified queue system to manage the resource and the scheduling, then the features like deployment autoscaling/preemption can be implemented based on this, without blocking by the resource quota (admission controller).

**Completion requirements**:


This enhancement requires the following artifacts:

- [*] Design doc
- [*] API change
- [*] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-22T14:31:33Z

Can you clarify what your expectations are in terms of atomicity?

Should all pods of the Deployment be admitted at the same time? If not, the pod integration might be a good way to Kueue support services today.

Also see #635

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-25T21:00:24Z

/close
Duplicate of #867

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-25T21:00:28Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2237#issuecomment-2189961908):

>/close
>Duplicate of #867


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
