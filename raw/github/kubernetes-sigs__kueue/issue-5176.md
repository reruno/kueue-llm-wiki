# Issue #5176: Support option to preempt admitted workload that exceed quota

**Summary**: Support option to preempt admitted workload that exceed quota

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5176

**Last updated**: 2025-05-07T22:08:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ACW101](https://github.com/ACW101)
- **Created**: 2025-05-06T16:45:22Z
- **Updated**: 2025-05-07T22:08:16Z
- **Closed**: 2025-05-07T17:59:40Z
- **Labels**: `kind/support`
- **Assignees**: _none_
- **Comments**: 3

## Description

**What would you like to be added**:
When cluster queue quota is adjusted down, the already admitted job/pod will stay admitted and possibly resulted in negative quota. This is less of an issue for a job that eventually runs to completion but for deployment pod that runs indefinitely it will be stuck at negative quota. I am able to fix this by manually deleting the extra pods that don't fit in current quota, but it would be nice to have kueue do this automatically.

**Why is this needed**:
To give a more concrete use case where this is useful, I have a MultiKueue setup with clusters spread across different cloud regions. Since a region may be out of compute resource at any point in time, we need to handle these stockout events by moving pods from one region to the other. Due to the issue above, this will involve changing the quota AND manually delete the UNSCHEDUABLE pods with by hand or with a script. With this option added, the latter will be eliminated.

**Completion requirements**:
Support an option to enable preemption on already admitted pod when quota changes resulted in negative quota. 

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-07T15:36:28Z

@ACW101 Did you evaluate CQ stop policy?
https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/#stoppolicy

### Comment by [@ACW101](https://github.com/ACW101) — 2025-05-07T17:59:40Z

@tenzen-y Thank you for pointing out CQ stop policy. That indeed works perfectly. I'll close the issue since it's already implemented.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-07T22:08:13Z

/remove-kind feature
/kind support
