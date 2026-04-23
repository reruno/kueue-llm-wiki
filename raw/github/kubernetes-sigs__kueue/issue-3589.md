# Issue #3589: Filter manageJobsWithoutQueueNames using a namespaceSelector for all integrations

**Summary**: Filter manageJobsWithoutQueueNames using a namespaceSelector for all integrations

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3589

**Last updated**: 2024-12-13T09:49:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@dgrove-oss](https://github.com/dgrove-oss)
- **Created**: 2024-11-18T22:24:24Z
- **Updated**: 2024-12-13T09:49:57Z
- **Closed**: 2024-12-13T09:48:58Z
- **Labels**: `kind/feature`
- **Assignees**: [@dgrove-oss](https://github.com/dgrove-oss)
- **Comments**: 14

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Add a `manageJobsWithoutQueueNameNamespaceSelector` to the Kueue configuration API and use it to restrict the jobs to which `manageJobsWithoutQueueName` is applied across all integrations.

We can then deprecate `podOptions.namepaceSelector` and eventually remove it from the configuration API. 

**Why is this needed**:

As discussed in the review of #3520,  because the Deployment and StatefulSet integrations are built on top of the Pod integration, they implicitly restrict the scope of `manageJobsWithoutQueueName` by filtering it with `podOptions.namepaceSelector`.   This results in an irregular API that may be confusing to users.  

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-11-18T22:25:19Z

/assign

I will work on drafting a KEP.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-19T09:26:10Z

cc @mwielgus @tenzen-y @mwysokin

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-19T17:20:24Z

IIRC, we did not introduce this mechanism in the previous discussions: https://github.com/kubernetes-sigs/kueue/issues/2119

Instead of introducing this knob, shouldn't we decouple the Stateful and Deployment integration from Pod integration?
Actually, the StatefulSet integration has dedicated controller, and I'm not sure the reason why we keep depending on the Pod integrations.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-11-19T18:18:04Z

This was discussed before (#2119), but what changed since then is the addition of the Deployment and StatefulSet integrations.  

Deployment and StatefulSet have the same fundamental issue with `manageJobsWithoutQueueNames` as Pod (independent of how we choose to implement the integrations).   If `manageJobsWithoutQueueNames` is true and you don't restrict its scope somehow things will break because system namespaces that use Deployments or StatefulSets will unexpectedly be suspended, breaking the system's functionality.   

So, the proposal is to put together a KEP to see what it would take to have a uniform API to modulate manageJobsWithoutQueueNames.  

An alternative that we can discuss in the KEP is to instead deprecate and then remove `manageJobsWithoutQueueNames` entirely in favor of a ValidatingAdmissionPolicy.  I've implemented such a policy as part of our MLBatch project (see [admissionPolicy.yaml](https://github.com/project-codeflare/mlbatch/blob/main/setup.k8s-v1.30/admission-policy.yaml)) and it was subtler than was suggested in the discussion of #2119.  In particular, dealing with child Jobs requires teaching the VAP about ownership links and (at least for me) that was tricky and I'm not convinced it is less complex than the namespaceSelector option.  Note that my VAP only deals with one level of ownership (because that's all I needed for our restricted use case).  A general one would have to deal with crawling several links to get to the "top-level" Job that was being managed by Kueue.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-19T18:31:22Z

Regarding the Deployments and StatefulSet via pod-based integration.

The fundamental difference between Deployments, StatefulSet and JobCRDs is that there is no suspend field ( and it is unlikely to be ever added, or it will take a year at very least to get into beta).

So, using scheduling Gates for suspending seems like a good fit, and this is already provided by the pod-based integration, so we are reusing it. I'm open to alternatives, but I think they need to be presented more holistically, and in detail, because they seem vague at the moment to me at least.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-11-20T02:54:30Z

Initial draft of the KEP in #3595

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2024-11-26T14:16:20Z

It seems local queue defaulting and manageJobsWithoutQueueNames deprecation solve should solve your issue, right? The admins will create default local queue and it will be used for jobs without queue name.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-11-26T14:52:06Z

> It seems local queue defaulting and manageJobsWithoutQueueNames deprecation solve should solve your issue, right? The admins will create default local queue and it will be used for jobs without queue name.

No.   I'm revising the KEP to clarify the point.  Whether it is manageJobsWithoutQueueNames or the local queue defaulting, there still needs to be a way to scope either mechanism to a subset of the namespaces.  Without the namespace scoping for at least `Pod`, `Deployment`, `StatefulSet` and `Job` it is not practical to enable any default management at the level of the Kueue manager for jobs without queue name.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-05T09:21:26Z

As mentioned in https://github.com/kubernetes-sigs/kueue/pull/3712#issuecomment-2519718280 I would like to yet:
- respect the new selector in the webhooks for Deployment and StatefulSet
- add documentation for the new feature - possibly migrate the use of podOptions.namespaceSelector, but could be left for follow up

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-12-05T20:57:03Z

Documented the new feature in #3748.

I'll do the migration of the documentation for `podOptions.namespaceSelector` in a separate PR to make it easier to review.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-06T10:39:54Z

Thanks, I think we still need to follow up with the implementation, to make the transition from `podOptions.namespaceSelector` possible:
- for deployment and statefulset webhook respect `mangedJobsNamespaceSelector` - to avoid adding the PodGroup levels and annotations to pods which would later not be considered by Kueue
- for pod_webhook respect also `mangedJobsNamespaceSelector` - effectively intersection of both pod and workload

With the changes above user can completely skip setting `podOptions.namespaceSelector` and we can deprecate it

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-12-06T14:44:44Z

Agreed on the webhooks... I didn't quite get it done yesterday.  Hoping to get there today.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-12-12T22:49:16Z

I believe #3828 is the last thing to be done.  Once that merges we should be able to close this issue as completed.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-13T09:48:58Z

/close 
as https://github.com/kubernetes-sigs/kueue/pull/3828 and https://github.com/kubernetes-sigs/kueue/pull/3817 are merged. I'm ok to handle the podOptions deprecation as a separate issue.
