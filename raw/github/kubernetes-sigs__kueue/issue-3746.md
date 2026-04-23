# Issue #3746: Add sanity e2e tests for the Kueue metrics

**Summary**: Add sanity e2e tests for the Kueue metrics

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3746

**Last updated**: 2025-01-30T07:01:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-12-05T14:43:35Z
- **Updated**: 2025-01-30T07:01:23Z
- **Closed**: 2025-01-30T07:01:23Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mykysha](https://github.com/mykysha)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Add sanity e2e tests to make sure the metrics endpoint returns Kueue metrics.

**Why is this needed**:

Currently, the metrics.Register() call can be removed from main.go, and all tests pass. This could have caused the bug in this PR: https://github.com/kubernetes-sigs/kueue/pull/3673/files#diff-64a1e0bd9f87bdadd12179b8e48ace63c6aa3ace3f7694375a8a0dd0e566e25dL133

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-05T14:44:04Z

cc @KPostOffice @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-06T08:47:00Z

/assign @mykysha

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-12-06T08:47:04Z

@mbobrovskyi: GitHub didn't allow me to assign the following users: mykysha.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3746#issuecomment-2522532985):

>/assign @mykysha 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kannon92](https://github.com/kannon92) — 2024-12-06T16:41:29Z

It could be worth adding securing metrics in this test.

### Comment by [@mykysha](https://github.com/mykysha) — 2024-12-09T10:06:31Z

/assign
