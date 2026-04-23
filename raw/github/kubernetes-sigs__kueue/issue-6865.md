# Issue #6865: Kubeflow Trainer v2 integration follow ups

**Summary**: Kubeflow Trainer v2 integration follow ups

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6865

**Last updated**: 2025-10-03T12:10:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-09-16T18:57:15Z
- **Updated**: 2025-10-03T12:10:59Z
- **Closed**: 2025-10-03T12:10:59Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 33

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

This is to address remaining comments to https://github.com/kubernetes-sigs/kueue/pull/6597

1. Don't lookup the JobSet object in the GenericJob implementation
2. Don't use the Background context, instead use the "request" context from PodSets() etc.


**Why is this needed**:
1 because:
a) JobSet should be an implementation detail of the Trainer which might be replaced in the future
b) it creates tricky race conditions to reason about, because the JobSet may not be immediately created
c) it couples the JobSet API version used for Trainer with the version we integrate with

Instead, helpers exposed by the Trainer should be used, but they require releasing 2.0.1.

2. becuase:
1. background context cannot be cancelled, so the goroutine leaks / remains running even if the main Kueue goroutine is terminated
2. the "request" context may have more data to log, like the workload name etc.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-16T18:57:52Z

/assign @kaisoz 
Who I think is already looking into the follow ups.
cc @tenzen-y @andreyvelich @astefanutti

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-17T18:50:26Z

Also can we add a page in our site for trainer?

cc @andreyvelich @kaisoz

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-18T08:09:59Z

For sure we need docs, but we can add docs post code release, potentially. 

So, I would prefer to focus on addressing the code follow ups.

### Comment by [@izturn](https://github.com/izturn) — 2025-09-24T08:21:05Z

Just tried the current code and it doesn’t seem to work in **TAS** mode. Looks like the Pods don’t get the proper podset/workload labels and annotations when they start up(at `RunWithPodSetsInfo`). Because of that, the ungater can’t find the matching Pods(at `podsForPodSet`), so the scheduling gate never gets removed and the pods just stays stuck in **Pending**. @kaisoz

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-24T08:36:42Z

Yes, this is the current "known limitation" due to the fact that Trainer v2 does not allow to update the podSetOverrides with labels & annotations, see open issue: https://github.com/kubernetes-sigs/kueue/issues/6865

It would be great to work on resoling this limitation.

cc @mwysokin

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-24T09:30:21Z

Actually, there might be a dirty workaround inside Kueue. We could access the JobSet object and inject the labels & annotations before unsuspending in the Resume phase. 

If we have a PR, I could support it as a "temporary fix" while waiting for Trainer v2 fixes.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-24T09:30:40Z

cc @kaisoz @andreyvelich @tenzen-y

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-09-24T09:38:12Z

> Actually, there might be a dirty workaround inside Kueue. We could access the JobSet object and inject the labels & annotations before unsuspending in the Resume phase. 
> 
> If we have a PR, I could support it as a "temporary fix" while waiting for Trainer v2 fixes.

Unfortunately that won't work @mimowo because the trainjob controller reconciles the jobset and removes the labels and annotations (I've tried this already)

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-24T09:53:32Z

Got it, what about mutating the Trainer's Runtime object before resuming

### Comment by [@andreyvelich](https://github.com/andreyvelich) — 2025-09-24T09:57:54Z

@mimowo @kaisoz Can we configure those labels/annotations in the Runtime before TrainJob is created?
Or labels must be set by the Kueue controller ?

### Comment by [@izturn](https://github.com/izturn) — 2025-09-24T10:03:11Z

the `podsForPodSet`'s filter is the podset & workload's name, so i guess they can't be configured?

> [@mimowo](https://github.com/mimowo) [@kaisoz](https://github.com/kaisoz) Can we configure those labels/annotations in the Runtime before TrainJob is created? Or labels must be set by the Kueue controller ?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-24T10:13:59Z

> Can we configure those labels/annotations in the Runtime before TrainJob is created?

before created I don't think, because Kueue may admit / evict multiple times during lifetime.

We could however "modify" the TainerRuntime object, unless it is explicitly prohibited by a webhook?

### Comment by [@andreyvelich](https://github.com/andreyvelich) — 2025-09-24T11:15:41Z

>before created I don't think, because Kueue may admit / evict multiple times during lifetime.

Does Kueue modify the TAS labels during admission or eviction ?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-24T11:20:52Z

> Does Kueue modify the TAS labels during admission or eviction ?

Both

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-24T11:39:10Z

@izturn one more thought - can you check using "main" Kueue. I suspect that maybe there is a difference after we stopped injecting the "tas" label. Still, we will not support the "implicit" mode, but I suspect that "required" and "preferred" modes have a chance to work.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-24T15:02:11Z

Additionally, I would like to narrow down the below annotation usage by renaming to `kueue.x-k8s.io/trainjob-override-idx` so that we can avoid accidentally introduce the annotation to different places.

https://github.com/kubernetes-sigs/kueue/blob/4c66b01c67e972c7250eeeb8ffeb87ccf961054a/pkg/controller/jobs/kubeflow/trainjob/trainjob_controller.go#L53

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-24T15:07:19Z

Ultimately I think the podSetOverrides should have the 'manager' field, then the annotation would not be needed. I discussed this with  Tomas and we came up with the annotation idea as a workaround, so that Kueue can know which overrides are done by Kueue and which by user.

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-09-24T20:48:20Z

> Got it, what about mutating the Trainer's Runtime object before resuming

I think that should work! Although it'd make both the `RunWithPodsetsInfo` and `RestorePodSetsInfo` a bit more complicated. Do you want me to try that out or better wait for Trainer PR to sink in?

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-09-24T20:49:17Z

> Additionally, I would like to narrow down the below annotation usage by renaming to `kueue.x-k8s.io/trainjob-override-idx` so that we can avoid accidentally introduce the annotation to different places.
> 
> [kueue/pkg/controller/jobs/kubeflow/trainjob/trainjob_controller.go](https://github.com/kubernetes-sigs/kueue/blob/4c66b01c67e972c7250eeeb8ffeb87ccf961054a/pkg/controller/jobs/kubeflow/trainjob/trainjob_controller.go#L53)
> 
> Line 53 in [4c66b01](/kubernetes-sigs/kueue/commit/4c66b01c67e972c7250eeeb8ffeb87ccf961054a)
> 
>  FirstOverrideIdx = "kueue.x-k8s.io/override-idx"

As @mimowo said, this is a workaround,but anyway I can rename the annotation 👍🏻

### Comment by [@izturn](https://github.com/izturn) — 2025-09-25T01:53:50Z

> [@izturn](https://github.com/izturn) one more thought - can you check using "main" Kueue. I suspect that maybe there is a difference after we stopped injecting the "tas" label. Still, we will not support the "implicit" mode, but I suspect that "required" and "preferred" modes have a chance to work.

Sure, I can try again. But tbh, as a beginner, I don’t really understand what you mean by the “main” kueue things. I’m not sure how to do that. Could you walk me through it with a bit more detail? Thanks!

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-25T05:12:57Z

> Ultimately I think the podSetOverrides should have the 'manager' field, then the annotation would not be needed. I discussed this with Tomas and we came up with the annotation idea as a workaround, so that Kueue can know which overrides are done by Kueue and which by user.

We probably need to generize the case for manager, then propose it to KF Trainer and it will not contain in the next Kueue release (v0.14).
Meanwhile, I would like to use `kueue.x-k8s.io/trainjob-override-idx` or `alpha.kueue.x-k8s.io/trainjob-override-idx` annotation.
I'm leaning towards annotation with "alpha" prefix since it should be a temporary annotation.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-25T05:40:51Z

Regarding the alpha prefix I think there used to be this guidance in the past, but the API reviewers moved away from putting maturity level into the label or annotation name. I added the backOffLinitPerIndex feature which introduces annotation and I wasn't asked to add the prefix. Also I see other Alpha annotations in 1.34 not adding this https://kubernetes.io/docs/reference/labels-annotations-taints/?utm_source=chatgpt.com#applyset-kubernetes-io-additional-namespaces
so the maturity level is emphasized in the docs, but not in the annotation name.

I think if we just add to comment: This is alpha level annotation it should be enough. We could also call it deprecated already which maybe is better maturity level. I will open an issue in trainer.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-25T08:08:33Z

As part of this cleanup task we can unexport the const field

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-25T11:11:07Z

> Regarding the alpha prefix I think there used to be this guidance in the past, but the API reviewers moved away from putting maturity level into the label or annotation name. I added the backOffLinitPerIndex feature which introduces annotation and I wasn't asked to add the prefix. Also I see other Alpha annotations in 1.34 not adding this https://kubernetes.io/docs/reference/labels-annotations-taints/?utm_source=chatgpt.com#applyset-kubernetes-io-additional-namespaces so the maturity level is emphasized in the docs, but not in the annotation name.
> 
> I think if we just add to comment: This is alpha level annotation it should be enough. We could also call it deprecated already which maybe is better maturity level. I will open an issue in trainer.

That makes sense. In that case, let's use `kueue.x-k8s.io/trainjob-override-idx`.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-25T12:49:31Z

> > [@izturn](https://github.com/izturn) one more thought - can you check using "main" Kueue. I suspect that maybe there is a difference after we stopped injecting the "tas" label. Still, we will not support the "implicit" mode, but I suspect that "required" and "preferred" modes have a chance to work.
> 
> Sure, I can try again. But tbh, as a beginner, I don’t really understand what you mean by the “main” kueue things. I’m not sure how to do that. Could you walk me through it with a bit more detail? Thanks!


Sure, by "main" I meant the latest build of Kueue from the main branch. You can install for example following https://kueue.sigs.k8s.io/docs/installation/#install-the-latest-development-version


However, I think it will not work anyway on the second thought, because we would not be able to inject the "workload" annotation :/

### Comment by [@izturn](https://github.com/izturn) — 2025-09-26T01:49:11Z

> > > [@izturn](https://github.com/izturn) one more thought - can you check using "main" Kueue. I suspect that maybe there is a difference after we stopped injecting the "tas" label. Still, we will not support the "implicit" mode, but I suspect that "required" and "preferred" modes have a chance to work.
> > 
> > 
> > Sure, I can try again. But tbh, as a beginner, I don’t really understand what you mean by the “main” kueue things. I’m not sure how to do that. Could you walk me through it with a bit more detail? Thanks!
> 
> Sure, by "main" I meant the latest build of Kueue from the main branch. You can install for example following https://kueue.sigs.k8s.io/docs/installation/#install-the-latest-development-version
> 
> However, I think it will not work anyway on the second thought, because we would not be able to inject the "workload" annotation :/

Oh, got it. My reply above was actually based on testing with the main branch.

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-09-30T08:20:25Z

/reopen 

closed by mistake, `2` should still be addressed

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-30T08:20:31Z

@kaisoz: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6865#issuecomment-3350610114):

>/reopen 
>
>closed by mistake, `2` should still be addressed


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-30T09:42:07Z

@mimowo @kaisoz Additionally, I would request 2 things as I mentioned in https://github.com/kubernetes-sigs/kueue/pull/7030#pullrequestreview-3283582303.

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-09-30T10:52:21Z

> [@mimowo](https://github.com/mimowo) [@kaisoz](https://github.com/kaisoz) Additionally, I would request 2 things as I mentioned in [#7030 (review)](https://github.com/kubernetes-sigs/kueue/pull/7030#pullrequestreview-3283582303).

Hi @tenzen-y , just saw this, I'll take care of it 😊

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-30T10:56:06Z

> > [@mimowo](https://github.com/mimowo) [@kaisoz](https://github.com/kaisoz) Additionally, I would request 2 things as I mentioned in [#7030 (review)](https://github.com/kubernetes-sigs/kueue/pull/7030#pullrequestreview-3283582303).
> 
> Hi [@tenzen-y](https://github.com/tenzen-y) , just saw this, I'll take care of it 😊

Thank you!

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-30T15:00:25Z

x-ref: https://github.com/kubernetes-sigs/kueue/pull/7081#discussion_r2391731893

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-10-01T07:39:32Z

> x-ref: [#7081 (comment)](https://github.com/kubernetes-sigs/kueue/pull/7081#discussion_r2391731893)

PR ready @tenzen-y  https://github.com/kubernetes-sigs/kueue/pull/7110
Thanks!
