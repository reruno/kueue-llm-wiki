# Issue #9741: Pending workload resource metric

**Summary**: Pending workload resource metric

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9741

**Last updated**: 2026-03-08T20:09:07Z

---

## Metadata

- **State**: open
- **Author**: [@amy](https://github.com/amy)
- **Created**: 2026-03-08T19:57:40Z
- **Updated**: 2026-03-08T20:09:07Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: [@amy](https://github.com/amy)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Similar to `kueue_cluster_queue_resource_reservation`, but I want to track the resources pending in the CQ. Today we just count the number of pending workloads.

Call it `kueue_cluster_queue_resource_pending`.

**Why is this needed**:
Helps with instrumenting Kueue to alert when something is broken. You can take the diff of Pending - Unallocated Nominal Quota to roughly gauge whether there's a scheduling issue and investigation needs to happen. (ex: fragmentation, scheduling gates not initiated by Kueue, bugs, etc.) If there's enough unallocated nominal quota to admit the pending workloads, but you see that diff for a prolonged period of time (ie not a spike shape), there's potentially an issue.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@amy](https://github.com/amy) — 2026-03-08T19:57:47Z

/assign
