# Issue #388: Add  a validation for Workload QueueName to validating webhooks

**Summary**: Add  a validation for Workload QueueName to validating webhooks

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/388

**Last updated**: 2022-09-12T13:08:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2022-09-10T06:56:59Z
- **Updated**: 2022-09-12T13:08:37Z
- **Closed**: 2022-09-12T13:08:37Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
I'd like to add validating-webhooks for [Workload QueuName](https://github.com/kubernetes-sigs/kueue/blob/9beead264a17e8845beae2691422b7740c35a38a/apis/kueue/v1alpha2/workload_types.go#L35-L37).

**Why is this needed**:
IIUC, we can set the `QueueName` within the `Workload` that has not been deployed in the tenant namespace.
But I believe the `Workload` should be deployed after the `LocalQueue` has been deployed.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-09-12T13:08:31Z

This goes against "eventual consistency"

It is possible that a user creates a Workload and the Queue at the same time and the controller observes the Workload first.
This entire operation should succeed when the controller observes the Queue.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-09-12T13:08:37Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/388#issuecomment-1243715985):

>This goes against "eventual consistency"
>
>It is possible that a user creates a Workload and the Queue at the same time and the controller observes the Workload first.
>This entire operation should succeed when the controller observes the Queue.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
