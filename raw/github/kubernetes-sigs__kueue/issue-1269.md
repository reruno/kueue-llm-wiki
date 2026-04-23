# Issue #1269: Requirements for v0.6

**Summary**: Requirements for v0.6

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1269

**Last updated**: 2024-02-14T18:42:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-10-26T13:03:38Z
- **Updated**: 2024-02-14T18:42:32Z
- **Closed**: 2024-02-14T18:42:31Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 25

## Description

```[tasklist]
### Accepted
- [ ] #168
- [ ] https://github.com/kubernetes-sigs/kueue/issues/976
- [ ] https://github.com/kubernetes-sigs/kueue/issues/1283
- [ ] https://github.com/kubernetes-sigs/kueue/issues/1284
- [ ] https://github.com/kubernetes-sigs/kueue/issues/1091
- [ ] https://github.com/kubernetes-sigs/kueue/issues/693
- [ ] https://github.com/kubernetes-sigs/kueue/issues/1282
- [ ] https://github.com/kubernetes-sigs/kueue/issues/1224
```

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-27T20:21:35Z

cc @tenzen-y @kerthcet for thoughts and additional suggestions.

Some of these things are big, so they might need to be split in smaller increments (like multi cluster and hierarchy), just like we did for Pod support (first single, then groups).

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-10-27T20:34:43Z

I will create an issue to add integration for the Serving use case by Kserve.

> Some of these things are big, so they might need to be split in smaller increments (like multi cluster and hierarchy), just like we did for Pod support (first single, then groups).

SGTM

@alculquicondor #79 is already accepted? I think we should take carefully the feature since the feature will provide more complexity to kueue.

Also, I think we should consider if Cohort can functional as an alternative of #79.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-27T20:47:21Z

@mwielgus is working on a proposal for #79 that guarantees backwards compatibility. And we will have stages so that we can make some progress in 0.6.

The plan is to actually make Cohort an object :)

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-10-27T20:49:37Z

> The plan is to actually make Cohort an object :)

Oh, it sounds like a nice idea. I can't wait for the KEP :)

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-11-07T08:19:12Z

Some feedbacks from our team, hope to support:
- https://github.com/kubernetes-sigs/kueue/issues/1224 if accepted
- https://github.com/kubernetes-sigs/kueue/issues/79 as an enterprise demand
- https://github.com/kubernetes-sigs/kueue/issues/976
- https://github.com/kubernetes-sigs/kueue/issues/940, this requires more time, but we can start to design now.


Also, it will be great to to hava:
- https://github.com/kubernetes-sigs/kueue/issues/1204, but this involves contributions to volcano upstream, still WIP.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-11-07T20:29:35Z

Awesome, it looks like we are inline @kerthcet. But we will probably need extra hands for #940.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-12-15T10:21:45Z

Now, kueue acts well in resource sharing, but not that fair, like lacking the capacity of https://github.com/kubernetes-sigs/kueue/issues/752 and https://github.com/kubernetes-sigs/kueue/issues/754. which is now mitigated by https://github.com/kubernetes-sigs/kueue/issues/973.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-16T16:21:35Z

@alculquicondor should we graduate `ProvisioningACC` to Beta?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-26T18:00:25Z

I cleaned up some of the issues.

I would like to cut a release in the first week of February.

#1282 has a basic form, but @tenzen-y wanted to add a few more knobs, which shouldn't be too controversial, so it can probably make it.

I think #1224 is at risk. Last time I checked, the calculations were not quite right. Also it touches some crucial parts of the code, so there might not be enough time to spot bugs. Maybe we can be more coarse about using the feature gate to guard the behavior? In other words, call the feature gate a few times in top level functions, as opposed to call it in multiple smaller functions. Or we can leave it for 0.7 by April? @kerthcet is shepherding this.

Thoughts?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-26T20:12:20Z

> https://github.com/kubernetes-sigs/kueue/issues/1282 has a basic form, but @tenzen-y wanted to add a few more knobs, which shouldn't be too controversial, so it can probably make it.

Yes, I want to include #1608 (Part-of #1282) in v0.6 since I changed the API change in #1608.

The design is completed and waiting for the review now.

Also, I want to include https://github.com/kubernetes-sigs/kueue/issues/1601 as much as possible, although I'm not sure that we should put it here due to only facing for developers.

I believe that we can finalize #1601 by the end of January since the remaining task for #1601 is only one.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-26T20:13:05Z

@alculquicondor @mimowo Did you discuss https://github.com/kubernetes-sigs/kueue/issues/1269#issuecomment-1894076704 anywhere?

> @alculquicondor should we graduate ProvisioningACC to Beta?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-26T21:07:09Z

Nope. But we are capacity constrained, so my answer is no for now.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-26T21:10:10Z

> Nope. But we are capacity constrained, so my answer is no for now.

SGTM 
I don't have strong objections.
If I had to say it, we should not delay the release day due to the graduation of ProvisioningACC.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-29T07:49:45Z

> > Nope. But we are capacity constrained, so my answer is no for now.
> 
> SGTM I don't have strong objections. If I had to say it, we should not delay the release day due to the graduation of ProvisioningACC.

I'm wondering what is yet needed before graduation, because the [KEP](https://github.com/kubernetes-sigs/kueue/pull/1147) says just "User feedback is positive.". 

One benefit of graduating to Beta is that we could delete the manifest from [DWS example](https://github.com/GoogleCloudPlatform/ai-on-gke/tree/main/gke-dws-examples), which currently is required to enable the feature gate.

I share the sentiment that we should not prolong Kueue release just because of that.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-01-29T08:48:42Z

For #1224, I think the calculations is right now, you can take a look, especially the tests, ~I'll catch with this until tomorrow evening, I have some urgent tasks in hand.~ I broke the words, reviewed and generally LGTM.

I think we can finish this until the end of this week if everything goes well .. What's the planning day for new release?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-01-29T08:53:13Z

FYI, from Feb. 9th, we'll on holiday for Chinese  New Year, we hope to finish this work before that time then little code conflicts to solve. 😢

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-29T13:01:36Z

> I'm wondering what is yet needed before graduation, because the https://github.com/kubernetes-sigs/kueue/pull/1147 says just "User feedback is positive.".
> 
> One benefit of graduating to Beta is that we could delete the manifest from [DWS example](https://github.com/GoogleCloudPlatform/ai-on-gke/tree/main/gke-dws-examples), which currently is required to enable the feature gate.

I'm not familiar with GKE DWS. So, I leave a decision on @alculquicondor whether we include the graduation of ProbisioningACC.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-29T13:05:29Z

> What's the planning day for new release?

@kerthcet Our deadline is 8th Feb (9th Feb at Asia TZ). If all tasks are done earlier, we can release a new version at that time.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-30T23:36:36Z

> I'm not familiar with GKE DWS. So, I leave a decision on [Aldo Culquicondor](https://github.com/alculquicondor) whether we include the graduation of ProvisioningACC.

Sure, it sounds like we don't need extra tests for now. Although thinking about metrics could be useful. I would be ok leaving it for the next release if @mimowo doesn't have time to think about this.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-31T15:25:55Z

I think it is better to leave for the next release in that case.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-02-12T00:04:19Z

This is the last piece of v0.6: #1709

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-13T19:16:58Z

Implementation is all done. We can work on documentation in parallel to the release steps.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-02-13T19:18:53Z

> Implementation is all done. We can work on documentation in parallel to the release steps.

SGTM

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-14T18:42:27Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-02-14T18:42:32Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1269#issuecomment-1944395249):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
