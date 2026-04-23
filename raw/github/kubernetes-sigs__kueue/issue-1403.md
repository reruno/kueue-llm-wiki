# Issue #1403: Respect NS ResourceQuota in Kueue

**Summary**: Respect NS ResourceQuota in Kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1403

**Last updated**: 2023-12-05T06:24:43Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2023-12-05T06:21:34Z
- **Updated**: 2023-12-05T06:24:43Z
- **Closed**: 2023-12-05T06:24:42Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

NS ResourceQuota helps to constrain the quota for each ns, however, we didn't count this resource in Kueue, this will lead to like workload admitted in kueue, but blocked by kubernetes pod creation as violating the NS ResourceQuota.

Some rough ideas:
- For localQueue, since it's namespaced, jobs belong to one localQueue should not exceed the NS ResourceQuota.
- For clusterQueue, in creation, if all NS has ResourceQuota, then the sum of clusterQueue should not exceed the sum of ResourceQuota.

Glad to hear other ideas.

**Why is this needed**:

Fill up the gap with plain kubernetes.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-12-05T06:23:35Z

cc @B1F030

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-05T06:24:35Z

This is duplicated with #696

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-05T06:24:38Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-12-05T06:24:43Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1403#issuecomment-1840086818):

>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
