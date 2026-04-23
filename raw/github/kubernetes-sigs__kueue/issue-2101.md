# Issue #2101: Add priority to LocalQueue

**Summary**: Add priority to LocalQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2101

**Last updated**: 2024-05-01T11:26:45Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@amy](https://github.com/amy)
- **Created**: 2024-04-29T18:50:39Z
- **Updated**: 2024-05-01T11:26:45Z
- **Closed**: 2024-05-01T11:26:43Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
We would like to add priority to LocalQueue.

**Why is this needed**:
We have a need to introduce 2 dimensions of priority/preemption. Here is an example:

- We have 2 types of workloads (A & B)
- A should always preempt B
- We also want ordering within A
- We have an indefinite number of workload types where we don't want to statically define say 4 priorities (Ex: A-high-priority, A-low-priority, B-high-priority, B-low-priority)
- So with the following submission order (Where A preempts all B): (A, workload priority 0) (B, 100) (A,100) (B,0) -> Queue order should be: (A,100) (A, 0) (B, 100) (B, 0)

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-01T11:26:40Z

This is duplicated with #752 
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-05-01T11:26:44Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2101#issuecomment-2088314481):

>This is duplicated with #752 
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
