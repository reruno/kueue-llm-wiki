# Issue #9734: Historical Usage Fair Sharing: half-life based score for cohort-level scheduling and preemption

**Summary**: Historical Usage Fair Sharing: half-life based score for cohort-level scheduling and preemption

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9734

**Last updated**: 2026-03-07T07:47:52Z

---

## Metadata

- **State**: open
- **Author**: [@mukund-wayve](https://github.com/mukund-wayve)
- **Created**: 2026-03-07T07:44:34Z
- **Updated**: 2026-03-07T07:47:52Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

An alternative fair sharing mode that uses half-life decayed historical resource usage for cohort-level admission ordering and preemption. This extends the mechanism from Admission Fair Sharing (KEP-4136), currently scoped to ordering LocalQueues within a single ClusterQueue to both ordering and preempting ClusterQueues within a cohort. It coexists alongside the current Dominant Resource Share (DRS) from KEP-1714 as a configurable option.

Where DRS answers "who is borrowing the most right now?", historical usage answers "who has consumed the most over time?" — giving the system memory of past consumption. The mode is configured globally in the Kueue FairSharing config, with observability through CQ status fields and Prometheus metrics.

**Why is this needed**:

DRS is point-in-time and has no memory of past consumption. This creates problems for organizations where teams budget compute as a percentage of the cluster over a longer period (e.g., a week) but have bursty workloads:

1. A team idle for six days that bursts on day seven is immediately penalized by DRS, even though their cumulative usage is well within their fair share.
2. A CQ that just finished consuming most of the cohort for a week gets DRS = 0 the moment its workloads complete — identical to a CQ that has been idle for months. Both get full scheduling and preemption power immediately.
3. Two CQs with identical current borrowing are treated equally by DRS, even if one has been borrowing for a week and the other started five minutes ago.

KEP-1714 explicitly listed historical data as a non-goal but noted the design should be "expandable to support history-based Fair Sharing without major redesign." KEP-4136 introduced half-life decay for intra-CQ ordering but acknowledged cohort-level scope as future work. This feature closes that gap and I believe will be a significant improvement in the fair sharing offering of Kueue.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mukund-wayve](https://github.com/mukund-wayve) — 2026-03-07T07:47:52Z

I'm happy to raise a KEP for this
