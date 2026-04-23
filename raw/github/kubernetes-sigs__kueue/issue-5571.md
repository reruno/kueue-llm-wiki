# Issue #5571: [TAS] Node failure controller should delete nodeToReplace annotation if a node recovers/reappears

**Summary**: [TAS] Node failure controller should delete nodeToReplace annotation if a node recovers/reappears

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5571

**Last updated**: 2025-08-01T09:53:38Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-06-09T11:40:38Z
- **Updated**: 2025-08-01T09:53:38Z
- **Closed**: 2025-08-01T09:53:38Z
- **Labels**: `kind/bug`
- **Assignees**: [@pajakd](https://github.com/pajakd)
- **Comments**: 7

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Let's assume a Workload uses the whole capacity in a cluster. After node failure, a Workload gets annotated with nodeToReplace annotation. Let's say a node has then recovered and Workload can run as usual. After that Workload still have the annotation even if, there's no need to replace the node. It has a few consequences. First of all we waste scheduling cycle for a Workload that doesn't need the replacement. Secondly, if another node fails then the Workload will gets evicted while it shouldn't.

I'd like add a symmetric mechanism to current node failure controller, so it deletes the annotation if a node recovers/reappears.

**Why is this needed**:

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-06-09T11:40:49Z

/kind bug
/remove label feature

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-06-09T11:41:23Z

/remove-kind feature

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-06-09T11:41:45Z

/cc @pajakd @mimowo @mwysokin

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-09T11:55:35Z

+1

### Comment by [@pajakd](https://github.com/pajakd) — 2025-06-09T12:21:27Z

Yes, definitely we have to fix this. One thing to keep in mind will be the time complexity -- in each reconcile of the node failure controller, we list all the workloads and if we will want to reconcile on each update of healthy nodes this might take some time. But overall I agree.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-06-09T12:28:17Z

> Yes, definitely we have to fix this. One thing to keep in mind will be the time complexity -- in each reconcile of the node failure controller, we list all the workloads and if we will want to reconcile on each update of healthy nodes this might take some time. But overall I agree.

I'd say we should list only on an Update that changes status of a node from Ready=False -> Ready=True or on a Create event. In this case I think the time complexity is acceptable

### Comment by [@pajakd](https://github.com/pajakd) — 2025-07-31T12:30:04Z

/assign
