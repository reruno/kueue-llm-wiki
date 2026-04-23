# Issue #1108: Pre-pull docker images used for testing

**Summary**: Pre-pull docker images used for testing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1108

**Last updated**: 2023-09-19T06:23:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2023-09-11T09:52:22Z
- **Updated**: 2023-09-19T06:23:32Z
- **Closed**: 2023-09-19T06:23:31Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 3

## Description

This is needed to prevent timeouts in e2e tests which now need to fetch images

Example flaky test, probably caused by the additional time on fetching the image: https://github.com/kubernetes-sigs/kueue/issues/1021. Another already closed issue: https://github.com/kubernetes-sigs/kueue/pull/1025.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-09-11T14:59:25Z

+1
We can use `kind load`

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-09-19T06:23:28Z

fixed by: https://github.com/kubernetes-sigs/kueue/pull/1126
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-09-19T06:23:32Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1108#issuecomment-1724896204):

>fixed by: https://github.com/kubernetes-sigs/kueue/pull/1126
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
