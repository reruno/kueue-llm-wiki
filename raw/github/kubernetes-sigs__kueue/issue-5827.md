# Issue #5827: [AFS] Order candidates for preemption within the same ClusterQueue based on LQ's resource usage

**Summary**: [AFS] Order candidates for preemption within the same ClusterQueue based on LQ's resource usage

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5827

**Last updated**: 2025-07-04T14:57:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-07-01T09:54:45Z
- **Updated**: 2025-07-04T14:57:30Z
- **Closed**: 2025-07-04T14:57:30Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Order candidates for preemption within the same ClusterQueue based on LQ's resource usage 

**Why is this needed**:
Feature requested after gathering initial feedback. This makes it more complete as well

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] KEP update
- [ ] Code changes
- [ ] Doc changes

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-07-01T09:54:55Z

KEP update: https://github.com/kubernetes-sigs/kueue/pull/5817

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-07-04T10:42:52Z

/cc @mwysokin
