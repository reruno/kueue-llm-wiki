# Issue #1198: Add UTs for AdjustResources

**Summary**: Add UTs for AdjustResources

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1198

**Last updated**: 2023-10-26T23:54:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-10-11T19:03:51Z
- **Updated**: 2023-10-26T23:54:23Z
- **Closed**: 2023-10-26T23:54:23Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

#1197 added a dedicated helper method to adjust resources from LimitRanges, RuntimeClass and limits.
They need some tests. I have a WIP in https://github.com/kubernetes-sigs/kueue/commit/7af676bc42aeef82e98d98930f0b04f67e483ffc

**Why is this needed**:

Increase coverage

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-10-18T06:30:36Z

/kind help
/assign @B1F030

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-10-18T06:30:38Z

@kerthcet: The label(s) `kind/help` cannot be applied, because the repository doesn't have them.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1198#issuecomment-1767759765):

>/kind help
>/assign @B1F030


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-10-18T06:30:38Z

@kerthcet: GitHub didn't allow me to assign the following users: B1F030.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1198#issuecomment-1767759765):

>/kind help
>/assign @B1F030


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
