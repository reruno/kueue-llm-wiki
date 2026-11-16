# Issue #9662: Migrate from Provisioning Request to Buffer API

**Summary**: Migrate from Provisioning Request to Buffer API

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9662

**Last updated**: 2026-10-28T16:41:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@DerekFrank](https://github.com/DerekFrank)
- **Created**: 2026-03-03T22:04:32Z
- **Updated**: 2026-10-28T16:41:04Z
- **Closed**: 2026-10-23T17:30:08Z
- **Labels**: `kind/feature`, `lifecycle/stale`
- **Assignees**: _none_
- **Comments**: 17

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

### Comment by [@jbtk](https://github.com/jbtk) — 2026-05-29T14:07:16Z

Capacity buffers do not offer capacity check nor atomic scale up. At the moment they do not even support being ”filled in"so as soon as workload takes their place they will trigger another scale up (though there are discussions to support that)

### Comment by [@nojnhuh](https://github.com/nojnhuh) — 2026-07-01T18:31:50Z

I can start putting together an implementation.

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-07-01T18:36:02Z

Awesome, we may start with a prototype to see what is feasible but I would like to have a KEP to discuss the design before merging the impl

### Comment by [@DerekFrank](https://github.com/DerekFrank) — 2026-07-23T23:50:27Z

We were thinking about having someone from the Karpenter space contribute the PR for this. @nojnhuh if you beat us to it be my guest. Pending Scheduler Driven Autoscaling providing kueue with a proper dry-run provisioning\binding API, Buffers is the right place to start, and capped buffers are a good iterative improvement

### Comment by [@fg91](https://github.com/fg91) — 2026-07-24T10:48:43Z

The issue says "Migrate from ...". 

I think it would be nice if the provisioning request admission check wouldn't be removed as e.g. GKE makes heavy use of it currently for what they call "dynamic workload scheduling/queued provisioning". 

https://docs.cloud.google.com/kubernetes-engine/docs/how-to/provisioningrequest

### Comment by [@nojnhuh](https://github.com/nojnhuh) — 2026-07-24T18:20:23Z

> We were thinking about having someone from the Karpenter space contribute the PR for this. @nojnhuh if you beat us to it be my guest.

@DerekFrank I've had other priorities the last few weeks so haven't made any meaningful progress on a proposal doc. Feel free to take over. @AaronLiChen has also done some exploration and might have some insight to share.

/unassign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-10-23T17:27:26Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@kannon92](https://github.com/kannon92) — 2026-10-23T17:30:01Z

/close

I think its too soon to migrate ProvRequest to Buffer API. And ProvRequest is v1 so we should invest resources in getting a capacity buffer support stable.

### Comment by [@kubernetes-prow[bot]](https://github.com/apps/kubernetes-prow) — 2026-10-23T17:30:09Z

@kannon92: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9662#issuecomment-6370826175):

>/close
>
>I think its too soon to migrate ProvRequest to Buffer API. And ProvRequest is v1 so we should invest resources in getting a capacity buffer support stable.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2026-10-23T18:20:17Z

> I think its too soon to migrate ProvRequest to Buffer API. And ProvRequest is v1 so we should invest resources in getting a capacity buffer support stable.

@kannon92 sure, but I think we need to have some issue to track the CapacityBuffer integration. Should we re-open this and re-title, or you prefer to open another one?

### Comment by [@kannon92](https://github.com/kannon92) — 2026-10-23T18:58:48Z

> @kannon92 sure, but I think we need to have some issue to track the CapacityBuffer integration. Should we re-open this and re-title, or you prefer to open another one?

Capacity buffer integration seems to be a requirement for Karpenter so I think its implictly tracked there. 

I am not sure if/when CAS would support Capacity buffers.

### Comment by [@DerekFrank](https://github.com/DerekFrank) — 2026-10-28T16:15:20Z

CAS already supports buffers

### Comment by [@jbtk](https://github.com/jbtk) — 2026-10-28T16:41:04Z

CAS supports buffers, but the GKE CAS provisioning requests still have some features that are not supported by the buffers (and not sure whether they will be supported in the near future).
