# Issue #6772: Improve emitting logs and metrics in the HA setup

**Summary**: Improve emitting logs and metrics in the HA setup

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6772

**Last updated**: 2025-12-17T08:38:10Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mwysokin](https://github.com/mwysokin)
- **Created**: 2025-09-09T12:57:18Z
- **Updated**: 2025-12-17T08:38:10Z
- **Closed**: 2025-12-17T08:38:10Z
- **Labels**: `kind/feature`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 9

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
I'd like to propose that we modify our existing HA behavior where we all Kueue replicas in a multi-replica setup emit logs and metrics. A solution to that would be to stop emitting logs and metrics from follower replicas or to have some kind of field in the logs and metrics to know whether they come from the leader or the followers.

**Why is this needed**:
Because we don't attach any information to the logs whether they were emitted by the leader or followers it gets unnecessarily noisy when browsing or searching through logs.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-09-14T04:31:08Z

/cc

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-10-07T12:51:33Z

@mimowo @tenzen-y WDYT?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-07T12:54:32Z

For the scheduler and controller, we can emit the logs, I guess.
But, for webhook servers, it would be better to keep output logs since in HA mode, all webhook server replicas actually process and handle requests.

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-10-07T12:55:53Z

What if we always have a tag that states whether the log was emitted by the leader or followers?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-07T13:04:17Z

> What if we always have a tag that states whether the log was emitted by the leader or followers?

That seems helpful to understand logs more precisely.
Once we implement the mechanism to dynamically obtain the information on whether the replica is a leader or a follower, we can provide the replica role information throughout loggers.
Because the loggers are initialized in the manager startup phase.
So I guess we need to reinitialize loggers based on leader replica change events.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-07T13:06:10Z

> A solution to that would be to stop emitting logs and metrics from follower replicas or to have some kind of field in the logs and metrics to know whether they come from the leader or the followers.

Let's go with the second proposal of the field. The logs from followers may still be useful because:
- the followers execute the webhook code
- the followers keep track of the cache events, so if cache gets out of sync we want to have a tool to investigate why

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-08T07:33:10Z

Ok, so there is the `LogConstructor` option which could be used when wiring a controller, eg [here](https://github.com/kubernetes-sigs/kueue/blob/ad4a71fd5b93bdc2dc57cdfbd9d34eb9c638f3af/pkg/controller/core/cohort_controller.go#L101-L104).

It would require also Kueue to get into the leader election "state" changes, but should be possible.

Alternatively, I'm wondering if there is an option to add this capability to the controller-runtime as "native". controller-runtime already injects a bunch of key-value pairs and is aware of the leader election.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-08T08:17:24Z

x-referencing the question: https://github.com/kubernetes-sigs/controller-runtime/issues/3342

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-12-02T14:24:49Z

/assign
