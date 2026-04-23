# Issue #1282: Policy to put Workloads in front of the queue after eviction

**Summary**: Policy to put Workloads in front of the queue after eviction

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1282

**Last updated**: 2024-02-14T14:05:47Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-10-27T19:50:41Z
- **Updated**: 2024-02-14T14:05:47Z
- **Closed**: 2024-02-14T14:05:47Z
- **Labels**: `kind/feature`
- **Assignees**: [@nstogner](https://github.com/nstogner), [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 6

## Description

**What would you like to be added**:

A policy that allows to put evicted jobs in the front of the queue after eviction.

**Why is this needed**:

This is particularly important for WaitForPodsReady: if a job is stuck in a low availability flavor, after timeout, it should go to the front of the queue and immediately considered for admission in other flavors, which might have higher availability (like being backed by a reservation).

The case of preemption might be more tricky: we want the preempted jobs to be readmitted as soon as possible. But if a job is waiting for more than one job to be preempted and the queueing strategy is BestEffortFIFO, we don't want the preempted pods to take the head of the queue.
Maybe we need to hold them until the preemptor job is admitted, and then they should use the regular priority.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@nstogner](https://github.com/nstogner) — 2023-10-27T20:40:48Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-05T19:08:14Z

As we discussed in KEP (https://github.com/kubernetes-sigs/kueue/pull/1311#issuecomment-1870531528), we will introduce a backoff and a max number of retries mechanism to prevent infinity requeuing the job to the head.

So, I will update KEP 1282.
/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-18T13:42:09Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-01-18T13:42:14Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1282#issuecomment-1898504218):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-12T21:01:15Z

@tenzen-y could you add a quick note in the documentation?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-02-12T21:02:30Z

> @tenzen-y could you add a quick note in the documentation?

Sure, I will extend documentation by stable v0.6 release.
