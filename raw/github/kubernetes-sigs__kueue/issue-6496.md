# Issue #6496: Metric measuring how long a workload is pending at head of CQ

**Summary**: Metric measuring how long a workload is pending at head of CQ

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6496

**Last updated**: 2025-09-18T19:29:47Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@amy](https://github.com/amy)
- **Created**: 2025-08-07T13:03:21Z
- **Updated**: 2025-09-18T19:29:47Z
- **Closed**: 2025-09-18T19:29:46Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Related to: https://github.com/kubernetes-sigs/kueue/issues/6143
Context: https://github.com/kubernetes-sigs/kueue/issues/6143#issuecomment-3162699319

We want to gauge how long a workload is pending at the head of a CQ

**Why is this needed**:
Want to be able to potentially help detect when a pod is stuck at the head of CQ despite having guarantees. This is probably only useful for this particular problem if the workload has guarantees and the admitting workload can fit. But besides that use case, it could also give us statistics on overall trends in how long cq heads remain pending.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-09-18T19:29:41Z

/close 

Thought about it some more and its not a particularly useful stat

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-18T19:29:47Z

@amy: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6496#issuecomment-3309308685):

>/close 
>
>Thought about it some more and its not a particularly useful stat


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
