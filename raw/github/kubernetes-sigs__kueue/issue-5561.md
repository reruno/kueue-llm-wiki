# Issue #5561: Don't trigger second scheduling pass for Finished or Evicted workloads

**Summary**: Don't trigger second scheduling pass for Finished or Evicted workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5561

**Last updated**: 2025-06-10T05:59:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-09T09:12:20Z
- **Updated**: 2025-06-10T05:59:12Z
- **Closed**: 2025-06-10T05:59:10Z
- **Labels**: `kind/bug`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 6

## Description

**What happened**:

Currently second pass of scheduling might be triggered for Evicted or Finished workloads. This occasionally happens in case of https://github.com/kubernetes-sigs/kueue/issues/5511

**What you expected to happen**:

evicted or finished workloads, or without quota reservation never trigger second pass.

**How to reproduce it (as minimally and precisely as possible)**:

There is no easy repro, but running the test in https://github.com/kubernetes-sigs/kueue/issues/5511 reproduces it occasionally when the workload is evicted, but the annotation is still present (because the annotation is removed in the follow up request).

This would not be happening if the annotation was replaced by status field as described here: https://github.com/kubernetes-sigs/kueue/issues/5560

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-09T09:12:36Z

cc @PBundyra 
/assign 
tentatively

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-09T10:33:05Z

What does `second scheduling pass` mean?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-09T11:37:08Z

It means that the scheduler makes another pass on the workload to adjust the "admission". Currently we have 2 use cases:
- TAS after new infra nodes are created after ProvisioiningRequest
- node replacement for TAS for failed nodes

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-10T05:52:28Z

> It means that the scheduler makes another pass on the workload to adjust the "admission". Currently we have 2 use cases:
> 
> * TAS after new infra nodes are created after ProvisioiningRequest
> * node replacement for TAS for failed nodes

Ah, I see. That makes sense. Thank you.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-10T05:59:06Z

/close 
as https://github.com/kubernetes-sigs/kueue/pull/5585 is merged. I forgot to add the issue to PR description.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-06-10T05:59:11Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5561#issuecomment-2957775162):

>/close 
>as https://github.com/kubernetes-sigs/kueue/pull/5585 is merged. I forgot to add the issue to PR description.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
