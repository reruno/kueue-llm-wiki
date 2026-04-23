# Issue #162: Do workload.NewInfo once when inserting updating

**Summary**: Do workload.NewInfo once when inserting updating

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/162

**Last updated**: 2022-08-08T03:47:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-03-29T18:37:55Z
- **Updated**: 2022-08-08T03:47:04Z
- **Closed**: 2022-08-08T03:46:18Z
- **Labels**: `good first issue`, `help wanted`, `lifecycle/stale`, `kind/cleanup`
- **Assignees**: [@nayihz](https://github.com/nayihz)
- **Comments**: 9

## Description

**What would you like to be cleaned**:

When we are inserting into Queues and ClusterQueues, we are calling `NewInfo` twice (once for Queue and once for ClusterQueue), which is wasteful.

Maybe we can call `NewInfo` in the manager and always insert `workload.Info` objects in the Queue and ClusterQueue.

Unless we want to store other information, such as last scheduling attempt? cc @denkensk
Then we need a better solution

**Why is this needed**:

The peformance of the event handlers is key to keep the cache up to date.

## Discussion

### Comment by [@denkensk](https://github.com/denkensk) — 2022-03-30T07:08:14Z

 I also found that we repeatedly call `NewInfo` in `ClusterQueue` and `Queue` when `addOrUpdateWorkload`.  :)

> Unless we want to store other information, such as last scheduling attempt

Yes. will add last scheduling attempt timestamp. Can you provide a function to sync some old info to the new workload info if we want to call `NewInfo` in manager ？like check if exist and partly deep copy?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-30T13:56:36Z

We could add some "recalculate" method in Info that doesn't touch queueing data

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-05-04T04:59:46Z

/good-first-issue
/help

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-05-04T04:59:47Z

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

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/162):

>/good-first-issue
>/help


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@nayihz](https://github.com/nayihz) — 2022-05-10T03:31:59Z

I would like to work on it.
/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-08-08T03:41:09Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues and PRs.

This bot triages issues and PRs according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue or PR as fresh with `/remove-lifecycle stale`
- Mark this issue or PR as rotten with `/lifecycle rotten`
- Close this issue or PR with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-08T03:46:09Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-08-08T03:46:19Z

@kerthcet: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/162#issuecomment-1207629356):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-08T03:47:03Z

As we merged https://github.com/kubernetes-sigs/kueue/pull/257.
