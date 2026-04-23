# Issue #6757: Gracefully handle Pods "stuck" terminating due to kubelet being down

**Summary**: Gracefully handle Pods "stuck" terminating due to kubelet being down

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6757

**Last updated**: 2025-11-21T08:16:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-09-08T15:03:37Z
- **Updated**: 2025-11-21T08:16:35Z
- **Closed**: 2025-11-21T08:16:35Z
- **Labels**: `kind/feature`
- **Assignees**: [@kshalot](https://github.com/kshalot)
- **Comments**: 30

## Description

**What would you like to be added**:

When Kubelet is down, then a terminating Pod is "stuck" in the Running (or Pending) phase forever.

I would like to have a small controller which could transition such Pods (on nodes which are NotReady) to Failed phase,  to unblock the quota.

I would consider the controller to be configured inside Kueue as 

```yaml
failureRecovery:
  podTerminationTimeout: 10min
```

Alternatively, the "recovery" controller could be adding the `node.kubernetes.io/out-of-service` taint to nodes in the NotReady state for a long time. This is enough as the built-in PodGC already would transition the Pod to Failed phase, see [here](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobframework/reconciler.go#L535-L545)

The API is inspired by the name mentioned here: https://github.com/kubernetes-sigs/jobset/issues/576

Arguably, the small controller could be:
1. a separate project (seems like overkill to have a new project for the small controller)
2. inside core k8s (probably ideal, but we need more effort to drive k8s core enhancements, also now is tricky to introduce for backwards compatibility)
3. per user basis (users repeatedly ask about it, so probably not ideal approach)
4. by k8s cloud provider (maybe, but Kueue is often used on prem)
4. Kueue (allows to develop it quickly and fix issues of our users quickly) 



**Why is this needed**:

The quota is considered in Kueue as locked as long as the workload IsActive, see [here](https://github.com/kubernetes-sigs/kueue/blob/307b5fc662827f5d18f3b710a5f724cd922cc600/pkg/controller/jobframework/reconciler.go#L535-L545).

On top of that, there might be other workloads waiting for the eviction of such a workload.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-08T15:03:51Z

cc @amy @gabesaba @tenzen-y

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-08T15:57:01Z

Actually, adding the OutOfService taint seems like already automatad by the https://github.com/medik8s/self-node-remediation project (option 1), see also [here](https://docs.redhat.com/en/documentation/workload_availability_for_red_hat_openshift/25.7/html/remediation_fencing_and_maintenance/self-node-remediation-operator-remediate-nodes#understanding-self-node-remediation-remediation-template-config_self-node-remediation-operator-remediate-nodes).

If someone could test / confirm this solution works we could recommend this to users of Kueue experiencing the issue (I think).

EDIT: OTOH, even if that project works, it makes sense to some users of Kueue to have a tiny recovery controller inside Kueue, because deploying another project means more cpu / mem, and operational costs. Also, some users would expect Kueue to be the main controllers for handling workloads. So, I'm still considering we could have a small version built-in.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-08T22:57:09Z

> When Kubelet is down, then a terminating Pod is "stuck" in the Running (or Pending) phase forever.

To clarify, by Pods stuck in “Terminating” I mean Pods that have been deleted, have a `metadata.deletionTimestamp` set, and whose `terminationGracePeriodSeconds` has already elapsed. Is that your understanding as well?

If so, Kubernetes’ [ResourceQuota evaluator excludes terminated Pods from usage accounting](https://github.com/kubernetes/kubernetes/blob/master/pkg/quota/v1/evaluator/core/pods.go#L489). Should Kueue mirror that by not counting capacity for Workloads whose Pods are terminal (`Succeeded`, `Failed`) or have a `deletionTimestamp` with an expired `terminationGracePeriodSeconds`, and by marking those Workloads as “Finished” and/or deleting them if needed?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-09T08:14:31Z

> To clarify, by Pods stuck in “Terminating” I mean Pods that have been deleted, have a metadata.deletionTimestamp set, and whose terminationGracePeriodSeconds has already elapsed. Is that your understanding as well?

I would say "for a prolonged amount of time", rather than strictly `terminationGracePeriodSeconds`, but yes this is the idea.

Maybe we could consider this direction, however:
1. In case of Kueue the quota is reserved at the workload level, not Pod. So, we should probably change "QuotaReserved" to false for such a workload, to avoid inconsistent "memory" and API state.
2. For large workloads, spanning thousands of Pods `terminationGracePeriodSeconds` will not be accurate, because the workload termination process may take longer due to various factors
3. it still keeps the cluster "unhealthy" - meaning new workloads may get admitted but cannot run as the quota no longer corresponds to available physical resources.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-09T18:27:54Z

> In Kueue, quota is reserved at the **Workload** level rather than at the **Pod** level.

For pod-based integrations, this should be semantically equivalent. Is that a correct understanding?

Also, to clarify, does the “pod stuck in Terminating” issue affect other Kueue integrations beyond pod-based ones (perhaps some more than others)?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-10T07:13:20Z

> For pod-based integrations, this should be semantically equivalent. Is that a correct understanding?

I don't think this is the same. For Pod integration termination of all Pods may take signifficantly longer that of a single Pods. Suppose you have a Workload with 10k Pods. Termination may take minutes longer that of individual Pod. So we would be releasing quota too early.

Maybe this approach could work if we introduce some configurable time buffer.

> Also, to clarify, does the “pod stuck in Terminating” issue affect other Kueue integrations beyond pod-based ones (perhaps some more than others)?

We also have reports of affecting JobSet integration (but I don't know exact details yet). 

The issue also exists for k8s batch Jobs when using `podReplacementPolicy: Failed`. In that case the replacement Pod will not be created at all, and as a consequence the entire Job is stuck. And this would not be fixed by releasing the quota itself.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-10T18:34:04Z

Are we currently introspecting actual Pod status in the context of Kueue Workloads?

I am not 💯  percent sure about pod-integration, but my understanding is that for higher-level integrations, for example, `batchv1/Job`, we do not. Instead, we assume the higher-level controller behaves correctly. For example, when a Job is suspended, we expect the Job controller to delete any Pods it owns as appropriate.

I want to tease out the common case here. Does it matter that it can take some time for Kubernetes to converge to the desired state? 

It would also help to frame a clear problem statement. For example, suppose deleted Pods are not garbage-collected promptly, or at all, due to an unhealthy kubelet or another issue. What is the observable impact on Kueue Workload?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-11T09:53:55Z

> Are we currently introspecting actual Pod status in the context of Kueue Workloads?
> I am not 💯 percent sure about pod-integration, but my understanding is that for higher-level integrations, for example, batchv1/Job, we do not. Instead, we assume the higher-level controller behaves correctly. For example, when a Job is suspended, we expect the Job controller to delete any Pods it owns as appropriate.

For all integrations we have the Workload status. IIRC only the Pod integration inspects the Pod statuses directly.

> It would also help to frame a clear problem statement. For example, suppose deleted Pods are not garbage-collected promptly, or at all, due to an unhealthy kubelet or another issue. What is the observable impact on Kueue Workload?

The impact may depend on the  specific integration. However, what is  essential is that the IsActive remains true. Because of that the  Workload  stays in the  QuotaReserved=True.

In particular, this happens for Jobs (or JobSet) integration when using podReplacementPolicy, is that the  replacement Pods are not created for the terminating Pods, and entire Job (or Jobset) is stuck,

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-11T13:00:08Z

Actually, I just have an idea for the users of Kueue to mitigate this problem already: use waitForPodsReady: recoveryTimeout. 

In that case, the "stuck" pod is terminating, so not considered "Ready". As a result the workload  will be requeued and scheduled on the  set of healthy nodes.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-12T08:14:55Z

I have opened the issue upstream: https://github.com/kubernetes/kubernetes/issues/134038.

However, as it may take a while there I'm happy to accept such an opt-in controller inside Kueue.

cc @tenzen-y @gabesaba

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-12T19:03:27Z

If I am not mistaken, the issue of pods stuck in a Terminating state only impacts pod-integration, and more specifically, pod-integration with pod-groups, not plain pods.

> **UPD:**
>
>> We also have reports that this may be affecting the JobSet integration (though I don't have exact details yet).
>
> After reviewing all frameworks, it appears that the **pod-integration** mentioned above is the **only** one directly relying on `pod.status.phase`.


This stems from the difference in interpretation of [IsActive() for pod-integration](https://github.com/kubernetes-sigs/kueue/blob/a56c8f1cdf5d7d28df42968f8909b63425711442/pkg/controller/jobs/pod/pod_controller.go#L393) when applied to pod-groups:
```golang
// IsActive returns true if there are any running pods.
func (p *Pod) IsActive() bool {
	for i := range p.list.Items { // <-- pod groups
		if p.list.Items[i].Status.Phase == corev1.PodRunning {
			return true
		}
	}
	return false // <-- plain pod
}
```
* Plain pods (and likely all higher-level Kueue frameworks) do not rely on checking pod.Status.Phase == Running.
* Pod-groups, however, do rely on this check, which makes them unique in this context.

Since [IsActive() is used by the generic job reconciler](https://github.com/kubernetes-sigs/kueue/blob/a56c8f1cdf5d7d28df42968f8909b63425711442/pkg/controller/jobframework/reconciler.go#L535) to handle evicted workloads, specifically to unset quota reservations and clear the admission status, as long as a single pod in the pod-group has phase: Running, the workload remains Admitted, potentially[likely] blocking scheduling of a preemptor workload.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-12T19:04:10Z

Per my comment in a https://github.com/kubernetes-sigs/kueue/issues/6757#issuecomment-3268285729, it appears we can "borrow" from the Kubernetes pod quota evaluator and consider implementing logic along the following lines:
```golang
// IsActive returns true if there are any running pods.
func (p *Pod) IsActive() bool {
	for i := range p.list.Items {
		pod := p.list.Items[I]

		// Pods that are not in the Running phase are never considered Active.
		if pod.Status.Phase != corev1.PodRunning {
			continue
		}

		// If a pod is stuck terminating (e.g., due to a lost node), we should avoid
		// charging quota for it, as doing so could block the user from scaling up
		// replacement pods.
		if pod.DeletionTimestamp != nil && pod.DeletionGracePeriodSeconds != nil {
			now := p.clock.Now()
			deletionTime := pod.DeletionTimestamp.Time
			gracePeriod := time.Duration(*pod.DeletionGracePeriodSeconds) * time.Second
			if now.After(deletionTime.Add(gracePeriod)) {
				continue
			}
		}

		// At this point, the pod is Running and not stuck terminating — count as active.
		return true
	}
	return false
}
```
WDYT?

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-12T19:09:12Z

> I have opened the issue upstream: [kubernetes/kubernetes#134038](https://github.com/kubernetes/kubernetes/issues/134038).

By mistake, I commented there first :/

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-16T07:55:39Z

> Per my comment in a https://github.com/kubernetes-sigs/kueue/issues/6757#issuecomment-3268285729, it appears we can "borrow" from the Kubernetes pod quota evaluator and consider implementing logic along the following lines:

I'm not sure about this. Releasing quota while Pods continue to run seems not a best practice. It would certainly need to be guarded by some API configuration. This can result for example, in autoscaled environments in over-provisioning of machines, and thus leaking costs. We had tickets in similar scenarios in the past. TBH, this behavior, without any guard looks more like a bug to me in ResourceQuota.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-16T08:02:09Z

> If I am not mistaken, the issue of pods stuck in a Terminating state only impacts pod-integration, and more specifically, pod-integration with pod-groups, not plain pods.

Considering "IsActive" currently, yes, but:
- ideally `IsActive()` for  Jobs and Jobset should ideally use `status.active + status.terminating`. Actually, we introduced in the k8s core `status.terminating` specifically for this use-case, for Kueue: https://github.com/kubernetes/enhancements/tree/master/keps/sig-apps/3939-allow-replacement-when-fully-terminated#tracking-the-terminating-pods. It reached GA in 1.34 in core. The work in Kueue is not planned yet, but this is the direction.
- the issue with "stuck" terminating Pods has ramifications in the Job and JobSet integrations beyond "IsActive":
  - This is the related JobSet issue where this phenomenon contributed to the issues: https://github.com/kubernetes-sigs/jobset/issues/1021
  - similarly we recently run into issues when users were using `podReplacementPolicy: Failed`, blocking re-creation of the Pod

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-16T16:00:30Z

I may not be fully understanding the use case here, so please feel free to correct me if I’m missing something.

From my current perspective, the issue seems to center around Pods getting stuck in the “terminating” state and potentially **blocking forward progress**. While I understand this can often occur in **capacity-constrained** clusters, I’d like to focus for now on the simpler case where there’s **sufficient capacity** to schedule new Pods.

My general view is that interpreting Pod status should ideally live **within**, or at least very close to, the controller that owns those Pods. In most cases, Kubernetes workload controllers seem to handle this pretty well. Similarly, I believe most of the Kueue-integrated controllers aren’t particularly affected by this problem.

The [[JobSet issue](https://github.com/kubernetes-sigs/jobset/issues/1021)](https://github.com/kubernetes-sigs/jobset/issues/1021) linked above describes behavior that aligns with how I think about this:

> I'd expect JobSet to filter out terminating leader Pods and wait until the new leader Pod with valid data is created.

One case where this might get tricky is with `pod-integration` and `pod-groups`, where Kueue effectively becomes the **de facto** Pod-managing controller. In those situations, it seems reasonable to expect that Kueue should be able to correctly interpret Pod state, including detecting when a Pod is “stuck”, so that forward progress isn’t unintentionally blocked.

Given that garbage collection of terminating Pods can take a bit of time, I think it’s fair to expect the owning controller, or in the case I mentioned earlier, the Pod quota controller, to account for that and avoid counting those Pods in a way that prevents further progress. That feels like a reasonable default behavior in most situations.

To be clear, I do recognize that there might be **valid scenarios** where we intentionally want to wait for terminating Pods to be fully cleaned up before proceeding. If so, it could be helpful to **explicitly call those out**, so we can better distinguish between the general case and the exceptions.

That said, my sense is that those blocking scenarios are probably **exceptions rather than the norm**. Especially in environments **without capacity pressure**, it seems a bit counterintuitive to delay progress, whether it’s a `Deployment` rollout or Kueue workload admission, just because some Pods are waiting to be garbage collected.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-16T16:07:38Z

If there is enough capacity to schedule without preemption then I don't think we have an issue for Pod integration. New pod workloads should be scheduled.

Actually, if there is enough capacity the only issue I know about is in the k8s Job when configured to use podReplacementPolicy: Failed. As mentioned this impacts then also JobSet.

Still, our users often want to squeeze max from their clusters and preemptions are common

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-16T17:11:59Z

> If there is enough capacity to schedule without preemption then I don't think we have an issue for Pod integration. New pod workloads should be scheduled.

I think I may not have stated my premise clearly. By “capacity constraint” I didn’t mean Kueue CQ/Cohort quota, but rather the overall compute capacity of the Kubernetes cluster. In other words, the cluster itself may have sufficient resources, but a given Kueue CQ/Cohort can still enforce a tighter quota (by configuration), requiring preemption before new workloads are admitted.
I’ve been calling this situation a Kubernetes cluster “capacity constraint” because it introduces interesting implications, especially when considering scenarios like “Unhealthy” nodes. For the purposes of this discussion though, I’d like to set those node-health implications aside and focus strictly on the quota vs. cluster-capacity aspect.


Per our working definition, a Pod “stuck” in terminating is one with:

* `deletionTimestamp` set and grace period expired, and
* `pod.Status.Phase == Running`.

Per [pod-integration with pod-groups](https://github.com/kubernetes-sigs/kueue/blob/a56c8f1cdf5d7d28df42968f8909b63425711442/pkg/controller/jobs/pod/pod_controller.go#L393):

```go
// IsActive returns true if there are any running pods.
func (p *Pod) IsActive() bool {
	for i := range p.list.Items { // <-- pod groups
		if p.list.Items[i].Status.Phase == corev1.PodRunning {
			return true
		}
	}
	return false // <-- plain pod
}
```

Given that, the pod-integration pod-group path will still treat such a Pod as `IsActive() == true`, which prevents forward progress even when there is ample capacity (in Kubernetes cluster).

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-16T18:31:52Z

> I think I may not have stated my premise clearly. By “capacity constraint” I didn’t mean Kueue CQ/Cohort quota, but rather the overall compute capacity of the Kubernetes cluster.

Ah, ok, thank you for explaining!

It also prompted to think me more, and now I also understand better your proposal in https://github.com/kubernetes-sigs/kueue/issues/6757#issuecomment-3286512076. 

I think I'm positive about fixing it this way for the PodGroups actually. Yes, it could mean that we are releasing quota while nodes remain busy, and Pods exist. However, this would actually make the code more consistent with the current implementation of Job integration, as you observed, for Jobs we rely on [`status.active`](https://github.com/kubernetes-sigs/kueue/blob/bbaa3eb3945a82cc72be6983ef7da7047d929f52/pkg/controller/jobs/job/job_controller.go#L157-L159) only which excludes terminating Pods. 

While this remains a long term aspiration to use `status.active + status.terminating` we could do that trick for now. Actually, for Jobs we release quota almost immediately (once all pods are terminating), even without waiting spec.terminatingGracePeriodSeconds, which is arguably even worse.

Let me know @amy if this would work for you as a quick fix (https://github.com/kubernetes-sigs/kueue/issues/6757#issuecomment-3286512076)?

### Comment by [@amy](https://github.com/amy) — 2025-09-16T19:52:59Z

Nice! Yeah I like this approach because it cuts lines cleaner between platform vs. Kueue like we were discussing in wg-batch meeting. (ie not needing to touch pod running/failed states and just handling it during scheduling internally to Kueue)

Thanks for all the thought folks, really appreciate it 🙏

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-17T06:58:01Z

One thing is that it will not solve the issue with Jobs stuck if they are using `podReplacementPolicy: Failed` (possibly other scenarios), but the priority of those might be lower, and solution different.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-03T12:00:03Z

Still, we have users who are hit by the "stuck" pods in case of using Jobs with `spec.podReplacementPolicy: Failed`. While there is an ongoing discussion upstream, even if we proceed it is unlikely to be in Beta earlier than 1.38 (a year from now).

So, I would like to move forward with the failure recovery controller inside Kueue. 

The early version of the controller could basically mark Pods as Finished after some default time buffer, say 1min from when the gracefulTermination period elapses.

I imagine eventually this will require API in the config to opt-in. I think for the early feedback it is ok to start enabling the controller with a feature gate. Still, it would be great to have a KEP.

cc @PBundyra @mwysokin @sanposhiho @amy

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-03T12:03:37Z

cc @tenzen-y

### Comment by [@kshalot](https://github.com/kshalot) — 2025-10-06T11:52:55Z

/assign

### Comment by [@kshalot](https://github.com/kshalot) — 2025-10-16T15:42:46Z

Here are the "low-hanging fruit" options I can see after playing with this locally:

1. Manage the [`node.kubernetes.io/out-of-service`](http://node.kubernetes.io/out-of-service%60) taint on nodes that are not ready for some time (something like a `notReadyNodeGracePeriod`).
    1. This is elegant, because it uses an [existing Kubernetes mechanism](https://github.com/kubernetes/kubernetes/blob/7104c1e426b92025aa25083edcd3dac128f3e206/pkg/controller/podgc/gc_controller.go#L157-L160) to the the actual cleanup.
    2. A significant drawback is that it can affect non-Kueue managed pods if they are assigned to the failed node. Since this is an opt-in configuration it might be something that the users are okay with in the end, but still I can imagine a setup where this would be undesireable.
2. Mark the pod as `Failed` if `gracefulTerminationPeriod` + a configurable `zombiePodTerminationPeriod` (working name) elapses and the pod is still running.
    1. We can target Kueue-managed pods.
    2. I'm not sure I'd set a default value for this `zombiePodTerminationPeriod` to make the behavior slightly more explicit to the user, i.e. force the user to consider their own scenario and set a value instead of risking a bad default.
3. Option 2 + immediately delete the Pod from `etcd` as well.
    1. This is how [`podgc` does it](https://github.com/kubernetes/kubernetes/blob/7104c1e426b92025aa25083edcd3dac128f3e206/pkg/controller/podgc/gc_controller.go#L341-L361), but I don't see a significant advantage here. This can be added later if needed.

I'm finishing a draft of a KEP that is leaning towards option 2, I also have a PoC implementation of that mechanism. But maybe there's some other thing I missed here.

cc @sanposhiho @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-16T15:51:19Z

> I'm finishing a draft of a KEP that is leaning towards option 2

Thanks, I'm also leaning for (2.) as the safer option, but we could consider API which allows to use (1.) as an optional strategy in the future.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-10-16T16:24:16Z

> 2. Mark the pod as `Failed` if `gracefulTerminationPeriod` + a configurable `zombiePodTerminationPeriod` (working name) elapses and the pod is still running.
> i. We can target Kueue-managed pods.
> II. I'm not sure I'd set a default value for this `zombiePodTerminationPeriod` to make the behavior slightly more explicit to the user, i.e. force the user to consider their own scenario and set a value instead of risking a bad default.

Marking a Pod as **Failed** by setting `status.phase: Failed` will not change behavior at the apiserver or kubelet. In other words, the Pod will stay stuck in **Terminating** and will not be garbage collected until it is either force-deleted, or the kubelet comes back and completes normal cleanup.

If that is the case, then the **Failed** phase is primarily useful to Kueue, because Kueue can release quota and proceed when a Pod is **Failed**, while it cannot make progress when Pods are stuck in **Terminating**.

Is that interpretation correct?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-16T16:33:51Z

For now we have solved the issue with releasing the quota in the context of PodGroups with your PR.

The remaining focus is on the scenario of using Job's `spec.podReplacementPolicy: Failed`. Currently such Jobs get stuck as the Job controller cannot create a replacement Pod. This would happen even if the quota is still held. See also here: https://github.com/kubernetes/kubernetes/issues/134038#issuecomment-3359896169

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-10-16T16:49:37Z

The key concern is that the **kubelet** is currently the *sole authority* for updating a Pod’s `status.phase` to either `Failed` or `Succeeded`.

While I understand that our scope focuses specifically on *deleted Pods*, I still believe a broader, Kubernetes-wide solution would be preferable.

In that context, I agree with Tim — *“The biggest issue is the ghost pod problem,”* and I don’t see how either of the proposed solutions (this discussion or [kubernetes-sigs/kueue#6757](https://github.com/kubernetes-sigs/kueue/issues/6757)) addresses that underlying issue.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-16T17:00:39Z

Sure, I'm aware of the risk, and an admin would need to be aware too, because this feature would be opt-in. 

> In that context, I agree with Tim — “The biggest issue is the ghost pod problem,” and I don’t see how either of the proposed solutions (this discussion or https://github.com/kubernetes-sigs/kueue/issues/6757) addresses that underlying issue.

This proposal doesn't solve the underlying problem for sure. Kueue doesn't have a tool to solve the underlying problem, and honestly there is only core k8s that could solve it with some sort of PowerOff for Node. 

This proposal just gives a tool for admins to solve the problem somehow in a pragmatic way without waking them up at night (again, on environments where the risk is minimal anyway).

Quoting on Tim from later that thread suggests me he would be ok with such an opt-in timeout: 
> For example, if a pod indicates "I am a friendly ghost", then controllers already have enough information (terminationGracePeriodSeconds). If a pod has been terminating for more than tGPS (or maybe 2x that) then you can pretend it is dead. This has to be totally opt-in.
> This is kind of what #134038 (comment) proposes but it could be on the Pod or the Job, IMO. Do we really need another timeout, or can we just derive that from tGPS?". 

Introducing it in Kueue rather than in the core k8s is just a way to "exercise" the approach in a project before proposing upstream. Also, maybe in the meanwhile upstream can solve it in the "proper" way.
