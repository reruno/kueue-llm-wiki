# Issue #6243: AFS: rename functions on ClusterQueues to avoid leaking implementation details about heaps

**Summary**: AFS: rename functions on ClusterQueues to avoid leaking implementation details about heaps

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6243

**Last updated**: 2025-07-30T15:36:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-29T13:00:23Z
- **Updated**: 2025-07-30T15:36:31Z
- **Closed**: 2025-07-30T15:36:31Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Currently, the implementation of AFS leaks implementation details to scheduler, for example: https://github.com/kubernetes-sigs/kueue/blob/2c0cb71c6d49a2066b9c4dbf99a908cd3f247c0d/pkg/scheduler/scheduler.go#L198-L201

Currently the function is named Heapify... leaks the implementation detail of the ClusterQueue as a heap. However, I would prefer to keep the API agnostic of the internals. We can rename it to "Repair" or "Rebuild".

**Why is this needed**:

It is anti-pattern to leak implementation details in the public API of a struct. Using heaps by ClusterQueues is an implementation detail. We have considered a couple of times in the past to change the underlying structure to BFS trees, or nested heaps.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-29T13:00:39Z

cc @PBundyra @IrvingMg

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-07-29T13:30:38Z

/assign
