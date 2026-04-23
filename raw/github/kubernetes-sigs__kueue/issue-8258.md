# Issue #8258: TAS NodeHotSwap: Kueue scheduler tries to indefinitely evict the workload using old version

**Summary**: TAS NodeHotSwap: Kueue scheduler tries to indefinitely evict the workload using old version

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8258

**Last updated**: 2025-12-19T09:34:49Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-16T10:58:51Z
- **Updated**: 2025-12-19T09:34:49Z
- **Closed**: 2025-12-19T09:30:09Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi), [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 20

## Description


**What happened**:

When using TAS NodeHotSwap in Kueue 0.15.1 I can see for some workloads Kueue scheduler goes into indefinite loop for trying to evict the workload, but it fails each time due to old ResourceVersion

I see in logs:

```
{"caller":"scheduler/scheduler.go:243", "clusterQueue":{…}, "error":"Operation cannot be fulfilled on workloads.kueue.x-k8s.io "job-xyz-abcdef": the object has been modified; please apply your changes to the latest version and try again", "id":"1111111-2222-3333-4444-5555555555555", "kubernetes":{…}, "level":"error", "logger":"scheduler", "msg":"Failed to evict workload after failed try to find a node replacement", "parentCohort":{…}, "rootCohort":{…}, "schedulingCycle":426, "stacktrace":"sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).schedule
```


**What you expected to happen**:
The workload used by scheduler in cache has the latest ResourceVersion.

**Investigation**

I looked at the code, and I think the problem is in workload_controller, that we don't update the workload kept in the cache:

https://github.com/kubernetes-sigs/kueue/blob/a5cfb137da2066e432036b1320f6100a0fafa9b8/pkg/controller/core/workload_controller.go#L966-L977

We should fire the case when "NodeToReplace" is changed.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-16T10:59:06Z

cc @mbobrovskyi @sohankunkerkar @PBundyra @pajakd

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-12-17T00:38:36Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-17T10:42:20Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-17T10:43:25Z

@sohankunkerkar I asked @mbobrovskyi to work on this issue too, as this is important for us. Feel free to review / sync or share some code. Let us know where you are.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-17T11:52:09Z

Probably https://github.com/kubernetes-sigs/kueue/pull/7933 should partially fix this issue. We are using EvictWithLooseOnApply and EvictWithRetryOnConflictForPatch.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-17T11:53:45Z

> We should fire the case when "NodeToReplace" is changed.

Shouldn’t it be updated in the default case?

https://github.com/kubernetes-sigs/kueue/blob/a5cfb137da2066e432036b1320f6100a0fafa9b8/pkg/controller/core/workload_controller.go#L979-L985

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-17T12:15:47Z

Hm yeah it could help, I can probably cherrypick that. but it will not fix the issue for using Patch. Also, I'm not sure how easy it would be to cherrypick to 0.14

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-12-17T16:12:41Z

I dug into this issue. I think the second pass queue holds a copy of the workload when it's queued. If the workload gets updated again before the scheduler picks it up, that copy becomes stale.
PR #7933 added `EvictWithRetryOnConflictForPatch()` which should handle this, but the retry logic only kicks in when `WorkloadRequestUseMergePatch` is enabled (which is off by default). So when the feature is off, we fall through to the SSA patch path which ignores the retry option entirely.
I think we should add `|| opts.RetryOnConflictForPatch` [here](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/workload/workload.go#L1044), which ensures the retry logic is used whenever `RetryOnConflictForPatch` is requested, regardless of the feature gate.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-18T07:38:06Z

> PR https://github.com/kubernetes-sigs/kueue/pull/7933 added EvictWithRetryOnConflictForPatch() which should handle this, but the retry logic only kicks in when WorkloadRequestUseMergePatch is enabled (which is off by default). So when the feature is off, we fall through to the SSA patch path which ignores the retry option entirely.

Indeed, thank you @sohankunkerkar and @mbobrovskyi for exploring this. I have decided to go with the recommendation of using https://github.com/kubernetes-sigs/kueue/pull/7933 to solve this problem.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-18T08:03:24Z

I think I have a likely scenario for the problem with stale second pass queue, consider this:
1. a node is unhealthy so the node_failure_controller added unhealthyNodes, and workload_controller added it to secondPassQueue
2. the node got healthy, and so node_failure_controller removed the node from unhealthy nodes
3. the stale entry stays in secondPassQueue, because the only scenario when we delete is [workload deletion](https://github.com/kubernetes-sigs/kueue/blob/00420464afed0ff31a39125e1a6cc51f38d33ae5/pkg/controller/core/workload_controller.go#L867) or workload [losing reservation](https://github.com/kubernetes-sigs/kueue/blob/00420464afed0ff31a39125e1a6cc51f38d33ae5/pkg/controller/core/workload_controller.go#L964). However, if the node became healthy we didn't lose reservation, so we still have the workload in the second pass queue. As a result scheduler keeps retrying to evict the workload.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-18T08:03:55Z

cc @PBundyra @mbobrovskyi @pajakd @sohankunkerkar

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-12-18T12:14:48Z

Makes sense! We should delete the workload from secondPassQueue if it's there and it doesn't have any unhealthy nodes in its status

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-12-18T12:59:54Z

After looking into it I think we actually do delete the workload from the secondPassQueue here: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/scheduler.go#L435

The workload no longer needs the second pass so it's skipped

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-12-18T13:16:51Z

I have an alternative explanation of this stale resource version issue. I think we might be lacking update to `queues` in the default case of this switch

> > We should fire the case when "NodeToReplace" is changed.
> 
> Shouldn’t it be updated in the default case?
> 
> [kueue/pkg/controller/core/workload_controller.go](https://github.com/kubernetes-sigs/kueue/blob/a5cfb137da2066e432036b1320f6100a0fafa9b8/pkg/controller/core/workload_controller.go#L979-L985)
> 
> Lines 979 to 985 in [a5cfb13](/kubernetes-sigs/kueue/commit/a5cfb137da2066e432036b1320f6100a0fafa9b8)
> 
>  default: 
>  	// Workload update in the cache is handled here; however, some fields are immutable 
>  	// and are not supposed to actually change anything. 
>  	if err := r.cache.UpdateWorkload(log, e.ObjectOld, wlCopy); err != nil { 
>  		log.Error(err, "Updating workload in cache") 
>  	} 
>  }

We update only `cache`. A similar update to `queues` is done here:

https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/core/workload_controller.go#L918-L927

But the workload with an unhealthy node is admitted so it skips this logic branch

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-18T13:19:22Z

Yeah, doing this in default case is one idea, but it seems better to me to generalize QueueSecondPassIfNeeded  to delete if no longer should be queued: https://github.com/kubernetes-sigs/kueue/blob/a5cfb137da2066e432036b1320f6100a0fafa9b8/pkg/controller/core/workload_controller.go#L986

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-12-18T13:20:31Z

Well, maybe in this case it still needed to be queued, but the object has changed

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-18T13:23:57Z

> Well, maybe in this case it still needed to be queued, but the object has changed

Yes, it is possible that it still needs to be queued, then we just update (this is what we already do). 

However, we can detect it no longer needs to be queued, and deleted. 

So we would rename if from `QueueSecondPassIfNeeded` to `UpdateSecondPassIfNeeded` (for example)

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-12-18T13:24:30Z

> I have an alternative explanation of this stale resource version issue. I think we might be lacking update to `queues` in the default case of this switch

Actually we might not be lacking this, we already do it in `QueueSecondPassIfNeeded`

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:30:09Z

I think cherrypicking https://github.com/kubernetes-sigs/kueue/pull/7933 will effectively solve the problem. 

Still, I think it would be good to follow up making sure QueueSecondPassIfNeeded removes if no longer needed. At this point this feels like a cleanup. So let me close this issue, and open follow up.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:34:49Z

Opened: https://github.com/kubernetes-sigs/kueue/issues/8357
