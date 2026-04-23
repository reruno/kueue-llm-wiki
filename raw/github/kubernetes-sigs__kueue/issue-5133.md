# Issue #5133: [Discussion]: Kueue and Karpenter Support

**Summary**: [Discussion]: Kueue and Karpenter Support

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5133

**Last updated**: 2026-04-13T05:28:50Z

---

## Metadata

- **State**: open
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-04-26T14:31:05Z
- **Updated**: 2026-04-13T05:28:50Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 20

## Description



**What would you like to be added**:
Similar to CAS, it would be nice to be able to integrate with Karpenter for autoscaling.
**Why is this needed**:
Karpenter is a popular autoscaling framework and I don't think it is possible to use this with Kueue.

**Discussion**:

The real way to support this is probably through use of admission checks like Kueue does for ProvisioningRequest. The main question i have is the only way to support this with Kueue would be to get ProvisionRequests in Karpenter?

Or should we explore other options?

Relevant issues:
- https://github.com/kubernetes-sigs/karpenter/issues/742
- https://docs.google.com/document/d/1SyqStWUt407Rcwdtv25yG6MpHdNnbfB3KPmc4zQuz1M/edit?tab=t.0

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-02T01:49:29Z

> Karpenter is a popular autoscaling framework and I don't think it is possible to use this with Kueue.

The mitigation way is specifying larger resources in cq. In that case, Kueue dispatches workloads beyond current actual cluster capacities, after that Karpenter tries to scale the cluster based on the Pending Pods.
However, I can understand that this is not ideal.

> The real way to support this is probably through use of admission checks like Kueue does for ProvisioningRequest. The main question i have is the only way to support this with Kueue would be to get ProvisionRequests in Karpenter?
> 
> Or should we explore other options?

I think a seamless way is supporting ProvisioningRequest in Karpenter as well as you say. However, if Karpenter provides any CustomResource to tell Pod spec in advance, we can reuse it. Do you know if Karpenter provides the way?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-13T21:04:17Z

> I think a seamless way is supporting ProvisioningRequest in Karpenter as well as you say. However, if Karpenter provides any CustomResource to tell Pod spec in advance, we can reuse it. Do you know if Karpenter provides the way?

I'm not sure. @jonathan-innis Do you know?

### Comment by [@jonathan-innis](https://github.com/jonathan-innis) — 2025-05-14T05:32:29Z

We don't have a way to do that right now outside of negative priority pods. I'm not 100% sure if we're going to support ProvisioningRequest in its current form. There's a separate proposal that's coming from folks in SIG Autoscaling at the same time called [Buffer](https://github.com/kubernetes-sigs/karpenter/issues/749#issuecomment-2877569528) that I think more folks are aligned with and supports similar use-cases. I'd be interested to hear what y'all think about that proposal in the context of Karpenter and Kueue

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-16T15:33:12Z

> We don't have a way to do that right now outside of negative priority pods. I'm not 100% sure if we're going to support ProvisioningRequest in its current form. There's a separate proposal that's coming from folks in SIG Autoscaling at the same time called [Buffer](https://github.com/kubernetes-sigs/karpenter/issues/749#issuecomment-2877569528) that I think more folks are aligned with and supports similar use-cases. I'd be interested to hear what y'all think about that proposal in the context of Karpenter and Kueue

Thank you for letting me know. TBH, I think the supporting ProvisioningRequest in Karpenter is not a requirement for Kueue.
We have an Intermediate resource, AdmissionCheck. So, if Karpenter provides any CustomResource to request provisioning node resources, Kueue can leverage it.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-19T06:44:50Z

> Thank you for letting me know. TBH, I think the supporting ProvisioningRequest in Karpenter is not a requirement for Kueue. 

Well, it would be great if Kueue supported Karpenter OOTB, but I think the code needs to be done either in Karpenter (to support the ProvReq), or inside autoscaler (to adjust the API definition for the needs of Karpenter). There is little that can be done inside Kueue.

> We don't have a way to do that right now outside of negative priority pods. I'm not 100% sure if we're going to support ProvisioningRequest in its current form. 

@jonathan-innis, so IIUC ProvReq API has some limitations that hold you back supporting it in Karpenter, related to "negative priority pods"? Could you expand on this a bit more so that we learn the context,  maybe this could be handled with a small adjustment of the API?

cc @mwielgus @mwysokin in case some of you have more context.

### Comment by [@jonathan-innis](https://github.com/jonathan-innis) — 2025-05-20T04:56:58Z

> We have an Intermediate resource, AdmissionCheck. So, if Karpenter provides any CustomResource to request provisioning node resources, Kueue can leverage it

I'd say it's much more likely that we support something like Buffer since it has overlapping use-cases with PR -- are there any parts of the Buffer proposal that don't work with Kueue? From my initial read of it, I'm not sure we would need both in the project.

I'd love to discuss more online! Happy to either join WG Batch or if y'all wanted to [join our Karpenter WG that we have bi-weekly](https://github.com/kubernetes-sigs/karpenter?tab=readme-ov-file#working-group-meetings) we could probably have a more fleshed-out discussion there.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-18T05:01:52Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-19T18:56:59Z

/remove-lifecycle stale

### Comment by [@Zhenshan-Jin](https://github.com/Zhenshan-Jin) — 2025-09-03T20:11:21Z

@tenzen-y what is the next step here to support Kueue with Karpenter? 

If I understand correctly, if Karpenter decide to support Buffer instead of ProvisioningRequest, then we will do something like similar as https://kueue.sigs.k8s.io/docs/admission-check-controllers/provisioning/ for the Buffer? 

Thank you!

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-03T20:14:14Z

That is correct. It looks like https://github.com/kubernetes/autoscaler/pull/8151 design merged at least.

### Comment by [@Zhenshan-Jin](https://github.com/Zhenshan-Jin) — 2025-09-04T15:35:13Z

Thank you! @kannon92 

@jonathan-innis have we concluded the plan to move forward about how to integrate Karpenter with Buffer API which has been merged already? Thank you!

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-12T10:58:19Z

> [@tenzen-y](https://github.com/tenzen-y) what is the next step here to support Kueue with Karpenter?
> 
> If I understand correctly, if Karpenter decide to support Buffer instead of ProvisioningRequest, then we will do something like similar as https://kueue.sigs.k8s.io/docs/admission-check-controllers/provisioning/ for the Buffer?
> 
> Thank you!

Yes, after the Buffer API has been released and support that in Karpenter. We can start the Kueue Karpenter support via Buffer Admission Check.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-11T11:33:33Z

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

### Comment by [@Zhenshan-Jin](https://github.com/Zhenshan-Jin) — 2025-12-11T21:56:36Z

hi is this in the roadmap for 2026? We are looking for leverage for our use case.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-11T22:09:09Z

/remove-lifecycle stale

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-11T22:14:09Z

@Zhenshan-Jin I have not heard anyone signing up for this work.

Its not really a priority for me for 2026.

If there is interest from you, you could consider creating an admission check once Karpenter supports the BufferAPI.

It seems that that work is still in the desigh phase so I don't think this is happening anytime soon.

### Comment by [@Zhenshan-Jin](https://github.com/Zhenshan-Jin) — 2025-12-12T02:19:47Z

link the issue here for future reference about the Karpenter integration with BufferAPI: https://github.com/kubernetes-sigs/karpenter/issues/2571

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-12T02:53:31Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-11T03:36:24Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-04-13T05:28:47Z

/remove-lifecycle rotten
