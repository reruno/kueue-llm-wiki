# Issue #3025: Surface errors when a PodTemplate or a ProvReq is invalid

**Summary**: Surface errors when a PodTemplate or a ProvReq is invalid

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3025

**Last updated**: 2025-01-31T15:40:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-09-11T17:53:48Z
- **Updated**: 2025-01-31T15:40:59Z
- **Closed**: 2025-01-31T15:40:59Z
- **Labels**: `kind/feature`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 8

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

When a ProvReq or PodTemplate is rejected by a webhook, Kueue just logs the error and continues retrying. These errors will not be visible to end-users and they might just interpret them as "kueue is stuck". We should communicate these errors in the Workload object, maybe even produce an event?

**Why is this needed**:

A cloud provider could have a webhook to validate PodTemplates created for ProvisioningRequests.

These errors need to be surfaced to users so they can fix any problem about them.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2024-09-11T19:14:52Z

In jobset, we did look at https://github.com/kubernetes-sigs/kubectl-validate to help with validation of these fields.

Not sure if this would be helpful here as you could try creating these objects and if they fail they you bubble of the error as a condition or event.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-11T20:17:47Z

The error could come from a webhook, for which kubectl-validate wouldn't help.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-12T10:30:54Z

+1 for the feature

The starting point could be to record any ProvReq creation errors [here](https://github.com/kubernetes-sigs/kueue/blob/1aa52db8eb60477558e502d835d0ad8ebb612649/pkg/controller/admissionchecks/provisioning/controller.go#L305C2-L305C20), or a [level up errors](https://github.com/kubernetes-sigs/kueue/blob/1aa52db8eb60477558e502d835d0ad8ebb612649/pkg/controller/admissionchecks/provisioning/controller.go#L177) in the check's message.

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2024-09-12T14:00:07Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-19T13:08:17Z

I see the event PR, but wondering if this is enough.

In particular, events are temporary objects, so it is not clear if an admin would notice them. OTOH the ProvReq creation is most likely re-attempted, so the event will be generated continuously, so should be easy to notice.

We could also explore the option of exposing the error as a status in the `Message` field in the AdmissionCheckState: https://github.com/kubernetes-sigs/kueue/blob/e971646642858835bf7050a514205155b7929a82/apis/kueue/v1beta1/workload_types.go#L249.

Any opinions on that?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-19T13:33:35Z

Yes, a status message is more important. An event is nice-to-have.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-01-31T13:03:21Z

/reopen

Due to still not updating workload AdmissionChecks status on AdmissionRequest creation error.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-01-31T13:03:27Z

@mbobrovskyi: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3025#issuecomment-2627279249):

>/reopen
>
>Due to still not updating workload AdmissionChecks status on AdmissionRequest creation error.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
