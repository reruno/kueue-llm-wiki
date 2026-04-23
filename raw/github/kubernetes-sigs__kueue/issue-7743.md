# Issue #7743: Add conversion webhook for Topology and Cohort APIs

**Summary**: Add conversion webhook for Topology and Cohort APIs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7743

**Last updated**: 2026-03-24T14:57:27Z

---

## Metadata

- **State**: open
- **Author**: [@Charleen-z](https://github.com/Charleen-z)
- **Created**: 2025-11-18T20:59:11Z
- **Updated**: 2026-03-24T14:57:27Z
- **Closed**: —
- **Labels**: `kind/support`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 26

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Add webhook-based conversion for Topology and Cohort CRDs.

**Why is this needed**:
Users upgrading from old CRD versions hit schema mismatch issues (e.g., Topology v1alpha1 → v1beta1, Cohort v1alpha1 -> v1beta1).

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-18T21:36:01Z

I think this is by design.

Kubernetes api conventions don't usually provide any guarantees for alpha -> beta APIs as alpha APIS can break.

Going forward I do expect that Topology v1beta1 -> v1beta2 or Cohort v1beta1 -> v1beta2 would be included in conversion webhooks if needed.

I'll tag the maintainers in case I am mistaken.

cc @mimowo @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-19T03:21:44Z

We follow the Kubernetes API deprecation policy: https://github.com/kubernetes-sigs/kueue?tab=readme-ov-file#production-readiness-status

So, as @kannon92 mentioned, the Alpha-level API will be terminated without compatibility.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-19T03:22:16Z

/remove-kind feature
/kind support

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-19T07:37:05Z

Yes, for Alpha APIs upgrading Kueue so far required manual steps as mentioned in the release notes for example in 0.9.0 or 0.13.0.

To make the upgrade easier going forward I see two options
1. support conversion webhooks also for alpha
2 make alpha APIs opt-in fully as in core k8s, using separate manifests for Alpha APIs. Then in helm we coukd have a flag like enableAlphaAPI=Topology,Cohort. Then we would inform users of the need to delete them on upgrade.

Im leaning to 2. as this approach is more inline with the corr k8s and clearly emphasizes the difference between Alpha and Beta APIs.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-19T07:37:19Z

cc @mwysokin

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-19T11:45:11Z

For Openshift we essentially do 2. But we don't give an option for it right now.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-19T12:06:44Z

> 2 make alpha APIs opt-in fully as in core k8s, using separate manifests for Alpha APIs. Then in helm we coukd have a flag like enableAlphaAPI=Topology,Cohort. Then we would inform users of the need to delete them on upgrade.

SGTM

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-19T13:33:40Z

As we dont have currently any Alpha API we can start doing so for the next Alpha API we introduce

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-19T16:34:17Z

> As we dont have currently any Alpha API we can staft doind so for the next Alpha API we ibtroduce

SGTM, I keep it in my mind.

### Comment by [@GonzaloLuminary](https://github.com/GonzaloLuminary) — 2025-11-20T13:59:46Z

Not having a conversion would be unfortunate. Many production clusters rely on TAS since waitForPodsReady is subpar. Would it be possible to maintain the conversion webhook if it's contributed by someone outside kueue's dev team?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-20T14:15:13Z

Sure, maybe an opt-in yaml or helm enabled by a param. wdyt @tenzen-y ?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-20T15:33:34Z

Is this for future alpha features?

Topology was promoted to v1beta1 in 0.14.

Cohorts was promoted to v1beta1 in 0.13.

So @GonzaloLuminary and @mimowo are you suggesting backporting support for conversion webhooks for older releases of Kueue?

I think Cohorts v1alpha1 API ( < 0.13) is no longer in support for upstream so I don't think that should be in scope.

I guess for TAS 0.13 -> 0.14 is still in support but when 0.15 gets released  next week, 0.13 goes out of support. So all supported releases of Kueue, starting next week, would only have v1beta1/v1beta2 APIs.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-20T17:25:11Z

Yeah we could consider conversion for Topology objects, but as mentioned above ROI is low at this point, and we are busy reviewing stuff which will be included in the release 0.15.0.

Also I know that the manual procedure for upgrading to 0.14.0 was tested by some users and it allowed upgrade without disruption, so I would encourage trying that actually.

### Comment by [@GonzaloLuminary](https://github.com/GonzaloLuminary) — 2025-11-20T17:32:43Z

I think the instructions mention deleting topologies before applying again with the new API version. How do CQs react to those changes while the new topology CRs are being applied?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-20T17:34:59Z

> Is this for future alpha features?
> 
> Topology was promoted to v1beta1 in 0.14.
> 
> Cohorts was promoted to v1beta1 in 0.13.
> 
> So [@GonzaloLuminary](https://github.com/GonzaloLuminary) and [@mimowo](https://github.com/mimowo) are you suggesting backporting support for conversion webhooks for older releases of Kueue?
> 
> I think Cohorts v1alpha1 API ( < 0.13) is no longer in support for upstream so I don't think that should be in scope.
> 
> I guess for TAS 0.13 -> 0.14 is still in support but when 0.15 gets released next week, 0.13 goes out of support. So all supported releases of Kueue, starting next week, would only have v1beta1/v1beta2 APIs.

I totally agree with @kannon92 
Kueue does not have commitment for alpha features and APIs, which are documented as I mentioned above.
We have such a guideline to answer such requests. Non-supported compatibilities in the OSS version should be provided by the enterprise vendor or end users. And I think that the extended such supports are one of primary advantage of enterprise-grade OSS support.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-20T17:44:32Z

> I think the instructions mention deleting topologies before applying again with the new API version. How do CQs react to those changes while the new topology CRs are being applied?

My recommendation for production is stop ClusterQueue by `stopPolicy` while Topology API updating process for more stable.
The stopped ClusterQueue stops to admit new workloads, but the already running workloads are still running (You can change the behavior for existing running workloads in stopPolicy).

### Comment by [@Charleen-z](https://github.com/Charleen-z) — 2025-11-20T18:06:30Z

Totally understand that Kueue doesn’t provide commitments for alpha features or APIs.

For our team’s use cases with Kueue (currently 0.12), not having a conversion webhook for alpha creates a lot of manual work to upgrade many clusters, and we’re also unsure about the upgrade behavior for different cluster states. This has been blocking our ability to upgrade and use new features.

We can contribute by implementing the conversion webhook for Topology and Cohort if maintainers can help review it — that would be really helpful.

### Comment by [@GonzaloLuminary](https://github.com/GonzaloLuminary) — 2025-11-20T18:28:59Z

>My recommendation for production is stop ClusterQueue by stopPolicy while Topology API updating process for more stable.
The stopped ClusterQueue stops to admit new workloads, but the already running workloads are still running (You can change the behavior for existing running workloads in stopPolicy).

That makes sense thanks. I think it's worth adding this information/workarounds to the release docs together with the upgrade instructions.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-20T19:17:08Z

> > My recommendation for production is stop ClusterQueue by stopPolicy while Topology API updating process for more stable.
> > The stopped ClusterQueue stops to admit new workloads, but the already running workloads are still running (You can change the behavior for existing running workloads in stopPolicy).
> 
> That makes sense thanks. I think it's worth adding this information/workarounds to the release docs together with the upgrade instructions.

That could be possible. I have no strong opinion.
@mimowo Any thoughts?

### Comment by [@Charleen-z](https://github.com/Charleen-z) — 2025-11-21T17:50:11Z

> Totally understand that Kueue doesn’t provide commitments for alpha features or APIs.
> 
> For our team’s use cases with Kueue (currently 0.12), not having a conversion webhook for alpha creates a lot of manual work to upgrade many clusters, and we’re also unsure about the upgrade behavior for different cluster states. This has been blocking our ability to upgrade and use new features.
> 
> We can contribute by implementing the conversion webhook for Topology and Cohort if maintainers can help review it — that would be really helpful.

@mimowo @tenzen-y @kannon92  Any thoughts about it? Thanks!

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-21T17:58:23Z

My thoughts are https://github.com/kubernetes-sigs/kueue/issues/7743#issuecomment-3558694896.

I'm not a maintainer though but what you are really asking for is webhooks backported to unsupported release branches of Kueue. For you, you would want to propose a webhook in 0.12 to help mitigate upgrades to 0.13, 0.14 or 0.15.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-24T08:25:09Z

> > As we dont have currently any Alpha API we can start doing so for the next Alpha API we introduce
> 
> SGTM, I keep it in my mind.

Opened the issue to track it: https://github.com/kubernetes-sigs/kueue/issues/7830

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-24T08:29:23Z

> > We can contribute by implementing the conversion webhook for Topology and Cohort if maintainers can help review it — that would be really helpful.
> 
> [@mimowo](https://github.com/mimowo) [@tenzen-y](https://github.com/tenzen-y) [@kannon92](https://github.com/kannon92) Any thoughts about it? Thanks!

I would suggest to follow https://github.com/kubernetes-sigs/kueue/issues/7830.

Regarding adding conversions for historical releases, I think it will be complex more than you think. For example we hit this issue when adding conversions to 0.15 (https://github.com/kubernetes-sigs/kueue/issues/7344) and are solving the problem now: https://github.com/kubernetes-sigs/kueue/pull/7772. So I think it would require to cherrypick that PR too. 

I basically think it is more pragmatic at this point to follow the manual upgrade procedures which were already tested on sizeable deployments.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-24T13:38:59Z

> > > We can contribute by implementing the conversion webhook for Topology and Cohort if maintainers can help review it — that would be really helpful.
> > 
> > 
> > [@mimowo](https://github.com/mimowo) [@tenzen-y](https://github.com/tenzen-y) [@kannon92](https://github.com/kannon92) Any thoughts about it? Thanks!
> 
> I would suggest to follow [#7830](https://github.com/kubernetes-sigs/kueue/issues/7830).
> 
> Regarding adding conversions for historical releases, I think it will be complex more than you think. For example we hit this issue when adding conversions to 0.15 ([#7344](https://github.com/kubernetes-sigs/kueue/issues/7344)) and are solving the problem now: [#7772](https://github.com/kubernetes-sigs/kueue/pull/7772). So I think it would require to cherrypick that PR too.
> 
> I basically think it is more pragmatic at this point to follow the manual upgrade procedures which were already tested on sizeable deployments.

SGTM

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-22T14:18:15Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-24T14:57:23Z

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
