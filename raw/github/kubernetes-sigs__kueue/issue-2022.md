# Issue #2022: [MultiKueue] Default managedBy for ClusterQueues configured to use MultiKueue AC

**Summary**: [MultiKueue] Default managedBy for ClusterQueues configured to use MultiKueue AC

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2022

**Last updated**: 2024-05-09T16:31:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-04-19T14:39:43Z
- **Updated**: 2024-05-09T16:31:04Z
- **Closed**: 2024-05-09T16:31:04Z
- **Labels**: `kind/feature`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 12

## Description

**What would you like to be added**:

Add the `managedBy` field if the JobSet is submitted to a ClusterQueue with MultiKueue AC.

**Why is this needed**:

Usability. The users should know as little about MK as possible, only admins. Once the system is setup by an admin the user does not need to know if this is MK or not. 

It will allow for smooth transition from single cluster to multiple cluster environments.

**Proposed approach**

The proposed solution is to use the `jobset_webhook` which would have access to the configuration of ClusterQueues via cache.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-19T14:40:01Z

/assign @trasc 
/cc @alculquicondor @mwielgus

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-19T14:43:28Z

I guess either the cache or the client (which is also cached). Whichever is less cumbersome.

There might be race conditions in either case, so that should not be a consideration when choosing between one or the other.

### Comment by [@trasc](https://github.com/trasc) — 2024-04-19T15:20:42Z

One problem that I see with this is that the `managedBy` field of the JobSet should be immutable (it looks like it's not the case now but I see this more as a bug on their side), and the workload queue of queue's admission checks are not. And we end up enforcing the state of the queues at the time the JobSet is created. 

What it might be more problematic, down the line is: 

- If multikueue is "added"  to the JobSet (added to the jobset's queue, or it's queue changes) the multikueue controller will reject it. (maybe not a huge problem)

- If multikueue is "removed"  from the JobSet  (from the jobset's queue, or it's queue changes )  when the JobSet will be admitted , since it's main controller will continue to ignore it, no progress will be done and the quota will remain reserved.

In case the `managedBy` mutability for JobSets is a feature , not  a bug,  then we can try to "flip" it from multikueue when ever it's the case.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-19T15:32:37Z

> In case the managedBy mutability for JobSets is a feature , not a bug, then we can try to "flip" it from multikueue when ever it's the case.

It should be immutable. We want consistency with Batch Job, where this was discussed at length.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-19T15:39:55Z

> What it might be more problematic, down the line is:

Yes, we are aware of race conditions like these, but the assumption is that ClusterQueue configurations are rare, once the system is setup.

That being said, the more helpful we can be in that situations the better. For example, maybe we could detect situations like these and evict the workloads, and mark as inactive.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-19T16:11:09Z

Btw, I think the scenarios are sort of orthogonal, they may happen regardless if managedBy was set by a user or by an automation.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-22T09:11:22Z

Expanding a little bit on the mutability of managedBy. According to the [mission of wg-batch](https://github.com/kubernetes/community/blob/master/wg-batch/charter.md) we should try make the ecosystem consistent as much as possible. 

In this case I think it means that Jobset should try to follow the Job's decisions in the [KEP](https://github.com/kubernetes/enhancements/tree/master/keps/sig-apps/4368-support-managed-by-for-batch-jobs). 

Some of the complications for making it mutable include:
1. Leaking of resources (Pods, but also Jobs or Services) in case of swapping the controller. Different controllers may use different labels or finalizers to manage their resources, which makes things complex. Ideally, there would be no resources during the swap. However, currently this may happen, For example, there might be pods terminating for a while for suspended jobs. And JobSet controller also keeps resources in the suspended state: [here](https://github.com/kubernetes-sigs/jobset/issues/535).
2. Debuggability, is important for this feature is the sentiment we got in a couple of threads for the batch Job KEP. Mutable managedBy will make debugging much harder (for example for leaking resources between controllers).
3. Overall complexity, for example the metric `job_by_external_controller_total` (in the KEP) will not make much sense in the current definition. We would probably need additional guage metric and a metric for the number of swaps.

Having said that, there is a [graduation point for GA](https://github.com/kubernetes/enhancements/tree/master/keps/sig-apps/4368-support-managed-by-for-batch-jobs#can-the-field-be-mutable). but IMO pushing in this direction will require a very good justification. Since MultiKueue is still alpha, the adoption is still low, and we don't have feedback indicating the scenarios are problematic for end-users, I don't think it provides such a justification.

So, for now, I would suggest to assume it is immutable.

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2024-04-23T07:33:54Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-26T11:17:39Z

@vladikkuzn I think it would be good to follow up with a docs update. I think we can drop [this](https://github.com/kubernetes-sigs/kueue/blob/main/site/content/en/docs/tasks/run/jobsets.md#multikueue-environment) example. A short note, that the webhook updates the field should be enough.

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2024-04-26T11:59:46Z

@mimowo Is it better to do it in separate PR or in the same?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-26T12:05:24Z

> @mimowo Is it better to do it in separate PR or in the same?

Either way would work for me. Maybe separate is slightly preferred.

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2024-04-29T13:09:50Z

Docs follow-up: https://github.com/kubernetes-sigs/kueue/pull/2048/commits/88d459f11e98bfea337d8c15defb5baade8992fd
