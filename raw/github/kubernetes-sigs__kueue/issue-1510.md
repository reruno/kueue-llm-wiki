# Issue #1510: High availability of the visibility extension API server

**Summary**: High availability of the visibility extension API server

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1510

**Last updated**: 2024-01-25T19:48:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@astefanutti](https://github.com/astefanutti)
- **Created**: 2023-12-22T09:28:13Z
- **Updated**: 2024-01-25T19:48:59Z
- **Closed**: 2024-01-25T19:48:59Z
- **Labels**: `kind/feature`
- **Assignees**: [@astefanutti](https://github.com/astefanutti)
- **Comments**: 11

## Description

**What would you like to be added**:

Enable high-availability setup for the visibility API service.

**Why is this needed**:

It's possible to deploy multiple replicas of the Kueue manager.

High-availability of admission webhooks has been fixed with #1509.

However, more work is required to enable high-availability for the visibility API service, given the stateful nature of the ClusterQueueReconciler. 

More context is available in #1509.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-26T11:28:16Z

Thanks for raising this issue. Yes, the visibility server needs to access the queuemanager in spite of the kueue-controller-manager doesn't start the queuemanager when that replica isn't primary.

I think we can select the following options:

1. Launch visibility servers separate from kueue-manager, then that server gets information from the primary kueue-manager.
2. The secondary kueue-manager gets information from the primary kueue-manager.

@alculquicondor @mimowo WDYT?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-27T14:34:30Z

Another solution would be for all managers to be able to serve the information. This is possible if every manager can react to the events to update the cache and queues, even though it wouldn't be scheduling.

We do the same in kube-scheduler.

However, I'm not sure if, in controller-runtime, event handlers are registered even if reconcilers aren't running. I would not expect so, otherwise the work queue would grow indefinitely.

Continue the comparison, in kube-scheduler we don't have reconcilers at all.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-27T18:04:12Z

> Another solution would be for all managers to be able to serve the information. This is possible if every manager can react to the events to update the cache and queues, even though it wouldn't be scheduling.
> 
> We do the same in kube-scheduler.
> 
> However, I'm not sure if, in controller-runtime, event handlers are registered even if reconcilers aren't running. I would not expect so, otherwise the work queue would grow indefinitely.
> 
> Continue the comparison, in kube-scheduler we don't have reconcilers at all.

When all managers can serve the information, is there a synchronization gap between managers In busy clusters?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-27T18:20:55Z

Yes, some managers might be ahead of others. But it shouldn't really matter, as even the output of the leader can be out of date pretty quickly.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-27T18:22:31Z

An alternate approach would be to have all webhooks running in a separate Deployment, so they can serve in HA. And then we would have the scheduler+visibility server in a different Deployment, where only one Pod can be ready at a time.

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-01-05T16:13:36Z

> Another solution would be for all managers to be able to serve the information. This is possible if every manager can react to the events to update the cache and queues, even though it wouldn't be scheduling.

That sounds like the best option functionally, and in an overall eventually consistent system, I agree it's acceptable to have some synchronisation gap between replicas, as they converge toward the stationary state. 

I just had a quick look, and it seems like it should be possible to have all the replicas serving the visibility API, with the event watchers running and maintaining the cache / queue manager, but skipping reconcilers altogether in non-leading replicas.

I can work on a PoC to validate the feasibility and share my findings.

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-01-08T13:53:09Z

/assign

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-01-09T08:14:56Z

I've open #1554, that gives an idea about the most minimal / less disruptive approach I could come up with. There may be other  ways, like separating the reconciler part from the watchers part of the controllers that contribute to the queue manager, but that felt more disruptive / risky.

I've successfully tested #1554 manually, by checking all replicas correctly serve the visibility API, also checking fail-over to a non leading replica works as expected when the leading replica terminates.

That should ideally be covered by an e2e test. I was thinking we could have a new e2e test dedicated to covering the HA aspects, including webhooks as well, to guarantee non-regression for #1445. WDYT?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-09T16:16:56Z

We can probably just configure the existing tests to run in HA mode. But we can have a separate suite package to exercise restarts.

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-01-10T08:24:15Z

Right, running existing tests in HA mode sounds like a good idea. It won't guarantee non-leading replicas work correctly, given the API server can still send traffic to the leading one. Having a separate test suite exercising HA and all replicas specifically  can mitigate that in a second step.

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-01-10T11:00:17Z

I've updated #1554 so the e2e tests deploy two replicas of the Kueue controller manager. The e2e tests pass, and we can see the two Pods for Kueue deployment in the run below, where their respective logs look correct / as expected to me:

https://gcsweb.k8s.io/gcs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1554/pull-kueue-test-e2e-main-1-29/1745014001227534336/artifacts/run-test-e2e-1.29.0/

How would you like to track the work for that dedicated HA e2e suite package? Maybe I can create a separate issue, or you have another suggestion / preference?
