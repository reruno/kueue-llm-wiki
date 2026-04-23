# Issue #754: Add MaxWaitingTime in case of job starvation of lower priority

**Summary**: Add MaxWaitingTime in case of job starvation of lower priority

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/754

**Last updated**: 2024-04-06T10:21:02Z

---

## Metadata

- **State**: open
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2023-05-09T06:04:36Z
- **Updated**: 2024-04-06T10:21:02Z
- **Closed**: —
- **Labels**: `kind/feature`, `lifecycle/frozen`
- **Assignees**: _none_
- **Comments**: 31

## Description

<!-- Please only use this template for submitting enhancement requests -->

We enqueue the jobs via the priorities mainly, which will cause job starvation of lower priorities，we can provide a mechanism to avoid this.

**What would you like to be added**:

A new field MaxWaitingTime to avoid job starvation. 

**Why is this needed**:

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-09T12:26:49Z

what would happen when the workload hits the maxWaitingTime?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-05-09T14:05:50Z

It will be popped out for scheduling whatever the priority.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-09T15:04:05Z

You mean it will go to the head of the ClusterQueue?

It seems a bit aggressive. Another way this can be modeled is that the priority actually goes up.
Another important question is at which object this is controlled. Workload? ClusterQueue? global?

And how to prevent abuse?

### Comment by [@trasc](https://github.com/trasc) — 2023-05-10T10:00:58Z

Only moving the workload to the head of the queue will be pointless when preemption is enabled, it will just be evicted at the next scheduler cycle.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-10T11:26:24Z

> It seems a bit aggressive. Another way this can be modeled is that the priority actually goes up.

I like this.

> Another important question is at which object this is controlled. Workload? ClusterQueue? global?

Maybe, ClusterQueue?
If Workload controls this, it means batch users can modify this.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-05-10T11:51:05Z

> It seems a bit aggressive. 

Yes, a bit aggressive but straightforward if some workloads have the deadline to run. But I'm not quite sure about this, I think we can wait for more feedbacks from the community. 

> Another way this can be modeled is that the priority actually goes up.

But how much to go up each time?

> Another important question is at which object this is controlled. Workload? ClusterQueue? global?

localQueue or clusterQueue both make sense to me.

> And how to prevent abuse?

I think it's hard to answer, this is configurable but considering localQueue should be created by admin, we can be optimistic about this?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-05-10T11:52:49Z

> Only moving the workload to the head of the queue will be pointless when preemption is enabled, it will just be evicted at the next scheduler cycle.

~We're not talking about preemption, just in case low priority jobs are starved by continuous high priority jobs.~

If resources are insufficient, this is a problem.

### Comment by [@Gekko0114](https://github.com/Gekko0114) — 2023-06-07T14:20:00Z

Hi,
It looks interesting, can I work on this issue?
If it is ok, I will clarify how to implement it later.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-06-07T14:39:19Z

Yes, you can take it if you like, but we haven't reached an agreement about the implementation, like a maxWaitingTime, or increate the priority per scheduling cycle, or something else. And we should also consider the preemption.

### Comment by [@Gekko0114](https://github.com/Gekko0114) — 2023-06-07T14:41:15Z

Sure, thanks! I will read this thread in detail and clarify it.
If I get an agreement, I will assign it to me.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-07T16:33:55Z

I would also consider adding an interface somewhere that allows us to implement different policies for ordering/priorities.

If you have a concrete use case, that would help us understand what the API can look like.

### Comment by [@Gekko0114](https://github.com/Gekko0114) — 2023-06-12T14:57:21Z

Hi,

I did some research this weekend and summarized my proposal.
Could you take a look?

----------------------------------
I am considering adding the following fields to clusterQueue.spec:
labels: Users can change the priority of specific jobs by setting labels.
maxWaitingTime: Set maxWaitingTime for timeout.
strategy: Set the action for handling timeouts in `strategy` field. You can choose "First" or "Prioritize" options (it might be good for adding "custom" option and preparing interface for customizing logic by developers, but I don't consider it now.)
addingPriority: If the "Prioritize" is chosen, set addingPriority. This value is added to each job's priority when timeout happens.

Use cases:
scenarios like raising the priority only for prod jobs or executing recommendation batches within 3 hours etc

What do you think? As discussed, since it is set for clusterQueue, developers wouldn't abuse this.


```yaml
spec:
  timeoutStrategy:
      labels:
         environment: prod
         system: recommendation         
      maxWaitingTime: 1hour
      strategy: Prioritize
      addingPriority: 10  
```

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-13T16:52:13Z

Maybe we should consider adding a separate object `WorkloadPriorityClass`. Then workloads refer to a priority class that have a base priority and a "dynamicPolicy".

```yaml
  basePriority: 100
  dynamicPolicy:
    delay: 1h
    action: PriorityDelta
    value: 10
```

Open questions:
- what could another action be?
- how to keep record of the last time the priority was increased? Do we actually update the priority in the object or we just track in memory?

Definitely worth a KEP: https://github.com/kubernetes-sigs/kueue/tree/main/keps

### Comment by [@Gekko0114](https://github.com/Gekko0114) — 2023-06-14T13:35:19Z

Hi @alculquicondor,

Thanks for your response.

I have a question.
Why do you think it's better to add a separate object `WorkloadPriorityClass` rather than adding a new field to `clusterQueue`? Is it because it would be easier for batch users to manage priority by choosing a PriorityClass for each job?

> what could another action be?

I think we should consider implementing another action going to the head of the ClusterQueue if it times out, which was the initial idea @kerthcet mentioned.

> how to keep record of the last time the priority was increased? Do we actually update the priority in the object or we just track in memory?

I don't have a strong opinion on this, but I think it's better to update the priority in the object. If so, admins can easily change the priority manually.

> Definitely worth a KEP:

I agree. I will create it.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-14T13:58:52Z

> Why do you think it's better to add a separate object WorkloadPriorityClass rather than adding a new field to clusterQueue? Is it because it would be easier for batch users to manage priority by choosing a PriorityClass for each job?

Yes, I don't think it's realistic that all jobs in a ClusterQueue would have the same behavior.

> I think we should consider implementing another action going to the head of the ClusterQueue if it times out, which was the initial idea @kerthcet mentioned.

I'm not too sure. Because this workload could be immediately preempted in the next iteration. It's better if it's priority changes.

> I don't have a strong opinion on this, but I think it's better to update the priority in the object. If so, admins can easily change the priority manually.

Yes, but also to my point above about not being easily preempted.
Another thing to think about is how do we know when the priority was bumped for the last time. In memory is not enough, because the controller could be restarted.

Can you look around in other queueing systems  if they have dynamic priority and how it works?

### Comment by [@Gekko0114](https://github.com/Gekko0114) — 2023-06-14T14:15:01Z

Thanks for your explanation! @alculquicondor

> I'm not too sure. Because this workload could be immediately preempted in the next iteration. It's better if it's priority changes.
> Yes, but also to my point above about not being easily preempted.

I have one question about preemption.
If we update the priority in the object and a pod starts running, my understanding is that the pod would not be easily preempted since it would have a higher priority. Is that correct?

> Another thing to think about is how do we know when the priority was bumped for the last time. In memory is not enough, because the controller could be restarted.

I agree. It's important.

> Can you look around in other queueing systems if they have dynamic priority and how it works?

Sure. I will look around and rethink the design based on your explanation.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-14T14:17:47Z

> If we update the priority in the object and a pod starts running, my understanding is that the pod would not be easily preempted since it would have a higher priority. Is that correct?

Exactly. That's probably desired? Which means we should probably add a `maxPriority` field in the priorityClass.
So we have `base`, `step`, `delayForStep`, and `max` fields (exact names TBD).

### Comment by [@Gekko0114](https://github.com/Gekko0114) — 2023-06-14T14:23:48Z

Sounds good!

I wasn't quite clear on the intention behind `step` and `maxPriority`.

So, if I understand correctly, `base` represents the priority when the job is initially created, `delayForStep` indicates the time (e.g., 1 hour) to wait before changing the priority after a timeout.
`step` determines the adding priority to set when a timeout occurs, and `maxPriority` is the priority used to override and prevent preemption of actively running pods, is that correct?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-14T18:37:52Z

Almost there. So after 1h, we have `p = base + step`. What happens after 2h? My thinking is that `p = base + step * 2`. Then we need a `maxPriority`, as we don't want it to go to infinity. By default we can probably cap it at MAX_INT32.

### Comment by [@Gekko0114](https://github.com/Gekko0114) — 2023-06-15T13:00:07Z

I see. Thanks.

Then I will create KEP (and also investigate on other queue systems).
If there's anything else we should discuss, please leave comments.

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-11T13:28:21Z

I created a simplified version of this feature request #973

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-12-29T06:46:14Z

I think we can leverage the workload priority to mitigate this issue. The general idea would like when waiting time ends, we'll raise the workload priority to a higher value and job will enqueue. Next scheduling cycle, the job will not be preempted as designed.

cc @B1F030

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-02T15:16:52Z

More generally, we will be needing a policy for dynamic priority. Another use case that popped out is to decrease priority based on evictions https://github.com/kubernetes-sigs/kueue/pull/1311#issuecomment-1870531528

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-01-03T06:22:34Z

For this case, maybe we can be more straightforward here like: 
1. Set the maxWaitingTime in localQueue/clusterQueue/Job
2. When hit the deadline, raise the priority to the top of the queue

Intuitive and easy to control the job queueing.

### Comment by [@B1F030](https://github.com/B1F030) — 2024-01-03T09:09:59Z

Here I drawed a simple design of this mechanism:

![image](https://github.com/kubernetes-sigs/kueue/assets/77265354/785fcc09-22d3-4c3f-88c9-f9a1d06d758f)

The `prototype` represents that there is a `basePriority`, when this workload hits the `maxWaitingTime`, we just simply change its priority to `MAX_INT32`.

And based on the `prototype`, here I have another design:
First we use the workload's priority as `basePriority`, and after `delayTime`(for example, 30m), add its priority by `step`(100), then after another `delayForStep`(10m), add step again.
Until the workload hits the `maxWaitingTime`, its priority will be add up straight to the `maxPriority`(MAX_INT32).

But the second design may be a little complex, and I think we should not expose the `step` and `delayForStep` to user in alpha version. We can define it properly, provide a default policy, that will be easy to use.

What do you think?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-03T16:42:13Z

Let's take a step back... do you have a real requirement from an end-user that you can share? What is the behavior they expect, regardless of how the API looks like.

To me, the idea of a Job getting the highest priority after some timeout sounds odd. Is the job really the most important of all? Additionally, this implies that the job is potentially never going to be preempted. Is this acceptable? Have you looked into older systems for inspiration?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-01-04T08:29:28Z

The goal is to prevent job starvation, which is also part of fair-sharing, low priority job will pending in the queue forever if higher priority jobs enqueueing continuously. 

Volcano has similar design https://github.com/volcano-sh/volcano/blob/master/docs/design/sla-plugin.md, however, the mechanism is when hitting the max waiting time, it will admit the queue and try to reserve resources for it until ready. 

Some of our users are using Volcano, we hope to provide smooth migrations for them. At the least, I think this demand still sounds reasonable, hope I'm not the only one. But we can think more about the API design.

> this implies that the job is potentially never going to be preempted

This is tricky... but we're somehow a preemption based system. Seems no better ways, I mean this design https://github.com/kubernetes-sigs/kueue/issues/754#issuecomment-1874899525.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-01-04T08:32:00Z

> But the second design may be a little complex, and I think we should not expose the `step` and `delayForStep` to user in alpha version. We can define it properly, provide a default policy, that will be easy to use.
> 
> What do you think?

Complex + 1 .., let's discuss the rationality first.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-04-05T12:19:24Z

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

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-04-06T10:15:53Z

/lifecycle froze

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-04-06T10:21:00Z

/lifecycle frozen
