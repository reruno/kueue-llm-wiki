# Issue #6143: Serialized pod preemption problem for scheduler

**Summary**: Serialized pod preemption problem for scheduler

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6143

**Last updated**: 2026-03-26T15:06:19Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@amy](https://github.com/amy)
- **Created**: 2025-07-23T00:39:20Z
- **Updated**: 2026-03-26T15:06:19Z
- **Closed**: 2026-03-26T15:06:19Z
- **Labels**: `kind/bug`
- **Assignees**: [@amy](https://github.com/amy)
- **Comments**: 49

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
If many tasks are launched for the same CQ, that all require preemption from the same target, it can cause significant delays in that cq's access to their nominal quota.

**What you expected to happen**:
CQs should be able to reclaim their guarantees faster. The scope of Multiple preemptions needs to expand. 

**How to reproduce it (as minimally and precisely as possible)**:
e2e reproduction: [https://github.com/kubernetes-sigs/kueue/pull/6125](https://github.com/kubernetes-sigs/kueue/pull/6125)
(In the e2e, you'll note that the pod workload types have `TerminationGracePeriod` and `PreStop` Lifecycle Hooks set)


**Anything else we need to know?**:
We encountered this issue during a cluster migration. 

I see existing contexts here:
Issue: [Can we preempt in more than one CQ per cohort in a cycle?](https://github.com/kubernetes-sigs/kueue/issues/2596#top)](https://github.com/kubernetes-sigs/kueue/issues/2596)
PR: [Enable Multiple Preemptions within Cohort in a single Scheduling Cycle](https://github.com/kubernetes-sigs/kueue/pull/2641)

Also recently discussed on slack here: [https://kubernetes.slack.com/archives/C032ZE66A2X/p1752770229994679](https://kubernetes.slack.com/archives/C032ZE66A2X/p1752770229994679)
A different user said this: "in our setup, we have a low priority job just consuming any GPUs whenever they become available and then get preempted whenever any other cluster queue wants them, but kueue is taking too long to evict all the low-priority jobs which is causing issues for the workloads on higher priority cluster queues"

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-07-23T00:41:56Z

(I am interested in assigning myself. But would defer to project owners if there's other preferences for assignee. Thank you!)

Would also be interested in understanding any other existing context not captured in [#2596](https://github.com/kubernetes-sigs/kueue/issues/2596) and [#2641](https://github.com/kubernetes-sigs/kueue/pull/2641)

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-07-23T16:22:51Z

> (I am interested in assigning myself. But would defer to project owners if there's other preferences for assignee. Thank you!)
> 
> Would also be interested in understanding any other existing context not captured in [#2596](https://github.com/kubernetes-sigs/kueue/issues/2596) and [#2641](https://github.com/kubernetes-sigs/kueue/pull/2641)

/assign amy

Happy to have you take a stab at this :). We can discuss here, or over slack, background to the problem

### Comment by [@amy](https://github.com/amy) — 2025-07-23T16:26:14Z

Adding offline discussion with @gabesaba here so context is together:

> We are, unfortunately, doing all of the preemption calculations independently. And many CQs are likely to pick the same workload - hence only one making progress while the preemption is ongoing.
> 
> after the initial flavor assignment, something we could consider is several cluster queues calculating preemption targets statefully - so that earlier cluster queues preemptions are taken into account (for both resources, and make sure that there are no overlaps)
> 
> it would require a pretty big update to the existing flow
> so flavor assignment
> then stateful preemption calculation
> to guarantee no more than 1 CQ selects same target
> 
> may run into the case where CQ that wants to be preemptions will be starved anyway, as there are no valid targets left

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-23T16:36:21Z

That is a good point. I think we might want to introduce Async Preemptions to improve Premeption performance which means that kueue-scheduler move to the next scheduling cycle after issuing preemptions (not waiting for completion of preemptons).

In the GPU environment, detaching GPUs from Pods occasionally takes a longer time, which introduces significant preemption durations. So, I think we should improve this Preemption performance problem.

### Comment by [@amy](https://github.com/amy) — 2025-07-23T17:28:54Z

(Will make sure this is behind a feature gate when I implement this)

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-07-23T18:16:14Z

>> We are, unfortunately, doing all of the preemption calculations independently. And many CQs are likely to pick the same workload - hence only one making progress while the preemption is ongoing

One potential low-hanging fruit could be to introduce randomization among preemption candidates (wholesale or within the same "preemption-score" category). For workloads with high cardinality (like pod-integration) and high preemption rates, this could help reduce the chance that multiple scheduling candidates target the same workload for preemption.

### Comment by [@amy](https://github.com/amy) — 2025-07-23T20:18:42Z

@ichekrygin the issue is in cases like something like migration, its a select few queues that are bursting (bc so much quota is available) and thus need to be preempted. So I don't think that randomization would solve the failure we saw in production. 

This is a simplification of what happened:
- new cluster with seeded CQs
- migrate 1 CQ's workloads. Can admit everything bc it can access all of burst.
- next CQ's workloads, needs to preempt. There's only 1 target CQ. 
- repeat

However, I do see it as useful perhaps for other issues related to serialized preemption. So I'll make sure to consider it in implementation.

### Comment by [@tskillian](https://github.com/tskillian) — 2025-07-23T21:52:25Z

The problem is also exacerbated by having multiple cluster queues needing preempt as well. I wrote a UT [here](https://github.com/kubernetes-sigs/kueue/pull/6165) to show that one workload preemption will also block preemptions for all other cluster queues (assuming they'd share the same target) even when other preemption targets are available.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-07-24T19:27:59Z

I wonder, have we considered performing flavor assignment and target nomination inline, i.e., within a single scheduling loop, rather than how it's done today in two distinct phases: nomination and scheduling?

If this has already been considered, what were the deterrent factors that led us to split the process into two separate phases?

+ @mimowo

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-07-25T01:12:19Z

The issue, as I see it, is rather straightforward, unless I am missing something. In any case, this is not an authoritative analysis, and I defer to the maintainers for the final say.

Consider a scenario where we have **100 pending workloads**, all of which require preemption.
Now, assume that we are currently running (active and admitted) another **100 workloads** all of which could be (and will be) preempted by pending workloads. 

What happens today is that **all 100 pending workloads may receive a flavor assignment and the same preemption target, pointing to a single admitted workload instance**. The scheduler tracks previously preempted workloads, and if it detects that a given pending workload has a preemption target that has already been preempted (by a previous workload in the same cycle), it will **skip scheduling that workload and defer it to the next scheduling cycle**.

As a result, each cycle proceeds as follows:

1. **Nominate 100 workloads**, all pointing to the same preemption target.
2. **Attempt to schedule all 100 nominations**:

   * Successfully schedule the first workload (preempting the target).
   * Skip the remaining 99 workloads (since the preemption target was already preempted).
     **Note:** All of these preemption collisions are avoidable in this example.
   * **Requeue all skipped workloads.**
3. **Repeat the cycle**.

---

### **Complexity Analysis**

The current approach has a time complexity of:

$$
N + (N-1) + (N-2) + \dots + 1 = 
\frac{N(N+1)}{2} = 
O(N^2)
$$

where **N** is the number of pending workloads that each require preemption.

However, the complexity could be reduced to:

$$
O(N)
$$

if, for every pending workload, we:

* **Assign a flavor and calculate preemption target(s)**, and
* **Preempt a workload in-line and schedule the candidate before moving to the next workload**,

without the need for tracking preemption collisions, since there either will be a valid **preemptable** target or there won’t be (and the workload will not fit).

**Note:** This calculation focuses solely on the scheduling and preemption steps. It does not include the complexity of flavor assignment or preemption target calculation, which remains the same between the current and "in-line" approaches.

It is also understood that switching to the "in-line" option will likely require changes to the scheduler throttling mechanism, as we currently throttle entire scheduling cycles (which can compound delay issues) rather than individual workload candidates. In my opinion, throttling at the workload level could be more efficient, similar to the controller-runtime work queue, but it would require deeper changes.

### Comment by [@amy](https://github.com/amy) — 2025-07-25T02:48:34Z

(@ichekrygin I think... you're discussing the difference between a greedy scheduling algorithm vs. what Kueue does? Ie, making greedy admission decisions per pod, vs. nominate/schedule. So here's my naive guess, (keen on understanding the history as well): For Kueue I assume the goal isn't extremely low scheduling latency per se, its more about scheduling fairness, reducing preemption churn, and binpacking.)

For instance, for GPU training platform, I think we'd rather have "better" scheduling decisions than fast ones. (within a certain threshold of reasonable-ness)

(This is assuming my interpretation of both the above comments, and Kueue scheduling are correct.)

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-07-25T03:33:08Z

> you're discussing the difference between a greedy scheduling algorithm vs. what Kueue does?

Not exactly. I am describing the efficiency of the current Kueue workload scheduling process. In my opinion, the scheduling strategy (fairness or otherwise) could still be implemented without unnecessary performance penalties.

### Comment by [@amy](https://github.com/amy) — 2025-07-25T04:18:13Z

I misinterpreted. You're expanding on the idea of processing preemption statefully.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-25T09:29:15Z

Hi folks, thank you for thinking about this. My gut feeling is that the issue with handling workload with overlapping preemption targets does not warrant big refactoring. I remember discussing this with @gabesaba and it was mostly "defensive" programming on our side, but most of the pieces are already there to allow for overlaps. (I might be missing something, this is based mostly on discussions and initial reading of the code).

Now, proposal in https://github.com/kubernetes-sigs/kueue/issues/6143#issuecomment-3115516859 seems going much further than than, and require signifficant refactor of scheduler. I need to think about it, I kind of hope it is a separate enhancement. I will try to read the proposal deeper next week.

### Comment by [@amy](https://github.com/amy) — 2025-07-29T16:14:56Z

Hey folks! Quick update. Working on a PR, need to write tests, but here's the direction I'm going towards. I don't think it involves major changes. The gist is that I'm now just tracking preemption targets within the `schedule()` loop to remove from the next head's snapshot to simulate preemption without the previous head's targets. This ensures that the next head will never have overlapping preemption targets.

```
Currently, here is the scheduling flow:
schedule() loop:
- snapshot = cache.Snapshot() // snapshot of cohort, cq resources
- nominate() // takes a list of candidate workloads & returns which are potentially admissible
  - CQ-A: getAssignments(snapshot) 
  - CQ-B: getAssignments(snapshot) // uses the same snapshot as CQ-A
 - for iterator.hasNext() { // iterates over admissible workloads
   - "Workload has overlapping preemption targets with another workload" 
       // ^ CQ-A and CQ-B share preemption targets because they were using the same snapshot

Upcoming PR, new scheduling flow:
schedule() loop:
- snapshot = cache.Snapshot() // snapshot of cohort, cq resources
- nominate() // takes a list of candidate workloads & returns which are potentially admissible
  - CQ-A: getAssignmentsStateful(snapshot)
    - add to preempted workloads list
  - CQ-B: getAssignmentsStateful(snapshot, preemptedWorkloads)
    - remove preempted workloads from snapshot using stateful oracle
    - oracle.SimulatePreemption() // simulates preemption with stateful snapshot. ie snapshot does not include CQ-A preemption targets
    - append CQ-B preemption targets to preempted workloads list
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-29T16:37:03Z

I had something like this in my mind. This would eliminate the need for the 2nd workload to wait until the first one completes the preemption - the second workload could start preempting its additional targets immediately. I don't think we need to rename `getAssignments`, but this is a detail. 

One possible drawback I see is more SimulationPreemption during the scheduling loop. However, I think this is acceptable -  it is only additional once per workload, and we already call it per workload (or even per resource) during the assignment phase. So worst case we will be calling SimulationPreemption 2x. 

Another important question (determining the scope of the improvement) - do we want to trigger getAssignment only in case of preemption target overlap (we can start here), or when processing any sequence of workloads. Potentially, even the previous "Fit" workload may cause the second workload to choose a different flavor.

We may consider guarding the change behind a feature gate like `RefreshAssignmentsDuringSchedulingCycle`.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-07-29T16:50:07Z

To clarify my understanding, it appears that in this context, "schedule loop" refers to a single invocation of `schedule(ctx)`, i.e., a **scheduling cycle**.

I’d like to draw a distinction between **"loop"** and **"cycle"**, since a scheduling cycle in Kueue consists of two distinct phases:

* [nominate](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/scheduler.go#L221): selects schedulable workloads and assigns flavors and potential preemption targets,
* [process](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/scheduler.go#L233): the actual loop that iterates over nominated candidates and performs admission.

It might be helpful to disambiguate this terminology, especially in the context of naming proposed feature gates, where “loop” could imply internal iteration, while “cycle” more accurately describes the top-level `schedule(ctx)` invocation.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-07-29T17:16:24Z

> * nominate() // takes a list of candidate workloads & returns which are potentially admissible
>
>   * CQ-A: getAssignments(snapshot)
>   * CQ-B: getAssignments(snapshot) // uses the same snapshot as CQ-A

My apologies for nitpicking, but based on the description above, one might get the impression that **nomination happens at the queue level**, i.e., "queue by queue", whereas in reality, **nomination occurs at the workload level**, regardless of which queue a workload belongs to.

Before calling `nominate()`, we collect all "ready" workloads into [headWorkloads](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/scheduler.go#L205). Despite the name, `headWorkloads` is effectively the **full list of workloads ready for scheduling**.

Inside `nominate()`, we call `getAssignments()` for each individual workload in that list, as seen [here](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/scheduler.go#L431). This means the snapshot is shared across all workloads during nomination, not partitioned by ClusterQueue.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-07-29T17:17:41Z

I think tracking the set of workloads "marked" as potential preemption targets is a reasonable approach. That said, I want to highlight a few considerations:

* **Reduced candidate set:** Stricter admission, due to targeted preemption decisions, may reduce the number of nominated workloads, which can be beneficial in this context.
* However, since the scheduler performs an [additional “fitness” check](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/scheduler.go#L286) after nomination, it is possible for a workload to be disqualified **after** its preemption target has already blocked other candidates from being nominated.

---

Overall, I think this proposal can help reduce **overlapping preemption targets** and streamline scheduling decisions. It's definitely worth considering.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-29T17:40:34Z

> To clarify my understanding, it appears that in this context, "schedule loop" refers to a single invocation of `schedule(ctx)`, i.e., a **scheduling cycle**.
> 
> I’d like to draw a distinction between **"loop"** and **"cycle"**, since a scheduling cycle in Kueue consists of two distinct phases:
> 
> * [nominate](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/scheduler.go#L221): selects schedulable workloads and assigns flavors and potential preemption targets,
> * [process](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/scheduler.go#L233): the actual loop that iterates over nominated candidates and performs admission.
> 
> It might be helpful to disambiguate this terminology, especially in the context of naming proposed feature gates, where “loop” could imply internal iteration, while “cycle” more accurately describes the top-level `schedule(ctx)` invocation.

IIUC, the Kueue scheduling cycle indicates an entire performance against the Head workloads (including Head workloads selection).
Couldn't we consider that each Kueue scheduling cycle has a nomination "phase" and a process "phase" instead of "loop" and "cycle" approach?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-29T18:23:52Z

In my mental model scheduler operates in "cycles" - single invocation of "schedule()", which +/- splits into two phases: "nomination" and "processing".

In [my last comment](https://github.com/kubernetes-sigs/kueue/issues/6143#issuecomment-3133266322) I used less formally "loop" thinking "cycle", and "assignment phase" thinking "nomination phase". 

Sorry if this caused some confusion, I'm not sure this vocab is well defined.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-29T18:27:36Z

> if, for every pending workload, we:
> 
> Assign a flavor and calculate preemption target(s), and
> Preempt a workload in-line and schedule the candidate before moving to the next workload,
> without the need for tracking preemption collisions, since there either will be a valid preemptable target or there won’t be (and the workload will not fit).
> 
> Note: This calculation focuses solely on the scheduling and preemption steps. It does not include the complexity of flavor assignment or preemption target calculation, which remains the same between the current and "in-line" approaches.
> 
> It is also understood that switching to the "in-line" option will likely require changes to the scheduler throttling mechanism, as we currently throttle entire scheduling cycles (which can compound delay issues) rather than individual workload candidates. In my opinion, throttling at the workload level could be more efficient, similar to the controller-runtime work queue, but it would require deeper changes.

I think that it's mostly challenging to improve the preemption performances by this proposed way, especially in GPU environments. The preempting workloads could take a longer and longer time, like minutes, since the post-processing (detaching PV and devices (GPUs)) will take a long time. So, this might decrease the performance.

The current approach tries to eliminate these potential risks by increasing the scheduling tries across multiple scheduling cycles.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-29T18:28:22Z

> In my mental model scheduler operates in "cycles" - single invocation of "schedule()", which +/- splits into two phases: "nomination" and "processing".
> 
> In [my last comment](https://github.com/kubernetes-sigs/kueue/issues/6143#issuecomment-3133266322) I used less formally "loop" thinking "cycle", and "assignment phase" thinking "nomination phase".
> 
> Sorry if this caused some confusion, I'm not sure this vocab is well defined.

That's the same understanding as mine.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-07-29T19:42:28Z

> I think that it's mostly challenging to improve preemption performance using this proposed approach, especially in GPU environments. The preempting workloads could take a long time, sometimes minutes, due to post-processing steps like detaching PVs and GPU devices. So, this might degrade performance.

Hi @tenzen-y, first of all, thank you for the feedback.
Second 🙂, just to clarify, my comment was not a formal design or proposal, but rather an idea I believe is worth considering.

That said, I believe the **number of operations per scheduling cycle** is the same in both models:

* In the current two-phase approach: for-all-candidates(`nominate`) followed by for-all-candidates(`process`),
* In the proposed one-phase inline approach: for-each-candidate(`nominate + schedule`)

Similarly, the **time required to preempt an individual workload** should remain unchanged between the two.

The key difference is in execution flow,
In the one-phase model, we eliminate **preemption target collisions** by performing flavor assignment, preemption evaluation, and scheduling **inline**, per workload. This removes the need to track or deduplicate preemption targets across workloads and avoids retrying skipped workloads in a subsequent scheduling cycle.

While the **cost per workload** for flavor assignment and preemption evaluation is the same, the difference lies in **how those evaluations are sequenced and isolated**, which could result in a **runtime complexity reduction** in some cases.

Please let me know if I’ve misunderstood your point or missed a subtle aspect of your comment, I’d be happy to continue the discussion.

### Comment by [@amy](https://github.com/amy) — 2025-07-29T21:28:30Z

⭐️ Hey folks! Let's move the discussion of @ichekrygin's approach here, I've also added some tactical suggestions of how we should proceed PTAL: https://github.com/kubernetes-sigs/kueue/issues/6260

For comments/clarifications for my proposal, will follow up 🫡

### Comment by [@amy](https://github.com/amy) — 2025-07-30T16:10:28Z

Offline discussions with @gabesaba (to keep context together)

Gabe: Does this handle ordering?  iterator.next relies on the nomination being complete, with preemption targets, to decide order. It could be that some lower-priority (for some broad definition of priority, including fair-sharing, etc) workload comes first in nomination, and makes preemption targets unavailable to a high-priority workload?

Me: I didn’t look too closely at how we get the heads. Are they not originally ordered? Meaning, is nomination itself not in some definition of priority order? 

Gabe: They are within CQ, but the ordering of which workload/clusterqueue within the Cohort is determined after nomination, and in the case of fair sharing, iteratively (as the DominantResourceShares may be affected by previous admissions within the cycle).

### Comment by [@amy](https://github.com/amy) — 2025-07-31T00:21:12Z

okay! I think I need to amend my approach based off the comments. Here's something I'm considering...

There's 2 places within the current flow we can consider passing preemption targets:

Bad Option 1 that I proposed - Within `nominate()`
- within `nominate()` today, it loops through all the heads and selects admissible workloads using the same snapshot
- what I proposed was passing preemption targets returned from `getAssignments` between loops, to remove from the snapshot of the following `getAssignments` call
- Problem: As pointed out by @gabesaba, Nominate doesn't handle ordering. This happens within the iterator itself on each pop. This would mean a "lower priority workload" could starve higher priority workloads of preemption targets within a `schedule()` invocation.
- 🙅🏻‍♀️ We cannot go with this option. 

Potential Option 2 - change `for iterator.hasNext() {.. here...}`
```
preemptedWorkloads := make(preemption.PreemptedWorkloads)
for iterator.hasNext() {
  ...
  ...
  // Conflict detected, get new assignments
  preemptionTargets := getAssignments(snapshot, preemptedWorkloads)
  // getAssignments removes preemptedWorkloads from snapshot to get new preemption target
  // add new preemption targets to growing list of actually preemptedWorkloads
  ...
  ...
  // complete admission
}
```
- This way, the tournament order is preserved. 
- Potential issue from @mimowo "Potentially, even the previous "Fit" workload may cause the second workload to choose a different flavor" 
  - ❓I'm not quite following the implications of this for either: 
    1.) admissible workloads from nominate -> Do you mean that the admissibility is stale? (I think that's the case for current implementation too. So waiting for the next `schedule()` invocation should be okay? maybe?)
    2.) potentially affecting tournament state or results

🙏 Thanks for everyone's time! Please let me know y'alls thoughts! Also let me know if there's something I'm fundamentally getting wrong about how schedule() works.

cc/ @mimowo @tenzen-y @gabesaba @ichekrygin

### Comment by [@amy](https://github.com/amy) — 2025-07-31T19:37:49Z

More updates. Through testing, I think even with my proposed fix to recalculate preemption targets on preemption... we still encounter serialized preemption problems because of how we process queue heads.

In my e2e example (using pod workload type) its:
* 2 CQs, each with 4 nominal quota
* Submit 8 to CQ-A, everything is admitted
* Submit 4 to CQ-B, serialized preemption problem occurs here

This still occurs even with the fix to find other preemption targets on conflict. 

Kueue stalls...
➡️ horizontally across CQs on preemption target overlap within a single `schedule()` invocation (above proposal remediates this)
⬇️ vertically within a CQ on preemption completion across `schedule()` invocations (above proposal does not resolve this)

-------
```
1. CQ-B: Workload needs preemption to be admitted
2. Workload is inadmisslbe & gets requeued with RequeueReasonPendingPreemption
3. manager heads() will still pop CQ-B's same workload until preemption completes
...
...
several more schedule() invocations later, preemption completes, admit CQ-B's head
4. Now we can assess the next workload in CQ-B

So the other issue is... between schedule() invocations where the head is blocking the clusterQueue when 
waiting for preemption completion. It blocks subsequent workloads within the same CQ from admission 
even though all 4 workloads are reclaiming its own guarantees. This can be viewed as a violation of 
nominalQuota guarantees.
```
---------

I'd like to have a solution that prioritizes ⭐️**reclaiming guarantees quickly**⭐️ while also:
1. preserving workload ordering within a CQ and
2. fairness across CQs

Naively... To address the head blocking its own ClusterQueue problem... I wonder if we can ensure this:

1. Ensure within a CQ, in a single `schedule()` invocation - Previous heads all result in some virtualized preemption (ie preemption targets are marked for admission/preemption in the snapshot only) - this preserves workload ordering within 1 CQ
2. Ensure all heads don’t overlap in preemption targets both within its own CQ and across CQs

So this probably involves... marking pods for target admission and target preemption in some virtualized state for a "fit as much as possible" step. Then committing that desired state when you're done assembling the batch.

Overall, we need a mechanism to add CQ depth in the head processing flow. 

---------
It could look something like this
```
So lets say you have 3 CQs:
- CQ 1, can fit 1 workload
- CQ 2 can fit 2 workloads
- CQ 3 can fit 3 workloads

Within 1 schedule() invocation you still do round robin pulls of CQ heads. 
Within schedule() track preemption targets and admission to omit from subsequent cycles. 
🚨 Each cycle does not make real admission or preemptions, just collect them.

⭐️ start schedule()
1. cycle 1 within schedule():
"Preempt" workloads for all 3 cq heads

2. cycle 2 within schedule():
Set CQ 1 aside. It no longer can fit workloads within guarantees
"preempt" workloads for 2 CQ heads

3. cycle 3 within schedule():
Set CQ 1 and CQ 2 aside.
"Preempt" workloads for CQ 3 head.

--- So at this point, Youve completed reclamation

4. Cycle 4:
Admit 1 workload to borrow within cohort. (This part probably needs more thought)

--- finished gathering all admission and preemption decisions 

5. Commit collected admission and preemption decisions at once based off 1 snapshot
 
⭐️ End schedule(). Start next schedule() invocation
```

### Comment by [@tskillian](https://github.com/tskillian) — 2025-08-02T19:43:32Z

I'm not very familiar with the code base, so good chance this is a naive question:

Why are workloads already marked for eviction included as preemption targets? When we have this issue (many pods suddenly scheduled for a cluster queue all needing to reclaim quota from another cluster queue), the logs make it look like the core problem is just that all of the preempting pods are getting the same preemption target even though whoever was at the head of the cluster queue caused it to be marked for preemption.

So what would happen if we just didn't consider workloads marked for preemption as candidates?

### Comment by [@amy](https://github.com/amy) — 2025-08-03T05:29:39Z

Oh this is potentially another dimension. 
So far its:
1.) ➡️ horizontally across CQs on preemption target overlap within a single schedule() invocation 
2.) ⬇️ vertically within a CQ on preemption completion across schedule() invocations waiting for preemption targets to complete preemption

Looking at the code... @tskillian I think you're potentially right. Where also:

The snapshot for the `N+1 invocation of schedule()` also still includes `N schedule()`'s preemption target workoads where `InvokePreemption` was already called. I see these comments:
```
// candidatesOrdering criteria:
// 0. Workloads already marked for preemption first.
```

I think your proposal doesn't work with how schedule works today. Its because...
- CQ head remains the same until its target preemption gets preempted so you'll have this:
1. Workload A gets nominated. Preempts workload B. Workload A waits for workload B to be preempted with `RequeueReasonPendingPreemption`. So workload A gets requeued to head of CQ. 
2. If you exclude Workload B from being considered in the next `schedule()` as a preemption target, Workload A (still the head of CQ) will incorrectly pick another workload for preemption and wait for it to be preempted.

We're looking for a way to make progress in the depth of a CQ. (ie to be able to move past the CQ head / the admission candidate)

### Comment by [@tskillian](https://github.com/tskillian) — 2025-08-03T15:00:41Z

Agreed, ignoring preempted workloads as candidates would also require us to track that a given entry has already preempted the workloads it needs to schedule. So the preemptor would stay in the cluster queue but it'd be skipped if had already preempted other workloads.

### Comment by [@tskillian](https://github.com/tskillian) — 2025-08-04T15:31:57Z

[Here](https://github.com/kubernetes-sigs/kueue/pull/6444) is an example. It seems like a potentially simple way to speed up preemption

### Comment by [@amy](https://github.com/amy) — 2025-08-04T15:48:40Z

Interesting and simple idea! What I wonder is... if there's a reason the CQs block at the head in the first place. Especially for Pod workload type, we don't have an operator like the Job workload type to outsource completing preemption. So the blocking is maybe part of the design.

What I mean is, if we just move past the head and preempted workloads without blocking, we're just trusting that the pod will complete preemption.

If blocking is necessary, I'd like to go with this approach: ["Batched CQ Head Processing"](https://github.com/kubernetes-sigs/kueue/issues/6143#issuecomment-3141133733)
If its not, your approach is very clean

Let's wait for project owner input.

### Comment by [@tskillian](https://github.com/tskillian) — 2025-08-04T15:55:01Z

> What I mean is, if we just move past the head and preempted workloads without blocking, we're just trusting that the pod will complete preemption.

I've been trying to think of a reason this may be needed too, though I'm unable to come up with one. Currently it blocks, but as far as I can tell nothing makes sure the pod completes preemption anyway, so it doesn't change that behavior for the preemptor pods.

> Let's wait for project owner input.

Agreed, my confidence that it's a plausible path forward is low without someone who's much more familiar with the project.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-06T12:26:19Z

> Let's wait for project owner input.

There has been a lot of discussion and ideas floating around, I will try to focus my attention on the most important aspects, but let me know if something is missed.

As discussed there are multiple dimensions to the problem of delayed preemptions, the most significant are:
1. horizontal - single scheduling cycle for multiple CQs - we skip preemption for workloads in case of overlapping preemption targets
2. vertical - across scheduling cycles - we wait for the head to complete preemptions before starting preemptions for the second high priority workload

I think (2.) is complicated because it would require scheduler to lookup multiple workloads per CQ, and (a) it is not clear how many we need, (b) the nomination for the second workload is likely to be invalidated by the results of admitting the first one.

I think (1.) is significantly simpler, and seems like the primary business concern, so I would start here. 

I think to solve (1.) we can:
1. drop this block of code: https://github.com/kubernetes-sigs/kueue/blob/36928e70fc50238b5b10ea2ed9c6391bfd399542/pkg/scheduler/scheduler.go#L278-L283
2. modify [fits()](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/scheduler.go#L443-L447) function to deduplicate the workloads so that we don't double subtract for the new & overlapping targets
3. call IssuePreemptions only for newPreemptionTargets (e.preemptionTargets - preemptionTargets)

I might be missing something. Let me know if this is the case.

### Comment by [@amy](https://github.com/amy) — 2025-08-06T17:54:04Z

@mimowo I think both are the problem.

Horizontal -> make sure downstream CQs can schedule despite overlap; TIm's primary problem
Vertical -> make sure downstream workloads within 1 CQ can schedule; Our primary problem

Even if we make the horizontal change, within the scope of 1 CQ, the head workload is still blocking. So the CQ will very slowly trickle in if the user submits a large batch of workloads that all need preemption. This is because preemption takes 15min for our pod workload types.

Can you offer insight to the batched `schedule()` proposal here (last section): https://github.com/kubernetes-sigs/kueue/issues/6143#issuecomment-3141133733
Let me know if I should offer any clarification as well. Primarily, within 1 `schedule()` there's multiple cycles that operate on the same snapshot. Then the final admission / preemption call happens at the same time at the end.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-06T18:02:08Z

I see, thank you for clarifying. 

Yeah, I dont know yet how to solve the vertical so offered a proposal for horizontal first to solve one issue at the time and see how the system performs overall in practice.

I agree vertical blocking remains an issue, but I need more time to think about it. I will read this in proposal in more detail tomorrow.

### Comment by [@amy](https://github.com/amy) — 2025-08-06T19:55:29Z

@mimowo Yeah after chatting with my team... here's what I propose tactically:

1. Implement the fix for overlapping preemption target within 1 CQ (the horizontal dimension you proposed)
    - https://github.com/kubernetes-sigs/kueue/issues/6488
2. Add a stopgap to prevent 1 clusterQueue from being blocked by the head. 
    - Here's the scenario: We have a pod stuck in terminating. This blocks its own CQ for hours. 
    - As a stopgap, let's implement a timeout where if the pod has been stuck in terminating, we remove it from being considered as a preemption target. This ensures the head can choose other preemption targets. Also probably emit a metric to flag that its stuck. 
      - https://github.com/kubernetes-sigs/kueue/issues/6489
      - https://github.com/kubernetes-sigs/kueue/issues/6490
3. Propose a KEP for depth of Kueue processing. ie, processing multiple workloads within 1 CQ during a schedule() invocation; (my proposal you're evaluating at a high level)

Thanks for your time! 🙏

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-07T06:37:06Z

> Yeah after chatting with my team... here's what I propose tactically:

Happy to see the tactical, step by step approach :) 

Actually I expect that after solving the horizontal blocking the vertical will be less problematic, because the waiting for the CQ head to get scheduled will be shorter, and thus the time to process the next one in the CQ.  

So I think it makes sense to re-evaluate the decision and approach for vertical blocking after we have more production data.

> Here's the scenario: We have a pod stuck in terminating. This blocks its own CQ for hours.

Why would it be so though? Hours sound like a lot, I suspect Pod misconfiguration, maybe some users set very high spec.terminationGracePeriodSeconds - you could enforce it as a policy to have spec.terminationGracePeriodSeconds < 5min (let's say) by VAP (validating admission policies).

Actually, this would remain a problem even if we implement the horizontal and vertical optimizations, because even with this optimizations we would assume the terminating pod eventually releases the quota - we would just start to preempt other workloads earlier. So this seems like related, but not exactly the same class of problem, I see it as:
- optimize time to trigger horizontal preemptions
- optimize time to trigger vertical preemptions
- handle workloads which are "stuck" in terminating state (new)

> As a stopgap, let's implement a timeout where if the pod has been stuck in terminating, we remove it from being considered as a preemption target. This ensures the head can choose other preemption targets. 

It may require some more clarification on the exact issue it is aiming to solve (previous comment). The timeout most likely will also require a KEP as it would require configuration in the API (iiuc).

> Also probably emit a metric to flag that its stuck.

Sounds reasonable, but maybe a metric measuring how long a workload is Pending at the head of the queue? It is not exactly the same, but "stuck" waiting for preemption may be tricky to define as in different scheduling cycles it may actually be assigned to different flavors.

### Comment by [@amy](https://github.com/amy) — 2025-08-07T12:55:27Z

> Why would it be so though? Hours sound like a lot, I suspect Pod misconfiguration, maybe some users set very high 

Termination grace period is set to 15min. But the pods can still be in a state where there's a zombie process that sticks around preventing the pod from terminating after the 15min. 

> Actually, this would remain a problem 

Sorry I wasnt clear about separating the issues. Yes this is blocking even if we process the queue vertically. So its:
1. Slow queue processing is still a separate issue we'd still like to solve.
2. We at least want to prevent the queue from being entirely blocked if a zombie pod fails to terminate

> The timeout most likely will also require a KEP 

sounds good

>  a metric measuring how long a workload is Pending at the head of the queue

Ah okay,
Cool I'll do this: `a metric measuring how long a workload is Pending at the head of the queue` -> https://github.com/kubernetes-sigs/kueue/issues/6496
And also combine with this: https://github.com/kubernetes-sigs/kueue/issues/6122 "Metric that measures time between eviction and actual preemption " We can probably set an alert when termination has lasted for longer than say... 16min. Then correlate the 2 on our end.

### Comment by [@samos123](https://github.com/samos123) — 2025-09-02T17:27:37Z

We've seen pods stuck in terminating when the node goes away suddenly (non-gracefully). Pod being stuck in terminating can last for up to an hour even if terminationGracePeriod is set to 60 seconds. This is also happening while using jobset.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-01T17:52:25Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-31T18:23:09Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-30T19:11:36Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-30T19:11:42Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6143#issuecomment-3825261359):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tskillian](https://github.com/tskillian) — 2026-02-04T21:49:10Z

The kubernetes scheduler evicts pods without waiting for them to fully terminate. Could kueue accomplish the same by having evicted workloads release quota as soon as they're evicted instead of when they are fully terminated?

See https://github.com/kubernetes-sigs/kueue/pull/8992

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-05T05:24:41Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-05T05:24:46Z

@mbobrovskyi: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6143#issuecomment-3851160727):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-05T05:25:01Z

/remove-lifecycle rotten
