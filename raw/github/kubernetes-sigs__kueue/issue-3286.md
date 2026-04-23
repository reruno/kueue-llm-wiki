# Issue #3286: Document how preemption fields interact with fair sharing strategies

**Summary**: Document how preemption fields interact with fair sharing strategies

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3286

**Last updated**: 2024-10-23T09:26:53Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-10-22T16:01:59Z
- **Updated**: 2024-10-23T09:26:53Z
- **Closed**: 2024-10-23T09:26:53Z
- **Labels**: `kind/documentation`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Clarify the semantics of `reclaimWithinCohort` and `withinClusterQueue` when using fair sharing and how it affects choosing candidates for preemption.

/kind documentation

**Why is this needed**:

The documentation leaves many open questions

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-10-22T16:02:09Z

/remove-kind feature
