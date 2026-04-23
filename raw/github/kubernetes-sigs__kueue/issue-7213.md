# Issue #7213: Graduate ManagedJobsNamespaceSelectorAlwaysRespected to Beta

**Summary**: Graduate ManagedJobsNamespaceSelectorAlwaysRespected to Beta

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7213

**Last updated**: 2025-11-06T14:25:10Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-09T07:23:23Z
- **Updated**: 2025-11-06T14:25:10Z
- **Closed**: 2025-11-06T14:25:10Z
- **Labels**: `kind/feature`
- **Assignees**: [@PannagaRao](https://github.com/PannagaRao)
- **Comments**: 8

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

I would like to move forward with ManagedJobsNamespaceSelectorAlwaysRespected to Beta. 

**Why is this needed**:

To improve the API as the new behavior under ManagedJobsNamespaceSelectorAlwaysRespected is more consistent.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-09T07:24:21Z

cc @tenzen-y @kannon92 @PannagaRao  @Singularity23x0

### Comment by [@PannagaRao](https://github.com/PannagaRao) — 2025-10-09T14:54:21Z

I can work on this!

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-09T15:34:46Z

/assign @PannagaRao

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-22T11:06:15Z

@PannagaRao @kannon92 any progress on that?

### Comment by [@PannagaRao](https://github.com/PannagaRao) — 2025-10-22T12:59:39Z

> [@PannagaRao](https://github.com/PannagaRao) [@kannon92](https://github.com/kannon92) any progress on that?

I was out last week so couldn't work on it. Will look into it soon. Thanks!

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-31T08:51:54Z

@PannagaRao I think we can basically turn the feature gate to Beta in kube_features.go, open PR and see what breaks (potentially no failures).

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-06T14:25:04Z

PR was merged.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-06T14:25:10Z

@kannon92: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7213#issuecomment-3497502094):

>PR was merged.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
