# Issue #6929: Workload scheduling failure when preemption (reclaimWithinCohort) is required and cluster queue head has not-schedulable workload(s).

**Summary**: Workload scheduling failure when preemption (reclaimWithinCohort) is required and cluster queue head has not-schedulable workload(s).

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6929

**Last updated**: 2025-10-17T15:38:47Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2025-09-20T05:47:12Z
- **Updated**: 2025-10-17T15:38:47Z
- **Closed**: 2025-10-08T13:17:02Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 23

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
When a workload is **not schedulable** in a ClusterQueue(CQ), other pending workloads in the same CQ that should be admitted via preemption are never scheduled.

**What you expected to happen**:
Job's workload is admitted.

**How to reproduce it (as minimally and precisely as possible)**:

### Setup

**Cohort**: `demo`

**ClusterQueues**

*CQ1*

```yaml
cohort: demo
reclaimWithinCohort: Any
resourceGroups:
- coveredResources: [cpu]
  flavors:
  - name: default-flavor
    resources:
    - name: cpu
      nominalQuota: 3
      borrowingLimit: 0  # nothing borrowed
```

*CQ2*

```yaml
cohort: demo
reclaimWithinCohort: Any
resourceGroups:
- coveredResources: [cpu]
  flavors:
  - name: default-flavor
    resources:
    - name: cpu
      nominalQuota: 0
      borrowingLimit: 3  # everything is borrowed
```

**LocalQueues**: `lq1` (CQ1), `lq2` (CQ2)

**Workloads**

* `job-1`: queue=`lq2`, request `cpu=1`
* `job-2`: queue=`lq2`, request `cpu=1`
* `job-3`: queue=`lq1`, request `cpu=4` *(unsatisfiable, >3 capacity)*
* `job-4`: queue=`lq1`, request `cpu=3`

All jobs have the same priority.

### Repro Steps
* _UPD: even smaller repro is posted in the [comment](https://github.com/kubernetes-sigs/kueue/issues/6929#issuecomment-3316112871) below_ 

Submit jobs in this order:

1. `job-1` → admitted
2. `job-2` → admitted
3. `job-3` → pending *(insufficient quota, 4 > 3)*
4. `job-4` → pending *(insufficient unused quota, needs 2 more CPU)*

At this point, periodic preemption cycles repeatedly evict `job-1` and `job-2`. However, `job-4` is **never admitted**.

#### Workaround

Deleting `job-3` (the `NoFit` workload) restores expected behavior:

* `job-1` and `job-2` are preempted
* `job-4` is admitted

### No Repro Cases

**Case 1: Submit `job-3` then `job-4`**

* `job-3`: pending (expected)
* `job-4`: admitted (expected)

**Case 2: Submit `job-1`, `job-2`, `job-4`**

* `job-1`: admitted
* `job-2`: admitted
* `job-4`: admitted, with `job-1` and `job-2` preempted (expected)

**Anything else we need to know?**:

* Preemption should allow `job-4` to be admitted even when a `NoFit` workload (`job-3`) exists in the same cohort.
* The presence of an unschedulable workload should not block scheduling progress for other valid workloads.


**Environment**:
- Kubernetes version (use `kubectl version`):  v1.31.2
- Kueue version (use `git describe --tags --dirty --always`): v0.13.4
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-20T06:17:53Z

### Analysis / Root Cause

* In *NoRepro(2)* (no `job-3`), `job-4` consistently reaches the head of the scheduling queue.

  * Scheduler log shows `job-4` issues preemptions, then eventually gets `Fit` once preemptions complete.
  * After that, `job-1` or `job-2` is skipped as “no longer fits,” leading to stable state.

* In the **Repro case** (with `job-3` present):

  * `job-3` (`NoFit`) is always at the head of the queue, even though it cannot be scheduled.
  * This blocks `job-4` from being evaluated in a clean cycle.
  * As a result, `job-2` (or `job-1`) keeps re-admitting after each preemption cycle, while `job-4` never gets a chance to reach `Fit`.

**Key difference:**

* With no `NoFit` interference and `job-4` at the head of the queue, `job-4` proceeds as expected.
* With `NoFit` interference from `job-3` at the head of the queue, `job-4` is perpetually starved out by the scheduling order.

---

Thinking out loud about possible fix direction

Ideally, the scheduler should recognize that `job-3` has unsatisfiable resource requirements and only retry it when the resource quota definition changes — either in the resource flavors or through cohort adjustments.
That said, detecting changes in resource quota definitions may not be a trivial task.

As an alternative, a longer backoff or retry interval for `NoFit` workloads could be introduced to reduce their interference with schedulable workloads.

### Comment by [@amy](https://github.com/amy) — 2025-09-21T02:40:38Z

/cc

### Comment by [@amy](https://github.com/amy) — 2025-09-21T02:43:34Z

I'm assuming job-3 and job-4 are the same priority? If so, can you add that to the description.

### Comment by [@hiboyang](https://github.com/hiboyang) — 2025-09-21T16:13:37Z

> I'm assuming job-3 and job-4 are the same priority? If so, can you add that to the description.

Yes, it is same priority. I am testing this issue together with @ichekrygin.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-21T16:48:10Z

Updated the issue description.

Note: a more minimal repro: `job-1`, `job-3`, `job-4` (i.e. no `job-2`) leads to the same outcome where `job-4` is not admitted. 

Helpful  scheduler  cycles trace:
* `job-1` cq-1 (borrows)
* `job-3` cq-2 (no-fit)
* `job-4` cq-2 (preempts `job-1`)

After `job-1` and `job-3` are submitted with:
1. `job-1 → admitted`
2. `job-3` → pending (insufficient quota, 4 > 3)

Submitting `job-4`:
```
"schedulingCycle":65,"cq-heads":"job-4"}
"schedulingCycle":65,"processing workload":"job-4","preemption targets":"job-1"}
"schedulingCycle":65,"workload":"job-4","assigned-mode":"Preempt"}
"schedulingCycle":65,"workload":"job-4","attempting to preempt workload":"job-1"}
"schedulingCycle":65,"workload":"job-4","preempted-count":1}
---
"schedulingCycle":66,"cq-heads":"job-4"}
"schedulingCycle":66,"processing workload":"job-4","preemption targets":"job-1"}
"schedulingCycle":66,"workload":"job-4","assigned-mode":"Preempt"}
"schedulingCycle":66,"workload":"job-4","skipping preemption as ongoing workload":"job-1"}
"schedulingCycle":66,"workload":"job-4","preempted-count":1}
...
repeat of few more cycles with identical message
...
"schedulingCycle":70,"cq-heads":"job-4"}
"schedulingCycle":70,"processing workload":"job-4","preemption targets":"job-1"}
"schedulingCycle":70,"workload":"job-4","assigned-mode":"Preempt"}
"schedulingCycle":70,"workload":"job-4","skipping preemption as ongoing workload":"job-1"}
"schedulingCycle":70,"workload":"job-4","preempted-count":1}
---
"schedulingCycle":71,"cq-heads":"job-1, job-3"} // <-- job-3 attempt again, together with job-1
"schedulingCycle":71,"workload":"job-3","preemption targets":""}
"schedulingCycle":71,"workload":"job-3","assigned-mode":"NoFit"}
"skipping NoFit mode","schedulingCycle":71,"workload":"job-3"} // <-- job-3 still NoFit
-
"schedulingCycle":71,"workload":"job-1","preemption targets":""}
"schedulingCycle":71,"workload":"job-1","assigned-mode":"Fit"}
"end","schedulingCycle":71,"workload":"job-1","status":"assumed","msg":""} // <-- job-1 is scheduled
---
"schedulingCycle":72,"cq-heads":"job-4"}
"schedulingCycle":72,"processing workload":"job-4","preemption targets":"job-1"}
"schedulingCycle":72,"workload":"job-4","assigned-mode":"Preempt"}
"schedulingCycle":72,"workload":"job-4","attempting to preempt workload":"job-1"} // <-- job-4 is stuck
"schedulingCycle":72,"workload":"job-4","preempted-count":1}
...
Repeat of the above over and over.

### Comment by [@amy](https://github.com/amy) — 2025-09-21T18:21:52Z

@ichekrygin This seems like another issue within the class of "Blocking at CQ head" problems. Where you want a mechanism to process beyond the CQ head. Or in this case, set aside an inadmissible head.

(Also thinking out loud, so these are loose ideas)
I wonder... if there's a way to rethink `nomination`. Where... per CQ, when you select "head", you...
1. continue popping until you find one admissible head
2. also stop when the priority is different from head

So you still end up with just 1 head per CQ selected as the scheduling algorithm works today. This way, you won't need to...
1. detect state changes
2. have time based backoff which could introduce CQ unfairness between priorities in 1 CQ. (ie, what if you have a p1 workload that backs off, then a p2 workload slips in during that time interval. Would violate fundamental priority ordering in CQ.)

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-21T18:53:10Z

> This seems like another issue within the class of "Blocking at CQ head" problems. Where you want a mechanism to process beyond the CQ head. Or in this case, set aside an inadmissible head.

Yes, this is similar to the “head-of-the-queue blocker” issue. Although in this case the queue is not completely blocked, the head workload `job-3` interferes with scheduling by letting jobs from other ClusterQueues get re-admitted, specifically, the very jobs that were preempted by the subsequent workload in the ClusterQueue where `job-3` resides.

Thinking out loud: one possible direction would be to prevent preempted workloads from re-entering the scheduling cycle **as long as** the _**preemptor**_ workload is still in the queue (i.e., not yet admitted).

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-21T19:09:56Z

The repro above involves an edge case, submitting a job (`job-3`) with clearly unsatisfiable resource capacity. In practice, guardrails like *“don’t submit jobs that exceed queue capacity”* or *“just delete that job”* could serve as possible workarounds.

That said, it’s important to note that the same **head-of-the-queue interference** can occur even when the head workload does not exceed ClusterQueue capacity, but still cannot be admitted for other reasons (e.g., waiting for earlier jobs in the same queue to complete).

**Example repro:**

* `cq-1` (nominal: 0 CPU, borrows: 3CPU)
* `cq-2` (nominal: 3 CPU, borrows: 0CPU)

---
All jobs have the same priority.

* `job-1` → `cq-1` (borrows)
* `job-2` → `cq-2` (1.5 CPU) admitted // no preemption necessary
* `job-3` → `cq-2` (2 CPU) pending // requires `job-2` to complete
* `job-4` → `cq-2` (1.5 CPU) // requires `job-1` preemption and  **should be admitted, but isn’t**

Removing `job-1` unblocks `job-4`.

### Comment by [@hiboyang](https://github.com/hiboyang) — 2025-09-23T01:35:15Z

+1 for "one possible direction would be to prevent preempted workloads from re-entering the scheduling cycle as long as the preemptor workload is still in the queue (i.e., not yet admitted)".

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-09-23T12:58:39Z

I talked to @gabesaba about this issue and seems like in both queueing strategies we're going to have issues. 

My understanding is that with `BestEffortFIFO` workloads are going to flap indefinitely and even though I partially agree with `Although in this case the queue is not completely blocked` the queue will be blocked because the workloads will be continuously preempted and re-tried which effectively leads to a blockage. With `StrictFIFO` the queue will be just deadlocked without any chance of getting unblocked.

Wouldn't the scenario `one possible direction would be to prevent preempted workloads from re-entering the scheduling cycle as long as the preemptor workload is still in the queue (i.e., not yet admitted)` cause a blockage too? I might be missing something but it sounds to me like the smaller workloads wouldn't be retried as long as the big blocking workload would be there which leads to a similar scenario as with `StrictFIFO`. In the given scenario wouldn't the preemptor `job-3` block other smaller jobs?

@gabesaba proposed a solution where we'd have some backoff mechanism to just inactivate a workload after we realize a couple of times that it's completely unschedulable.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-23T15:01:27Z

> Wouldn't the scenario one possible direction would be to prevent preempted workloads from re-entering the scheduling cycle as long as the preemptor workload is still in the queue (i.e., not yet admitted) cause a blockage too? 

In the current repro, when the “borrowing” CQ (cq2) is empty, the issue doesn’t occur. I think the core problem is that cq1 has a workload at the head that blocks or interferes with scheduling cycles. Specifically, previously preempted workloads from cq1 can “sneak in” when the unschedulable workload at the head of cq2 is retried in subsequent scheduling cycles.

The “unschedulable” state of the head workload can be either temporary (e.g., waiting for other workloads to complete) or permanent (e.g., exceeding CQ quota, even with borrowing).

I first considered introducing progressive backoff/retry for head workloads as a workaround. But the concern is that since there’s no practical limit on how many unschedulable workloads can precede an eligible (schedulable) workload in the queue, this would at best *mitigate* the issue rather than fully resolve it.

What seems needed instead is a more insightful mechanism that can introspect the CQ beyond just the head when selecting workloads for a scheduling cycle. Simply peeking at the head is insufficient. Retry/backoff might help rotate heads within a CQ, but it, most likely, will not provide a guarantee.

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-09-23T15:31:55Z

Got it. Thanks for the explanation @ichekrygin!

It sounds like a lot of work though and this would probably require significant changes to the scheduling logic. I'm a bit concerned that we have issues pilling up which require significant changes in Kueue's scheduler (`head-of-the-queue blocker` issues). Unless we tackle them all with a small number of changes I'm worried we might need to spread them over time not to cause significant issues and frequent changes in scheduling behavior.

CC @amy @mimowo @gabesaba @tenzen-y

### Comment by [@amy](https://github.com/amy) — 2025-09-23T16:31:36Z

Can we consider this suggestion (or point out issues with it 🙏): https://github.com/kubernetes-sigs/kueue/issues/6929#issuecomment-3316170804 -> though this also doesn't solve the core of head of queue blocking problems.

Its not a large deviation from how Kueue scheduling works today (ie. we will still just nominate 1 head per CQ, "head" becomes more flexible).

### Comment by [@pajakd](https://github.com/pajakd) — 2025-09-25T16:17:40Z

I tend to agree with https://github.com/kubernetes-sigs/kueue/issues/6929#issuecomment-3316170804 -- I don't see any major issues (except perhaps implementation difficulties). But let me think a bit more on this.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-02T07:27:45Z

I think https://github.com/kubernetes-sigs/kueue/issues/6929#issuecomment-3316170804 is tricky actually. Because "nomination" only happens for heads, so it seems like a lot of work. Also, the drilling of the CQ may not only be driven by "priority", but also DRS, etc. This makes it error prone.

So, I would like to consider an alternative to introduce a new enum value like "NeverFit" (stronger than "NoFit") which would be used for the `job-3` from the issue description as it can never get admitted even if the other workloads complete. 
The "NeverFit" jobs could be moved to "inadmissibleWorkloads" (or even deactivated). Then, the `job-4` will be moved to head. Seems like also easier to reason about when debugging.  Let me know if this is not enough.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-10-02T12:27:34Z

I have a proposal which should solve this issue and #7101:

When `BestEffortFIFO` is enabled, we make the head of the queue sticky. That is, we keep trying to schedule it until the workload is admitted or the scheduling cycle returns a signal that it is inadmissible.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-02T12:38:23Z

Sounds good in principle, and I can see it fixing the issue 👍 

One possible consideration is dynamic setup, when a new high priority (or low DRS) workload comes in the meanwhile, that has not been considered yet. IIUC ideally we would give up the stickiness and let it in. OTOH the system should reach eventual consistency after admitting the sticky head, and evicting by the new workload, which is the important property.

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-10-02T17:16:39Z

@gabesaba @mimowo  What about situations where a workload is inadmissible right now, but it might be admissible later e.g. the quota was raised?

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-10-03T10:25:10Z

> [@gabesaba](https://github.com/gabesaba) [@mimowo](https://github.com/mimowo) What about situations where a workload is inadmissible right now, but it might be admissible later e.g. the quota was raised?

This workload will be processed once the head either proves inadmissible or successfully schedules. With my proposed solution, we will not boot the head out of place for this workload (after, for example, quota is raised), even if it is higher priority.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-10-03T16:48:12Z

> With BestEffortFIFO enabled, the scheduler makes the head of the queue sticky. In other words, it keeps trying to schedule the head workload until it is admitted, or the cycle determines it is inadmissible.

Applied to the reproduction:

* `job-1` in `cq-1` (borrows)
* `job-3` in `cq-2` (no-fit)
* `job-4` in `cq-2` (should preempt `job-1`)

Submission order and outcomes:

1. `job-1` → admitted
2. `job-3` → pending, insufficient quota, needs 4 but only 3 available
3. `job-4` → pending

**Problem:** when `job-4` tries to schedule by preempting `job-1`, `job-3` periodically re-enters the cycle. That lets `job-1` get re-admitted, so the preemption for `job-4` never completes. `job-4` is effectively starved.

**Proposed behavior under sticky head:** once the scheduler selects `job-4` and initiates eviction of `job-1`, `job-4` remains pinned at the head of the queue until the preemption of `job-1` completes and capacity frees for `job-4`. In other words, `job-3` does not re-enter the queue head while `job-4` is in flight.

**Is this interpretation correct?**

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-10-08T13:17:00Z

> Is this interpretation correct?

Yes, that is correct. There are some new test case which cover your scenario in #7157. See [these test cases](https://github.com/kubernetes-sigs/kueue/blob/1ea074de47d0f5c4a751cc8f62764bfbf117c3e0/test/integration/singlecluster/scheduler/fairsharing/fair_sharing_test.go#L812-L951).

We released this as part of 0.13.6, and 0.14.1.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-10-15T19:31:49Z

> Proposed behavior under sticky head: once the scheduler selects job-4 and initiates eviction of job-1, job-4 remains pinned at the head of the queue until the preemption of job-1 completes and capacity frees for job-4. In other words, job-3 does not re-enter the queue head while job-4 is in flight.

@gabesaba, In that case, wouldn’t the “sticky” job-4 effectively block other eligible jobs in the same queue while it’s waiting for the preemption to complete?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-17T15:38:47Z

Gabe is ooo until 27th Oct. Yes, I think this is what will happen.
