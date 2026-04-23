# Issue #3756: TAS: optimize the algorithm to minimize fragmentation

**Summary**: TAS: optimize the algorithm to minimize fragmentation

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3756

**Last updated**: 2025-02-14T11:02:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-12-06T15:07:15Z
- **Updated**: 2025-02-14T11:02:23Z
- **Closed**: 2025-02-14T11:02:23Z
- **Labels**: `kind/feature`
- **Assignees**: [@PBundyra](https://github.com/PBundyra)
- **Comments**: 1

## Description

**What would you like to be added**:

In some cases there are low-hanging fruit optimizations to the algorithm. For example, if the workload requires 2GPU, and there are two nodes allowing to fit the workload, we currently choose the one with more space, say 4GPUs, which leaves us with 2 nodes each having 2 GPUs free - the capacity gets fragmented. Similar heuristics are possible for cases with 2 nodes, but probably it is a hard problem in general. 

We may need to decide if we just go with the low-hanging fruit heuristics or we have some API which allows to control fragmentation vs. complexity of the scheduling algorithm.

**Why is this needed**:

The current algorithm leads to create unnecessary fragmentation of the capacity, as indicated in the simple example above.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-01-21T13:13:10Z

/assign
