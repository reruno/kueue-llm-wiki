# Issue #7524: Add feature gate for reclaimable Pods feature

**Summary**: Add feature gate for reclaimable Pods feature

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7524

**Last updated**: 2025-11-05T08:40:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-11-04T13:30:53Z
- **Updated**: 2025-11-05T08:40:55Z
- **Closed**: 2025-11-05T08:40:55Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Feature gate for reclaimable Pods feature

**Why is this needed**:
To disable the feature. We observed that it can lead to too aggressive preemption.

When part of the quota is released, the preemption is issued whereas if the quota was released entirely an incoming workload could fit in without preemption. The rest of the quota is released O(100ms) later  so the improvement is negligible.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-04T14:23:44Z

> The rest of the quota is released O(100ms) later so the improvement is negligible.

It is negligible on some environments, but might be important on others, especially using embarassingly parallel Jobs where different tasks complete independently at different times.
