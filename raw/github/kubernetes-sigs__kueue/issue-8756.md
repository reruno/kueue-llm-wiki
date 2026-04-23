# Issue #8756: Investigate: the cache invariant for finished workload seems broken

**Summary**: Investigate: the cache invariant for finished workload seems broken

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8756

**Last updated**: 2026-01-27T14:51:15Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-23T08:53:58Z
- **Updated**: 2026-01-27T14:51:15Z
- **Closed**: —
- **Labels**: `kind/bug`, `priority/important-soon`
- **Assignees**: _none_
- **Comments**: 16

## Description

**What happened**:

It seems the cache invariant about the finished workloads being tracked in [workloadAssignedQueues](https://github.com/kubernetes-sigs/kueue/blob/74e77c93677bb5b4dcdfeb232628358e1f00c6e2/pkg/cache/queue/manager.go#L119-L120)
is invalid, becasue we wouldn't track the finished workloads on restarting Kueue (Create events), see here: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/core/workload_controller.go#L810-L812

**What you expected to happen**:

We maintain the assumed invariants after restart of Kueue.

**How to reproduce it (as minimally and precisely as possible)**:

1.  Create some workload and let it finish
2. Restart Kueue
Issue: it would not be accounted in the workloadAssignedQueues (IIUC) leading to potentially unexpected consequences (I'm not yet clear what)

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-23T08:55:10Z

cc @Singularity23x0 @PBundyra 
Thank you @mbobrovskyi for drawing attention to this while working on https://github.com/kubernetes-sigs/kueue/pull/8724

Let's make sure the logic is sound before building much on top of it.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-23T09:01:49Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-23T11:37:26Z

/priority important-soon

### Comment by [@Singularity23x0](https://github.com/Singularity23x0) — 2026-01-26T13:59:13Z

As part of https://github.com/kubernetes-sigs/kueue/issues/5310 I will soon be doing a refactor of the update/create logic in the Workload Controller.
I can implement a fix for this issue as part of that, but it would be part of a larger whole and, as a result, arrive sooner than a dedicated fix.
@mimowo @mbobrovskyi lmk what are your opinions on the matter.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-26T15:42:52Z

@Singularity23x0 I think this issue is independent of what you’re doing. We need to reconsider workloadAssignedQueues as a whole. Right now, we partially keep quotaReserved, finished, and inactive workloads. On Update events, we keep these workloads in workloadAssignedQueues – it's ok, but on Create events, we don’t add them at all. Let me try to explain what’s going on.

Here is the Create event, and we skip finished workloads entirely:

https://github.com/kubernetes-sigs/kueue/blob/a6db1ccaa134076b125da2ba5057d59167e3733c/pkg/controller/core/workload_controller.go#L813-L816

On the other hand, if the workload is not admissible, we also skip adding it to this map.

https://github.com/kubernetes-sigs/kueue/blob/a6db1ccaa134076b125da2ba5057d59167e3733c/pkg/controller/core/workload_controller.go#L829-L834

So on create event we missed quotaReserved, finished and inactive workloads.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-26T15:45:40Z

So I’m not sure what result we expect. Should we add workloads to workloadAssignedQueues during the Create event, or should we remove this kind of workload on Update? That’s the open question. But we definitely need to keep this consistent.

@mimowo WDYT?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-26T15:49:44Z

Also, even if we try to add it to the cache, we have a guard that prevents us from doing that.

https://github.com/kubernetes-sigs/kueue/blob/a6db1ccaa134076b125da2ba5057d59167e3733c/pkg/cache/queue/manager.go#L536-L539

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-26T16:11:58Z

One question I would have before choosing one way or another - are we able to come up with a user-observable issue caused by the cache invariant breaking after Kueue restart? I would love to fix it in TDD way, by adding the test first.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-26T17:10:02Z

Yes, that’s the key question: what behavior do we expect after a restart? I don’t see any use of these types of workloads in the queue cache.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-26T17:21:31Z

Ah, I think this is not needed currently, but this was a preparatory work for the deletion handling planned by @Singularity23x0 : https://github.com/kubernetes-sigs/kueue/pull/8655

We need to make sure that finished workloads are correctly accounted after restart

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-26T17:22:07Z

@mbobrovskyi do we have a test which demonstates that a finished workload is accounted in metrics after Kueue restart?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-26T17:24:50Z

> @mbobrovskyi do we have a test which demonstates that a finished workload is accounted in metrics after Kueue restart?

No. But for finished workloads we are using another map.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-26T17:28:48Z

Let's add that test then. It will be useful to make sure we don't regress in https://github.com/kubernetes-sigs/kueue/pull/8655

### Comment by [@Singularity23x0](https://github.com/Singularity23x0) — 2026-01-26T18:49:03Z

When considered outside of QueueAssociatedInadmissibleWorkloadsAfter the map should be filled only while the workloads are in the cache.

The mechanism of queueing inadmissible workloads complicates things however, as we need to extract the information on what queue the workload was assigned to when calling this function.
We need to either make the cache hold the information of this assignment until the workload is deleted from the system or source that information form outside the function (like it was done before).
The problem with the latter is that, once moved to the "Reconcile" method, the deletion logic has no way of gaining that information easily. We could try retrieving it form the other cache (scheduler cache), but we have no guarantee that the other cache did not get updated due to an error of the system before the queue cache did, making it impossible to figure out what queue the workload was assign to in such a case.

### Comment by [@Singularity23x0](https://github.com/Singularity23x0) — 2026-01-27T09:06:53Z

As an fyi - https://github.com/kubernetes-sigs/kueue/pull/8655 got merged so this issue should be made a priority. If any help is needed @mbobrovskyi feel free to ping me on it.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-27T14:51:12Z

/unassign
