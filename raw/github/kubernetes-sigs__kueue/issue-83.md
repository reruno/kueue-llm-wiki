# Issue #83: Support for workload preemption

**Summary**: Support for workload preemption

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/83

**Last updated**: 2023-01-30T16:34:54Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-03-01T22:06:52Z
- **Updated**: 2023-01-30T16:34:54Z
- **Closed**: 2023-01-30T16:34:54Z
- **Labels**: `kind/feature`, `priority/important-longterm`, `lifecycle/frozen`, `kind/grand-feature`
- **Assignees**: _none_
- **Comments**: 23

## Description

Preemption can be useful to reclaim borrowed capacity, however the obvious tradeoff is interrupting workloads and potentially losing significant progress.

There are two high-level design decision we need to make and whether they should be tunable:
1. What triggers preemption? reclaiming borrowed capacity? workload priority?
2. What is the scope? is preemption is cohort knob? a capacity knob? a queue knob?

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-07-12T03:12:09Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues and PRs.

This bot triages issues and PRs according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue or PR as fresh with `/remove-lifecycle stale`
- Mark this issue or PR as rotten with `/lifecycle rotten`
- Close this issue or PR with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-07-12T13:14:00Z

/lifecycle frozen

### Comment by [@anirudhjayakumar](https://github.com/anirudhjayakumar) — 2022-08-22T18:16:15Z

I feel this is a very useful feature. On top of priority and reclaiming borrowed resources, this feature is useful to maintain fairness by assigning some notion of time slice to each workload. This way long running workloads will not block other workloads specially short-running ( in a namespace with tight resource quotas). 

With this approach, we don't need to think about preemption triggers. After the time-slice, a workload will be put back into the queue allowing for higher-priority jobs to be scheduled and borrowed resources to be reclaimed.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-08-22T19:44:43Z

@anirudhjayakumar are you thinking of max runtime per job that when reached, instead of declaring the job failed, we place it back into the queue?

### Comment by [@anirudhjayakumar](https://github.com/anirudhjayakumar) — 2022-08-22T19:54:40Z

Yes, that is correct.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-22T20:32:11Z

I would think of that as a separate feature from preemption. It's actually much easier to implement, as we don't have to decide which workloads should be suspended. We have all the information in the Workload object (start time and max runtime).

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-23T11:28:15Z

Time-slice RR will require us to switch between different workloads, considering the cost is really high, e.g. when we suspend a job, we'll delete all running pods, when we unsuspend the job, we'll create them again, so, I'm doubt about the earnings.

For preemption, we can consider this in two dimensions, one is preempt between workloads in the same queue, we have priority for each workloads now. Another one is preempt between shared clusterQueue, currently we can borrow resources from another clusterQueue when they're in a same cohort, but when the borrowed clusterQueue is insufficient of resources, we should reclaim the borrowed resources.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-23T13:28:32Z

@anirudhjayakumar can you open a separate issue for time-based suspension? I don't see any problem with the feature request. The user intent is clear: if a job doesn't finish within X time, suspend and requeue. I guess there could be an option for just terminate.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-23T15:13:56Z

I think there're two different understandings here around the time-slice:
1) Let's achieve the fairness between long running tasks and short running tasks, we may define a not too long and not too short timeout.
2) Hey, the task is running for quite a long time, let's stop it and leave the opportunity for other tasks, this is more like a "failover"

The good thing here is they are actually the same thing. Option2 seems better to me.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-23T16:05:20Z

I'm thinking more along the lines of 2. However, I would have it as a field in the Workload. And if an administrator wants to enforce a timeout for the cluster (or a namespace), they can add admission webhook. Or maybe we can justify adding the timeout in the LocalQueue or ClusterQueue. Although if we add it in ClusterQueue, I guess it's closer to option 1, and thus it's a form of preemption.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-23T16:06:01Z

@anirudhjayakumar maybe you can describe your use case a bit more, in the light of the suggestions above.

### Comment by [@anirudhjayakumar](https://github.com/anirudhjayakumar) — 2022-08-23T18:47:31Z

My specific use cases is of long running jobs hogging resources while other jobs (short and long) keep waiting. The problem is mostly around user experience, where the user see no progress of their jobs for long periods of time. This also prevent the system from providing any loose guarantees around job execution. Example: A job that creates daily report only needs 10 mins of execution time, but the job cannot be run in this setup because there is no guarantee that the job will complete one run each day. 

My solution to this problem is to allow each job to get a slice of the resources. For my use case, I feel it is okay for low_pri job keep waiting in presence of high_pri jobs. But I'm not sure if that is acceptable as a general rule. May be low_jobs will have a smaller time slice compared to high_pri jobs.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-23T19:03:53Z

1. Do you expect to pause the job just because it reaches the timeout? Or is a pre-requisite that there must be other jobs waiting.
2. It sounds like you don't want a global timeout. What do you think of adding the timeout as a parameter of the Workload (job)?

I see the appeal of having the timeout be defined by the priority, however I'm not sure where exactly we would add it. We could add it as an annotation to the [PriorityClass object](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/#priorityclass). Alternatives are adding it to the LocalQueue (@ahg-g has toyed with the idea of adding "priority" parameters here) or the ClusterQueue.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-08-23T19:03:54Z

@anirudhjayakumar the degree to which the approach you propose will work depends on the workload, specifically whether it can restart without loosing too much progress. If on each suspend/preemption it needs to start over, and it is a long running job, then the reward of suspending to give way for other jobs is not obvious.

### Comment by [@anirudhjayakumar](https://github.com/anirudhjayakumar) — 2022-08-24T03:22:33Z

> Do you expect to pause the job just because it reaches the timeout? Or is a pre-requisite that there must be other jobs waiting.

For my use case, job needs to suspend (and go back to the queue) only when there are other jobs waiting. But if that is not possible, I don't mind jobs put back into the queue once the timeout is reached. The assumption here is that, the system will soon figure out (in few seconds) that there is enough resources to run this suspended job that it resume execution of the job within a few seconds/minutes. 

>It sounds like you don't want a global timeout. What do you think of adding the timeout as a parameter of the Workload (job)?

A global timeout is nice but in the absence of it, I would end up setting a timeout on each workload/job that gets scheduled. 

>the degree to which the approach you propose will work depends on the workload, specifically whether it can restart without loosing too much progress.

I totally overlooked that. For my use case, we do checkpoint every few minutes, so progress is not lost. But I do understand that this may not be true for all batch use cases. But having said that, K8s could move pods between node due to various reasons. Shouldn't we assume that most workloads should have some mechanism to store intermediate state to make the job reliable.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-24T10:15:13Z

 > I see the appeal of having the timeout be defined by the priority, however I'm not sure where exactly we would add it. We could add it as an annotation to the [PriorityClass object](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/#priorityclass)

Couple priorityClass with timeout seems not a good idea to me, for different type of workloads may have different timeouts. If we define timeout in priorityClass, we have to apply multi priotyClasses, but as we known, this is usually privilege controlled by administrator.

Maybe define the timeout in localQueue is a good idea for localQueue is tenant isolated, and usually we submit the similar jobs to the same queue. 

ClusterQueue usually works for resource sharing, so we may submit different types of jobs to the same clusterQueue for fine-gained resource managements, so I think it's not a good choice.

If we want to gain more flexibilities, workload can also have a timeout but defaultly inherit from localQueue.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-24T10:45:40Z

> My solution to this problem is to allow each job to get a slice of the resources. 

This makes me think of DRF, it is also a common strategy. Maybe we can add this as another choice in https://github.com/kubernetes-sigs/kueue/issues/312.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-24T13:40:46Z

I agree that adding the timeout to the localQueue seems like a good idea. We should copy the value into the Workload like we do for priority.

This seems like a very explicit way of doing preemption (only preempt if certain conditions are true). This is good to avoid surprises, but we probably need other rules for preemption. Otherwise there could be cases where jobs with higher priority need to run, but no jobs are past the deadline.

### Comment by [@kumariitr](https://github.com/kumariitr) — 2022-08-24T14:53:20Z

Few points:
What do we want to preempt ? Pod , Workload?

Why do we want to preempt ?
1. A job is running in borrowed capacity and original owner of that capacity wants to reclaim
2. A job with low priority is running in its own capacity quota and other higher priority job in the same capacity quota needs to be scheduled
3. A job with low priority is running in its own capacity quota but other higher priority job of different capacity quota needs to be scheduled by borrowing the first job's capacity by preempting it (maybe less useful case)
4. A high priority job is running for too long and needs to be preempted for other equal or low priority jobs.

How do we want to preempt ?
1. Fully preempt one job vs partially preempt the pods of multiple jobs ?
2. Keep track of preempted jobs / pods and reschedule these later or leave it to the applications to handle the rescheduling part ?

Also, what about workloads / jobs which have dynamic resource allocation ?

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-11-30T17:11:31Z

One thing we should potentially add to the current proposal is cooperative preemption. If the workload does checkpointing, then we can assume they are able to communicate the latest checkpoint via a status condition. We can take that into account when selecting victims and prioritize ones that checkpointed lately.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-11-30T17:43:23Z

I think we can treat that as a separate requirement. Do you mind creating a new issue?

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-11-30T21:36:41Z

I mean it is not separate from workload preemption, I feel we can append the KEP to take this into consideration?  or you prefer we do it as a followup?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-12-01T13:26:43Z

I can use the same KEP, to save some process. But I'll do so after I finish implementing the design we already have.
