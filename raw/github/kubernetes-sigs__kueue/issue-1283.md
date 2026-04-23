# Issue #1283: Do not consider priorities when sorting workloads from different ClusterQueues

**Summary**: Do not consider priorities when sorting workloads from different ClusterQueues

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1283

**Last updated**: 2025-02-13T08:13:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-10-27T20:10:06Z
- **Updated**: 2025-02-13T08:13:03Z
- **Closed**: 2024-01-17T21:09:58Z
- **Labels**: `kind/feature`
- **Assignees**: [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk)
- **Comments**: 12

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Use priorities to sort workloads within a ClusterQueue, but ignore the priorities when sorting the heads of multiple cluster queues within a cohort.

The design needs to avoid the race condition presented here https://github.com/kubernetes-sigs/kueue/pull/1024

**Why is this needed**:

In organizations where teams do not know each other, they might be incentivized to use higher priorities to always be ahead of the rest. Ignoring priorities across ClusterQueues would remove this incentive, while allowing users to use priorities within their ClusterQueue.

Maybe this calls for a setting in a new Cohort object.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2023-11-20T09:36:29Z

/assign

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2023-11-30T13:43:18Z

Having that StrictFIFO is actually a priority queueing, I couldn't reproduce the bug that was described in https://github.com/kubernetes-sigs/kueue/pull/1024. Maybe there was no bug but actually not desired behavior when low priority workload was admitted and it was preempted just in the next scheduling cycle and we wanted to avoid such scenario and schedule higher priority workload in the first place? 

Anyway, my understanding is that we want to have the priority sorting in the scheduling loop as optional (enabled by default), so feature gate could be a solution here.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-11-30T15:20:40Z

IIRC, the case was like this:
![image](https://github.com/kubernetes-sigs/kueue/assets/1299064/1ad41b9e-b9eb-48a1-8327-b1cbec4f0916)

The important bit here is that the job X can fit by borrowing. But borrowing workloads are sorted last https://github.com/kubernetes-sigs/kueue/blob/8431cbd69a14882f2c465be6c56e006494093be2/pkg/scheduler/scheduler.go#L496-L501

But you are right, priorities shouldn't really matter, just the timing.

However, I think this was solved by #1039. Before that, the only option was to give jobs in Team-A-Standard a higher priority.

If we can prove that a higher priority is no longer necessary (through an integration test that does the above), then we can proceed with optionally disabling priority checks in the cohort.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-11-30T18:53:11Z

The example above has some problems
but we can implement this much simpler case

![image](https://github.com/kubernetes-sigs/kueue/assets/1299064/3d8ebcd1-5a4a-4938-93c9-7d51e2d3db85)

workload `#4` shouldn't be blocked.

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2023-12-05T13:17:34Z

I've added a test cases that you described https://github.com/kubernetes-sigs/kueue/issues/1283#issuecomment-1834370396 in https://github.com/kubernetes-sigs/kueue/pull/1399 and it turns out that the pending workload is still blocking borrowing. Note, that priorities doesn't matter here, I putted the highest priority for borrowing workload. The reason is that the pending workload has "Preempt" FlavorAssignmentMode and has no borrowing, so in sorting it goes before any workload that requires borrowing and since it considered as Preempt, scheduler accounts for its resources in the cohort. 

It's definitely a bug, however it's not related to disabling priority feature. So I've added a feature gate to a separate PR https://github.com/kubernetes-sigs/kueue/pull/1406 and will look further how to fix this bug.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-05T15:53:21Z

For completeness when investigating a solution: in the following case, workload `#3` should be blocked, because `#2` (of size 2) is waiting to use its nominal quota.

![image](https://github.com/kubernetes-sigs/kueue/assets/1299064/7d3bcceb-eaf7-440e-ba56-0d39ce7acb47)

See this comment:

https://github.com/kubernetes-sigs/kueue/blob/e75090ab7ade6b55349768de8f3dff3c9becfaa4/pkg/scheduler/flavorassigner/flavorassigner.go#L201-L204

I think a potential solution could be to change this logic https://github.com/kubernetes-sigs/kueue/blob/e75090ab7ade6b55349768de8f3dff3c9becfaa4/pkg/scheduler/scheduler.go#L190 to only "use" (or block) up to the nominal quota.

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2023-12-12T14:41:53Z

Probably adding minimum from `workload resources` and `clusterQueue nominal resources that are left` [here](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/scheduler.go#L205) will help

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-15T17:09:57Z

@yaroslava-serdiuk @alculquicondor I think this is almost done.

I guess that leaving task is adding docs for featureGate, `PrioritySortingWithinCohort`?
https://github.com/kubernetes-sigs/kueue/blob/main/site/content/en/docs/installation/_index.md#change-the-feature-gates-configuration

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-15T18:14:16Z

yes, we should document this feature.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-02-12T21:28:16Z

@tenzen-y @yaroslava-serdiuk 

This feature is beta since 0.6. Any major issues with promoting this as GA?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-13T08:06:04Z

cc @mwielgus to keep me honest here, but IIRC this feature-gate is introduced as a tactical measure to allow users to set it to `false` for deployments where admins are concern about abusing priorities for scheduling (before introduction of fair sharing). Since the introduction of fair sharing the need to disable the feature should be gone, and we can make it GA. 

However, I would like to first notify some of our users and make sure they adopt fair sharing before this feature-gate is graduated (removed). So I propose to GA it in 0.12.

cc @gabesaba @mwysokin

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-13T08:13:02Z

> cc [@mwielgus](https://github.com/mwielgus) to keep me honest here, but IIRC this feature-gate is introduced as a tactical measure to allow users to set it to `false` for deployments where admins are concern about abusing priorities for scheduling (before introduction of fair sharing). Since the introduction of fair sharing the need to disable the feature should be gone, and we can make it GA.
> 
> However, I would like to first notify some of our users and make sure they adopt fair sharing before this feature-gate is graduated (removed). So I propose to GA it in 0.12.
> 
> cc [@gabesaba](https://github.com/gabesaba) [@mwysokin](https://github.com/mwysokin)

+1
