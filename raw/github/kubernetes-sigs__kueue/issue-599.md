# Issue #599: WaitForPodsReady: Requeue at the back of the queue after timeout

**Summary**: WaitForPodsReady: Requeue at the back of the queue after timeout

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/599

**Last updated**: 2023-10-13T10:16:47Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-02-27T16:27:17Z
- **Updated**: 2023-10-13T10:16:47Z
- **Closed**: 2023-04-27T14:54:19Z
- **Labels**: `kind/feature`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 22

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

When WaitForPodsReady is enabled, and a workload hits the timeout, it should go to the back of the queue, potentially using the sorting logic https://github.com/kubernetes-sigs/kueue/blob/b2a5e386d7e9c0e3346660dd01001734f631d7fd/pkg/scheduler/scheduler.go#L322

This can be implemented in different ways:
1.  Removing the Workload object at the time of eviction, so that the job controller creates a new Workload object that will have a new creationTimestamp. However, this requires #518.
2.  Add a field in the WorkloadStatus that stores the time when the Workload was preempted, then use in sorting.
3. Use the LastTransitionTimestamp of the Admitted condition for sorting. However, this requires #532 to be completed (I'm on it)
4. **[Chosen]** Add a new condition `Evicted` that records when the pod was evicted, use the timestamp for sorting. Also requires #532.

**Why is this needed**:

We currently just remove the Admission field from the Workload object, essentially putting the Workload at the head of the queue, to be scheduled right after the head that was waiting to be admitted.

This could lead to constant waiting in the queue if the workload happens to be to big to fit or simply badly configured with scheduling requirements that can't be satisfied.

Eventually, we could make the behavior configurable, but for now, it's more reasonable to put the workload that timed-out at the back of the queue.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-27T20:52:35Z

@ahg-g @mimowo @kerthcet for debate.

Option 3 could potentially be the cleanest option. But I'm not sure if we can distinguish between the first admission attempt and eviction.
Option 2 gives us more control.

### Comment by [@mimowo](https://github.com/mimowo) — 2023-02-28T07:35:05Z

I vote for Option 3 - reuse the `Admitted` condition, use its `Reason` to differentiate the different reasons  (preemption, pods ready timeout exceeded, or a new workload) for eviction.

Option 2 - a new field with just time of eviction may not be enough to differentiate reasons for it. Thus, it might be better to go straight for a new condition, such as `AdmissionCancelled` with `LastTransitionTime` and `Reason` for it. This would be essentially option 3, but with a new condition, which does not seem necessary.

Option 1 - I'm still not sure how we would differentiate the different reasons for the workload re-creation. Also, it involves unnecessary API requests.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-02-28T08:26:52Z

How you are going to re-queue at the back, are you going to change the lessFunc?

### Comment by [@mimowo](https://github.com/mimowo) — 2023-02-28T09:01:36Z

Yes, this will mean modifying the `byCreationTime` function (and rename it). Even currently the name is misleading as it also takes the priority into account. 

We will also probably want to modify the entry ordering in scheduler to break the tie between nominated queue heads: https://github.com/kubernetes-sigs/kueue/blob/b2a5e386d7e9c0e3346660dd01001734f631d7fd/pkg/scheduler/scheduler.go#L322.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-28T14:39:38Z

Let's keep in mind that we already have two cases of "removing admission":
- timeout from pods ready
- preemption

I don't think we should put the workloads at the back of the queue in the case of preemption, so we actually need to differentiate between the two scenarios.

We could use the reason of the `Admitted` condition. But I think it might not be appropriate, because the Admitted condition is also used to report why the workload is inadmissible on the next admission attempt.

We can't also reuse the `PodsReady` condition, because it doesn't transition at the time of eviction.

As a result, I like the idea of a new condition. Not sure if we should make it specific to PodsReady as `PodsReadyTimedOut` or something more generic like `Evicted` which can have two reasons: `Preemption` or `PodsReadyTimeout`.

### Comment by [@mimowo](https://github.com/mimowo) — 2023-02-28T14:47:20Z

> We could use the reason of the `Admitted` condition. But I think it might not be appropriate, because the Admitted condition is also used to report why the workload is inadmissible on the next admission attempt.

Good point, so in that cases we would lose track of the time of eviction.

> As a result, I like the idea of a new condition. Not sure if we should make it specific to PodsReady as `PodsReadyTimedOut` or something more generic like `Evicted` which can have two reasons: `Preemption` or `PodsReadyTimeout`.

I prefer something more generic so that it can be used for other eviction reasons too. `Evicted` sgtm.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2023-02-28T15:54:02Z

I think we should keep the workload object to preserve relevant timestamps, like creation timestamp; but also to stress that its life is associated with the job object.

I think it makes sense to go with option 3; why would option 2 give more control?

### Comment by [@ahg-g](https://github.com/ahg-g) — 2023-02-28T16:10:43Z

Sorry, the page was stale and I didn't see the latest comments on adding a new condition; I think that makes sense.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-28T16:31:39Z

Updated the description with concluded solution.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-03-01T04:56:07Z

> We can't also reuse the PodsReady condition, because it doesn't transition at the time of eviction.

I think we updated here https://github.com/kubernetes-sigs/kueue/blob/b2a5e386d7e9c0e3346660dd01001734f631d7fd/pkg/controller/core/workload_controller.go#L158-L161

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-01T13:30:28Z

Note that's the `Admitted` condition.

### Comment by [@trasc](https://github.com/trasc) — 2023-03-01T13:47:00Z

/assign

### Comment by [@mcariatm](https://github.com/mcariatm) — 2023-03-02T10:02:00Z


/assign

### Comment by [@trasc](https://github.com/trasc) — 2023-04-06T14:13:39Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-06T14:33:26Z

/unassign @mcariatm

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-12T20:52:18Z

@trasc is implementing the sorting based on the timestamp of the Evicted condition. Even though we are adding the condition for both PodsReadyTimeout and Preemption, the timestamp is being only used for sorting if it's PodsReadyTimeout.

I think this makes sense: if a job is preempted, it shouldn't be penalized and sent to the back of the queue, as opposed to a job that was never able to become ready.

Any concerns?

### Comment by [@ahg-g](https://github.com/ahg-g) — 2023-04-13T14:28:39Z

+1 from my end

### Comment by [@mimowo](https://github.com/mimowo) — 2023-04-13T14:34:56Z

sgtm

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-10-11T15:27:29Z

Revisit this issue, currently the queueing logic is 
```
func GetQueueOrderTimestamp(w *kueue.Workload) *metav1.Time {
	if c := apimeta.FindStatusCondition(w.Status.Conditions, kueue.WorkloadEvicted); c != nil && c.Status == metav1.ConditionTrue && c.Reason == kueue.WorkloadEvictedByPodsReadyTimeout {
		return &c.LastTransitionTime
	}
	return &w.CreationTimestamp
}
```

I have two questions for FIFO queue:
- Do you think we should consider the *PodsReadyTimeout* , or we should just consider the creation time
- Because we'll rebuild workloads sometimes, can we use the job creation time when ordering to enqueue, because recreated workload may queue in the end. If we can update the workload rather than rebuild, then the problem not exists.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-11T15:57:27Z

Maybe it can be a configuration.

Some users find it valuable to requeue at the back of the queue when NotReady, so that other jobs have the chance to run.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-10-12T03:17:29Z

Then they can choose the BestEffort queue, the FIFO should be strict.

### Comment by [@trasc](https://github.com/trasc) — 2023-10-13T10:16:46Z

> * Do you think we should consider the _PodsReadyTimeout_ , or we should just consider the creation time

I thing doing so it's very similar to not have PodsReady.

> * Because we'll rebuild workloads sometimes, can we use the job creation time when ordering to enqueue, because recreated workload may queue in the end. If we can update the workload rather than rebuild, then the problem not exists.

This could be tricky to do, the workload may or may not have a parent. 
Also if , as the owner of an old job that sits in a queue (lq1), you decide to change to another one (lq2), wil it be fair to go in front of workloads that are already in lq2?
