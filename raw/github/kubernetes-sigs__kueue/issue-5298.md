# Issue #5298: Remove the finalizers (kueue.x-k8s.io/managed) from the Pod.

**Summary**: Remove the finalizers (kueue.x-k8s.io/managed) from the Pod.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5298

**Last updated**: 2026-01-16T03:40:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@zhifei92](https://github.com/zhifei92)
- **Created**: 2025-05-20T14:04:46Z
- **Updated**: 2026-01-16T03:40:58Z
- **Closed**: 2026-01-13T15:07:39Z
- **Labels**: `priority/important-soon`, `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 15

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
I noticed that the Pods created by Deployment and StatefulSet are being injected with finalizers (kueue.x-k8s.io/managed). However, this finalizer doesn't seem to have any actual effect. From what I understand by looking at the code, its original intent was to prevent successfully completed Pods from being accidentally deleted, which could interfere with correctly tracking whether a job has finished.

However, Pods belonging to Deployments and StatefulSets will never stay in a Completed state, because their `restartPolicy` can only be set to `Always`. Therefore, this finalizer is unnecessary for such workloads.
**Why is this needed**:

Since the finalizer doesn't serve any actual purpose, we should clean it up. It brings significant overhead and confusion for both users and code maintainers.

## Discussion

### Comment by [@zhifei92](https://github.com/zhifei92) — 2025-05-20T14:06:14Z

If I understand correctly, I would be very willing to work on this.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-20T14:09:46Z

@zhifei92 thank you for opening the issue, I think the same case is for LWS.

This would improve performance also as we wouldn't need to send many patches to remove them. This would be particularly useful improvement for LWS which is used at scale.

cc @PBundyra

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-20T14:10:25Z

cc @mbobrovskyi who might have some extra insights about the finalizers

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-20T14:11:17Z

in short, I don't see why they were introduced for the APIs, I would assume for simplicity as they were all based on Pod integration which is using finalizers by default.

### Comment by [@zhifei92](https://github.com/zhifei92) — 2025-05-21T02:05:33Z

> I think the same case is for LWS.

Yes, that's correct.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-19T03:04:53Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-19T18:54:04Z

/remove-lifecycle stale

### Comment by [@munali](https://github.com/munali) — 2025-09-03T19:36:26Z

The pod finalizer is causing issues in our use case where we are scheduling pods for Spark Application.

We have a pod group representing the job with a driver pod that dynamically launches worker pods. Worker pods are created, run to completion, and deleted by the driver. While active workers never exceed a configured max at once, over the job lifetime, many more workers may be created.

We set the pod-group-total-count annotation to max workers + 1 for the driver and use kueue.x-k8s.io/pod-group-serving to mark it as a serving workload. This prevents the ReclaimablePods tracking since workers can be replaced dynamically, per the [Serving Workload model](https://github.com/kubernetes-sigs/kueue/tree/main/keps/976-plain-pods#serving-workload).

However, completed pods with deletion timestamps are not finalized, so the pod controller keeps tracking them and labels replacement worker pods as "Excess," deleting them automatically.

Proposal: Kueue's [pod-webhook](https://github.com/kubernetes-sigs/kueue/blob/06cb5118a7a155c96cf358358d676fdccc7de19a/pkg/controller/jobs/pod/pod_webhook.go#L191) should skip adding the pod finalizer for pods with the pod-group-serving annotation, or alternatively provide an annotation to opt out of the finalizer.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-17T21:47:05Z

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-18T05:41:02Z

/remove-lifecycle stale

### Comment by [@zhifei92](https://github.com/zhifei92) — 2025-12-26T06:33:37Z

Is there any update on this issue?

In the `isGroup` scenario, if a Pod within a PodGroup is deleted—whether manually by a user or automatically by `kube-controller-manager` due to its Node becoming abnormal—the Pod’s finalizer cannot be removed, regardless of whether the PodGroup contains one Pod or multiple Pods.

I understand that the original design intention was to ensure state consistency: the Workload represents the status of the entire PodGroup, and the Job should only be considered complete when the entire group no longer exists. This was done to prevent state inconsistency caused by partial Pod deletions.

However, the current user experience is very poor—especially in cases where Pods are evicted due to underlying resource failures. Users find it unacceptable that these Pods cannot be deleted.

https://github.com/kubernetes-sigs/kueue/blob/ae75bac9048c9c6dd30c1536b3b39527f92045c1/pkg/controller/jobs/pod/pod_controller.go#L658-L666

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-09T14:47:43Z

No update yet, I also opened the issue for LWS and StatefulSet: https://github.com/kubernetes-sigs/kueue/issues/8497 and https://github.com/kubernetes-sigs/kueue/issues/8276

They don't yet have assigninees so you are free to grab them. 

Since the finalizers were with us for long I think for safety it is better to update the code under the feature gate like "SkipPodGroupFinalizersForOwnedPods", or maybe a better name you can think of. We can backport the fix along with the scheduling gate then.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-09T14:48:33Z

cc @munali @zhifei92

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-09T14:49:27Z

/priority important-soon

### Comment by [@zhifei92](https://github.com/zhifei92) — 2026-01-16T03:40:58Z

> No update yet, I also opened the issue for LWS and StatefulSet: [#8497](https://github.com/kubernetes-sigs/kueue/issues/8497) and [#8276](https://github.com/kubernetes-sigs/kueue/issues/8276)
> 
> They don't yet have assigninees so you are free to grab them.
> 
> Since the finalizers were with us for long I think for safety it is better to update the code under the feature gate like "SkipPodGroupFinalizersForOwnedPods", or maybe a better name you can think of. We can backport the fix along with the scheduling gate then.

@mimowo Sorry for the delay!  I'm willing to contribute to Kueue. Please feel free to assign me tasks if there are any further needs. Thank you!"
