# Issue #6335: Add MultiKueue support for WorkloadSlices (KEP-77)

**Summary**: Add MultiKueue support for WorkloadSlices (KEP-77)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6335

**Last updated**: 2025-09-26T18:38:19Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2025-07-31T16:41:35Z
- **Updated**: 2025-09-26T18:38:19Z
- **Closed**: 2025-09-26T18:38:19Z
- **Labels**: `kind/feature`
- **Assignees**: [@ichekrygin](https://github.com/ichekrygin)
- **Comments**: 1

## Description

**Description:**

Now that the core WorkloadSlices functionality has been introduced in Kueue (as part of [KEP-77](https://github.com/kubernetes-sigs/kueue/tree/main/keps/77-dynamically-sized-jobs)), we would like to extend this support to MultiKueue.

Currently, MultiKueue does not propagate or track `WorkloadSlice` objects, which limits the ability to:

* Manage elastic jobs and dynamically sized workloads across clusters
* Perform cluster-aware slicing, scaling, and preemption
* Support distributed scheduling decisions based on partial slices

**Proposal:**

Enhance MultiKueue to:

* Track and propagate `WorkloadSlice` objects between member clusters and the central MultiKueue controller
* Maintain appropriate relationships and status sync between `Workload` and `WorkloadSlice` in multi-cluster topology
* Enable routing and admission logic that respects slice granularity and cluster-specific constraints

**Motivation:**

Support for WorkloadSlices in MultiKueue is a natural next step in enabling:

* True multi-cluster elastic job scheduling
* Fine-grained quota enforcement and admission control across slices
* Better control over preemption and workload fragmentation at scale

This enhancement will also help validate and evolve the WorkloadSlice API in more dynamic, distributed configurations.

**Related Work:**

* [KEP-77: WorkloadSlices](https://github.com/kubernetes-sigs/kueue/tree/main/keps/77-dynamically-sized-jobs)
* Initial WorkloadSlice support in core Kueue (v0.13)
* Existing MultiKueue implementation and sync primitives

/kind feature

## Discussion

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-08-07T15:45:50Z

/assign
