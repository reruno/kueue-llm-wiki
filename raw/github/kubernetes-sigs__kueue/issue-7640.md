# Issue #7640: Add performance tests for v1beta2 TopologyAssignment encoding

**Summary**: Add performance tests for v1beta2 TopologyAssignment encoding

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7640

**Last updated**: 2025-11-26T17:30:46Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@olekzabl](https://github.com/olekzabl)
- **Created**: 2025-11-13T12:41:11Z
- **Updated**: 2025-11-26T17:30:46Z
- **Closed**: 2025-11-26T17:30:46Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@olekzabl](https://github.com/olekzabl)
- **Comments**: 1

## Description

**What would you like to be cleaned**:

#7544 adds `V1Beta2From()` to convert "internal" representation of a TopologyAssignment to the "public" v1beta2 format, aiming at fitting more nodes within a single etcd entry.

Ideally I'd like to have "performance" tests for this, of 2 kinds:

- verifying that, at least for the most popular node naming schemes, we can fit 60k nodes
- verifying that the conversion itself does not take too much time (a Golang benchmark)

**Why is this needed**:

This will have some value right away, plus it will become helpful once we consider switching to more sophisticated encoding approaches (i.e. using multiple TopologyAssignmentSlices).

## Discussion

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-11-20T22:29:22Z

/assign
