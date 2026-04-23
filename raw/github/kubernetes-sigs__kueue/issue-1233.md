# Issue #1233: Inject tolerations from ResourceFlavors

**Summary**: Inject tolerations from ResourceFlavors

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1233

**Last updated**: 2023-12-12T15:01:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-10-20T16:34:27Z
- **Updated**: 2023-12-12T15:01:04Z
- **Closed**: 2023-12-12T15:01:04Z
- **Labels**: `kind/feature`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 12

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

A field in ResourceFlavor that is used to inject tolerations in jobs that land in the flavor.

This information can then be communicated to ProvisioningRequest to inform scale ups.

Note that the ResourceFlavor already has a `nodeTaints` field that prevents jobs from landing on them, unless they explicitly tolerate them. The new `tolerations` field would be a complementary API.

**Why is this needed**:

It's useful to have taints in the nodes that back a ResourceFlavor so that they are not accidentally used by pods that are not supposed to be there.

This is common for hardware accelerators such as GPUs, to prevent non-GPU pods to land on the nodes. Cloud provider webhooks sometimes inject these tolerations into Pods, when a Pod requests the accelerator. However, they cannot possibly target every job CRD.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-20T16:35:28Z

@trasc I think the ResourceFlavor API is the best place to put these tolerations, as it goes beyond ProvisioningRequest.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-20T16:36:06Z

cc @mwielgus

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-10-20T20:13:29Z

How does the kueue pass tolerations's `operator` from resourceFravor to jobs?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-20T20:16:44Z

this would be a new field `tolerations`, in addition to the existing `nodeTaints`.
The `tolerations` would include an `operator`.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-10-20T20:19:23Z

> this would be a new field `tolerations`, in addition to the existing `nodeTaints`. The `tolerations` would include an `operator`.

Ah, this feature aims to extend the ResourceFlavor API by adding a `tolerations` field. Thanks.

### Comment by [@trasc](https://github.com/trasc) — 2023-10-23T08:23:39Z

> @trasc I think the ResourceFlavor API is the best place to put these toleration, as it goes beyond ProvisioningRequest.

On the other hand, talking strictly about provisioning ACC, when changing the configuration of a admissions check will add a new object type to take into account, additionally, the provisioning admission check controller might need to check the flavors assigned (have a whitelist or something). Having the toleration in the provisioning config will just require adding them in the PodSetUpdates to make it to the actual pod.

But I don't have any strong feelings on any of the approaches.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-23T14:35:28Z

> the provisioning admission check controller might need to check the flavors assigned (have a whitelist or something)

Don't we already do that for injecting node selectors into the template?

That said, we should probably consider putting the node selectors and tolerations somewhere in the Workload status during quota reservation. This way, the job controllers and the AC controllers don't need to know about ResourceFlavor.

Maybe we can do it as part of this effort.

> Having the toleration in the provisioning config will just require adding them in the PodSetUpdates to make it to the actual pod.

I agree that it looks simpler, but in ResourceFlavor seems more universally useful.

### Comment by [@trasc](https://github.com/trasc) — 2023-10-23T14:50:35Z

> Don't we already do that for injecting node selectors into the template?

It's done in order to add the node selectors in the pod templates, but there is no decision in terms of I "like" this flavor or not.

> That said, we should probably consider putting the node selectors and tolerations somewhere in the Workload status during quota reservation. This way, the job controllers and the AC controllers don't need to know about ResourceFlavor.

This could be helpful, but maybe in another issue.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-23T15:35:31Z

> It's done in order to add the node selectors in the pod templates, but there is no decision in terms of I "like" this flavor or not.

The tolerations would behave the same way. There is not decision at this point, just injection. The decision is already done by the kueue scheduler.

### Comment by [@trasc](https://github.com/trasc) — 2023-10-24T06:46:07Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-08T17:35:07Z

/reopen 

We need to add documentation about this feature.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-12-08T17:35:12Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1233#issuecomment-1847571722):

>/reopen 
>
>We need to add documentation about this feature.
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
