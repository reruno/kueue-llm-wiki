# Issue #9876: Support guaranteed minimum runtime before fair sharing preemption

**Summary**: Support guaranteed minimum runtime before fair sharing preemption

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9876

**Last updated**: 2026-03-14T21:31:58Z

---

## Metadata

- **State**: open
- **Author**: [@mukund-wayve](https://github.com/mukund-wayve)
- **Created**: 2026-03-14T21:31:39Z
- **Updated**: 2026-03-14T21:31:58Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

A minAdmitDuration configuration option for fair sharing that prevents recently admitted workloads from being preempted by workloads in other ClusterQueues. Workloads admitted less than minAdmitDuration ago would be excluded from cross-CQ preemption candidates.

**Why is this needed**:

When the owner ClusterQueue wants its nominal quota back, the scheduler may preempt workloads before they have had enough time to make meaningful progress. There is currently no way to guarantee a minimum runtime for workloads against cross-CQ fair sharing preemption.

A configurable minimum admit duration would ensure all workloads make at least some progress before becoming eligible for fair sharing preemption.

This is complementary to [#8522](https://github.com/kubernetes-sigs/kueue/issues/8522), which addresses time-based preemption protection within a single ClusterQueue. This issue covers the cross-ClusterQueue case during fair sharing rebalancing.

User Story

As a cluster administrator, I want to configure a minimum duration that workloads must be admitted before they can be preempted by fair sharing, so that workloads borrowing resources from other ClusterQueues are guaranteed enough time to make meaningful progress.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.
