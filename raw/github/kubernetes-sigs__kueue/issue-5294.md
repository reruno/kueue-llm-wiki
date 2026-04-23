# Issue #5294: Create a util function for evicting a Workload

**Summary**: Create a util function for evicting a Workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5294

**Last updated**: 2025-08-12T12:11:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-05-20T12:18:34Z
- **Updated**: 2025-08-12T12:11:32Z
- **Closed**: 2025-08-12T12:11:31Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
Across the codebase similar code is called a few times so I think it would be useful to have a separate function that evicts the workload, to not repeat it multiple times

Example:
- https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/core/workload_controller.go#L437-L447
- https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/core/workload_controller.go#L528-L538

**Why is this needed**:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-12T12:11:26Z

/close
we already have it: https://github.com/kubernetes-sigs/kueue/blame/main/pkg/workload/workload.go#L1083C6-L1102

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-08-12T12:11:32Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5294#issuecomment-3179059441):

>/close
>we already have it: https://github.com/kubernetes-sigs/kueue/blame/main/pkg/workload/workload.go#L1083C6-L1102


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
