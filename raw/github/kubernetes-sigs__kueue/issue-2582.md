# Issue #2582: SuspendJob feature gate is now removed

**Summary**: SuspendJob feature gate is now removed

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2582

**Last updated**: 2024-07-11T17:05:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@m-mamdouhi](https://github.com/m-mamdouhi)
- **Created**: 2024-07-11T12:08:46Z
- **Updated**: 2024-07-11T17:05:04Z
- **Closed**: 2024-07-11T17:05:03Z
- **Labels**: `kind/support`
- **Assignees**: _none_
- **Comments**: 2

## Description

SuspendJob feature gate is now removed in kubernetes but it is still in the installation guide.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-07-11T17:04:59Z

We still support older kubernetes version like v1.25.
So, keeping the mentioning of the featureGate name would be worth it.

/kind support
/remove-kind bug
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-07-11T17:05:03Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2582#issuecomment-2223449458):

>We still support older kubernetes version like v1.25.
>So, keeping the mentioning of the featureGate name would be worth it.
>
>/kind support
>/remove-kind bug
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
