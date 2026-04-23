# Issue #2320: [MultiKueue] When a JobSet is deleted on management cluster it takes up to 1min to delete from workers

**Summary**: [MultiKueue] When a JobSet is deleted on management cluster it takes up to 1min to delete from workers

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2320

**Last updated**: 2024-06-12T12:57:00Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-05-29T15:32:33Z
- **Updated**: 2024-06-12T12:57:00Z
- **Closed**: 2024-06-04T11:30:37Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 12

## Description

**What happened**:

When running a MultiKueue environment you delete a JobSet on the manager it is not deleted instantly on the worker.
It takes up to 1min to delete the JobSet on worker by the garbage collector.

**What you expected to happen**:

When a user deleted the JobSet on manager it should be deleted instantaneously on a worker. 
Only if the delete request fails we fallback to the Garbage-collector mechanism

**How to reproduce it (as minimally and precisely as possible)**:

1. Setup a MultiKueue environment. Single worker is enough for reproduction.
2. Create a JobSet
3. Delete the jobset on the management cluster

**Issue**: the mirror JobSet remains running on the worker for a prolonged amount of time.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-29T15:32:48Z

/cc @alculquicondor @trasc

### Comment by [@trasc](https://github.com/trasc) — 2024-05-29T15:50:18Z

This is not a bug it's a known limitation, the multikueue workload reconciler it's unable to know if a workload that is currently not found was the subject of delegation. 

Sure we can try to work around this (by using a finalizer, try to detect this in the Delete event predicate...).

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-29T15:53:53Z

I didn't know this is known. 

I think this is certainly a bug-like behavior from the user perspective. If the improvement does not require API change I think we can categorize as a bugfix rather than new feature.

EDIT: I think one advantage of categorizing as a bug is that we could cherry-pick for 0.7.1 if the fix does not make for 0.7.0. We don't cherry-pick new features.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-29T16:29:39Z

Maybe we can avoid the use of finalizers. 

I think based on the delete event we could enqueue cleanup of the worker clusters? So we would have a in-memory queue of workloads to clean. Sure, if the kueue controller is restarted it means fallback to the regular garbage-collector, but this is fine.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-29T16:32:22Z

I'm thinking about a queue-based mechanism, something similar as we use in the Job controller to cleanup the orphan pods, [ref](https://github.com/kubernetes/kubernetes/blob/1cfaa95cab0f69ecc62ad9923eec2ba15f01fc2a/pkg/controller/job/job_controller.go#L115-L116).  

EDIT : I'm open to something more involving or simpler if we have other ideas.

### Comment by [@trasc](https://github.com/trasc) — 2024-06-03T14:29:31Z


> EDIT: I think one advantage of categorizing as a bug is that we could cherry-pick for 0.7.1 if the fix does not make for 0.7.0. We don't cherry-pick new features.

I don't see any issues with backporting small features, we did it in the past (v0.6.3, v0.6.1).

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-04T11:40:15Z

I was surprised by the delay, and I expect other users who are not intimately familiar with MultiKueue code to consider the delay as a bug,. AFAIK this isn't documented as known as a limitation, so not sure how users would know that.

Having said that I'm fine either way, I will leave the final tagging to @alculquicondor, who anyway updates tagging when preparing release notes.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-12T12:19:37Z

> I was surprised by the delay, and I expect other users who are not intimately familiar with MultiKueue code to consider the delay as a bug,. AFAIK this isn't documented as known as a limitation, so not sure how users would know that.
> 
> Having said that I'm fine either way, I will leave the final tagging to @alculquicondor, who anyway updates tagging when preparing release notes.

I wonder that mentioning this limitation in the troubleshooting guide would be worth it.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-12T12:49:58Z

> I wonder that mentioning this limitation in the troubleshooting guide would be worth it.

I'm not sure, this is still an alpha feature, so probably some small issues are acceptable. We have also cherry-picked the fix on 0.7 branch

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-12T12:52:37Z

> > I wonder that mentioning this limitation in the troubleshooting guide would be worth it.
> 
> I'm not sure, this is still an alpha feature, so probably some small issues are acceptable. We have also cherry-picked the fix on 0.7 branch

I agree with you. It would be better to mention this limitation when the MultiKueue graduates to beta.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-12T12:54:48Z

Yeah, but it is fixed already, so imo nothing to be mentioned.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-12T12:56:59Z

> Yeah, but it is fixed already, so imo nothing to be mentioned.

Oh, I didn't find that :) NVM
Thank you!
