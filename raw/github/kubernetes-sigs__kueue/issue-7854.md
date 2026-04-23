# Issue #7854: TAS: Improve debuggability when scheduling fails

**Summary**: TAS: Improve debuggability when scheduling fails

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7854

**Last updated**: 2025-12-08T13:27:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-24T16:55:29Z
- **Updated**: 2025-12-08T13:27:31Z
- **Closed**: 2025-12-08T13:27:31Z
- **Labels**: `kind/feature`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 7

## Description

**What would you like to be added**:

Improve the debug information for why TAS flavor couldn't admit the workload. The information could be surfaced in the condition, even, and logs. 

The information which would be particularly useful:
1. how many nodes were excluded per taint
2. how many nodes were excluded per resource which was considered the most restrictive (say we have 100 nodes excluded total, out of which 10 due to gpu, 90 due to cpu)


**Why is this needed**:

It is really hard to tell why we see "TAS flavor can only admit 0/1" pods - even in the simple cases. The information like, "TAS flavor can only admit 0/1 pods, 1 pod excluded by taint avoid-me" would be very helpful.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-24T16:56:00Z

cc @PBundyra @pajakd @tenzen-y wdyt?
cc @mykysha who is currently working on another flavor debuggability task: https://github.com/kubernetes-sigs/kueue/pull/7646

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-11-28T13:43:44Z

/assign @sohankunkerkar

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-12-01T09:21:19Z

I definitely support this, especially 1. Additionally I would increase verbosity of this log line: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/cache/scheduler/tas_flavor.go#L143 and think if there are any that could also use lower verbosity

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-12-01T21:10:45Z

I've been digging into this. I think the core issue is definitely that "0/1 pods admitted" is too opaque. I'm working on aggregating the exclusion reasons so we can see a summary like "X nodes excluded by taint Y, Z nodes excluded by insufficient CPU". This directly addresses the need to understand why the flavor couldn't admit the workload without digging through thousands of log lines.

I'm also looking at the log levels. I think we can reduce the noise by reducing the per-node exclusion logs (since we'll have the summary).

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-02T11:32:31Z

I would start with surfacing the information to user as condition message and event. 

The logging guide for kubernetes indeed allows to use v(2) for https://github.com/kubernetes/community/blob/master/contributors/devel/sig-instrumentation/logging.md#what-method-to-use for scheduler decisions, but I would keep it for later. I think the main priority is to inform the user, and later we can think what are the gaps for admins / oncallers.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-12-02T12:31:47Z

> I would start with surfacing the information to user as condition message and event.
> 
> The logging guide for kubernetes indeed allows to use v(2) for https://github.com/kubernetes/community/blob/master/contributors/devel/sig-instrumentation/logging.md#what-method-to-use for scheduler decisions, but I would keep it for later. I think the main priority is to inform the user, and later we can think what are the gaps for admins / oncallers.

I agree with this. We should start by well-informative event and condition message.
If we really need to expose such information to a dedicated condition or more API surfaces, we can revisit the discussion on where the best place is for rich information. As we discussed in another place, exposing Topology information observed by Kueue via the visibility API might be helpful as another PoV.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-02T13:05:17Z

I think the condition and message is very useful here. The on demand is a bit lower priority. For example we had a debug for TAS with ProvisioningRequest. The issue with on demand is that after 10min the cluster auto scaler would remove the faulty provisioned nodes, so oncallers would not be able to use it to investigate an accident. The condition will be recorded, and the event is recorded in logs for long 

EDIT: even without ProvisioningRequests, the on-demand API is not that useful for debugging retrospectively scheduling decisions. It can be useful if there is an on-going problem and the user and the admin can work on the issue together at the same time. Still, good event / condition messages is the place to start for me.
