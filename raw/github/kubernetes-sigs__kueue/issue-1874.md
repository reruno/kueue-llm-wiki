# Issue #1874: Distinguish between preemption within ClusterQueue, reclaim within Cohort and preemption with borrowing

**Summary**: Distinguish between preemption within ClusterQueue, reclaim within Cohort and preemption with borrowing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1874

**Last updated**: 2024-04-10T15:20:00Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-03-20T20:07:20Z
- **Updated**: 2024-04-10T15:20:00Z
- **Closed**: 2024-04-10T15:20:00Z
- **Labels**: `kind/feature`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 15

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Preemption in Kueue can happen due to the following reasons:

- Within a Cluster Queue, due to an incoming Pod with higher priority
- Within a Cohort, to reclaim quota
- Within a Cohort, due to preemption with borrowing, because the preempted workload is below a threshold.

We need to enhance the Condition reason and messages to incorporate this information.

**Why is this needed**:

For users to better understand why Kueue preempted their Jobs.

Administrators might want to aggregate information for multiple preemptions, so ideally the Reason should be different, with a common prefix.
A potential problem is to break users that already depend on the `Preempted` reason to identify preemptions. Perhaps highlighting the breaking change should be enough in the release notes.

We can also incorporate the information in a metric label.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-20T20:08:15Z

cc @tenzen-y @astefanutti @kerthcet wdyt of the breaking change?

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-03-21T10:23:09Z

+1 not maintaining backward compatibility is OK on our side.

I think that relates to #1741 for the metrics part.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-21T16:00:31Z

Actually, the current state could be considered buggy, because the message in the Evicted condition always says: "Preempted to accommodate a higher priority Workload".

So at the very least we can start by distinguishing the message.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-22T07:28:28Z

@alculquicondor, I agree with making UX better.
And I'm ok with these breaking changes. I my side, we expose such reasons via our gRPC API. So, I can just modify the internal Server logic.

But, I think we need to announce this change as breaking in RELEASE NOTE and release announcement in google groups.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-22T12:21:37Z

Yes, we can put `ACTION REQUIRED` in the notes to highlight at the top.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-03-27T09:05:11Z

+1. The current message is misleading because when `reclaimWithinCohort: Any` then a workload might get preempted by a lower priority workload actually.

I'm not sure using `reason` for this purpose is the right way. Currently we have 3 modes of preemption, we are likely to have more in the future, for example, if fair sharing is implemented. So we may end up adding many reasons, and determining the reasons might be tricky at some point as we need to propagate the information via a couple of functions.

I'm thinking about enriching the message, similarly as we build the events in the [k8s scheduler](https://github.com/kubernetes/kubernetes/blob/227c2e7c2b2c05a9c8b2885460e28e4da25cf558/pkg/scheduler/framework/preemption/preemption.go#L390). We could have a message like: `Preempted to accommodate the "UID-x" workload  submitted to the "team-y" ClusterQueue."

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-27T14:22:57Z

The thing is that messages are not machine-readable. For direct users of Kueue, messages are acceptable. But if you use kueue as a low-level component, then you might need a reason to distinguish between the different kinds of preemption.

The reasons having a common prefix could be good enough to group them as one thing with different variants.

Btw, in fair sharing, the preemption reason would still be PreemptDueToReclaim (or something similar). It's just that the "reclamation thresholds" are dynamic.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-03-27T14:34:43Z

>  The thing is that messages are not machine-readable. 

I see, so maybe instead we have an extra condition type `Preempted`, with a dedicated reason. So we have 2 conditions:
```yaml
- type: Evicted
  reason: Preempted
  message: preempted to accomodate workload UID
- type: Preempted
  reason: ReclaimWithinCohort / PreemptionWithinClusterQueue / FairSharingWithinCohort ... 
  message: preempted to accomodate workload UID # possibly some more data here 
```

> For direct users of Kueue, messages are acceptable. But if you use kueue as a low-level component, then you might need a reason to distinguish between the different kinds of preemption.

Yes, but then when a new reason is added by Kueue, then the external system also needs to be extended for monitoring, when a new version of Kueue introduces a new reason (if the system does not need fine grained information). I guess we could mitigate this by some convention, say all reasons start with "PreemptedDueTo".

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-27T14:37:31Z

I like the idea of a dedicated Preempted condition. It's fully backwards compatible. We just need to make sure that the documentation makes a distinction between the two conditions (or that one is a subset of the other).

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-03-27T15:31:45Z

A separate Preempted condition looks like a good solution, bringing better structure maintaining backward compatibility.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-28T18:55:01Z

+1 on having the `Evicted` and the `Preempted` condition type.
Also, we may need to clarify what the difference is between Preemption and Eviction in the documentation.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-03T08:51:27Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-04T12:59:18Z

I'm wondering if we should distinguish `reclaimWithinCohort` and preemption while borrowing, at the reason level, as suggested in the issue description. 

I think preemption while borrowing can happen it two scenarios:
1. we are only preempting workloads within ClusterQueue [here](https://github.com/kubernetes-sigs/kueue/blob/1aa8adee3ca6ed55405ed468a947cbe2cd99090c/pkg/scheduler/preemption/preemption.go#L102)
2. we are preempting workloads within cohort (enabled by `preemption.BorrowWithinCohort`), see [here](https://github.com/kubernetes-sigs/kueue/blob/1aa8adee3ca6ed55405ed468a947cbe2cd99090c/pkg/scheduler/preemption/preemption.go#L116).

Then, there are variants of (2), because the threshold does not need to be specified. Also, `preemption.BorrowWithinCohort` can only be enabled when `preemption.reclaimWithinCohort` is enabled, so it is more of an additional configuration option, rather than a new "mode" of preempting.

My suggestion would be to just go with two reasons:
`PreemptionInClusterQueue` and `ReclaimWithinCohort` .  Then, we put the preemptor UID into the message so that one can figure out more if has access to the workload (this is is what I do in the initial version of the PR: https://github.com/kubernetes-sigs/kueue/pull/1942).

Any views?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-04T14:07:01Z

If we can make the distinction between the two, that would be better IMO.

End users might have access to the preemption condition, but they might not have access to the names or priorities or other workloads. But they still would want to know roughly why they were preempted.

A nit on `PreemptionInClusterQueue`: It shouldn't start with preemption, because that's already the name of the condition. But maybe we can say `HigherPriorityWithinClusterQueue`. And similarly `UnderPriorityThresholdForPreemptionWithBorrowing` (I'm open to ideas for a shorter version).

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-04T15:22:56Z

From the offline discussions we want to balance two aspects: satisfy the MVP which distinguishes "In ClusterQueue" and "In cohort", and being as granular as possible.

I think there will always be a possibility, that a new config option or threshold is introduced, making the reason to split into two or more detailed reasons.

In that case, I would suggest to start with something simple for now, two reasons: `InClusterQueue` and `InCohort`. Then, we say that reasons prefixed by them are meant to provide more detailed information. So, in the future we may have:
`InClusterQueueByHigherPriorityWorkload` or `InCohortByBorrowingWorkload`, etc.
