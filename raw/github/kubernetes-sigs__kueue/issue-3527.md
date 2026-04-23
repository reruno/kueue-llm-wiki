# Issue #3527: Imprecise log line: LocalQueue for workload didn't exist

**Summary**: Imprecise log line: LocalQueue for workload didn't exist

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3527

**Last updated**: 2024-12-13T09:56:27Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2024-11-13T14:58:49Z
- **Updated**: 2024-12-13T09:56:27Z
- **Closed**: 2024-12-13T09:56:27Z
- **Labels**: `kind/bug`, `good first issue`, `help wanted`, `kind/cleanup`
- **Assignees**: [@7h3-3mp7y-m4n](https://github.com/7h3-3mp7y-m4n)
- **Comments**: 5

## Description

**What would you like to be cleaned**:
When [AddOrUpdateWorkloadWithoutLock](https://github.com/kubernetes-sigs/kueue/blob/2c8e7da1a23f2bc7218a2f08a2c9858a316fb053/pkg/queue/manager.go#L328) returns false, there are several lines which may log that a LocalQueue does not exist

e.g. 
https://github.com/kubernetes-sigs/kueue/blob/2c8e7da1a23f2bc7218a2f08a2c9858a316fb053/pkg/controller/core/workload_controller.go#L732-L734

Unfortunately, this function can also return false when the ClusterQueue is not located
https://github.com/kubernetes-sigs/kueue/blob/2c8e7da1a23f2bc7218a2f08a2c9858a316fb053/pkg/queue/manager.go#L336-L339

We should differentiate whether the ClusterQueue or LocalQueue is missing in the log lines which depend on (directly or indirectly) the return value of this function.

**Why is this needed**:
To assist with future debugging, and to make our logging more precise.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-20T08:28:56Z

it seems like
/good-first-issue

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-11-20T08:28:58Z

@mimowo: 
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

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3527):

>it seems like
>/good-first-issue


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@7h3-3mp7y-m4n](https://github.com/7h3-3mp7y-m4n) — 2024-11-20T19:33:37Z

I'll pick it up :)

### Comment by [@7h3-3mp7y-m4n](https://github.com/7h3-3mp7y-m4n) — 2024-11-20T20:27:47Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-13T09:30:33Z

/kind bug
because the logs are not just not precise - they are misleading - as pointed out in the description the message `LocalQueue for workload didn't exist or not active; ignored for now` can be logged when ClusterQueue does not exist.
