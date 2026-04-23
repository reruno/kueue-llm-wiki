# Issue #1098: Release the lock as soon as possible when computing the snapashot for CQ visibility

**Summary**: Release the lock as soon as possible when computing the snapashot for CQ visibility

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1098

**Last updated**: 2023-09-19T06:25:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2023-09-08T08:00:30Z
- **Updated**: 2023-09-19T06:25:55Z
- **Closed**: 2023-09-19T06:25:55Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

This is a follow up for review remark: https://github.com/kubernetes-sigs/kueue/pull/1069/files/3b1f7c19d16b67a267d30ba8945ae1a3bb2b501e#r1319099583

**What would you like to be cleaned**:

The sort operation can be done once the lock is released.

**Why is this needed**:

Improve performance of Kueue by reducing lock contention.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-09-19T04:28:57Z

/assign @lowang-bh

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-09-19T04:28:59Z

@tenzen-y: GitHub didn't allow me to assign the following users: lowang-bh.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1098#issuecomment-1724814725):

>/assign @lowang-bh 
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
