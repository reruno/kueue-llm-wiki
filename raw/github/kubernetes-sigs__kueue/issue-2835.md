# Issue #2835: Add a guide for deleting ClusterQueues

**Summary**: Add a guide for deleting ClusterQueues

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2835

**Last updated**: 2024-08-28T16:14:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-08-13T18:08:49Z
- **Updated**: 2024-08-28T16:14:58Z
- **Closed**: 2024-08-28T16:14:58Z
- **Labels**: `kind/feature`, `help wanted`, `kind/documentation`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 6

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

A task page for how to delete a ClusterQueue that has running workloads.

Alternatives include using the `kubectl kueue` plugin or directly using `kubectl edit`.

**Why is this needed**:

It's not immediately obvious what `kubectl delete clusterqueue` does. It currently just looks like the command is hanging.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-08-13T18:09:05Z

/kind documentation
/help

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-08-13T18:09:07Z

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

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2835):

>/kind documentation
>/help


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-08-27T18:17:01Z

> Alternatives include using the kubectl kueue plugin plugin

The `kubectl kueue delete` command is essentially a pass-through to `kubectl delete`. Should we add logic to force delete `ClusterQueue`? Or is it sufficient to mention that this can be done using `kueuectl`?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-08-27T18:43:06Z

I'm not asking for a guide to force delete. I'm asking for an explanation of what happens when you do a delete, what we are waiting for and how to get out of the situation.

Likely, you might want to do a drain before deleting the queue.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-08-27T18:48:30Z

Ah, I see. Thanks for the explanation.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-08-27T19:48:01Z

/assign
