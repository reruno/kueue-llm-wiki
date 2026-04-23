# Issue #1994: [metrics] Add `admission_check_wait_time` metric

**Summary**: [metrics] Add `admission_check_wait_time` metric

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1994

**Last updated**: 2024-06-25T16:03:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-04-17T09:00:32Z
- **Updated**: 2024-06-25T16:03:04Z
- **Closed**: 2024-06-17T17:30:44Z
- **Labels**: `kind/feature`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 8

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

A new histogram metric `admission_check_wait_time`. The metric has the `controller_name` label to discriminate between different types of admission checks.

**Why is this needed**:

The metric will allow administrators how long workloads wait for different admission checks, depending on their type (controller).

**Completion requirements**:

Aside from the implementation update the docs: https://kueue.sigs.k8s.io/docs/reference/metrics/.

## Discussion

### Comment by [@kaisoz](https://github.com/kaisoz) — 2024-04-18T12:14:32Z

I can take this one 😊 

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-06-14T03:41:36Z

@kaisoz Is it still in progress?

### Comment by [@kaisoz](https://github.com/kaisoz) — 2024-06-14T06:20:55Z

> @kaisoz Is it still in progress?

@mimowo and I talked about this one on Slack and decided to put on hold for now because there's already a metric which is quite similar. He was going to open a discussion and come back to me.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-17T10:58:30Z

That's right, I'm not sure about the benefits of this metric since we already have: https://github.com/kubernetes-sigs/kueue/blob/e8e0810115f3bef7518b4c07eb4c2e2579660060/pkg/metrics/metrics.go#L128C2-L135.
The benefit is more granular, but most of the time our users still have only one AdmissionCheck - MultiKueue or ProvisioningRequest. Another benefit could be to introduce the `result` label which could have values `failed`, and `success` to indicate the result per admission check. Then, an admin could see how long it takes for ProvisioningRequests to fail / provision. 

On the implementation level we have two choices: 
1. use `workload_controller` [update handler](https://github.com/kubernetes-sigs/kueue/blob/e8e0810115f3bef7518b4c07eb4c2e2579660060/pkg/controller/core/workload_controller.go#L621) and measure the time it took from `Pending` to `Rejected`, `Retry` (for failed), or `Ready` for success
2. set the metric it per admission check, in case of ProvReq, after the update [here](https://github.com/kubernetes-sigs/kueue/blob/e8e0810115f3bef7518b4c07eb4c2e2579660060/pkg/controller/admissionchecks/provisioning/controller.go#L511-L513)

I would be leaning towards (1.) as this would work OOTB for external admission checks. A potential downside is that the metric would get counted for non-leading replicas, but we aren't strict about it anyway.

@tenzen-y @alculquicondor any opinion? Do you think its benefits (more granular, and `result` label) outweight the extra complexity? I would be in favor of adding it.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-17T17:30:37Z

Let's close this one for now.

We have enough information for most use cases with the existing metric.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-17T17:30:41Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-17T17:30:45Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1994#issuecomment-2173956783):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-25T16:03:03Z

> That's right, I'm not sure about the benefits of this metric since we already have: https://github.com/kubernetes-sigs/kueue/blob/e8e0810115f3bef7518b4c07eb4c2e2579660060/pkg/metrics/metrics.go#L128C2-L135. The benefit is more granular, but most of the time our users still have only one AdmissionCheck - MultiKueue or ProvisioningRequest. Another benefit could be to introduce the `result` label which could have values `failed`, and `success` to indicate the result per admission check. Then, an admin could see how long it takes for ProvisioningRequests to fail / provision.
> 
> On the implementation level we have two choices:
> 
> 1. use `workload_controller` [update handler](https://github.com/kubernetes-sigs/kueue/blob/e8e0810115f3bef7518b4c07eb4c2e2579660060/pkg/controller/core/workload_controller.go#L621) and measure the time it took from `Pending` to `Rejected`, `Retry` (for failed), or `Ready` for success
> 2. set the metric it per admission check, in case of ProvReq, after the update [here](https://github.com/kubernetes-sigs/kueue/blob/e8e0810115f3bef7518b4c07eb4c2e2579660060/pkg/controller/admissionchecks/provisioning/controller.go#L511-L513)
> 
> I would be leaning towards (1.) as this would work OOTB for external admission checks. A potential downside is that the metric would get counted for non-leading replicas, but we aren't strict about it anyway.
> 
> @tenzen-y @alculquicondor any opinion? Do you think its benefits (more granular, and `result` label) outweight the extra complexity? I would be in favor of adding it.

I'm fine without this metric. Once we find any situations where we want to make it more granular, we can revisit here.
