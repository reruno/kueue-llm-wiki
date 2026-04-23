# Issue #1741: Expose an eviction / re-queue related prometheus metric

**Summary**: Expose an eviction / re-queue related prometheus metric

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1741

**Last updated**: 2024-05-08T19:12:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@astefanutti](https://github.com/astefanutti)
- **Created**: 2024-02-15T17:18:35Z
- **Updated**: 2024-05-08T19:12:55Z
- **Closed**: 2024-05-08T19:12:55Z
- **Labels**: `kind/feature`
- **Assignees**: [@lowang-bh](https://github.com/lowang-bh)
- **Comments**: 9

## Description

**What would you like to be added**:

A Prometheus metric that exposes the number of evicted / inactive workloads, per cluster queue, and per eviction reasons, e.g., preempted, readiness timeout, admission check down, become inactive, or cluster queue stopped.

**Why is this needed**:

The `pending_workloads` metric exposes the current number of pending workloads that are either active or inadmissible, but does not provide any finer-grained visibility to monitor eviction / re-queuing. 

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-21T12:33:32Z

oh, big +1

Are you suggesting 2 metrics? One for eviction and one for requeue?

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-03-22T16:49:58Z

My current thinking is:
* One metric for eviction, with a reason label, e.g.:
    ```
    prometheus.NewGaugeVec(
		prometheus.GaugeOpts{
			Name: "evicted_workloads",
		},
		[]string{"cluster_queue", "reason"},
	)
    ```
* Maybe, one metric for re-queuing attempts, like an histogram with the number of attempts, e.g.:
    ```
    prometheus.NewHistogram(
		prometheus.HistogramOpts{
			Name:           "workload_requeueing_attempts",
			Buckets:        metrics.ExponentialBuckets(1, 2, 5),
		},
		[]string{"cluster_queue", "attempts"},
	)
    ```
* Should _inactive_ workloads, either by manual deactivation or exceeding re-queueing backoff limit, be also observed? If yes, what would be the best approach? Would adding an `inative` label to the `pending_workloads` make sense?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-22T17:05:38Z

> Maybe, one metric for re-queuing attempts, like an histogram with the number of attempts.

I'm not sure what you propose to record: how many attempts we did before admitting a workload?

If it is just the number of requeues, then shouldn't it be a counter?

> Should inactive workloads, either by manual deactivation or exceeding re-queueing backoff limit, be also observed? If yes, what would be the best approach? Would adding an inative label to the pending_workloads make sense?

I think it's better to put them in a separate metric.

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-03-22T17:14:37Z

> > Maybe, one metric for re-queuing attempts, like an histogram with the number of attempts.
> 
> I'm not sure what you propose to record: how many attempts we did before admitting a workload?
> 
> If it is just the number of requeues, then shouldn't it be a counter?

More the distribution, by number of attempts / re-queue count, of workloads that are currently being evicted and pending re-enqueue, waiting for the backoff duration. Does that make sense?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-22T17:29:05Z

I'm not sure that's how a histogram works. Once you call `Observe`, there is no taking back, that is, when the workload is admitted.

Are you thinking more of a combination of a histogram and a gauge?

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-03-22T18:05:19Z

Right, I see what you mean. A histogram samples observations as these are made (not the state at a point in time), so that'd be more the re-queuing events that'd be observed.

So that'd indeed be closer to what you've said, the re-enqueued workloads, distributed by the number of previous attempts, but I'm not sure if that's the right approach.

Yet I still think having a metric that'd make the number of accrued attempts visible (one way or another) would be useful for the "understandability" of the system behavior.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-22T18:14:19Z

I'm open to other suggestions, but if the usability isn't clear, we can leave it for later.

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-03-22T18:19:49Z

Agreed, a metric for eviction alone would be a good improvement.

### Comment by [@lowang-bh](https://github.com/lowang-bh) — 2024-04-05T14:10:26Z

/assign
