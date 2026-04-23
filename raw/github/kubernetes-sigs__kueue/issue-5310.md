# Issue #5310: Reconciliation logic should not happen in predicates

**Summary**: Reconciliation logic should not happen in predicates

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5310

**Last updated**: 2026-02-06T14:04:01Z

---

## Metadata

- **State**: open
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2025-05-22T08:57:27Z
- **Updated**: 2026-02-06T14:04:01Z
- **Closed**: —
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 17

## Description

**What would you like to be cleaned**:
In some controllers such as [ClusterQueue](https://github.com/kubernetes-sigs/kueue/blob/2484ec74226aa47271e037d2457e8ad7045c8e02/pkg/controller/core/clusterqueue_controller.go#L319-L338) and Workload, we perform some reconcillation logic in the event filters. Compare this to [Cohort Controller](https://github.com/kubernetes-sigs/kueue/blob/2484ec74226aa47271e037d2457e8ad7045c8e02/pkg/controller/core/cohort_controller.go#L107-L127), where the event filter decides whether a reconciliation is needed

This is especially problematic when the logic may throw an error

**Why is this needed**:
Errors are being swallowed by filters, and not retried. If we had logic which may throw errors in the Reconciler, we could solve #5276 by having the TASCache throw an error

## Discussion

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-05-22T08:57:35Z

cc @mimowo

### Comment by [@adoi](https://github.com/adoi) — 2025-05-30T13:43:43Z

@mimowo / @gabesaba  is this already under progress? I can take a look here if needed.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-30T13:46:45Z

No it is ready to be grabbed, but we are not yet fully committed to the final shape of the solution, so please share early PR and thoughts for early feedback.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-30T16:04:38Z

It looks like `filiter` indicates predicates.

/retitle Reconciliation logic should not happen in predicates

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-30T16:06:45Z

@gabesaba @mimowo Do we look for ways to re-trigger reconciliation instead of just ignoring when predicates face any errors?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-28T17:02:29Z

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

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-09-01T12:45:12Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-16T08:22:52Z

Maybe it is important to decompose the problem. I would probably suggest focusing on this place specifically: https://github.com/kubernetes-sigs/kueue/blob/39ac24559f93bba69d6b74098dd04de3a336c4e6/pkg/controller/core/workload_controller.go#L625. 

I believe this is the source of issues on Kueue reboot, so this would not be just cleanup, but bugfix if proven.

### Comment by [@Singularity23x0](https://github.com/Singularity23x0) — 2025-10-07T14:28:55Z

/assign

### Comment by [@Singularity23x0](https://github.com/Singularity23x0) — 2025-10-09T09:32:43Z

Core controllers (`pkg/controller/core/`) identified to have reconciliation logic embedded in predicates:

* `admissioncheck_controller.go`
* `clusterqueue_controller.go`
* `localqueue_controller.go`
* `resourceflavor_controller.go`
* `workload_controller.go`

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-09T10:01:44Z

Let's focus on the workload_controller, I think this the most involving

### Comment by [@Singularity23x0](https://github.com/Singularity23x0) — 2025-10-15T12:34:08Z

Upon researching the contents of the controller, I can see that the reconciliation logic differs significantly depending on whether we create, update or delete - do we have a way to assume what is the case in the "Reconcile" method specifically? I know we don't get that information by design, so what are the condition describing what is happening to the workload that can help infer whether the workload is being created, updated or deleted?

### Comment by [@Singularity23x0](https://github.com/Singularity23x0) — 2025-10-30T14:29:45Z

> Maybe it is important to decompose the problem. I would probably suggest focusing on this place specifically:
> 
> [kueue/pkg/controller/core/workload_controller.go](https://github.com/kubernetes-sigs/kueue/blob/39ac24559f93bba69d6b74098dd04de3a336c4e6/pkg/controller/core/workload_controller.go#L625)
> 
> Line 625 in [39ac245](/kubernetes-sigs/kueue/commit/39ac24559f93bba69d6b74098dd04de3a336c4e6)
> 
>  log.V(2).Info("ignored an error for now", "error", err) 
> .
> I believe this is the source of issues on Kueue reboot, so this would not be just cleanup, but bugfix if proven.

Based on research done utilizing the #5276 test, the issue mentioned seems to occur for the same order of the "Create" predicate calls for the workloads (1 and 2) and the queues (local and cluster).

Running multiple iterations of the test without the step creating the 3rd, auxiliary workload (wl3), the test proved to be both successful and unsuccessful for the same event configurations:

* when the specific parts of the "Create" predicates for the inadmissible workload and local queue were run in the same order, in both cases the addition of the local queue (indicated by acquiring a lock on the queue manager) happening before the addition of the second workload (as indicated by it being granted the lock).
* with the cluster queue being recreated last,
* with the wl1 (the admitted workload) being recreated before the cluster queue, as such not performing any changes to the queues nor cache.

As such the bug seems to be more complex and the refactor is unlikely to be the only thing needed for the bug to be resolved.

### Comment by [@Singularity23x0](https://github.com/Singularity23x0) — 2025-10-30T14:47:27Z

One thing that seems to be consistent for each failing run is that upon the update of the admitted workload to the finished status, the cluster queue is consistently missing the inadmissible workload from its "inadmissibleWorkloads" list (see https://github.com/kubernetes-sigs/kueue/blob/94aa4c112962110377fb63f701bcbfd928b1ebe2/pkg/cache/queue/manager.go#L535 -> https://github.com/kubernetes-sigs/kueue/blob/94aa4c112962110377fb63f701bcbfd928b1ebe2/pkg/cache/queue/manager.go#L601)

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-09T15:24:24Z

Once we move some predicate logics to the reconciler, which could occur, reconcile request requeuing in case of errors during reconciliations.

It will increase the number of processing reconciliations, increase the number of attempts to take the cache lock, and eventually might cause a deadlock for the cache Lock.
So, we might need to make our cache locks more fine-grained.

But, basically, I agree with this approach.

### Comment by [@Singularity23x0](https://github.com/Singularity23x0) — 2026-02-06T14:03:41Z

Status:
- Currently was able to move the logic form the Delete predicate of WorkloadController to the Reconcile.
- Doing a more widespread rework requires a comprehensive design of updating all of our core controllers with the following issue in mind:
   1. The logic in the Predicates and Event handlers behaves differently based on what event has occurred (including what exactly changed when an update was performed) - it is not possible to move the logic directly as is without losing the idempotency of the Reconcile.
   2. Kueue uses two separate sources of truth: the state of kubernetes objects and the data in the cache (queue cache and scheduler cache). Currently access to them is not synced and they are accessed in multiple places across Kueue.

An example of how issue (ii) could be problematic is when moving the Backoff handling form the Update predicate to the Reconciler, we allow for the following issue to occur:
1. We add wl with missing lq.
2. Reconciler marks wl as inadmissible.
3. lq becomes active -> we add the wl to the queue cache
4. Reconciler begins an update to the wl - it gets it in state Pending form the Client.
5. In the meantime scheduler schedules the wl. It updates the caches (moves wl form queue cache to scheduler cache) and sends the update to the Client.
6. Reconciler continues, overriding the caches: wl is Pending, so it adds it to the queue cache (where it is missing) and removes it from scheduler cache (where it was placed).
7. Scheduler begins another cycle, retrieving the wl again from the queue cache, and schedules it for a second time -> BUG

### Comment by [@Singularity23x0](https://github.com/Singularity23x0) — 2026-02-06T14:03:58Z

/unassign
