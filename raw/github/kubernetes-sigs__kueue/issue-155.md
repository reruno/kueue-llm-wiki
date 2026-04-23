# Issue #155: Scheduler integration tests should be independent of the job controller

**Summary**: Scheduler integration tests should be independent of the job controller

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/155

**Last updated**: 2022-08-05T15:49:48Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-03-25T20:26:22Z
- **Updated**: 2022-08-05T15:49:48Z
- **Closed**: 2022-08-05T15:49:48Z
- **Labels**: `good first issue`, `help wanted`, `kind/cleanup`
- **Assignees**: [@thisisprasad](https://github.com/thisisprasad)
- **Comments**: 10

## Description

**What would you like to be cleaned**:

The scheduler integration should create QueuedWorkloads instead of Jobs.

**Why is this needed**:

Separation of concerns.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-25T20:26:31Z

/good-first-issue

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-03-25T20:26:32Z

@alculquicondor: 
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

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/155):

>/good-first-issue


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-25T20:52:57Z

I still think having end-to-end tests like the ones we have are necessary to have.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-25T20:59:35Z

we could move them to be under the job controller integration tests.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-28T13:17:27Z

We could have a simple test case in the job controller.

But more advanced scenarios should just create a QueuedWorkload.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-06-26T13:33:21Z

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

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-06-26T13:43:13Z

/remove-lifecycle stale

### Comment by [@thisisprasad](https://github.com/thisisprasad) — 2022-07-09T12:55:38Z

@alculquicondor Here are my findings:
1. we can replace each job in the test by a workload
2. The assertions of the job should also be removed. Assertions should only be done on the basis of workload and its metrics.

Correct me if I'm wrong.
Would like to know more details on this task if there are any.

### Comment by [@thisisprasad](https://github.com/thisisprasad) — 2022-07-09T12:56:08Z

I would like to work on this task
/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-07-11T13:24:27Z

That is correct. Feel free to start.

But remember to leave at least one test that uses a Job. If possible, do it in the job_controller test. But it's fine to be somewhere else if it doesn't make sense from a technical point of view.
