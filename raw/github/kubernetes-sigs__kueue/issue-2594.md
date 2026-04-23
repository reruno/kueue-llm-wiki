# Issue #2594: Adding waitForPodsReady capability for all the jobs kueue supports

**Summary**: Adding waitForPodsReady capability for all the jobs kueue supports

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2594

**Last updated**: 2024-08-06T18:40:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@m-mamdouhi](https://github.com/m-mamdouhi)
- **Created**: 2024-07-12T15:09:27Z
- **Updated**: 2024-08-06T18:40:02Z
- **Closed**: 2024-07-25T05:06:50Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 6

## Description

If my implementation is correct the waitForPodsReady capability is limited and not extended to the kubeflow jobs correct? it would be nice to have this "gangscheduling" capability with all of the jobs that kueue supports

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-07-25T05:06:00Z

/remove-kind feature
/kind help

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-07-25T05:06:03Z

@tenzen-y: The label(s) `kind/help` cannot be applied, because the repository doesn't have them.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2594#issuecomment-2249440205):

>/remove-kind feature
>/kind help
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-07-25T05:06:47Z

Actually, the `waitForPodsReady` is supported for all Jobs, including the kubeflow jobs.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-07-25T05:06:51Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2594#issuecomment-2249441692):

>Actually, the `waitForPodsReady` is supported for all Jobs, including the kubeflow jobs.
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@FWCoder](https://github.com/FWCoder) — 2024-08-06T18:27:17Z

What is the behavior on "waitForPodsReady" that can help on "Gand Scheduling" use case?

### Comment by [@FWCoder](https://github.com/FWCoder) — 2024-08-06T18:40:01Z

> What is the behavior on "waitForPodsReady" that can help on "Gand Scheduling" use case?

I mean "Gang Scheduling".
