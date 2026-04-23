# Issue #8: Efficient re-queueing of unschedulable workloads

**Summary**: Efficient re-queueing of unschedulable workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8

**Last updated**: 2022-04-12T17:15:42Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-02-17T22:15:01Z
- **Updated**: 2022-04-12T17:15:42Z
- **Closed**: 2022-04-12T17:15:42Z
- **Labels**: `kind/feature`, `size/XL`, `priority/critical-urgent`
- **Assignees**: [@denkensk](https://github.com/denkensk)
- **Comments**: 25

## Description

Currently we relentlessly keep trying to schedule jobs. 

We need to do something similar to what we did in the scheduler: re-queue based on capacity/workload/queue events.

/kind feature

## Discussion

### Comment by [@denkensk](https://github.com/denkensk) — 2022-02-21T13:08:56Z

/assign
List the parts that may need to be developed:
1.  Add UnschedulableQ to store the schedule failed workload.
2. Support re-queue by capacity update (includes the capacities in the same Cohort) 
3. Support re-queue by workload update/delete (in the same Cohort). Conditional judgment is required
4. Support re-queue by queue events? Maybe other queues is deleted?
5. Backoff Mechanism is needed.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-02-21T16:34:10Z

good initial list, but can we focus on the important-soon ones first? they are relatively simple enhancements with big impact: https://github.com/kubernetes-sigs/kueue/issues?q=is%3Aissue+is%3Aopen+label%3Apriority%2Fimportant-soon

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-02-22T14:19:14Z

Actually this is important to prevent starvation. A short term fix is to re-queue based on last scheduling attempt just to make the system usable, but we should start working on event-based re-queueing now.

I think the solution should ideally avoid time-based backoff, a workload should not be re-tried at all unless there was an event that could potentially make it schedulable.

### Comment by [@denkensk](https://github.com/denkensk) — 2022-02-22T14:22:36Z

put the comments from @ahg-g  here https://github.com/kubernetes-sigs/kueue/pull/46#discussion_r811980213

### Comment by [@denkensk](https://github.com/denkensk) — 2022-02-22T14:35:45Z

I think that in order to avoid blocking the development of other features, we can choose the simple fix as you said: use the last scheduling attempt timestamp to sort the workloads in the queue firstly.

Then I will start working on adding the event driven for re-queueing for now. But it's not enough. Starvation may be divided into different situations: like older block the new one(something we can solve it by backoff) and some small jobs block a large one(A more specific design is needed here).

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-02-22T14:37:36Z

ok, can you start a doc discussing the possible scenarios of starvation so we can evaluate possible solutions?

### Comment by [@denkensk](https://github.com/denkensk) — 2022-02-22T14:40:22Z

> ok, can you start a doc discussing the possible scenarios of starvation so we can evaluate possible solutions?

Okay, I will draft a doc for discussion.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-22T16:20:36Z

> use the last scheduling attempt timestamp to sort the workloads in the queue firstly.

I think this should be an option. There are users of kube-scheduler that wanted **strict** FIFO guarantees. https://github.com/kubernetes/kubernetes/issues/83834

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-02-22T20:50:25Z

Strict FIFO as in: even if the next job is schedulable, it shouldn't be assigned until the head is?

Another temporary solution is to take a snapshot of the queues, continue to process them as long as the capacity snapshot didn't change (need a generation id to track that). This will force FIFO as long as the jobs are schedulable.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-22T21:16:18Z

> Strict FIFO as in: even if the next job is schedulable, it shouldn't be assigned until the head is?

Correct, because the old job could be starved by a constant influx of small jobs.

> Another temporary solution is to take a snapshot of the queues, continue to process them as long as the capacity snapshot didn't change (need a generation id to track that).

Not sure if I understand. We continue to process them today and that wouldn't change if we place add an "unschedulable" staging area.

However, I think we need to distinguish between 2 types of requeues, given the current algorithm:
- A workload that didn't fit should go through the unschedulable queue.
- A workload that could have fit but we didn't assign because other queues where pointing to the same capacity or cohort should go back directly to the queue.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-02-22T22:00:48Z

> Correct, because the old job could be starved by a constant influx of small jobs.

That would also lead to starvation of smaller jobs by larger jobs as you can see [here](https://github.com/kubernetes-sigs/kueue/pull/46#discussion_r811980213). 

> Not sure if I understand. We continue to process them today and that wouldn't change if we place add an "unschedulable" staging area.

We currently re-queue in the same queue that we continue to process, so we are indefinitely processing the same head, so the next job never gets a scheduling attempt. The queue sanpshot wouldn't include the re-queue of the unschedulable job; so as long as nothing has changed in the capacity snapshot (meaning no new capacity added or a job deleted), we continue to process the jobs from the last queue snapshot until done, then we snapshot again.

I am looking to explore a quick fixes that strike a reasonable balance and makes the current system a little more usable until we flush out a comprehensive re-queueing solution. In the taints integration test for example, a job is completely blocking another that could schedule using capacity not usable by the first.

> However, I think we need to distinguish between 2 types of requeues, given the current algorithm:
> 
> * A workload that didn't fit should go through the unschedulable queue.
> * A workload that could have fit but we didn't assign because other queues where pointing to the same capacity or cohort should go back directly to the queue.

Right, the latter is a detail of the current implementation that is ideally something users shouldn't care about or tune and should just be handled in a way aligned with the general semantics of queueing promised to the user. We are discussing the re-queueing semantics of a completely unschedulable job.

### Comment by [@denkensk](https://github.com/denkensk) — 2022-02-23T10:49:16Z

> I think this should be an option. There are users of kube-scheduler that wanted strict FIFO guarantees. https://github.com/kubernetes/kubernetes/issues/83834

Strict FIFO guarantees make sense when all jobs are requesting the same kind of resources with constrains. If we let new and small job scheduled successfully, it may lead to old and big job starvation.  But if things get a little more complicated like the old one requests gpu card and the new one only requests cpu. The new job won't influence the schedule of old one. This leads to a waste of cpu resources in the cluster if the new one is schedulable and can't be scheduled because of it's not the head. This is very similar to the problem we are facing in #46  Strict FIFO is guaranteed at the expense of cluster resource utilization.

> Another temporary solution is to take a snapshot of the queues, continue to process them as long as the capacity snapshot didn't change (need a generation id to track that). This will force FIFO as long as the jobs are schedulable.

> We currently re-queue in the same queue that we continue to process, so we are indefinitely processing the same head, so the next job never gets a scheduling attempt. The queue sanpshot wouldn't include the re-queue of the unschedulable job; so as long as nothing has changed in the capacity snapshot (meaning no new capacity added or a job deleted), we continue to process the jobs from the last queue snapshot until done, then we snapshot again.

This is probably the same idea as adding unscheduleQ. We don't include the re-queue of the unschedulable job in sanpshot. It it like we put them in unscheduleQ.  And after new capacity added or a job deleted, we snapshot it again. It is like moving all unschedulable jobs which belongs to the same Cohort to the activeQ. I simulated the implementation and felt that using snapshot might be more complicated or worse performance because we at leaset need the deepcopy for the current queue and a version id to track the snapshot.

The easiest and fastest fix I can think of is the one mentioned by Abdullah at the beginning: use the last scheduling attempt timestamp to sort the workloads in the queue as in the default-scheduler. This one at least doesn't make people feel weird

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-23T14:57:18Z

> That would also lead to starvation of smaller jobs by larger jobs

That's working as intended, if the user wants it. I think we should at least allow strict FIFO at the queue level.

> But if things get a little more complicated like the old one requests gpu card and the new one only requests cpu.

Maybe you should use a different queue for GPUs?

> The easiest and fastest fix I can think of is the one mentioned by Abdullah at the beginning: use the last scheduling attempt timestamp to sort the workloads in the queue as in the default-scheduler. This one at least doesn't make people feel weird

It does https://github.com/kubernetes/kubernetes/issues/83834

But I'm fine with it as long as it's an option.
The next step would be to add the unschedulableQ and add elements back to regular queues based on events. Maybe we won't ever need a backoffQ.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-02-23T15:12:29Z

> Maybe you should use a different queue for GPUs?

I am not sure, I feel this pattern will lead to creating many queues and complicates the job user experience (which queue I should submit to), and it is not something we should be recommending to deal with taints. 

I am fine with making the change as an option; it seems we are all on the same page that this is a temporary "fix" while we work the details of a more comprehensive re-queueing solution which I think is better discussed over a google doc; I would like to see a list of the use cases that we intend to cover because likely there will be conflicting ones that will require managing via knobs on either the capacity or the queue objects (and perhaps a cohort one).

### Comment by [@denkensk](https://github.com/denkensk) — 2022-02-24T19:01:33Z

I'm now working on providing a quick fix firstly. But I need to hear suggestions on how to make the option configurable. like  CreateTimeFIFO / EnqueueTimeFIFO

@ahg-g @alculquicondor  There are maybe serval ways here:
1. a feature gate
2. a cmd flag
3. add a policy field to the API of the queue. like
4. config file like `KubeSchedulerConfiguration` (This is definitely needed in the future, as we may have many different strategies in different part)

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-24T19:15:56Z

I vote for 3, maybe `sortingPolicy` or `sortingStrategy`

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-02-24T20:12:52Z

yeah, this needs to be a field in the API so that it is easy to experiment with by users in the initial iterations of Kueue.

### Comment by [@denkensk](https://github.com/denkensk) — 2022-03-09T03:01:13Z

Depends on https://github.com/kubernetes-sigs/kueue/pull/97
It will continue after #97 has merged.

### Comment by [@denkensk](https://github.com/denkensk) — 2022-03-10T12:58:19Z

https://docs.google.com/document/d/1VQ0qxWA-jwgvLq_WYG46OkXWW00O6q7b1BsR_Uv-acs/edit?usp=sharing

@ahg-g @alculquicondor   
I draft a doc for the different queueing strategies in Kueue. We can discuss on the doc.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-10T16:27:11Z

You forgot to open the doc for comments :)

### Comment by [@denkensk](https://github.com/denkensk) — 2022-03-10T16:33:27Z

> You forgot to open the doc for comments :)

Sorry opened.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-20T17:24:00Z

Hi Alex, what is your execution plan for this issue and expected timelines (not that we are late, just asking :))?

### Comment by [@denkensk](https://github.com/denkensk) — 2022-03-21T02:57:32Z

Hi Abdullah @ahg-g  Thanks for your reminder. I think it's better to add an umbrella here for tracking the process on this feature. :)

- [x] Draft a proposal for [The Queueing Strategies in Kueue](https://docs.google.com/document/d/1VQ0qxWA-jwgvLq_WYG46OkXWW00O6q7b1BsR_Uv-acs/edit?usp=sharing) 
- [x] Support QueueStrategy in ClusterQueue 
   - #80 
   - #97 Finished By Aldo
   - #126
- [x] Support PriorityClass in Workload
   - #104 
- [x] Support BestEffortFIFO
   - [x] #135 
   - [x] Add event-driven, move workload back to ClusterQueue
   - [ ] #178
- [ ] Support BalancedFIFO
   - [ ] Add a new less func: workloads are sorted by the priority and the time of enqueue.
- [x] doc
   - [x] #180 By Aldo

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-04-12T17:15:32Z

Let's open a different issue for Balanced (although I would wait for user feedback) and consider this one done.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-04-12T17:15:42Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8#issuecomment-1096987774):

>Let's open a different issue for Balanced (although I would wait for user feedback) and consider this one done.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
