# Issue #5590: Kueue Scheduler getting stuck if preemption request fails

**Summary**: Kueue Scheduler getting stuck if preemption request fails

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5590

**Last updated**: 2025-11-21T16:12:36Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-09T15:13:58Z
- **Updated**: 2025-11-21T16:12:36Z
- **Closed**: 2025-11-21T16:12:36Z
- **Labels**: `kind/bug`
- **Assignees**: [@olekzabl](https://github.com/olekzabl)
- **Comments**: 12

## Description

**What happened**:

When IssuePreemptions returns an error, and there are no successfully preempted workloads, then scheduler "gives up" and does not retry. 

**What you expected to happen**:

Scheduler to retry regardless if there were any successful preemptions or not. Surprisingly scheduler would retry if there are some.

Here is the code in question: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/scheduler.go#L266-L273

**How to reproduce it (as minimally and precisely as possible)**:

Inject an random error for the preemption request like [here](https://github.com/kubernetes-sigs/kueue/pull/5589/files#diff-cd44f6e671ae7fdc7882224c13986f4b1b98e1ea45f65bdbcc9ae185d8e91496R195-R197)

**Anything else we need to know?**:

This bug was discovered when investigating https://github.com/kubernetes-sigs/kueue/issues/5511

This may not be a huge issue for production systems with a constant inflow of Jobs which would trigger scheduling, but it might be a very hard to debug situation if there is no inflow - say the admin sent "hero" job and is observing the system.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-09T15:14:09Z

cc @gabesaba @PBundyra

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-07T15:24:50Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-09-08T09:24:53Z

/remove-lifecycle stale

### Comment by [@Manish4044](https://github.com/Manish4044) — 2025-09-18T17:31:52Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-06T10:19:54Z

/unassign Manish4044
since there is no progress reported for 3 weeks or so, and this items is on our radar as important

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-11-12T14:01:49Z

/assign

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-11-14T13:00:40Z

I'm assuming that:

* The fix should only apply to `BestEffortFIFO`, not to `StrictFIFO`.
* Fully-failed preemptors shouldn't get sticky (in the sense of #7157). \
  (While we can afford "blocking" the queue for the time of waiting for preemption(s) to complete, I imagine "failing preemption" is a situation which may hold for longer, or even be non-retryable, so blocking the queue for so long would be wrong).

Please speak up if these assumptions are wrong.

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-11-14T13:01:54Z

Also @mimowo let me check if I correctly understood these parts of your earlier comments:

> then scheduler "gives up" and does not retry

> This may not be a huge issue for production systems with a constant inflow of Jobs which would trigger scheduling, but it might be a very hard to debug situation if there is no inflow

At first, these sounded to me as if the problem was in not scheduling subsequent scheduler cycle(s).

However, AFAICS, subsequent cycles do happen anyway: whenever we reach the code where preempting _may fail_

https://github.com/kubernetes-sigs/kueue/blob/36e330ef5aa07ec20157cd523805cd173dac488b/pkg/scheduler/scheduler.go#L299-L307

then - AFAICS - the only options to return from `schedule()` are these:

https://github.com/kubernetes-sigs/kueue/blob/36e330ef5aa07ec20157cd523805cd173dac488b/pkg/scheduler/scheduler.go#L371-L374

so subsequent scheduler cycles are going to happen ~soon, regardless of "inflow".

IIUC the real difference is in _how_ we do requeue the unsuccessful preemptor: depending on the `requeueReason` (set to `PendingPreemption` if any preemption succeeded, left empty otherwise), we flip the boolean param here

https://github.com/kubernetes-sigs/kueue/blob/36e330ef5aa07ec20157cd523805cd173dac488b/pkg/cache/queue/cluster_queue.go#L544

which then controls whether the workload will land in the "proper queue" or "inadmissible waitroom" here:

https://github.com/kubernetes-sigs/kueue/blob/36e330ef5aa07ec20157cd523805cd173dac488b/pkg/cache/queue/cluster_queue.go#L287-L296

https://github.com/kubernetes-sigs/kueue/blob/36e330ef5aa07ec20157cd523805cd173dac488b/pkg/cache/queue/cluster_queue.go#L306

In the latter case (empty `reason`, inadmissible waitroom), if there are no triggers towards rescheduling, the subsequent scheduler cycle(s) may likely hang waiting here:

https://github.com/kubernetes-sigs/kueue/blob/36e330ef5aa07ec20157cd523805cd173dac488b/pkg/cache/queue/manager.go#L656-L665

So I guess this is what you meant by "giving up & not retrying" - is that right?

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-11-14T13:08:43Z

For now, I checked that #7665 fixes @mimowo's repro from #5589.
However, I'll need to test that code more thoroughly.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-14T13:09:43Z

> The fix should only apply to BestEffortFIFO, not to StrictFIFO.

yes 

> Fully-failed preemptors shouldn't get sticky (in the sense ...

Yes, we don't have "sticky preemptions" yet at all. We only have "sticky" preemptor - the head.

> However, AFAICS, subsequent cycles do happen anyway: whenever we reach the code where preempting may fail

Yes the cycle happens, but IIUC the workload would be put into inadmissibleList, and so not part of "head"

> So I guess this is what you meant by "giving up & not retrying" - is that right?

Yes. 

> or now, I checked that #7665 fixes @mimowo's repro from #5589.

Yes, this repro should capture pretty well what I meant

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-14T13:10:38Z

Now, from my preliminary static code analysis it depends on inflow of new workloads. because a new workload will requeue all workloads in inadmissibleList, and so the workload for which preemption failed will be retried

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-11-18T23:17:11Z

Update: I extended #7665 with some draft test coverage; will now look for reviews of that.
