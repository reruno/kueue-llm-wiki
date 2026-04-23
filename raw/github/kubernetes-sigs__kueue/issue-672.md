# Issue #672: Example needed for borrowing limit

**Summary**: Example needed for borrowing limit

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/672

**Last updated**: 2023-05-25T13:54:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@moficodes](https://github.com/moficodes)
- **Created**: 2023-04-03T17:28:17Z
- **Updated**: 2023-05-25T13:54:31Z
- **Closed**: 2023-05-25T13:54:30Z
- **Labels**: `kind/feature`
- **Assignees**: [@KunWuLuan](https://github.com/KunWuLuan)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

An example of borrowing limit being used.

**Why is this needed**:

There is a bit of confusion about what borrowing limit actually do in a cohort. A concrete example of borrowing limit being used in a cohort and show what the numbers look like with the limit in place would help clarify this topic.

**Completion requirements**:

A yaml example added in this section. https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/#borrowinglimit

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-04-20T08:36:58Z

/assign

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-04-20T09:05:16Z

@moficodes hi, I have added a sample in site and config/samples. It will be appreciated if you have time to review the sample and give me your suggestions. Thanks

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-05-25T03:55:47Z

@moficodes Hi, I think this issue can be closed cause pr #709 has been merged

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-25T13:54:26Z

yes, thanks!

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-05-25T13:54:30Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/672#issuecomment-1562952814):

>yes, thanks!
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
