# Issue #9711: Support TAS defragmentation triggered by JobSet restart

**Summary**: Support TAS defragmentation triggered by JobSet restart

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9711

**Last updated**: 2026-03-09T18:16:59Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-06T12:10:09Z
- **Updated**: 2026-03-09T18:16:59Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

When a JobSet is fully restarting, all Jobs are restarted it is a good opportunity to find new TAS placement for the Pods, maybe more optimal. However, currently the TAS domain assignments are not re-computed. The re-computation happens on re-admission. 

A relatively simple idea is to evict the restarting JobSet to trigger the full re-admission cycle. For that we need some APIs to communicate the express the intent.

My current idea is to have two permanent annotations, added by user on JobSet creation: 
- `kueue.x-k8s.io/evict-on-suspend: true` - instructs Kueue to "evict whenever suspended"
- `jobset.x-k8s.io/suspend-on-restart: true` - instructs JobSet controller to set `spec.suspend=true` on restart. I think this could be the same request as bumping `jobSet.status.restarts += 1`

**Why is this needed**:

To defragment capacity when full JobSet restart is required anyway.

**Completion requirements**:

Maybe there are alternative approaches to communicate the intention, so a small KEP would be userful.


This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-06T12:10:30Z

cc @sanposhiho @mwysokin @mwielgus @GiuseppeTT

### Comment by [@sanposhiho](https://github.com/sanposhiho) — 2026-03-07T01:02:21Z

This is very nice way for "opportunistic" defrag, like keep bin-packing nicely without any actual interruption (preempt running jobs).

The proposed solution looks great as a starting point. But I see the future where such rescheduling has to evolve further. e.g., in some environment, moving jobs from one to another comes with a cost even if that runs at jobset restarts. That cost might be acceptable when moving enhances the bin-packing situation, but otherwise no.
So, eventually, I would expect this feature to evict->reschedule jobsets based on the situation that the jobset is in. Like, when two mid-sized jobs fully occupy the whole rack, they don't have to be moved to somewhere else at restart as the rack is fully utilized. But, when one of them completes and now the whole rack is only partially utilized just for one mid-sized job, then it has to be moved to somewhere else possibly at restarts.
