# Issue #5527: Update KEP-77 with details on batch/v1.Job support for horizontal scaling

**Summary**: Update KEP-77 with details on batch/v1.Job support for horizontal scaling

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5527

**Last updated**: 2025-07-31T16:21:07Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2025-06-05T22:55:19Z
- **Updated**: 2025-07-31T16:21:07Z
- **Closed**: 2025-07-31T16:21:06Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 36

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

The current version of [KEP-77 – Dynamically Sized Jobs](https://github.com/kubernetes-sigs/kueue/tree/main/keps/77-dynamically-sized-jobs) provides a high-level overview of the motivation and goals for supporting elastic workloads in Kueue but lacks sufficient detail in key implementation areas.

We propose updating the KEP to:

- Emphasize batch/v1.Job as the primary target for initial support of horizontal scaling via WorkloadSlices.
- Provide a more detailed explanation of how scaling is achieved using WorkloadSlices, including:
  - Slice creation, admission, and garbage collection.
  - Scheduling gates for controlling pod execution. 
  - Full-count slice representation instead of delta-based scaling.
  - Slice preemption and admission behavior.
- Clarify the phased rollout plan (single-cluster → multi-cluster).
- Improve consistency with the current controller implementation and inform follow-up design reviews.

**Why is this needed**:

This update will help align the KEP with recent development efforts and provide a clearer path for contributors and reviewers.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-06T09:47:56Z

Thank you @ichekrygin for taking the work on the issue. 

Following up on the discussion during wg-batch on June 5th, I think the major design decision is about the scale-up. 

The options I see:
1. the delta workload and merging (as proposed in the initial KEP)
2. the replacement workload which needs to preempt and preemption needs to be explicitly enabled
3. the replacement workload which always preempts the 'stem' workload, even if priority based preemption is disabled. It may or may not preempt other workloads.

Some exploratory questions to guide the design choice:
1. what are the main complications with (1.)? IIUC you decided on (2.) due to some complications. Choosing (2.) allowed to prototype the solution quickly, so I suppose the "replacement workload" has simplicity advantages, but it would be good to summarize them
2. would doing (3.) instead of (2.) increase the complexity significantly? I think it is conceptually cleaner, because in case of (2.) the preemption of the "stem" workload by the "replacement" workload isn't really priority-based. So, I think this is a new kind of "preemption" which does not need to be explicitly enabled. Conceptually slicing could work also when priority-based preemption is disabled (I think).

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-06-06T15:33:12Z

I'm currently working on the KEP-77 update PR, and this issue will serve as a tracker for that effort. We can use both this issue and the (upcoming) PR to discuss the content.

My plan is to use this issue to clarify some initial assumptions and address potential misconceptions, then incorporate those refinements into the PR, where we can proceed with a more thorough review.

Does that sound like a good approach?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-06T15:37:19Z

> I'm currently working on the KEP-77 update PR, and this issue will serve as a tracker for that effort. We can use both this issue and the (upcoming) PR to discuss the content.

awesome

> My plan is to use this issue to clarify some initial assumptions and address potential misconceptions

yes, there might have been some gaps in the initial "delta" proposal which make this really hard.

> Does that sound like a good approach?

sgtm

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-06-06T15:37:29Z

> 2\. the replacement workload which needs to preempt and preemption needs to be explicitly enabled

To follow up on the requirement for explicit preemption enablement—could you please point me to the specific feature or mechanism you're referring to?
I came across the MultiplePreemptions feature gate, but I'm not sure if that's the one you had in mind.

Update...

After reviewing the issue linked in the GoDoc for MultiplePreemptions, I don't believe this is the correct feature. It doesn’t appear to be a general preemption enablement mechanism, but rather addresses coordination of multiple workload preemptions—specifically in the context of admission decisions involving workloads from different ClusterQueues.

Does that interpretation align with your understanding?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-06T15:41:49Z

I assumed (without looking at your PR yet) only based on the wg-batch discussion, that you require preemption enabled at CQ-level, like [here](https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/#preemption), for example setting `preemption. withinClusterQueue: LowerPriority`, and setting higher priority for the replacement workload.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-06-06T16:26:09Z

I think I now understand what you meant by "explicitly enabled preemption."

In the context of Workload Slices, we do not rely on the ClusterQueue's preemption configuration (e.g., withinClusterQueue) to drive preemption decisions. Instead, the preemption target (i.e., the old workload slice) is explicitly added to the preempted workload list during scheduling, regardless of the final flavor assignment mode.

To clarify:

- The preemption of the old workload slice is not a result of the ClusterQueue's generatePreemptionTargets logic.
- The flavor assignment is computed using adjusted capacity requirements, taking into account that the old slice will be preempted and its resources reclaimed.

I've attempted to document this behavior in the implementation. Please take a look and let me know if the documentation is unclear or needs refinement.
Relevant code: [scheduler.go#L501](https://github.com/ichekrygin/kueue/blob/wl-slices/pkg/scheduler/scheduler.go#L501)

In summary, I don’t believe the current workload slice preemption implementation requires any additional, explicit ClusterQueue preemption enablement.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-06-06T18:10:56Z

> 2. the replacement workload which needs to preempt and preemption needs to be explicitly enabled
> 3. the replacement workload which always preempts the 'stem' workload, even if priority based preemption is disabled. It may or may not preempt other workloads.

I believe bullets 2 and 3 are closely related, in the sense that they do not require explicit preemption enablement via the Kueue `ClusterQueue` configuration (or any other setting).

To elaborate on how WorkloadSlice preemption works, here is a high-level decision tree describing how the scheduler handles flavor assignment and preemption:

1. The scheduler attempts to compute a flavor assignment mode for a given workload against a given `ClusterQueue` capacity.
  - In the context of workload slices, this flavor assignment is based on pod count only (ignoring other resources for simplicity in this discussion).
2. The result of this flavor assignment can be one of the following modes:
  - `"NoFit"`: the workload’s requirements exceed the available capacity.
  - `"Fit"`: the workload fits within the available capacity.
  - `"Preempt"`: the workload could fit if some existing workloads are preempted (evicted).

When computing the flavor assignment for a WorkloadSlice, the scheduler uses an adjusted pod count:
`adjusted_pods = new_slice.pods - old_slice.pods`.
This adjustment reflects that the old slice will be preempted as part of the scheduling process. Crucially, this preemption is guaranteed and happens independently of the ClusterQueue preemption mechanism.

Here is how the scheduler handles the different modes:

- "NoFit":
Even with the old slice preempted, the new slice still doesn't fit.
→ No scheduling action is taken; the new slice remains Pending.
- "Fit":
The new slice fits within the capacity after accounting for the old slice preemption.
→ The scheduler proceeds to admit the new slice.
- "Preempt":
The new slice fits only if additional workloads are preempted.
→ This relies on ClusterQueue-level preemption being enabled, and on the availability of suitable preemption targets.
If either is missing, the new slice stays Pending.

So, to summarize:
- The preemption of the old workload slice is mandatory and does not depend on the ClusterQueue’s preemption configuration.
- Preempting other workloads (in addition to the old slice) requires:
  - ClusterQueue-level preemption to be explicitly enabled, and
  - Suitable preemption targets to be available.
  - Failure to meet these requirements (due to disabled preemption or lack of targets) will result in the new workload slice not being admitted—this is handled by the current Kueue scheduler logic, and the workload remains in the Pending state.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-06-06T18:30:37Z

> 1. the delta workload and merging (as proposed in the initial KEP)

### New Workload Slice: Delta vs. Full
Key differences:

- **Delta**: The new workload slice contains the **additional** pod count required for a scale-up event (i.e., the difference from the current state).
- **Full**: The new workload slice contains the entire **desired** pod count after the scale-up.

After evaluating both options, my assessment is that the Full model offers significant advantages over Delta, for the following reasons:

- The _Full_ model follows a declarative pattern that aligns well with Kubernetes’ declarative API style. A close analogy is how a **new ReplicaSet** represents the full desired replica count, rather than a delta from previous ReplicaSets.
- As a result, the _Full_ model greatly simplifies the processing of the new workload slice. It limits changes to internal logic by reusing Kueue’s existing scaled placement primitives, specifically in the **adjusted flavor assignment** computation.
- In the _Full_ model, the preempted (old) workload slice is deactivated and marked as finished, and the new workload slice takes its place—**no additional cleanup or merging steps are required**.
- In contrast, the _Delta_ model introduces complexity: the new workload slice represents only a partial state, and would likely require a third transformation step to resolve the final state—e.g., `old + delta → final`.

Finally, if the end goal is to produce a final workload state that reflects the desired pod count, then both `old + delta → final` and `old → final` serve the same purpose. The distinction between them is effectively an implementation detail, and the Full model achieves this more cleanly.

I would love to hear your thoughts on this.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-09T08:56:04Z

> After evaluating both options, my assessment is that the Full model offers significant advantages over Delta, for the following reasons:

@ichekrygin thank you for the clear outline of the arguments. I think I agree with them. Especially I can see the complication with ensuring `old + delta → final` is "atomic".

That said, would you also like to think about using the ["second pass" of scheduler](https://github.com/kubernetes-sigs/kueue/blob/2b0c22bdeb9ea3d46842820f0d7b46be412a576e/pkg/workload/workload.go#L651C9-L669) for that? This is a new mechanism we now use for ProvisioningRequest+TAS, and node replacement for TAS, which conceptually fits very close to what we need here. 

IMO this would be an cleaner model as it would be scoped to a single Workload, which already owns the pods. 

For example we could have `status.scalingRequest`  inside the Workload, which would trigger the second pass of scheduler. As a result the new assignment would be built and replaced the old one. This was we can also guarantee the "replacement" workload is assigned to the same flavor, as we already have similar code for TAS: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/flavorassigner/flavorassigner.go#L426-L441.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-06-09T20:33:37Z

> would you also like to think about using the ["second pass" of scheduler](https://github.com/kubernetes-sigs/kueue/blob/2b0c22bdeb9ea3d46842820f0d7b46be412a576e/pkg/workload/workload.go#L651C9-L669)

Thanks for the follow-up, @mimowo — and good point about the second pass.

I’ve been looking at [KEP-2724](https://github.com/kubernetes-sigs/kueue/tree/2b0c22bdeb9ea3d46842820f0d7b46be412a576e/keps/2724-topology-aware-scheduling) as the main reference for **TAS**, and I think it’s useful to call out that while there are some surface-level similarities between **TAS** and **WorkloadSlices** (like how **TAS** uses pod scheduling gates for PodSet assignment), I see them addressing pretty different goals overall.

From the perspective of **WorkloadSlices**:

* **WorkloadSlices** apply to all workloads, regardless of whether **TAS** is enabled. That means users can scale up any workload (TAS or not), and the mechanism works the same. It’s really just a general way to express incremental resource needs when a workload scales up.
* Because of that, I’m not sure the "second pass" mechanism adds much value for **WorkloadSlices**. Once a slice is admitted, it typically doesn’t need to go through additional topology checks, unless the workload is TAS-enabled, in which case TAS already handles that logic.
* If we *did* try to tie WorkloadSlices into the second pass flow, we’d run into a few problems. One of the big ones is that a failed admission in the second pass could lead to full workload eviction. That seems less than ideal, especially if we’re just talking about a scale-up. In that case, we’d probably want to keep the original slice running and let the new one sit pending instead.
* There’s also a more nuanced TAS-specific case to consider: imagine a workload that gets admitted fine at first, but then a scale-up slice fails because of topology constraints. What should happen? Do we leave the new slice pending, or do we evict the whole workload? That kind of situation makes me think it’d be useful to let users explicitly define their preferred behavior when a scale-up slice can’t be scheduled.

So, in short: **TAS** "second pass" and **WorkloadSlices** are related in some ways, but I wouldn't say we would benefit from using "second pass" scheduling in **WorkloadSlices** per se. If anything, it probably makes sense to keep **WorkloadSlice** scheduling as close as possible to existing workload handling, regardless of whether **TAS** is in the picture.

Let me know if I’ve misunderstood the intent behind the "second pass" here, or if you see it solving something I’ve missed. Happy to keep the conversation going.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-10T06:55:21Z

Hi @ichekrygin thanks for the summary. Yes, currently "second pass" is only used for TAS, but I think conceptually it isn't really that coupled and we could say `TopologAwareScheduling=true || resizeRequest`. 

This is a new mechanism so I appreciate there might still be some bugs or gaps. For example, the deactivation after some limit of retries could be easily made dependent on the reason for triggering the second pass, so I'm not concerned here.

Let me ask some exploratory questions:
1. how do you make sure the resized PodSet of the replacement Workload has the same flavor assigned?
2. Do you allow that we would choose another flavor if the old one does not fit the resized workload?

The "second pass" respects the flavor choice. 

Another small benefit of the second pass, is that the "resizeRequest" would be inside the Workload.status, so the relaxation of validation might be conditional.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-06-10T17:15:42Z

Thanks for the clarification @mimowo.

> Yes, currently "second pass" is only used for TAS, but I think conceptually it isn't really that coupled and we could say `TopologAwareScheduling=true || resizeRequest`.

Let me try to recap the “second pass” scheduling mechanism—primarily to confirm my understanding:

1. **First pass (initial admission):** This is the standard workload admission step, as used in traditional "one-pass" scheduling. However, for certain workloads (e.g., those with topology constraints), this step alone may not be sufficient, since Kueue cannot guarantee that pod placement will respect the desired topology.
2. **Second pass:** To address this, Kueue introduces a second phase in which it waits for all pods in the admitted workload to be scheduled *and* to meet the placement constraints (e.g., those defined via TAS). This validation may take one or more iterations.
3. **Successful completion:** If all pods are scheduled within the placement constraints before a timeout or retry threshold, the workload is considered fully admitted, completing the scheduling process.
4. **Failure case:** If pod scheduling fails to satisfy the constraints within the threshold, the workload is considered to have failed scheduling and is evicted.

A key point here is that scheduling is performed at the granularity of the entire workload—i.e., it's all-or-nothing. A critical requirement for entering the "second pass" phase is that the workload has already passed the initial **admission step**, meaning the necessary capacity has been successfully reserved. The second pass is then focused on validating that pod placement satisfies any additional constraints, such as those specified by TAS.

Now, if I understand the direction of this conversation correctly, there's interest in potentially using the “second pass” mechanism to handle *scale-up* requests for already admitted workloads. That’s an interesting idea, though there are a few nuances worth highlighting.

First, while a workload may support `WorkloadSlice`, there’s no guarantee it will be scaled up during its lifetime. But assuming a scale-up *does* occur, the flow might look something like this:

1. A scale-up request is issued for a running workload. The implementation detail is still TBD, but let’s assume we have a mechanism (e.g., `status.conditions` or similar) to communicate the updated desired pod count.  (There may be some concerns around tracking updates—particularly scaling—through the status subresource of a single object, but we can address those separately.)
2. Although the workload is already admitted and running, it re-enters a scheduling state under "second pass" processing to request additional capacity.
3. The scheduler processes the updated workload as a **second pass**, treating the original admission and placement as the **first pass**. In this model, the newly requested capacity is evaluated within the context of an already running workload. The scheduler re-evaluates the workload with the updated pod count, effectively extending the scheduling process without resetting the original admission state.

The key distinction here is that in traditional TAS-style second-pass scheduling, the workload has already been fully admitted and the system is simply enforcing placement constraints. In contrast, for a `WorkloadSlice`-based scale-up, the additional portion of the workload has not yet been admitted—it is still in the process of requesting quota.

If we pursue this direction, we may need to broaden the conceptual and implementation boundaries of the “second pass” to cover workloads that are already running but seeking additional capacity. (Do not confuse this state with "partial admission" since this term already has a specific meaning in Kueue.) Clarifying these semantics will likely require adjustments to how we define admission state and second-pass behavior within Kueue.

If I understand the "second pass" scheduling concept correctly, it addresses a distinctly different problem. Specifically, the WorkloadSlice scale-up case involves a request for a new (additional) capacity, which falls squarely within the domain of the first pass—i.e., traditional Kueue scheduling. There’s a strong argument to be made for keeping the responsibilities of the two passes clearly separated: the first pass is responsible for obtaining and reserving capacity, while the second pass is responsible for validating additional scheduling constraints (such as placement, affinity, or topology). From this perspective, the WorkloadSlice scale-up does not fit into the “additional constraint” category handled by the second pass, but rather represents a new admission request that should go through the standard capacity reservation logic of the first pass.

Please let me know if I’ve correctly understood the concept of "second pass" scheduling, or if there are any issues or gaps in my reasoning.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-06-10T17:25:53Z

> 1. how do you make sure the resized PodSet of the replacement Workload has the same flavor assigned?

This is an excellent observation—thank you for calling it out.

The current `WorkloadSlice` implementation does **not** restrict replacement slices to use the same flavor as the original. In other words, the scheduler will assign *any available* flavor when admitting the replacement. As a result, a single workload may span multiple flavors, which could be problematic in some scenarios—or potentially beneficial in others.

This highlights the need for more refined control over flavor assignment in `WorkloadSlices`. One possible direction is to introduce a concept of **"flavor affinity"**, inspired by Kubernetes’ existing affinity conventions—e.g., `Preferred` vs. `Required`.

I consider this a valuable enhancement that could be addressed in a future phase. That said, please let me know if you view consistent flavor assignment as a **hard requirement**

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-10T17:29:44Z

Excellent summary, thank you for elaborating so precisely what alle the nuances. I'm convinced we are on the same page in terms of understanding the mechanics of second pass.

> In contrast, for a WorkloadSlice-based scale-up, the additional portion of the workload has not yet been admitted—it is still in the process of requesting quota.

Very good point indicating the conceptual difference - yes second pass so far does not request quota but only tweaks TAS assignment.

> If we pursue this direction, we may need to broaden the conceptual and implementation boundaries of the “second pass” to cover workloads that are already running but seeking additional capacity. 

Yes, I agree it could be confusing if we start to broaden the term second pass to all request more quota.

However, Im still not clear if there could exist a separate similar mechanism like 'resize pass' just so that we could operate within the realm of a single wlWrokload rather than two. What is simpler in this model is making sure everything is atomic.

To give you one more potential issue with two workloads:
- how do you transfer and sync the state of other status fields such as requeueState tracking the number of evictions due to WaitForPodsReady

Let me alsl return to the question about using the same or different flavor. When you scale a PodSet, do you enforce the same flavor, if so, how to achieve it.

I think the above two problems become easier ib the single Workload model, but I agree, at the expense of complicating scheduler to do the "resize pass".

EDIT: The 'second pass' is still very fresh and nothing is written in stone. if we introduce resize pass, then we could rename 'second pass' as 'tas pass', or 'post quota pass'.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-10T17:43:06Z

> I consider this a valuable enhancement that could be addressed in a future phase. That said, please let me know if you view consistent flavor assignment as a hard requirement

It is definetly not a hard requirement for the first iteration of the feature. This was more exploratory to see how hard / easy it is in both models of the separate WrokloadSlice vs. another resize pass. Since the information lives in a separate object it feels intrinsically more involving to add this enhancement.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-10T19:14:57Z

One more question /scenario regarding the different flavors handling. 

Say we have a Job using old flavor with quota 5cpu, then we resize to use additional 5cpu quota but from new flavor. Now a pod still running on the old flavor fails, so it is replaced, but will WorkloadSlice schedule it on the new flavor or the old flavor? On the new you don't have quota, but for the old I'm not sure how you would know to inject old selectors. 

It seems not an easy problem, I would expect resize either stays in the old flavor, or migrates fully to the new, rather than running partially in both.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-06-12T16:02:22Z

> It seems not an easy problem

Indeed, this is not an easy problem.

In my initial implementation of KEP-77, I did not consider overlapping resource flavors and (incorrectly) assumed that flavor definitions were mutually exclusive. Upon learning that flavors can in fact overlap, I expected Kueue would track their shared resource utilization accordingly. However, it appears that Kueue currently treats overlapping resource flavors as independent, non-overlapping capacities.

This creates a potential (or even actual) issue. For example, if two flavors are defined identically and fully overlap, Kueue will treat them as separate resources. As a result, it may admit workloads into both, effectively doubling the perceived available capacity. This could lead to overcommitment and workloads getting stuck in a `Pending` state once the real underlying capacity is exhausted.

This behavior is what prompted my recent question in Slack ([https://kubernetes.slack.com/archives/C032ZE66A2X/p1749595150273899](https://kubernetes.slack.com/archives/C032ZE66A2X/p1749595150273899)) regarding the relationship between ClusterQueue resource flavor quota tracking and Kubernetes’ native ResourceQuota.

As a Kueue user, I would expect to be able to define ClusterQueue quotas that prevent overprovisioning and ensure predictable scheduling behavior. However, with overlapping resource flavors, this appears to be unachievable in the current model, given the reasons outlined above.

---

With this understanding, I need to revise my implementation for assigning resource flavors to `WorkloadSlice`s. The current draft imposes no restrictions on flavor selection, which can lead to incorrect capacity accounting—particularly in the presence of overlapping resource flavors.

As a first step, a practical improvement would be to restrict `WorkloadSlice` admission to the flavor(s) already assigned to the original workload. That is, we continue admitting slices into the previously assigned flavor if capacity allows. If not, the slice remains in a `Pending` state due to lack of capacity.

If a user wants to scale up into a different flavor (e.g., if the current flavor is exhausted and new capacity is available elsewhere), they would need to delete and re-create the job to trigger a new scheduling decision that considers the updated flavor availability.

While this approach is admittedly sub-optimal in the broader scheme—especially in terms of user experience and flexibility—it may serve as a reasonable first step until Kueue gains support for more intelligent overlapping-flavor accounting and rebalancing.


Let me know if you want to make it more assertive, exploratory, or align it more tightly with SIG/WG discussions.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-12T16:08:14Z

> In my initial implementation of KEP-77, I did not consider overlapping resource flavors and (incorrectly) assumed that flavor definitions were mutually exclusive.

Actually, I didn't assume overlapping flavors. I think overlapping flavors is a corner case we don't need to take into account for now. Let's consider fully non-overlapping flavors for now.

So, let's say you have two flavors (non-overlapping):
1. reservation (5cpu)
2. on-demand (autoscaled) (10cpu)

Now, you have a workload running on reservation , 5 pods. Now you want to resize it to 10pods, so "on-demand" flavor is used in the replacement Workload. As long as we delete the Pods in the old flavor (reservation) I think this is fine.

If we don't delete the old pods running on the "reservation", then we would keep running Pods outside of our quota assignment. This is not very good, because it may block scheduling another workload which would get quota for reservation.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-06-12T16:13:56Z

>Now, you have a workload running on reservation , 5 pods. Now you want to resize it to 10pods, so "on-demand" flavor is used in the replacement Workload. As long as we delete the Pods in the old flavor (reservation) I think this is fine.
---
With the proposed restriction on flavor assignment for `WorkloadSlice`s—i.e., continuing to use the original flavor—the behavior would still be consistent with the current model. In this case, the new `WorkloadSlice` created during scale-up would simply remain in the `Pending` state if no additional capacity is available in the originally assigned flavor. It would not attempt to switch to another flavor, thereby avoiding issues with quota misaccounting.

As a possible enhancement, we could treat this situation as an eviction trigger. Specifically, if the scale-up cannot be accommodated in the original flavor, it may signal the need for a full workload restart (i.e., delete and recreate the workload) similar to how Kueue currently handles replacement workloads without slices. This would enable re-evaluation of flavor assignments from scratch, allowing the new pods to be scheduled on a different flavor with available capacity.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-06-12T16:16:16Z

> Actually, I didn't assume overlapping flavors

In my mind, I was treating "overlapping flavors" and a workload qualifying for multiple flavors as the same issue—but you're right, these are distinct cases.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-06-12T16:27:49Z

>If we don't delete the old pods running on the "reservation", then we would keep running Pods outside of our quota assignment. This is not very good, because it may block scheduling another workload which would get quota for reservation.

The key idea behind workload slices is to avoid interrupting workloads whenever possible. However, we're now identifying scenarios—such as resource flavor reassignment during scale-up—where such interruption may be unavoidable.

This issue becomes even more nuanced when dealing with multiple `PodSet`s assigned to different flavors. In such cases, some `PodSet`s may require flavor reassignment to accommodate scale-up, while others may not.

There seem to be two straightforward options for handling this:

* **Treat flavor reassignment as an evictable event**, following the current Kueue model for handling workload updates. This would allow the workload to be torn down and recreated with a new flavor assignment.

* **Disallow flavor reassignment altogether**, in which case the new `WorkloadSlice` would remain in a `Pending` state if the original flavor lacks capacity—similar to how Kueue currently handles out-of-capacity situations.

Selective pod migration between flavors is certainly a more advanced feature. Realistically, Kueue may not have enough contextual data or policy input to determine whether such disruption is desirable from the workload's perspective. If we decide to support this behavior, perhaps it could be governed by a user-specified policy—e.g., a `DisruptionDueToFlavorReassignment` flag—to explicitly allow or disallow flavor migration during scale-up.

What are your thoughts on this direction?

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-06-12T16:37:23Z

In my opinion, **disallowing flavor reassignment altogether** is the safest approach and aligns best with the "principle of least surprise." It ensures that a user's workload—or individual pods within it—will not be torn down and recreated in response to a scale-up event.

This behavior closely mirrors how `Deployment` scaling works in Kubernetes: new pods may fail to schedule due to insufficient capacity, but existing pods are not affected or deleted as a result. Maintaining this predictability in the face of scale-up makes the system easier to reason about and reduces the risk of unintended disruption.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-12T16:49:21Z

Thank you. We are on the same page. I think `Treat flavor reassignment as an evictable event` and `disallowing flavor reassignment altogether` are both sensible defaults for Alpha version of the feature. 

However, I'm just thinking it might be harder to achieve any of them in the WorkloadSlice approach, because then you need to do lookup between two workloads.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-12T16:50:50Z

Finally, there is multiKueue in the picture. I think the WorkloadSlice-based approach may be trickier to make work than the new `status,resizeRequest` field. Let me summarize the status of my considerations in a table.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-06-12T16:59:57Z

> However, I'm just thinking it might be harder to achieve any of them in the WorkloadSlice approach, because then you need to do lookup between two workloads.

It appears that we can retrieve the flavor assignment from the preemptable WorkloadSlice (via WorkloadInfo), as shown here:

![Image](https://github.com/user-attachments/assets/9053911c-596f-46ee-8218-f40c5c067cfd)

With that in mind, we could restrict all future flavor assignments to those already used by the existing workload. If there’s a mismatch, we could potentially treat it as an eviction trigger.

https://github.com/kubernetes-sigs/kueue/blob/489e0a6f15ee585ad74419362a465d432136283f/pkg/scheduler/scheduler.go#L504

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-06-12T17:04:30Z

> Finally, there is multiKueue in the picture. I think the WorkloadSlice-based approach may be trickier to make work than the new `status,resizeRequest` field. Let me summarize the status of my considerations in a table.

I completely agree—multiKueue introduces additional complexity to the WorkloadSlice model, particularly with the added dimension of maintaining consistent placement across remote clusters. Fortunately, this complexity is isolated to the multiKueue workload controller and does not propagate into the core workload scheduler logic.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-06-12T17:11:26Z

> the new `status,resizeRequest`

I believe I have a few clarification questions about this feature, but I’m hesitant to raise them here in order to keep the conversation focused on the topic of WorkloadSlice. 

Is there a separate GitHub issue/pr dedicated to `status,resizeRequest` ?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-12T17:12:45Z

> Is there a separate GitHub issue/pr dedicated to `status,resizeRequest` ?

No, we don't have it. It is just another technical means to achieve issue 77 I'm thinking about.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-06-12T17:15:23Z

Got it, thanks for clarifying.

It would be a good idea to capture this as a standalone issue and link it to KEP-77. That would help frame it either as an alternative approach or a potential prerequisite, depending on where consensus lands. Happy to help review or contribute once the issue is opened.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-12T17:19:47Z

Possibly, I can try to capture this in more details indeed. 

I know this is not formally written down. I could do that, but probably after June 22. So, here is for now just a quick snapshot of different considerations aspects I have:

Complexity & requirements:
| Feature support                          | WorkloadSlice | WorkloadResize | Needed for alpha                                   | Needed for beta |
| --------------------------------- | ------------- | -------------- | -------------------------------------------------- | --------------- |
| MultiKueue support                | medium        | easy           | No                                                 | no              |
| Enforcing resize within flavor    | medium        | easy           | No (but it will be tricky to recommend without it) | Yes             |
| Resizing multiple PodSets at once | high          | medium         |      No                                              |       No          |
| WaitForPodsRrady                  | medium        | for free       | No                                                 | No              |


| Other aspects                          | WorkloadSlice                                                                               | WorkloadResize |
| -------------------------------------- | ------------------------------------------------------------------------------------------- | -------------- |
| Validation                             | relaxed                                                                                     | can be strict  |
| Metrics interpretation                 | Misleading, e.g. Workloads count may show double. Preemption metrics might be confusing too | clear          |
| Complexity of state management changes | high                                                                                        | medium         |
| Complexity of scheduling changes       | medium                                                                                      | high           |
| Atomicity                              | No                                                                                          | Yes            |


So, in this picture, I don't see `WorkloadSlice` being blocked as Alpha solution, but I think there are a couple of serious problems to graduate it as long term solution. So, we could start with it, and either improve, or replace by "WorkloadResize" as the other idea matures.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-06-12T17:36:28Z

> I know this is not formally written down.

Yeah, it's a bit hard to comment meaningfully without a better understanding of what WorkloadResize actually is. Looking forward to the write-up with more details!

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-06-12T21:44:42Z

An early proof-of-concept demonstrating *"sticky"* resource flavor enforcement in action.

### Concept:

Once a workload is admitted using a specific resource flavor, it will retain (or "stick to") that flavor for all future scale-up events—even if this results in failure to admit due to insufficient capacity in that flavor. This enforcement occurs regardless of whether sufficient capacity exists in *other* flavors that could otherwise satisfy the request.

![Image](https://github.com/user-attachments/assets/f7fd0fad-42a6-4d77-b60f-7dc490ed52e8)

### In the screenshot above:

We observe a `ClusterQueue` with two defined resource flavors:

```yaml
- name: default-flavor
  resources:
  - name: cpu
    nominalQuota: 1
  - name: memory
    nominalQuota: 36Gi
- name: vanilla-flavor
  resources:
  - name: cpu
    nominalQuota: 1500m
  - name: memory
    nominalQuota: 36Gi
```

* An initial workload (`demo-slice`) was admitted with a request for 1 pod using `[cpu: 100m, memory: 200Mi]`, and was placed on the `default-flavor`.
* The job was then scaled to 11 pods, resulting in the creation of a new `WorkloadSlice`.
* This new slice failed to be admitted due to insufficient quota in the previously assigned flavor (`default-flavor`), despite the availability of sufficient capacity in the alternative `vanilla-flavor`.

### Admission failure condition:

```yaml
- lastTransitionTime: "2025-06-12T21:32:56Z"
  message: "couldn't assign flavors to pod set main: couldn't change flavor from: default-flavor to: vanilla-flavor, insufficient quota for cpu in flavor default-flavor, request > maximum capacity (1100m > 1)"
  observedGeneration: 1
  reason: Pending
  status: "False"
  type: QuotaReserved
```

### Key takeaway:

Even though `vanilla-flavor` has sufficient capacity to admit the scaled-up workload, admission fails due to the enforced flavor affinity. The workload is not allowed to switch from `default-flavor` to `vanilla-flavor`, illustrating the effect of sticky flavor assignment.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-22T17:09:35Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-22T17:09:41Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5527#issuecomment-3103920133):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-31T16:21:02Z

Closing as the implmentations and KEP has already been merged to main branch.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-31T16:21:07Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5527#issuecomment-3140569712):

>Closing as the implmentations and KEP has already been merged to main branch.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
