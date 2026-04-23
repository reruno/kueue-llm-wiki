# Issue #9559: Add TASBalancedPlacement as a workload-level setting

**Summary**: Add TASBalancedPlacement as a workload-level setting

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9559

**Last updated**: 2026-02-27T09:37:21Z

---

## Metadata

- **State**: open
- **Author**: [@varunsyal](https://github.com/varunsyal)
- **Created**: 2026-02-27T09:37:21Z
- **Updated**: 2026-02-27T09:37:21Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Today, we can use the `TASBalancedPlacement` feature gate to set a global cluster-wide placement strategy. Can we add this at the workload-level as well? If it makes sense, the same could be done for other placement strategies supported by Kueue like `BestFit`.

**Why is this needed**:

This could enable use cases, where we can set  one global policy regarding the placement at the cluster level, but allow workloads to specify and override this through an annotation.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x ] API change
- [x ] Docs update

The artifacts should be linked in subsequent comments.
