# Issue #6777: Consider deprecating and dropping LocalQueueFlavorStatus on v1beta2

**Summary**: Consider deprecating and dropping LocalQueueFlavorStatus on v1beta2

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6777

**Last updated**: 2025-10-24T07:21:36Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-09-10T07:55:18Z
- **Updated**: 2025-10-24T07:21:36Z
- **Closed**: 2025-10-24T07:21:36Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@iomarsayed](https://github.com/iomarsayed)
- **Comments**: 9

## Description

We had some discussions if we should keep LocalQueueFlavorStatus. This was introduced under the [KEP-3122: Expose Flavors in LocalQueue Status](https://github.com/kubernetes-sigs/kueue/tree/main/keps/3122-expose-flavors-in-localqueue-status), see [thread](https://github.com/kubernetes-sigs/kueue/pull/4543#discussion_r1989906588).

I think the KEP introduced the API in status back before we had the on-demand API, so we didn't have a clear alternative. I think on-demand API would have been a better fit, but we already have the API.

Now, as we are approaching v1beta2 (hopefully in 0.15) I would like to align on the approach here:
1. deprecate in 0.14, drop in v1beta2 along without replacement
2. deprecate in 0.14, drop in v1beta2 along with on-demand API replacement
3. keep supported in v1beta2, but plan for the on-demand API for similar use-cases. Plan migration when ready, possibly v1beta3 of v1.
4. keep supported in v1beta2, no specific plans for on-demand API until we have contributors willing to take it

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-10T07:59:28Z

(1.) is least amount of work but would be breaking, cc @KPostOffice @dgrove-oss @kannon92 who might be using the feature (I don't know)
(2.) is probably the cleanest, but we should act quickly if we want to do it, so that we can develop the replacement without delaying v1beta2 (similarly as we dropped QueueVisibility in favor of on-demand API)
(3.) "keep as is and defer decisions for later"
(4.) "keep as is", because the maintenance of the APi is not too high.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-10T07:59:47Z

cc @tenzen-y @mwielgus @mwysokin

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-10T07:59:53Z

cc @gabesaba

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-10T10:44:16Z

I think ideally we would like to deprecate it and ultimately drop (1.) or (2.). 

The question which could help the decision making process is if we need replacement (2.), and if we have contributors willing to work on it?

Looking for  any hints in the  community, but particularly from RedHat as I think there was some interest in the feature in the past, cc @kannon92

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-13T16:27:23Z

As discussed on wg-batch on 9th Oct we prefer to drop the feature entirely. Still, I would prefer to do it in two steps, so the first PR would only deprecate, even if we send the follow up PR in the same release. This way we can easily rollback the dropping if it turns out that we need to keep the feature.

### Comment by [@iomarsayed](https://github.com/iomarsayed) — 2025-10-16T13:59:53Z

/assign

### Comment by [@iomarsayed](https://github.com/iomarsayed) — 2025-10-20T10:20:16Z

@mimowo 

What are the chances we will just entirely drop it for the release?
I am asking the question, because if we will drop it in the same release, why do we need to deprecate first and not just go for the drop instantly?

I think we will have the ability to rollback in both cases (If we depreciate then drop ... or just drop entirely).

Correct me if I am wrong at any point.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-20T10:34:00Z

I would deprecate for now. And potentially drop in the follow up PR.

The chances that we drop in this release are some, but dropping is a bit aggressive given the k8s deprecation policy: https://kubernetes.io/docs/reference/using-api/deprecation-policy/#deprecating-a-feature-or-behavior: "Rule #7: Deprecated behaviors must function for no less than 1 year after their announced deprecation.". 

While this is a guideline there are also exceptions https://kubernetes.io/docs/reference/using-api/deprecation-policy/#exceptions, so if the community agrees we could proceed dropping in 0.15. Also, this is k8s guideline, and in Kueue we move a bit faster, so I'm happy to consider dropping in 0.15. However, here the chances are 50% I would say. 

I want to raise this topic on the next wg-batch meeting. Note that I mentioned that on the last community meeting and there were no objections for dropping.

### Comment by [@iomarsayed](https://github.com/iomarsayed) — 2025-10-20T11:33:45Z

Okay great, Will proceed with deprecation first.
