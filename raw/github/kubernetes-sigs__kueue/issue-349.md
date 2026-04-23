# Issue #349: An option to unsuspend jobs only after previously unsuspended ones are assigned nodes

**Summary**: An option to unsuspend jobs only after previously unsuspended ones are assigned nodes

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/349

**Last updated**: 2023-02-07T14:49:46Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-08-22T19:53:49Z
- **Updated**: 2023-02-07T14:49:46Z
- **Closed**: 2023-02-07T14:49:45Z
- **Labels**: `kind/feature`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 26

## Description

**What would you like to be added**:

An option, perhaps on ClusterQueue, where jobs are unsuspended not only if there is quota, but also if previously unsuspended jobs are assigned nodes (meaning they truly got assigned resources).


**Why is this needed**:
This offers all-or-nothing semantics, and can actually be used in setup with unlimited quota.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-22T20:30:12Z

We should try to do this without having to list pods. Perhaps the Job `.status.ready` counter could become handy.

Other than that, this mode would have very low throughput.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-23T03:21:10Z

Do you mean we should unsuspend the job until the previously one got scheduled by kube-scheduler?

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-08-24T19:19:22Z

> Do you mean we should unsuspend the job until the previously one got scheduled by kube-scheduler?

Yes, but this would be only an option.

This also could use preemption, for example if the job failed to become ready after some period of time, then suspend it again and try the next one.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-25T06:54:54Z

There's really a gap between kueue and scheduling, for we can't guarantee that the workloads admitted by kueue will always be scheduled successfully.

I think this is a pessimistic strategy, I can think of an optimistic one, we'll always admit the workloads self determined by Kueue, but we will have a background thread to preempt the unsuccessful scheduled workloads, like suspend to reclaim then requeue. This can be helpful in throughput and backed by the belief that most of the scenarios workloads will be successfully scheduled. For reference.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-25T13:46:00Z

Another alternative would be some sort of "maximum inflight workloads being scheduled".

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-08-25T21:21:19Z

> There's really a gap between kueue and scheduling, for we can't guarantee that the workloads admitted by kueue will always be scheduled successfully.

Yes, and we proposed a solution for that: [bit.ly/k8s-reservations](https://bit.ly/k8s-reservations); but in the meantime, we need something that we can do on our side to offer better all-or-nothing guarantees.

> I think this is a pessimistic strategy, I can think of an optimistic one, we'll always admit the workloads self determined by Kueue, but we will have a background thread to preempt the unsuccessful scheduled workloads, like suspend to reclaim then requeue.

We can have that strategy as well, it is basically an extension of what I discussed above in https://github.com/kubernetes-sigs/kueue/issues/349#issuecomment-1226140994; but more complex because now we need to make a decision which job to suspend etc. 

While for the general case starting one job at a time is slow, in practice there are cases where this may not be too bad. The idea is to start with something simple to proof the idea, even if it offers lower performance, and then expand on that to make it more performant.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-11-21T15:27:59Z

One use case to consider is that you could have a ClusterQueue where some flavors are "reservations", while others are "scaled-up" on demand.

It would be nice to restrict the feature per resource-flavor in a ClusterQueue. This would allow to maximize throughput in simple scenarios.

### Comment by [@mimowo](https://github.com/mimowo) — 2022-11-23T12:50:43Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2022-11-23T12:59:48Z

I’m going to propose a design doc in a PR. Still, I would like to first ask some questions and discuss the overall approach I'm thinking about. 

First, I would like to clarify what it means that a job has assigned nodes, in order to be precise about the condition that all previously started jobs have assigned nodes. I suggest that it means that enough job’s pods are ready, more precisely: `job.status.ready + job.status.succeeded >= job.spec.parallelism`. Note that, it means that some pods can be scheduled later when the job's `parallelism` is less than `completions`. However, I think checking against completions may decrease the throughput too much. Also, even if we checked against completions we cannot rule out rescheduling in case a pod fails. 

I call a job or a workload to be `scheduled` if it satisfies that condition.

Next, I’m thinking which API concept should be used to indicate that jobs within that concept should not be co-scheduled. We have a couple of options: workload, localqueue, flavor, clusterqueue, cohort. I suggest that being non-coschedulable is a property of a workload itself. For example, there might be workloads which are embarrassingly parallel and they would complete even if they have a single pod running at the same time. The main problem I assume is with jobs which require all pods running at the same time, requiring pod-to-pod communication.

Following up on this idea, I suggest introducing a new job annotation, called `kueue.x-k8s.io/kueue-avoid-workload-coscheduling`. When a new workload for a job with this annotation is admitted we wait unsuspending the job until all previously admitted workloads, which overlap with the workload in selected flavors (this belong to the same clusterqueue / cohort) are scheduled. When a new workload without this annotation is scheduled then we still delay its start if there are already admitted workloads that are non-coschedulable, are not yet scheduled, and overlap in the selected resource flavors.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-11-23T14:14:25Z

+1 to this interpretation: `job.status.ready + job.status.succeeded >= job.spec.parallelism`. Just make sure that `parallelism` is guaranteed to be less than or equal to `completions`.

You also need to think about how to communicate the information to kueue internals. The Workload controller shouldn't know about Job. So maybe kueue's job controller can add a condition into the Workload status to communicate that the first batch of pods were scheduled.

The annotation seems good. It needs to have a counterpart in the Workload API. I would name it something like: `kueue.x-k8s.io/wait-for-pod-scheduling`. The functionality could be simpler: just unsuspend, but block further admission until it's scheduled.

### Comment by [@mimowo](https://github.com/mimowo) — 2022-11-23T14:47:42Z

> You also need to think about how to communicate the information to kueue internals. The Workload controller shouldn't know about Job. So maybe kueue's job controller can add a condition into the Workload status to communicate that the first batch of pods were scheduled.
> 
Yes, I think a condition, called `PodsScheduled` in workload status is the way to go. I guess we need a watcher on the job status updates and add the condition once the first batch is scheduled.

> The annotation seems good. It needs to have a counterpart in the Workload API. I would name it something like: `kueue.x-k8s.io/wait-for-pod-scheduling`. 

I was thinking about translating the job annotation into Workload boolean field, say `waitForPodScheduling`.

> The functionality could be simpler: just unsuspend, but block further admission until it's scheduled.

Yeah, I guess so, at least in the first iteration. 

I was thinking of allowing admission of more than one workload in order to check if their set nodes can overlap and start them concurrently if we can deduce they would not. However, I'm not sure if we can make any of such conclusions currently. For example, if two workloads are admitted to different cohorts, can we conclude they will be scheduled on disjoint sets of nodes? Similarly, can flavors overlap in terms of nodes?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-11-23T16:06:34Z

> For example, if two workloads are admitted to different cohorts, can we conclude they will be scheduled on disjoint sets of nodes?

No, cohorts define borrowing semantics, but they don't dictate anything about the nodes.

>  Similarly, can flavors overlap in terms of nodes?

Different flavors should refer to different sets of nodes. For that reason, we encourage different flavors to have the same label key, but with different label values. This is not enforced, but you can take it as an assumption, at least to explore what can we do with it.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-11-23T16:50:24Z

> For example, if two workloads are admitted to different cohorts, can we conclude they will be scheduled on disjoint sets of nodes?

We can't conclude that, different cohorts could use the same flavors. So there is still a risk of deadlocks even with this feature implemented until we do some form of active management: medium term solution is to preempt stuck workloads, and the long term solution is integration with CA provisioning API.

> I was thinking about translating the job annotation into Workload boolean field, say waitForPodScheduling.

We can discuss on the KEP, but worth considering an enum.

### Comment by [@mimowo](https://github.com/mimowo) — 2022-11-25T13:13:53Z

Please review the design doc: https://github.com/kubernetes-sigs/kueue/pull/433
@alculquicondor @kerthcet @ahg-g

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-12-21T18:02:15Z

with https://github.com/kubernetes-sigs/kueue/pull/473 merging, I guess users can start testing, nothing left on the functionality front, right?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2022-12-21T18:22:42Z

This is not functional, but maybe we want to update the documentation.

https://github.com/kubernetes-sigs/kueue/blob/9f27bc3dbc6d07e23efc301940d7487baceb0d8a/docs/setup/install.md#install-a-custom-configured-released-version

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-12-21T18:54:36Z

> nothing left on the functionality front, right?

timeouts :)

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-12-21T19:01:52Z

At least one integration test is flaky #488

### Comment by [@mimowo](https://github.com/mimowo) — 2022-12-22T12:21:51Z

> > nothing left on the functionality front, right?
> 
> timeouts :)

That is correct, we also planned to timeout workloads taking long to start (reaching the PodsReady=true state). However, the mechanism of avoiding deadlocks should now be functional, so some early feedback from testing by users would be great.

### Comment by [@mimowo](https://github.com/mimowo) — 2022-12-22T12:25:08Z

> This is not functional, but maybe we want to update the documentation.

I'm going to work on that. The place you pointed out might be good to show an example configuration and probably to reference a new doc page here: https://github.com/kubernetes-sigs/kueue/tree/main/docs/tasks.

### Comment by [@mimowo](https://github.com/mimowo) — 2022-12-22T12:26:05Z

> At least one integration test is flaky #488

A PR to fix the tests is opened https://github.com/kubernetes-sigs/kueue/pull/491, please review. Changes to the code don't seem necessary.

### Comment by [@mimowo](https://github.com/mimowo) — 2023-01-18T10:41:35Z

The PR to enforce PodsReady timeout (https://github.com/kubernetes-sigs/kueue/pull/498) is merged and the PR with docs is on the way: https://github.com/kubernetes-sigs/kueue/pull/515. Testing and feedback on the feature would be great!

As discussed (https://github.com/kubernetes-sigs/kueue/pull/498#discussion_r1071424145) we may also need a mechanism to minimize the risk of clogging the queue by a workload that exceeded the pods-ready timeout. @ahg-g @alculquicondor do you think it is something we should do now or can we wait as we collect feedback?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-18T15:16:09Z

I think it can wait.

### Comment by [@mimowo](https://github.com/mimowo) — 2023-02-07T08:41:39Z

The feature is ready for testing from the main branch. Here is the documentation page: https://github.com/kubernetes-sigs/kueue/blob/main/docs/tasks/setup_sequential_admission.md.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-07T14:49:42Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-02-07T14:49:46Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/349#issuecomment-1420900480):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
