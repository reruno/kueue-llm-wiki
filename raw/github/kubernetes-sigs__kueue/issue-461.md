# Issue #461: Add e2e tests for each release of Kubernetes that we support

**Summary**: Add e2e tests for each release of Kubernetes that we support

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/461

**Last updated**: 2022-12-06T14:45:53Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2022-12-05T15:26:17Z
- **Updated**: 2022-12-06T14:45:53Z
- **Closed**: 2022-12-06T14:45:52Z
- **Labels**: `kind/feature`
- **Assignees**: [@kannon92](https://github.com/kannon92)
- **Comments**: 7

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Now that we have e2e tests, we should run e2e test for each version of Kubernetes that we support. For this issue, let's target 1.23, 1.24 and 1.25.

**Why is this needed**:
This allows us to find out if we have breaking changes with the releases that we support.

**Completion requirements**:

We add prow e2e tests that run for each kubernetes release that we support.  

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-12-05T15:37:43Z

We shouldn't test 1.22, as it's no longer supported https://kubernetes.io/releases/
It might work, but we shouldn't commit to it.

### Comment by [@kannon92](https://github.com/kannon92) — 2022-12-05T15:40:49Z

> We shouldn't test 1.22, as it's no longer supported https://kubernetes.io/releases/ It might work, but we shouldn't commit to it.

Updated the ticket.

### Comment by [@kannon92](https://github.com/kannon92) — 2022-12-05T20:34:18Z

/assign @kannon92

### Comment by [@kannon92](https://github.com/kannon92) — 2022-12-05T21:40:35Z

https://github.com/kubernetes/test-infra/pull/28182 is the new PR for this.

### Comment by [@kannon92](https://github.com/kannon92) — 2022-12-06T12:56:08Z

I think the tests are working so I think we can call this done.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-12-06T14:45:49Z

/close
awesome, thanks!

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-12-06T14:45:53Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/461#issuecomment-1339494176):

>/close
>awesome, thanks!


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
