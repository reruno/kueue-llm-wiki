# Issue #1195: [clusterQueue] Keep different counters of `reserved` and `in use` resources in the queues status.

**Summary**: [clusterQueue] Keep different counters of `reserved` and `in use` resources in the queues status.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1195

**Last updated**: 2023-10-20T17:28:49Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@trasc](https://github.com/trasc)
- **Created**: 2023-10-11T14:04:03Z
- **Updated**: 2023-10-20T17:28:49Z
- **Closed**: 2023-10-20T17:28:49Z
- **Labels**: `kind/feature`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Different counters of `reserved` and `in use` resources in the queues status.

**Why is this needed**:

To be able to check the difference between the quota that is reserved and the one that is reserved and workload admitted. In a tow stem admission scenario.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2023-10-11T14:06:37Z

/assign

### Comment by [@trasc](https://github.com/trasc) — 2023-10-11T15:10:15Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-10-11T15:10:20Z

@trasc: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1195#issuecomment-1757913142):

>/reopen
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@trasc](https://github.com/trasc) — 2023-10-11T17:54:32Z

/assign
