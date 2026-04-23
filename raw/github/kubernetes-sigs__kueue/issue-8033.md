# Issue #8033: Add flavor information to workload

**Summary**: Add flavor information to workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8033

**Last updated**: 2025-12-19T09:43:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@LarsSven](https://github.com/LarsSven)
- **Created**: 2025-12-02T09:22:11Z
- **Updated**: 2025-12-19T09:43:04Z
- **Closed**: 2025-12-19T09:43:03Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
When Kueue admits a workload, it adds the name of the flavor to the status of the workload. We would however like to have other details of the flavor that the workload was admitted to added to the workload when it's admitted. This could for example be a label/annotation that we can add to a flavor, where if a workload gets admitted by that flavor, the label/annotation is also added to the workload.

**Why is this needed**:
We have a microservice that creates workloads, and sends gRPC requests when the workload is admitted. The host/port that the gRPC request should be sent to is however based on which flavor admits the workload, so we would like to communicate the hostname to the workload so that the service knows where to send the request.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-02T09:36:42Z

The flavor assignment is per PodSet, not necessarily the entire workload. The name of the selected flavor is already under
Workload's [.status.admission.podSetAssignment[].flavors](https://github.com/kubernetes-sigs/kueue/blob/6e9e0a619af9eca2c8192dd6fa5e18b1360d8d8a/apis/kueue/v1beta2/workload_types.go#L258). Once you have the name of the flavor you can find all its details by lookup to the ResourceFlavor instance. 

It would be good to clarify if the above workflow is enough, or clarify why it is not enough.

### Comment by [@LarsSven](https://github.com/LarsSven) — 2025-12-02T09:57:22Z

That's fair, technically it would work it's just that it's a very high throughput scenario where we get lots of workloads so doing an extra kubernetes lookup to the flavor is something we try to avoid, so that's why I wanted to propose this so we don't have to do an extra lookup of the ResourceFlavor, but I could also definitely understand that that's not enough reason to add something like this.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-02T10:06:41Z

Yeah, I would rather suggest using a cache for ResourceFlavor instances based on the List and Watch pattern in your external controller.

### Comment by [@LarsSven](https://github.com/LarsSven) — 2025-12-02T10:07:47Z

That may be a good idea, thanks for the suggestion.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:42:57Z

/close
To avoid distractions. If you disagree feel free to re-open.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-19T09:43:04Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8033#issuecomment-3674320741):

>/close
>To avoid distractions. If you disagree feel free to re-open.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
