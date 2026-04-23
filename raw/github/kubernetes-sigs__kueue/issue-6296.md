# Issue #6296: Commonize the code for workload eviction

**Summary**: Commonize the code for workload eviction

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6296

**Last updated**: 2025-08-05T06:15:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-30T15:46:44Z
- **Updated**: 2025-08-05T06:15:40Z
- **Closed**: 2025-08-05T06:15:40Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Commonize workload eviction by using the common workload.EvictWorkload function (or just workload.Evict).

**Why is this needed**:

Currently many different places handles workload eviction in slightly different ways, we should commonize to make bugs less likely.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-30T15:47:01Z

/assign 
tentatively
