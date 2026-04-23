# Issue #998: Hierarchical Quota

**Summary**: Hierarchical Quota

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/998

**Last updated**: 2023-07-18T16:49:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2023-07-18T16:30:59Z
- **Updated**: 2023-07-18T16:49:39Z
- **Closed**: 2023-07-18T16:49:38Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Support for hierarchical quota.

**Why is this needed**:

Currently Kueue supports two levels of quota management which is sufficient for many users. However, some users have deeper organizations and require hierarchical quota.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-07-18T16:34:18Z

Is this the same as #79?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-18T16:49:35Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-07-18T16:49:39Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/998#issuecomment-1640580870):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
