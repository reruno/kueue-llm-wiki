# Issue #1692: Only requeue workloads in cohort when space frees up

**Summary**: Only requeue workloads in cohort when space frees up

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1692

**Last updated**: 2024-02-26T16:41:45Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-02-06T13:57:31Z
- **Updated**: 2024-02-26T16:41:45Z
- **Closed**: 2024-02-26T16:41:44Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

When something happens in the cluster that frees up space, like:
- Workload finishing
- Workload partial reclaim
- ClusterQueue resize,

only requeue the Workloads that are in the same cohort as the event

**Why is this needed**:

This would avoid unnecessary admission attempts for Workloads that don't fit.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-06T13:59:17Z

Oops, this is actually what is currently implemented https://github.com/kubernetes-sigs/kueue/blob/892d85c35a94c875005d6b547710ad06704bccf9/pkg/queue/manager.go#L371-L377

### Comment by [@Bharadwajshivam28](https://github.com/Bharadwajshivam28) — 2024-02-26T10:04:45Z

Hey @alculquicondor I can try it but I need some steps to get started

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-02-26T14:15:49Z

@alculquicondor As I checked [this comment](https://github.com/kubernetes-sigs/kueue/issues/1692#issuecomment-1929726356), this had already completed, right?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-26T16:41:40Z

Oh yes, sorry, I forgot to close

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-02-26T16:41:44Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1692#issuecomment-1964608743):

>Oh yes, sorry, I forgot to close
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
