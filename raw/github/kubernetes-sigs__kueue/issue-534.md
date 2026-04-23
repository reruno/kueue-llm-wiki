# Issue #534: Prevent starvation of large jobs

**Summary**: Prevent starvation of large jobs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/534

**Last updated**: 2023-05-03T15:16:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2023-01-30T03:20:46Z
- **Updated**: 2023-05-03T15:16:16Z
- **Closed**: 2023-05-03T15:16:16Z
- **Labels**: `kind/feature`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 11

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Workloads with the same priority don't preempt each other within a ClusterQueue, one consequence is that large size jobs may be starved if users submit a stream of smaller jobs from the same priority class. 

To address this case, we could add a preemption strategy that allows older jobs to preempt newer ones from the same priority class.

**Why is this needed**:

To prevent starvation of large jobs via preemption. 

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-30T17:44:06Z

The field `TriggerAfterWorkloadWaitingSeconds` in [1] was a proposal along these lines. Any extra signal we can incorporate in a new design?

[1] https://github.com/kubernetes-sigs/kueue/tree/main/keps/83-workload-preemption#extra-knobs-in-clusterqueue-preemption-policy

### Comment by [@ahg-g](https://github.com/ahg-g) — 2023-01-30T18:02:15Z

Yes, so smaller jobs that were submitted after the big job, but got a chance to start before the big one because they happen to fit, should be the primary candidates for preemption. 

Imagine this example (all jobs from the same priority class):
1) quota is 100
2) job1 and job2 each consumes 30; available quota is 40
3) job3 submitted and requests 50, it doesn't fit and will wait
4) job4 submitted and requests 30, it fits and will start; available quota is 10
5) job1 finishes, available quota is 40, so job3 still doesn't fit, but we can preempt job4 to fit it; job4 is a candidate because it was submitted after job3.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-30T18:12:12Z

Gotcha, the creation timestamps for each Jobs is a very clear signal.

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-04-18T07:44:20Z

Maybe we can add a property in clusterQueue to allow workload preempting workloads with same priority after some time?

### Comment by [@trasc](https://github.com/trasc) — 2023-04-19T14:27:31Z

/assign

### Comment by [@trasc](https://github.com/trasc) — 2023-04-20T09:04:39Z

A middle ground between this and `TriggerAfterWorkloadWaitingSeconds` could be something like:
```go
	// PreemptIfNewerThen if set, jobs with the same priority having a scheduling timestamp
	// bigger than the current workload + PreemptIfNewerThen seconds will be
	// considered for preemption in order to avoid starvation of large jobs.
	// This is only applicable within the same cluster queue when WithinClusterQueue
	// is set to LowerPriority.
	//
	// +optional
	PreemptIfNewerThen *int64

```

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-20T16:02:43Z

This should be a Clusterqueue API field.
I like the flexibility of the proposal above. However, the wording needs to include that this affects the same priority. And maybe that this is specific to ClusterQueue preemption, and not cohort reclaim? does it have to be?

Also, do we expect more tuning options? If so, it could be something like:

```yaml
preemption:
  withinClusterQueue: LowerThanOrEqualPriority
  samePriority:
     ifNewerThanSeconds: 100
```

Although I'm not convinced about the wording

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-21T09:28:33Z

Let's step back.
@KunWuLuan, do you have a use case for configuring the time threshold?
We could start simple and just add the policy for LowetThanOrEqualPriority

### Comment by [@trasc](https://github.com/trasc) — 2023-04-21T14:25:50Z

I have opened #710, but I'd hold the merge and use workload.GetSchedulingTimestamp after #689 is merged.

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-04-23T11:11:48Z

> Let's step back. @KunWuLuan, do you have a use case for configuring the time threshold? We could start simple and just add the policy for LowetThanOrEqualPriority

Hi, Aldo. I think `ifNewerThanSeconds ` is enougth. Thanks. 👍

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-24T17:47:10Z

My question was whether we could start without `ifNewerThanSeconds`.
Can you clarify why do you think this is important?
Could there be other alternatives that apply to any kind of preemption? Like `TriggerAfterWorkloadWaitingSeconds` in [1]
Or something like `IfAdmittedLessThanSeconds`.

[1] https://github.com/kubernetes-sigs/kueue/tree/main/keps/83-workload-preemption#extra-knobs-in-clusterqueue-preemption-policy
