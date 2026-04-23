# Issue #6896: Add unit test coverage for preservePreviousMessage changes

**Summary**: Add unit test coverage for preservePreviousMessage changes

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6896

**Last updated**: 2025-09-18T14:32:27Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@amy](https://github.com/amy)
- **Created**: 2025-09-17T17:13:48Z
- **Updated**: 2025-09-18T14:32:27Z
- **Closed**: 2025-09-18T14:32:26Z
- **Labels**: `good first issue`, `help wanted`, `kind/cleanup`
- **Assignees**: [@ichekrygin](https://github.com/ichekrygin)
- **Comments**: 6

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
Add unit test coverage for preservePreviousMessage changes

Context: https://github.com/kubernetes-sigs/kueue/pull/6819/files#r2355510227

**Why is this needed**:
Verify that we fixed the bug that a workload going repeatedly via the preemption and re-admission cycle would accumulate the
"Previously" prefix in the condition message, eg: "Previously: Previously: Previously: Preempted to accommodate a workload ..."

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-09-17T17:17:42Z

/good-first-issue

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-17T17:17:44Z

@amy: 
	This request has been marked as suitable for new contributors.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://www.kubernetes.dev/docs/guide/help-wanted/#good-first-issue) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-good-first-issue` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6896):

>/good-first-issue


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-17T18:32:15Z

/assign

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-18T14:11:26Z

Fixed via #6903

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-18T14:32:21Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-18T14:32:27Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6896#issuecomment-3307804201):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
