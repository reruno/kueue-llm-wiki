# Issue #4531: TAS: support co-scheduling (and rank-based ordering) of leaders and workers for LWS groups

**Summary**: TAS: support co-scheduling (and rank-based ordering) of leaders and workers for LWS groups

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4531

**Last updated**: 2025-09-17T14:45:18Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-10T08:08:41Z
- **Updated**: 2025-09-17T14:45:18Z
- **Closed**: 2025-09-17T14:45:17Z
- **Labels**: `kind/feature`
- **Assignees**: [@lchrzaszcz](https://github.com/lchrzaszcz)
- **Comments**: 16

## Description

**What would you like to be added**:

Enhanced support for rank-based ordering for LWS across groups.

There are two problems to solve:
1. currently LWS leader and worker PodSets aren't co-scheduled and may be scheduled on separate racks (even if "topology-required" annotation is used
2. there is no consistent Pod numbering across PodSets

**Why is this needed**:

To improve performance by rank-based ordering of Pods when using NCCL .

Currently the rank-based ordering in LWS only works among workers within a group, see: https://github.com/kubernetes-sigs/kueue/blob/833adb1955e225be2af843c6f3fffd7999d9e831/test/e2e/tas/leaderworkerset_test.go#L149

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-10T08:11:15Z

cc @tenzen-y @mwysokin @mwielgus 

This is a follow up for https://github.com/kubernetes-sigs/kueue/issues/3232

### Comment by [@vivekskrishna](https://github.com/vivekskrishna) — 2025-04-05T03:17:40Z

Is any help needed here to get this going? We are interested in TAs placing both leader and worker podsets on same topology rack/dc etc

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-04-16T08:46:53Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-23T09:59:21Z

/retitle TAS: support co-scheduling (and rank-based ordering) of leaders and workers for LWS groups

To pivot the title on the more essential part of the problem which is co-scheduling. If the leaders and workers aren't co-scheduled then rank-based ordering will not give much.

### Comment by [@lchrzaszcz](https://github.com/lchrzaszcz) — 2025-06-23T10:03:17Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-06-23T10:38:13Z

/unassign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-23T13:14:17Z

@mimowo Does this mean colocation for the same group?
Let's say that now, we have 3 groups and each group has a single leader and 5 workers.
In that case, does this issue try scheduling 1 leader and 5 workers within the same group to the same topology (e.g., rack) as much as possible?

Or, does this mean to try scheduling all 3 groups (3 leaders and 15 workers) to the same topology?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-23T13:22:56Z

Co-scheduling within the group so the 1 leader and 5 workers together as they often talk to each other. 

Cross talking between workers from different groups is rare, so it is a lower priority, but we can consider it if it fits naturally into 2-level scheduling.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-23T13:27:58Z

> Co-scheduling within the group so the 1 leader and 5 workers together as they often talk to each other.
> 
> Cross talking between workers from different groups is rare, so it is a lower priority, but we can consider it if it fits naturally into 2-level scheduling.

That makes sense. If we support both scheduling algorithms (same group vs cross groups), we should provide any knob for users since those usecases depend on their workload.

### Comment by [@lchrzaszcz](https://github.com/lchrzaszcz) — 2025-06-23T13:34:11Z

My idea so far for that was to introduce two LWS-specific annotations:
```
kueue.x-k8s.io/leaderworkerset-required-topology
kueue.x-k8s.io/leaderworkerset-group-required-topology
```
First one specifies required topology for the whole LWS. Second one specifies required topology for leader+workers group. I will expand KEP to include that API.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-24T10:20:38Z

> First one specifies required topology for the whole LWS. Second one specifies required topology for leader+workers group. I will expand KEP to include that API.

As I checked in my comment, this issue try to schedule same group leader and workers to the same topology.
So, I would recommend starting to support only same group case.

Because, increasing annotations will decrease UX. once we find the real use case for the whole group topology scheduling story, we should support it.

In other words, for now, I would like to support the same group scheduling w/o dedicated annotations.

### Comment by [@lchrzaszcz](https://github.com/lchrzaszcz) — 2025-06-24T10:30:20Z

I agree and that was also my intention to start with leader+workers group topology first.

> w/o dedicated annotations.

I am not sure what would be the best approach to that without dedicated annotation? I thought that I will just start with a single annotation: `kueue.x-k8s.io/leaderworkerset-group-required-topology`, but I am open to suggestions if you have something specific in mind.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-24T10:49:16Z

> I agree and that was also my intention to start with leader+workers group topology first.
> 
> > w/o dedicated annotations.
> 
> I am not sure what would be the best approach to that without dedicated annotation? I thought that I will just start with a single annotation: `kueue.x-k8s.io/leaderworkerset-group-required-topology`, but I am open to suggestions if you have something specific in mind.

In batch/v1 Job case, TAS try to pack all Pods to the required topology as much as possible based on the TAS profile like `TASProfileLeastFreeCapacity`, which means the way to change Pod packing approach is TAS profile.

However, in the LWS case, you try to provide another option that doesn't care about the topology within the same group.
Why not just rely on the podset slice mechanism? Why do we need to introduce additional LWS specific annotations?

### Comment by [@lchrzaszcz](https://github.com/lchrzaszcz) — 2025-07-07T20:22:45Z

> > I agree and that was also my intention to start with leader+workers group topology first.
> > > w/o dedicated annotations.
> > 
> > 
> > I am not sure what would be the best approach to that without dedicated annotation? I thought that I will just start with a single annotation: `kueue.x-k8s.io/leaderworkerset-group-required-topology`, but I am open to suggestions if you have something specific in mind.
> 
> In batch/v1 Job case, TAS try to pack all Pods to the required topology as much as possible based on the TAS profile like `TASProfileLeastFreeCapacity`, which means the way to change Pod packing approach is TAS profile.
> 
> However, in the LWS case, you try to provide another option that doesn't care about the topology within the same group. Why not just rely on the podset slice mechanism? Why do we need to introduce additional LWS specific annotations?

This is something different than slice mechanism. Slices are limited to a single PodSet, but Leader and Workers are two separate PodSets, so we need something to glue them together.

If I get it right, we need to do 2 steps:
- Ensure leader and workers end up on the same flavor - I have just opened a KEP update here: https://github.com/kubernetes-sigs/kueue/pull/5895 and I am working on implementation here: https://github.com/kubernetes-sigs/kueue/pull/5878
- Change TAS algorithm so it finds a place for leader among the workers.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-17T14:45:12Z

/close 
This is already done by the work referenced in the issue

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-17T14:45:18Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4531#issuecomment-3303357723):

>/close 
>This is already done by the work referenced in the issue


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
