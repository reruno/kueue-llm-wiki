# Issue #465: Validate using open API where possible

**Summary**: Validate using open API where possible

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/465

**Last updated**: 2023-01-03T15:48:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-12-06T18:18:32Z
- **Updated**: 2023-01-03T15:48:29Z
- **Closed**: 2023-01-03T15:48:28Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@nayihz](https://github.com/nayihz)
- **Comments**: 6

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

We do validation through webhooks. Some validations could be translated to openAPI using this documentation https://book.kubebuilder.io/reference/markers/crd-validation.html

When doing so, we should remove the go code that does the same validation, to avoid duplication. And we need to make sure the validation is covered in integration tests, as opposed to unit tests. Maybe we should be running the integrations tests in 1.23, the oldest k8s supported version.

**Why is this needed**:

We eventually want to get rid of webhooks #463. Before CEL support is widespread, we can at least start migrating some logic.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-12-06T18:18:56Z

cc @cmssczy, would you like to work on this?

### Comment by [@nayihz](https://github.com/nayihz) — 2022-12-07T03:13:45Z

Yes.
/assign

### Comment by [@nayihz](https://github.com/nayihz) — 2022-12-27T02:12:14Z

closed this as completed in https://github.com/kubernetes-sigs/kueue/pull/466
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-12-27T02:12:17Z

@cmssczy: You can't close an active issue/PR unless you authored it or you are a collaborator.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/465#issuecomment-1365555108):

>closed this as completed in https://github.com/kubernetes-sigs/kueue/pull/466
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-03T15:48:24Z

/close
Thanks!

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-01-03T15:48:28Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/465#issuecomment-1369925005):

>/close
>Thanks!


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
