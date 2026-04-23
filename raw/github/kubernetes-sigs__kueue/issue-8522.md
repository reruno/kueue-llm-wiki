# Issue #8522: [Time Sharing]  Support Time-Sharing in ClusterQueue

**Summary**: [Time Sharing]  Support Time-Sharing in ClusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8522

**Last updated**: 2026-03-23T08:39:41Z

---

## Metadata

- **State**: open
- **Author**: [@dddwsd](https://github.com/dddwsd)
- **Created**: 2026-01-10T09:16:26Z
- **Updated**: 2026-03-23T08:39:41Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 15

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

A same-priority preemption mechanism based on a minimum admitted runtime (minAdmitDuration) to prevent starvation and improve fairness among workloads in a ClusterQueue.

Scenario
* A ClusterQueue has a fixed quota of 8 GPUs.
*  Three users submit workloads A, B, and C with:
    * the same ClusterQueue and WorkloadPriorityClass
    * unknown execution durations
    * each workload requests 8 GPUs
* Workload A is admitted first and starts running.
* Shortly after, workloads B and C are queued.

Current behavior (without this proposal)
* Workload A continues running until completion.
* Workloads B and C remain pending, potentially for hours or days.
* Even though all workloads have the same priority, A monopolizes the ClusterQueue quota, causing excessive starvation.

Behavior with minAdmitDuration-based same-priority preemption
* Workload A is guaranteed to run for at least minAdmitDuration = 30 minutes after being admitted.
* After 30 minutes, if workloads B or C are still pending:
* Kueue may preempt workload A
* A is re-queued to the back of the ClusterQueue
* Workload B is then admitted and runs for at least 30 minutes.
* The same process repeats for C, enabling round-robin–style fairness at the admission level.

**Why is this needed**:

In environments where workloads of the same priority with unknown execution durations are continuously submitted by multiple users, this mechanism ensures fair resource allocation while guaranteeing a minimum resource holding time so that workloads are not preempted too aggressively.

**Completion requirements**:

This enhancement requires the following artifacts:

- [v] Design doc
- [v] API change
- [v] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-13T16:10:58Z

Yeah, this looks like a valid feature request. I looked into this. Today, withinClusterQueue: `LowerOrNewerEqualPriority` allows older waiting workloads to preempt newer admitted ones at the same priority, and Admission Fair Sharing provides usage-based ordering but operates at the LocalQueue level rather than individual workloads. Neither provides a minimum runtime guarantee before a workload becomes preemptible. I'm guessing this matters for workloads that checkpoint periodically and need minimum runtime to save progress or interactive sessions like Jupyter notebooks that need guaranteed allocation time.

I'm happy to drive this feature if @mimowo or @tenzen-y  feels okay with it.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-13T16:24:26Z

Hm, I can see the problem and I'm open for solving this, but I'm wondering about the API and the scope. 

For example doing it by wall time has some drawbacks, as measuring by GPU time might be preferred. It feels better for me to measure the usage as in AdmissionFairSharing. Maybe we could have an option like `LowerOrEqualPriority`, but then in AdmissionFairSharing we would have a strategy of allowing to evict if sufficiently lower usage.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-13T17:12:20Z

That makes sense; especially for heterogeneous workloads. I have one clarification: the original issue's scenario (Workloads A, B, C competing), would this be across different LocalQueues, or within the same LocalQueue? 
AdmissionFairSharing currently tracks usage per LocalQueue, so if A, B, C are from the same queue, we'd need workload-level usage tracking rather than queue-level. If they're from different queues (different tenants), then extending strategy would fit nicely.

### Comment by [@Ladicle](https://github.com/Ladicle) — 2026-01-14T00:22:10Z

+1 on this feature.

We are facing the exact same challenge in our production environment. Our setup consists of dedicated ClusterQueues for reserved resources and shared ClusterQueues for spare resources. For the shared ones, fairness is critical to prevent starvation.

Currently, to achieve this, we maintain a custom controller that monitors the runtime of Workloads. Once a Workload exceeds our minimum guaranteed runtime (e.g., 24 hours), the controller dynamically downgrades the priority of the kueue Workload resource. This is how we implement same-priority preemption for now.

### Comment by [@dddwsd](https://github.com/dddwsd) — 2026-01-14T01:22:38Z

My situation is identical to Ladicle’s use case.

> For example doing it by wall time has some drawbacks, as measuring by GPU time might be preferred. It feels better for me to measure the usage as in AdmissionFairSharing

Since these workloads are meant to consume **spare resources**, GPU time tends to be high across all workloads. Because of that I don’t expect there to be many cases where eviction would happen based on sufficiently low usage.

>I have one clarification: the original issue's scenario (Workloads A, B, C competing), would this be across different LocalQueues, or within the same LocalQueue?

In our case, the workloads all belong to the same LocalQueue.

### Comment by [@mwielgus](https://github.com/mwielgus) — 2026-01-14T11:51:07Z

Would it be ok to rename this request as "Time Sharing" (in the identical sense as operating systems grant cpu shares/access to processes running on the same machines)? 

A simple implementation could be to start adding same priority processes to preemption candidates after X seconds/minutes after they are admitted.

### Comment by [@Ladicle](https://github.com/Ladicle) — 2026-01-14T16:05:48Z

That sounds reasonable to me. We’ve been using a similar "N duration since admission" logic in our current controller, and it works well for our use cases.

A quick note on our use case: in our Hierarchical Cohort setup, we need to prevent a CQ from preempting its own workloads. As long as the new time-sharing mechanism respects the existing withinClusterQueue policy (specifically Never), this should work well for us.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-14T16:21:11Z

/assign
I will propose this KEP soon.

### Comment by [@dddwsd](https://github.com/dddwsd) — 2026-01-15T21:17:12Z

'Time Sharing' provides great clarity—I was looking for a term exactly like that. 

Thanks to everyone for the quick feedback and alignment. We're eager to see this in action and plan to deploy it in our environment as soon as possible.

### Comment by [@Ladicle](https://github.com/Ladicle) — 2026-01-19T14:30:32Z

Thanks! Overall, it looks good to me. This should work for my use case.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-16T10:24:02Z

Folks, @Ladicle, @sohankunkerkar @dddwsd I think the "time-sharing" deserves to be a native feature.

However, maybe it is achievable with minimal effort by a small controller based on the "priority-boost" mechanism: https://github.com/kubernetes-sigs/kueue/pull/9120. The controller could do round-robin and boost priority of a selected workload so that it can preempt.

I think this could be our "example controller" for the mechanism as we are planning to develop as part of the "priority boost" story. wdyt? cc @vladikkuzn 

If that works well, maybe we could just make the controller opt-in.

### Comment by [@Ladicle](https://github.com/Ladicle) — 2026-03-16T10:46:19Z

The opt-in controller approach sounds good to me. The negative 'priority boost' behavior aligns well with our in-house controller and works fine with TAS. I’m still catching up on the details, but at a glance, the negative unit test cases seem to meet our requirements.

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-03-17T12:03:39Z

> I think this could be our "example controller" for the mechanism as we are planning to develop as part of the "priority boost" story

Yeah, sound reasonable, as long as we can define how "priority boost" is calculated

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-03-19T20:40:38Z

@Ladicle @dddwsd Please review https://github.com/epam/kubernetes-kueue/blob/priority-boost-controller/cmd/experimental/priority-boost-controller/README.md
I think we can continue the collaboration on [PR](https://github.com/kubernetes-sigs/kueue/pull/9959) if it suites your needs

### Comment by [@dddwsd](https://github.com/dddwsd) — 2026-03-23T08:39:41Z

@mimowo  @vladikkuzn 
Thanks for the great suggestion — this appears to align very closely with what I was looking for.
I’ve left my review as a comment on the [PR](https://github.com/kubernetes-sigs/kueue/pull/9959).
