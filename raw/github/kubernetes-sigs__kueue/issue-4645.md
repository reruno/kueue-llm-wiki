# Issue #4645: HierarchicalCohorts: Introduce a helper function to iterate to the root

**Summary**: HierarchicalCohorts: Introduce a helper function to iterate to the root

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4645

**Last updated**: 2025-03-17T10:24:00Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-17T10:22:09Z
- **Updated**: 2025-03-17T10:24:00Z
- **Closed**: 2025-03-17T10:23:58Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 3

## Description

**What would you like to be cleaned**:

In a couple of places in the code we loop to iterate to the root, examples:
- https://github.com/kubernetes-sigs/kueue/pull/4572/files/fc1aaa51dae1c5e8ed7280b0483e343e575cd5be#diff-92413f1d0b96fa9ae57fe83440a2114578ac55edf9b7f108fef4d983b1cb8d81R36-R42
- https://github.com/kubernetes-sigs/kueue/pull/4572/files/fc1aaa51dae1c5e8ed7280b0483e343e575cd5be#diff-92413f1d0b96fa9ae57fe83440a2114578ac55edf9b7f108fef4d983b1cb8d81R52-R59
- https://github.com/kubernetes-sigs/kueue/pull/4572/files/fc1aaa51dae1c5e8ed7280b0483e343e575cd5be#diff-c791c7f8f43735ff11274e29bfe6eb9320dfc913d4a5a0f14b3ba03038b076b4R70-R74
- https://github.com/kubernetes-sigs/kueue/blob/f82aae0ba5a16cd6e3346d5d8d6b87772eba14f7/pkg/scheduler/fair_sharing_iterator.go#L212-L218

**Why is this needed**:

To make the "business logic" code not be mixed with technical iteration over the tree. (Single Level of Abstraction principle).

In some cases like [this](https://github.com/kubernetes-sigs/kueue/blob/f82aae0ba5a16cd6e3346d5d8d6b87772eba14f7/pkg/scheduler/fair_sharing_iterator.go#L207-L217) it also leads to a small duplication of code (DRY principle).

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T10:22:24Z

cc @gabesaba

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T10:23:53Z

/close
as duplicate of https://github.com/kubernetes-sigs/kueue/issues/4644

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-17T10:23:58Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4645#issuecomment-2728969543):

>/close
>as duplicate of https://github.com/kubernetes-sigs/kueue/issues/4644


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
