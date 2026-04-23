# Issue #72: Ensure test cases are independent

**Summary**: Ensure test cases are independent

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/72

**Last updated**: 2023-02-07T13:19:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-02-25T20:20:38Z
- **Updated**: 2023-02-07T13:19:03Z
- **Closed**: 2023-02-07T13:19:03Z
- **Labels**: `good first issue`, `help wanted`, `priority/backlog`
- **Assignees**: [@shuheiktgw](https://github.com/shuheiktgw), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 9

## Description

In an effort to get a binary that "works", we wrote some tests where a test case depends on the state left by previous test cases.

This is problematic for debugging problems and it tends to lead to a lot of test changes when there is a behavior change or you want to insert a case in the middle of the existing ones.

Places that I'm aware of:

- [ ] TestCacheCapacityOperations in https://github.com/kubernetes-sigs/kueue/blob/main/pkg/capacity/capacity_test.go
- [ ] TestCacheWorkloadOperations in https://github.com/kubernetes-sigs/kueue/blob/main/pkg/capacity/capacity_test.go
- [ ] Scheduler suite https://github.com/kubernetes-sigs/kueue/blob/main/test/integration/scheduler/scheduler_test.go

And there are similar situations in the following, but it's more like a single complex test case in each:
- [ ] TestSnapshot in https://github.com/kubernetes-sigs/kueue/blob/main/pkg/capacity/snapshot_test.go
- [ ] TestFIFOQueue in https://github.com/kubernetes-sigs/kueue/blob/main/pkg/queue/queue_test.go

/priority backlog

## Discussion

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-09T01:25:04Z

/help
/good-first-issue

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-03-09T01:25:05Z

@ahg-g: 
	This request has been marked as suitable for new contributors.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- Does this issue have zero to low barrier of entry?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://git.k8s.io/community/contributors/guide/help-wanted.md#good-first-issue) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-good-first-issue` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/72):

>/help
>/good-first-issue 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@shuheiktgw](https://github.com/shuheiktgw) — 2022-05-13T00:14:31Z

Let me work on this issue!
/assign

### Comment by [@shuheiktgw](https://github.com/shuheiktgw) — 2022-05-13T00:15:59Z

Seems like TestCacheCapacityOperations does not exist anyomre?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-05-13T15:15:18Z

It's now `TestCacheClusterQueueOperations`

### Comment by [@shuheiktgw](https://github.com/shuheiktgw) — 2022-05-15T01:16:14Z

Looks like the issue with TestCacheCapacityOperations (TestCacheClusterQueueOperations) was already resolved in https://github.com/kubernetes-sigs/kueue/pull/133 🙂  Looking into the scheduler integration test

### Comment by [@shuheiktgw](https://github.com/shuheiktgw) — 2022-05-17T00:21:19Z

I found the problem with the scheduler integration tests was resolved in https://github.com/kubernetes-sigs/kueue/pull/90
I'm looking into snapshot_test.go next

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-01-05T20:30:24Z

/reopen
/assign

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-01-05T20:30:28Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/72#issuecomment-1372709532):

>/reopen
>/assign
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
