# Issue #2858: Document labels/annotations that Kueue use in well-known labels/annotations

**Summary**: Document labels/annotations that Kueue use in well-known labels/annotations

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2858

**Last updated**: 2024-10-08T16:26:47Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2024-08-19T17:07:04Z
- **Updated**: 2024-10-08T16:26:47Z
- **Closed**: 2024-10-03T08:17:21Z
- **Labels**: `kind/documentation`
- **Assignees**: _none_
- **Comments**: 21

## Description

It has came to my attention that kubernetes-sig related projects should publish their labels/annotations on the Kubernetes website.

We should document the labels/annotations that Kueue sets and publish them [here](https://kubernetes.io/docs/reference/labels-annotations-taints/).

This came up during a review of our blog post for JobSet (ref: https://github.com/kubernetes/website/issues/47373).

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-19T17:13:13Z

/kind documentation

### Comment by [@kannon92](https://github.com/kannon92) — 2024-08-19T17:16:04Z

TBH I wanted to help with this one but I can't find labels/annotations that Kueue actually uses. Is there a single location where we have this?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-11T16:01:45Z

> TBH I wanted to help with this one but I can't find labels/annotations that Kueue actually uses. Is there a single location where we have this?

Actually, we have some annotations and labels, but we did not summarize those. One things are here: https://github.com/kubernetes-sigs/kueue/blob/d4331979e09c7096f1f17426c9551476b3fe77fc/pkg/constants/constants.go

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-11T16:20:33Z

+1 on the summary / list of those.

> Actually, we have some annotations and labels, but we did not summarize those. One things are here: https://github.com/kubernetes-sigs/kueue/blob/d4331979e09c7096f1f17426c9551476b3fe77fc/pkg/constants/constants.go

This would be a good starting point. We may also add `provreq.kueue.x-k8s.io/maxRunDurationSeconds` which proves to be useful per https://github.com/kubernetes-sigs/kueue/issues/2802.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-27T12:42:57Z

@mimowo @tenzen-y I'm trying to summarize these, and here's what I've found:

**Labels:**

https://github.com/kubernetes-sigs/kueue/blob/d4331979e09c7096f1f17426c9551476b3fe77fc/pkg/constants/constants.go#L46-L47

https://github.com/kubernetes-sigs/kueue/blob/d4331979e09c7096f1f17426c9551476b3fe77fc/apis/kueue/v1alpha1/multikueue_types.go#L27-L29

https://github.com/kubernetes-sigs/kueue/blob/d4331979e09c7096f1f17426c9551476b3fe77fc/pkg/controller/constants/constants.go#L20-L21

https://github.com/kubernetes-sigs/kueue/blob/d4331979e09c7096f1f17426c9551476b3fe77fc/pkg/controller/constants/constants.go#L28-L29

https://github.com/kubernetes-sigs/kueue/blob/d4331979e09c7096f1f17426c9551476b3fe77fc/pkg/controller/constants/constants.go#L31-L33

https://github.com/kubernetes-sigs/kueue/blob/d4331979e09c7096f1f17426c9551476b3fe77fc/pkg/controller/constants/constants.go#L35-L38

https://github.com/kubernetes-sigs/kueue/blob/d4331979e09c7096f1f17426c9551476b3fe77fc/pkg/controller/jobs/pod/pod_webhook.go#L46

**Annotations:**

https://github.com/kubernetes-sigs/kueue/blob/d4331979e09c7096f1f17426c9551476b3fe77fc/pkg/controller/jobs/pod/pod_controller.go#L68

https://github.com/kubernetes-sigs/kueue/blob/d4331979e09c7096f1f17426c9551476b3fe77fc/pkg/controller/jobs/pod/pod_webhook.go#L47-L49

https://github.com/kubernetes-sigs/kueue/blob/d4331979e09c7096f1f17426c9551476b3fe77fc/pkg/controller/jobs/job/job_controller.go#L54-L56

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-30T11:23:57Z

@mbobrovskyi thanks for the summary. 

I think only a small subset of labels and annotations are well known here. Here is my thinking about them:

1. Important / well known:
- kueue.x-k8s.io/queue-name 

2. Relevant for some features:
- kueue.x-k8s.io/pod-group-total-count, kueue.x-k8s.io/pod-group-name (pod groups)
- kueue.x-k8s.io/job-min-parallelism (partial preemption, but is buggy in 0.8*)

3. Somewhat relevant for end-users for some less popular features or use-cases:
- kueue.x-k8s.io/prebuilt-workload-name (generic feature, but not used outside of MK yet)
- kueue.x-k8s.io/job-completions-equal-parallelism
- kueue.x-k8s.io/managed
- kueue.x-k8s.io/priority-class
- kueue.x-k8s.io/retriable-in-group

4. Not relevant for end users, unless for very niche use-cases (mostly debugging):
- kueue.x-k8s.io/is-group-workload
- kueue.x-k8s.io/multikueue-origin
- kueue.x-k8s.io/job-uid
- kueue.x-k8s.io/stopping
- kueue.x-k8s.io/role-hash

I think for upstream documentation starting with (1.) is enough. WDYT @tenzen-y @alculquicondor @kannon92 ?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-01T17:28:33Z

@mbobrovskyi Thanks for great summarization!

@mimowo I think that which labels should be included in the upstream docs depending on the k/k policy / criteria.
Do you know those?

Or, we may want to ask SIG Docs which labels should be included in the upstream docs based on your category.

### Comment by [@sftim](https://github.com/sftim) — 2024-10-01T22:16:29Z

> It has came to my attention that kubernetes-sig related projects should publish their labels/annotations on the Kubernetes website.

This isn't quite true. Instead, you can choose an option:
- don't use `k8s.io` or `kubernetes.io` (eg, Karpenter uses `karpenter.sh` for its vendor-neutral annotations)
- register the annotations / label that are in the kubernetes.io or k8s.io domains
- a mix of the above

See https://kubernetes.io/docs/reference/labels-annotations-taints/

### Comment by [@sftim](https://github.com/sftim) — 2024-10-01T22:19:02Z

You might like to register `kueue.kubernetes.io/queue-name` and support that **in addition to** `kueue.x-k8s.io/queue-name` - because `x-k8s.io` is kind of unofficial and for things less finished.

If you do, you can promote `kueue.kubernetes.io/queue-name` and tuck the legacy `kueue.x-k8s.io/queue-name` away in a footnote. Obviously it needs some care about how you roll that out, but it's feasible to do.

But that's entirely optional.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-10-01T22:22:29Z

We intentionally used `x-k8s.io` to match our API group. We would like to use `kubernetes.io` (or `k8s.io`) once we migrate the CRDs to the `k8s.io` domain as well.

This should probably happen when we target a `v1` API and a `v1.0` release.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-01T22:27:18Z

> We intentionally used `x-k8s.io` to match our API group. We would like to use `kubernetes.io` (or `k8s.io`) once we migrate the CRDs to the `k8s.io` domain as well.
> 
> This should probably happen when we target a `v1` API and a `v1.0` release.

Basically sgtm. The only unclear point is the meaning of the "v1" API. This just indicates graduating the API to GA in this repo, or promoting APIs to k/k. Maybe I guess that it means just GA graduation in this repo, though.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-01T22:28:31Z

Anyway, we can keep parking here without any actions now.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-10-01T22:42:43Z

It would be great to do both together. Although maybe it's even worth migrating to `k8s.io` as we migrate to v1beta2.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-01T22:55:55Z

> It would be great to do both together. Although maybe it's even worth migrating to `k8s.io` as we migrate to v1beta2.

That sounds a great idea. When we graduate APIs from Beta to GA, I wouldn't like to introduce new concepts including API domain.
Additionally, by supporting deprecating (x-k8s.io) and new domain (k8s.io) in the v1beta2 API, we can give users a reprieve for the domain switching.

If we can move any commonly conceptual API to k/k, it would be great. As far as I know, the gateway-api is progressing to contribute the ReferenceGrant API to k/k sig-auth.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-03T07:51:02Z

As summarized in my [comment](https://github.com/kubernetes-sigs/kueue/issues/2858#issuecomment-2382913510) there are big differences between the usage scope of labels, so I would like to have a strategy which allows us to promote only a selected subset of "well known" labels to the k/k documentation. The reason being that we have a bunch of very low-level labels which are just to control the mechanics within Kueue. So, I think documenting such labels in k/k, even if GA, will be polluting the k8s documentation as users are not supposed to interact with them directly.

I like as the idea in [comment](https://github.com/kubernetes-sigs/kueue/issues/2858#issuecomment-2387185418) to support `kueue.kubernetes.io/queue-name` along with `kueue.x-k8s.io/queue-name`. IIUC we could do this even with API v1beta2. WDYT @alculquicondor @tenzen-y ?

### Comment by [@sftim](https://github.com/sftim) — 2024-10-03T08:05:33Z

I think for now we can close this issue; there is nothing to do yet (ie `/close not-planned`)

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-03T08:17:16Z

/close 
For now, as there is no immediate action and we need to promote the labels (or a subset of them) first to the k8s domain. I added a point to https://github.com/kubernetes-sigs/kueue/issues/768 to revisit it then as a reminder.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-10-03T08:17:21Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2858#issuecomment-2390801763):

>/close 
>For now, as there is no immediate action and we need to promote the labels (or a subset of them) first to the k8s domain. I added a point to https://github.com/kubernetes-sigs/kueue/issues/768 to revisit it then as a reminder.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-08T15:57:00Z

> /close For now, as there is no immediate action and we need to promote the labels (or a subset of them) first to the k8s domain. I added a point to #768 to revisit it then as a reminder.

@mimowo Could we open an issue to add those labels to our documentation page (https://kueue.sigs.k8s.io/docs/)?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-08T16:04:29Z

Sure, it is fair to start with Kueue docs. Feel free to open one.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-08T16:26:46Z

> Sure, it is fair to start with Kueue docs. Feel free to open one.

Opened: https://github.com/kubernetes-sigs/kueue/issues/3198
