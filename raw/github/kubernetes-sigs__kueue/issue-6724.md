# Issue #6724: Specify the go version entirely within the Kueue repository

**Summary**: Specify the go version entirely within the Kueue repository

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6724

**Last updated**: 2025-09-05T08:13:27Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-09-04T11:10:51Z
- **Updated**: 2025-09-05T08:13:27Z
- **Closed**: 2025-09-05T08:13:27Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 7

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to encapsulate the version of golang used for testing Kueue in the Kueue repo.

We applied similar approach for bumping Kubernetes version under https://github.com/kubernetes-sigs/kueue/issues/4729

**Why is this needed**:

To prevent bumping it "blindly" without running Kueue tests in the test-infra.

This was a source of issues are required revert here: https://github.com/kubernetes/test-infra/pull/35437

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-04T11:11:00Z

cc @tenzen-y @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-04T11:18:21Z

We still need to update `public.ecr.aws/docker/library/golang` in `test-infra` since it’s a container image. However, I think we can move the `BUILDER_IMAGE` environment variable to the `kueue` repository.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-04T12:10:05Z

> We still need to update `public.ecr.aws/docker/library/golang` in `test-infra` since it’s a container image. However, I think we can move the `BUILDER_IMAGE` environment variable to the `kueue` repository.

Hmm, I see, what about replacing the container image with a generic one as for some tests, and only use the golang image inside to run tests?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-04T14:54:51Z

/reopen
it does not seem done, we probably also need some changes in test-infra

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-04T14:54:56Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6724#issuecomment-3254116008):

>/reopen
>it does not seem done, we probably also need some changes in test-infra


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-04T14:55:07Z

let me know if I'm missing something @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-04T19:56:37Z

Yes, you're right. We need to update test-infra as well.
