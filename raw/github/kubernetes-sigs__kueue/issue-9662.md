# Issue #9662: Migrate from Provisioning Request to Buffer API

**Summary**: Migrate from Provisioning Request to Buffer API

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9662

**Last updated**: 2026-03-16T11:20:24Z

---

## Metadata

- **State**: open
- **Author**: [@DerekFrank](https://github.com/DerekFrank)
- **Created**: 2026-03-03T22:04:32Z
- **Updated**: 2026-03-16T11:20:24Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Given that both CAS and Karpenter will eventually support the CapacityBuffer API, Kueue should be able to leverage that API to be autoscaler agnostic.

Additional Context:
* https://github.com/kubernetes-sigs/kueue/issues/5133
* https://github.com/kubernetes-sigs/karpenter/issues/749
* https://github.com/kubernetes-sigs/karpenter/issues/2571
* https://docs.google.com/document/d/1ergKWH28EpGyYVISZbqPqIBS1wN7VNhjNa_Sl1pAFI8/edit?usp=sharing

**Why is this needed**:

Karpenter support and autoscaler API parity.

**Completion requirements**:

* Use Buffer API
* Stop Using ProvisioningRequest API

This enhancement requires the following artifacts:

- [X] Design doc
- [X] API change
- [X] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2026-03-03T22:12:38Z

@DerekFrank and I were discussing this.

For Karpenter (#https://github.com/kubernetes-sigs/kueue/issues/5133), Buffers will be the integration point.

That work is still ongoing but Buffer API will also be V1 soon and supported in both CAS/Karpenter.

We should consider supporting Buffers but I am not sure if we should deprecate/stop ProvisionRequest.

It is at least useful for Kueue to also support Buffers for both CAS/Karpenter sake.

We also have https://docs.google.com/document/d/1ergKWH28EpGyYVISZbqPqIBS1wN7VNhjNa_Sl1pAFI8/edit?usp=sharing so I think its worth thinking through how to support these potential APIs.

I am curious if we want to continue maintaining https://github.com/kubernetes-sigs/kueue/blob/main/apis/kueue/v1beta2/provisioningrequestconfig_types.go if autoscaling decides to go with newer APIs.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-09T15:45:58Z

@DerekFrank thank you for the issue 👍 I'm happy to make Kueue support autoscaling with Karpenter well.

Let me ask some clarifying questions:
1. Do you know if the CapacityBuffers API has feature parity with ProvisioningRequests wrt "check-capacity" and "atomic-scalup" modes? This is not a blocker, mostly exploring where we are.
2. Do you maybe have some folks who could work on the implementation? 

cc @44past4 @mwielgus @yaroslava-serdiuk @mwysokin

### Comment by [@44past4](https://github.com/44past4) — 2026-03-16T11:05:15Z

From what I know Capacity Buffers API can be used in a very similar way like Provisioning Request API with a buffer referencing a pod template and specifying the number of replicas. So from this perspective I believe that adding support for Capacity Buffers API in Kueue should not be that complicated and overall makes sense taking into account that both Cluster Autoscaler and Karpenter wants to support this API.

What I am concerned about is the part where this issue suggests that the existing support for Provisioning Request API should be removed from Kueue while adding support for Capacity Buffers API. Assuming that Capacity Buffers API will gain in popularity and will offer implementations matching the functionality of current Provisioning Request implementations we may consider a slow depreciation of Provisioning Request API support. However in the meantime I strongly believe that Kueue should support both APIs.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-16T11:09:34Z

Indeed, I'm happy to accept the integration for CapacityBuffers API, analogously as for ProvisioningRequests. However, dropping ProvisioningRequests integration is very long way off, if ever.
