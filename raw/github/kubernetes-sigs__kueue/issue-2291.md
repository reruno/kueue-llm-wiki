# Issue #2291: [WaitForPodsReady] Wrong transitions of the Requeued condition when using WaitForPodsReady

**Summary**: [WaitForPodsReady] Wrong transitions of the Requeued condition when using WaitForPodsReady

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2291

**Last updated**: 2024-06-06T11:42:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-05-28T11:16:59Z
- **Updated**: 2024-06-06T11:42:41Z
- **Closed**: 2024-06-06T11:42:41Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 14

## Description

/kind bug

**What happened**:

Deactivation (setting `.status.active: false`) is delayed unnecessarily until `Requeued: true`. This is unnecessary, because the fate of the workload is already known once the timeout is exceeded and `requeuingState.count = backoffLimitCount`.

Also, when `Requeue: true` race conditions are possible with scheduler which tries to re-admit.

**What you expected to happen**:

The workload should be deactivated as soon as it exceeds PodsReady timeout and requeuingState.count = backoffLimitCount`.

**How to reproduce it (as minimally and precisely as possible)**:

1. Enable WaitForPodsReady with the following, or analogous, config:
```yaml
      waitForPodsReady:
        enable: true
        timeout: 30s
        blockAdmission: false
        requeuingStrategy:
          timestamp: Eviction
          backoffLimitCount: 3 # null indicates infinite requeuing
          backoffBaseSeconds: 10
```
2. Create a watch for the workloads `kubectl get workload -w --output-watch-events -ocustom-columns=EVENT:.type,NAME:.object.metadata.name,ACTIVE:.object.spec.active,CONDITIONS:.object.status.conditions | ts "%Y-%m-%d %H:%M:%.S"`

3. Issue: the `active: false` is only set when `Requeued; true`, which is delayed.

**Anything else we need to know?**:

We discussed slack with @tenzen-y to implement the following flow as a bugfix:
1. increment ` requeuingState.count` to `backoffLimitCount+1`   to exceed `backoffLimitCount` when handling PodsReady timeout
2. deactivate, set `active: false`
3. set `Evicted: true` with `WorkloadInactive` condition and message

Note that 2., and 3. already happen.

We also discussed, that in a longer run, for  0.8 we may additionally introduce `DeactivatedTarget` condition to store the message.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-28T11:17:13Z

/cc @tenzen-y @alculquicondor

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-28T13:12:15Z

@mimowo Thank you for creating this issue.
This also has the advantage that we can have the same WaitForPodsReady specifications between v0.6 and v0.7 regardless of the `Requeued` condition.

In the current v0.7 implementation, we deeply depend on the `Requeued` condition. So it is challenging to keep consistency specification between v0.6 and v0.7.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-28T15:16:23Z

> We also discussed, that in a longer run, for 0.8 we may additionally introduce DeactivatedTarget condition to store the message.

This has a problem when the user tries to set `active=true` after the fact. We don't know whether the user did it or the controllers didn't have a chance to set it.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-29T07:56:17Z

We transition `active: true` to `false` whenever there is `DeactivationTraget: true`. Once we transition `active: true -> false` we add `Evicted` condition with "WorkloadInactive" reason. Along with setting the `Evicted` condition we would flip `DeactivationTarget` back to `false`.

So when a user sets `active: true` we generally should have `DeactivationTarget: false`, and respect the user re-activation. There is a small window between setting `active: false` and `DeactivationTarget: false` by the system, in which case the manual flip is reverted indeed. However, I believe this would not be a regression from what we have now.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-29T12:57:17Z

Ok, that can work. My only concern is the big amount of conditions we have, which now will be harder to document.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-29T13:09:19Z

Right, but the alternatives we have on the table:
1. reverse engineering deactivation message, or
2. Move the active field to status

also have their drawbacks. 

I think if we document well the condition it should be fine. We may also add to the documentation the graph of possible transitions.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-29T13:12:55Z

Last time I tried to draw the graph, I almost ran out of space :)

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-29T13:27:25Z

The new one will be on the margin :)

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-05-30T09:56:56Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-05-31T15:07:22Z

We have not delay between requeue and deactivation. After requeue workload will admitted and if it'll happens timeout again it will deactivated without waiting for requeue. Look [here](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/core/workload_controller.go#L457-L466).

@mimowo @tenzen-y Or I missed something?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-03T10:55:44Z

Interesting, can you please double-check / confirm that there is no delay on a running Kueue? 

I think during my testing I observed the delay, I think it might be coming from [this place](https://github.com/kubernetes-sigs/kueue/blob/078109938e9fda81ef02030d68304c2726d4a364/pkg/controller/core/workload_controller.go#L156-L181) which is before the function you mentioned.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-03T15:23:34Z

@mbobrovskyi thank you for investigating this issue.
I guess that you can observe, obviously, once you increase the backoffMaxSecond and backoffBaseSecond, maybe.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-04T07:18:07Z

In order to clarify the confusion I present the example output for the following config:

```yaml
      waitForPodsReady:
        enable: true
        timeout: 1m
        blockAdmission: false
        requeuingStrategy:
          timestamp: Eviction
          backoffLimitCount: 1 
          backoffBaseSeconds: 60
          backoffMaxSeconds: 3600
```

```sh
> kubectl get workload -w --output-watch-events -ocustom-columns=EVENT:.type,NAME:.object.metadata.name,ACTIVE:.object.spec.active,CONDITIONS:.object.status.conditions | ts "%Y-%m-%d %H:%M:%.S"
2024-06-04 09:06:58.564580 EVENT   NAME                   ACTIVE   CONDITIONS
2024-06-04 09:06:58.564735 ADDED   job-sample-job-992ea   true     <none>
2024-06-04 09:06:58.572070 MODIFIED   job-sample-job-992ea   true     [map[lastTransitionTime:2024-06-04T07:06:58Z message:Not all pods are ready or succeeded observedGeneration:1 reason:PodsReady status:False type:PodsReady]]
2024-06-04 09:06:58.583652 MODIFIED   job-sample-job-992ea   true     [map[lastTransitionTime:2024-06-04T07:06:58Z message:Not all pods are ready or succeeded observedGeneration:1 reason:PodsReady status:False type:PodsReady] map[lastTransitionTime:2024-06-04T07:06:58Z message:Quota reserved in ClusterQueue cluster-queue observedGeneration:1 reason:QuotaReserved status:True type:QuotaReserved] map[lastTransitionTime:2024-06-04T07:06:58Z message:The workload is admitted observedGeneration:1 reason:Admitted status:True type:Admitted]]
2024-06-04 09:07:58.013507 MODIFIED   job-sample-job-992ea   true     [map[lastTransitionTime:2024-06-04T07:06:58Z message:Not all pods are ready or succeeded observedGeneration:1 reason:PodsReady status:False type:PodsReady] map[lastTransitionTime:2024-06-04T07:06:58Z message:Quota reserved in ClusterQueue cluster-queue observedGeneration:1 reason:QuotaReserved status:True type:QuotaReserved] map[lastTransitionTime:2024-06-04T07:07:58Z message:Exceeded the PodsReady timeout default/job-sample-job-992ea observedGeneration:1 reason:PodsReadyTimeout status:True type:Evicted] map[lastTransitionTime:2024-06-04T07:06:58Z message:The workload is admitted observedGeneration:1 reason:Admitted status:True type:Admitted]]
2024-06-04 09:07:59.042140 MODIFIED   job-sample-job-992ea   true     [map[lastTransitionTime:2024-06-04T07:06:58Z message:Not all pods are ready or succeeded observedGeneration:1 reason:PodsReady status:False type:PodsReady] map[lastTransitionTime:2024-06-04T07:07:59Z message:Exceeded the PodsReady timeout default/job-sample-job-992ea observedGeneration:1 reason:Pending status:False type:QuotaReserved] map[lastTransitionTime:2024-06-04T07:07:58Z message:Exceeded the PodsReady timeout default/job-sample-job-992ea observedGeneration:1 reason:PodsReadyTimeout status:True type:Evicted] map[lastTransitionTime:2024-06-04T07:07:59Z message:The workload has no reservation observedGeneration:1 reason:NoReservation status:False type:Admitted] map[lastTransitionTime:2024-06-04T07:07:59Z message:Exceeded the PodsReady timeout default/job-sample-job-992ea observedGeneration:1 reason:PodsReadyTimeout status:False type:Requeued]]
2024-06-04 09:08:58.014986 MODIFIED   job-sample-job-992ea   true     [map[lastTransitionTime:2024-06-04T07:06:58Z message:Not all pods are ready or succeeded observedGeneration:1 reason:PodsReady status:False type:PodsReady] map[lastTransitionTime:2024-06-04T07:07:59Z message:Exceeded the PodsReady timeout default/job-sample-job-992ea observedGeneration:1 reason:Pending status:False type:QuotaReserved] map[lastTransitionTime:2024-06-04T07:07:58Z message:Exceeded the PodsReady timeout default/job-sample-job-992ea observedGeneration:1 reason:PodsReadyTimeout status:True type:Evicted] map[lastTransitionTime:2024-06-04T07:07:59Z message:The workload has no reservation observedGeneration:1 reason:NoReservation status:False type:Admitted] map[lastTransitionTime:2024-06-04T07:08:58Z message:The workload backoff was finished observedGeneration:1 reason:BackoffFinished status:True type:Requeued]]
2024-06-04 09:08:58.027117 MODIFIED   job-sample-job-992ea   true     [map[lastTransitionTime:2024-06-04T07:06:58Z message:Not all pods are ready or succeeded observedGeneration:1 reason:PodsReady status:False type:PodsReady] map[lastTransitionTime:2024-06-04T07:08:58Z message:Quota reserved in ClusterQueue cluster-queue observedGeneration:1 reason:QuotaReserved status:True type:QuotaReserved] map[lastTransitionTime:2024-06-04T07:08:58Z message:Previously: Exceeded the PodsReady timeout default/job-sample-job-992ea observedGeneration:1 reason:QuotaReserved status:False type:Evicted] map[lastTransitionTime:2024-06-04T07:08:58Z message:The workload is admitted observedGeneration:1 reason:Admitted status:True type:Admitted] map[lastTransitionTime:2024-06-04T07:07:59Z message:Exceeded the PodsReady timeout default/job-sample-job-992ea observedGeneration:1 reason:PodsReadyTimeout status:False type:Requeued]]
2024-06-04 09:08:58.042313 MODIFIED   job-sample-job-992ea   true     [map[lastTransitionTime:2024-06-04T07:06:58Z message:Not all pods are ready or succeeded observedGeneration:1 reason:PodsReady status:False type:PodsReady] map[lastTransitionTime:2024-06-04T07:08:58Z message:Quota reserved in ClusterQueue cluster-queue observedGeneration:1 reason:QuotaReserved status:True type:QuotaReserved] map[lastTransitionTime:2024-06-04T07:08:58Z message:Previously: Exceeded the PodsReady timeout default/job-sample-job-992ea observedGeneration:1 reason:QuotaReserved status:False type:Evicted] map[lastTransitionTime:2024-06-04T07:08:58Z message:The workload is admitted observedGeneration:1 reason:Admitted status:True type:Admitted] map[lastTransitionTime:2024-06-04T07:08:58Z message:The workload backoff was finished observedGeneration:1 reason:BackoffFinished status:True type:Requeued]]
2024-06-04 09:09:58.013151 MODIFIED   job-sample-job-992ea   false    [map[lastTransitionTime:2024-06-04T07:06:58Z message:Not all pods are ready or succeeded observedGeneration:1 reason:PodsReady status:False type:PodsReady] map[lastTransitionTime:2024-06-04T07:08:58Z message:Quota reserved in ClusterQueue cluster-queue observedGeneration:1 reason:QuotaReserved status:True type:QuotaReserved] map[lastTransitionTime:2024-06-04T07:08:58Z message:Previously: Exceeded the PodsReady timeout default/job-sample-job-992ea observedGeneration:1 reason:QuotaReserved status:False type:Evicted] map[lastTransitionTime:2024-06-04T07:08:58Z message:The workload is admitted observedGeneration:1 reason:Admitted status:True type:Admitted] map[lastTransitionTime:2024-06-04T07:08:58Z message:The workload backoff was finished observedGeneration:1 reason:BackoffFinished status:True type:Requeued]]
2024-06-04 09:09:58.025217 MODIFIED   job-sample-job-992ea   false    [map[lastTransitionTime:2024-06-04T07:06:58Z message:Not all pods are ready or succeeded observedGeneration:1 reason:PodsReady status:False type:PodsReady] map[lastTransitionTime:2024-06-04T07:08:58Z message:Quota reserved in ClusterQueue cluster-queue observedGeneration:1 reason:QuotaReserved status:True type:QuotaReserved] map[lastTransitionTime:2024-06-04T07:09:58Z message:The workload is deactivated due to exceeding the maximum number of re-queuing retries observedGeneration:2 reason:InactiveWorkload status:True type:Evicted] map[lastTransitionTime:2024-06-04T07:08:58Z message:The workload is admitted observedGeneration:1 reason:Admitted status:True type:Admitted] map[lastTransitionTime:2024-06-04T07:08:58Z message:The workload backoff was finished observedGeneration:1 reason:BackoffFinished status:True type:Requeued]]
2024-06-04 09:09:59.052521 MODIFIED   job-sample-job-992ea   false    [map[lastTransitionTime:2024-06-04T07:06:58Z message:Not all pods are ready or succeeded observedGeneration:1 reason:PodsReady status:False type:PodsReady] map[lastTransitionTime:2024-06-04T07:09:59Z message:The workload is deactivated due to exceeding the maximum number of re-queuing retries observedGeneration:2 reason:Pending status:False type:QuotaReserved] map[lastTransitionTime:2024-06-04T07:09:58Z message:The workload is deactivated due to exceeding the maximum number of re-queuing retries observedGeneration:2 reason:InactiveWorkload status:True type:Evicted] map[lastTransitionTime:2024-06-04T07:09:59Z message:The workload has no reservation observedGeneration:2 reason:NoReservation status:False type:Admitted] map[lastTransitionTime:2024-06-04T07:09:59Z message:The workload is deactivated due to exceeding the maximum number of re-queuing retries observedGeneration:2 reason:InactiveWorkload status:False type:Requeued]]
```

There are two issues actually (probably closely related):
1. the transition from `active: true -> false` takes 1min delay ( from `2024-06-04 09:08:58.042313` to `2024-06-04 09:09:58.013151`), after second PodsReady timeout. This delay is the original motivation for opening the issue. It is unnecessary because after second violation of the timeout we know the workload is going to be deactivated.
2. the transition from `Requeued: False -> true` takes almost no time (from `2024-06-04 09:08:58.027117` to `2024-06-04 09:08:58.042313`) after the second failure. However, because this is the second violation of the timeout, we don't need this transition at all. We can stay with `Requeued: false`. Transition took around 1min after the first failure, properly.

EDIT: it is not shown in the output, but when deactivating the workload we still have `status.requeueState.count: 1`. Incrementing the counter to `2` after the second timeout violation can help to make the [code for setting the message](https://github.com/kubernetes-sigs/kueue/blob/a14bc68990c2ff1e5ae6a93474b3f9c4dc84fd25/pkg/controller/core/workload_controller.go#L187-L197) easier, and maybe also can have with the timing issues.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-05T11:45:03Z

I have renamed the issue, it seems I was mislead by the transitions of the Requeued condition. 
The delay for setting active=false comes from PodsReady timeout which is expected. 

As investigated by @mbobrovskyi the culprit is that the workload goes to the heap (queue) while Requeued=false.
