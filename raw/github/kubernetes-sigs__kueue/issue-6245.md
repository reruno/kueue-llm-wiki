# Issue #6245: AFS: consider encapsulating the entry penalties logic within ClusterQueues

**Summary**: AFS: consider encapsulating the entry penalties logic within ClusterQueues

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6245

**Last updated**: 2025-09-05T09:15:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-29T13:18:42Z
- **Updated**: 2025-09-05T09:15:29Z
- **Closed**: 2025-09-05T09:15:29Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Currently Kueue scheduler is aware of the penalties and triggeres "fixing" of the ClusterQueues. 

I would like to investigate encapsulating the logic within ClusterQueues, at least so that they decide when to "rebuild" / "heapify" themselves. 

**Why is this needed**:

Drawbacks of the current design:
- Scheduler needs to know about the internals of the ClusterQueus - when Heapify/Rebuild needs to happen
- The access to ClusterQueues requires multiple calls, like HasPendingPenalties, Heapify etc, and the scope of locking is just one call. It means that results of the first call might get invalidated before the next call.

For example, we could consider a design in which scheduler just sets the penalties (or other controller), and the "Head()" function on Cluster Queue fixes the CQ if needed - if there are any pending penalties, then it would "rebuild" itself.

Similar design is often practiced in structures like self-balancing BFS trees, where the user of the structure does not need to "rebalance" the structure externally.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-29T13:18:53Z

cc @PBundyra @IrvingMg

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-09-01T07:52:59Z

/assign
