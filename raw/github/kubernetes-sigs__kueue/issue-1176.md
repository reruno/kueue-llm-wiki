# Issue #1176: A mechanism for admin to requeue a Job after some time

**Summary**: A mechanism for admin to requeue a Job after some time

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1176

**Last updated**: 2023-10-04T19:41:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-10-03T12:24:01Z
- **Updated**: 2023-10-04T19:41:32Z
- **Closed**: 2023-10-04T19:41:31Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 3

## Description

**What would you like to be added**:

A mechanism for an admin to requeue a Job (and clear the flavor assignment).

**Why is this needed**:

After a job has been assigned to a flavor, an admin should have the ability to requeue the workload.

The admin might want to requeue a job for multiple reasons like:
- the job is stuck in a flavor that cannot be provided
- the job is running, but the admin seems appropriate for it to be run in a different flavor (manual preemption).

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-03T12:26:03Z

I'm confirming the full requirements. Do not take this yet.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-04T19:41:26Z

/close

This doesn't offer much improvement over the existing mechanism of WaitForPodsReady.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-10-04T19:41:31Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1176#issuecomment-1747524823):

>/close
>
>This doesn't offer much improvement over the existing mechanism of WaitForPodsReady.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
