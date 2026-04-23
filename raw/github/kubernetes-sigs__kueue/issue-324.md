# Issue #324: Add label to pending_workloads metric to show the inadmissible workloads

**Summary**: Add label to pending_workloads metric to show the inadmissible workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/324

**Last updated**: 2022-08-18T15:52:24Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-08-11T21:13:56Z
- **Updated**: 2022-08-18T15:52:24Z
- **Closed**: 2022-08-18T15:52:24Z
- **Labels**: `kind/feature`, `help wanted`, `priority/important-soon`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Add a label for the workloads that are inadmissible and are not being retried.

**Why is this needed**:

It's useful to understand the health of kueue and the cluster queues.
For example, if there are inadmissible workloads, the performance of the scheduler is not affected, but it might be an indication of a misconfiguration of the queues, or an attempt from a namespace to use resources that they shouldn't.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-11T21:14:25Z

/priority important-soon

/help

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-08-11T21:14:26Z

@alculquicondor: 
	This request has been marked as needing help from a contributor.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- Does this issue have zero to low barrier of entry?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://git.k8s.io/community/contributors/guide/help-wanted.md) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-help` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/324):

>/priority important-soon
>
>/help


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
