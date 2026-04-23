# Issue #4961: [Fair Sharing] Preempting Nominal Quota when FairSharing Weight is 0

**Summary**: [Fair Sharing] Preempting Nominal Quota when FairSharing Weight is 0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4961

**Last updated**: 2025-05-06T09:43:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2025-04-14T14:17:06Z
- **Updated**: 2025-05-06T09:43:03Z
- **Closed**: 2025-04-15T11:53:10Z
- **Labels**: `kind/bug`
- **Assignees**: [@gabesaba](https://github.com/gabesaba)
- **Comments**: 2

## Description

**What happened**:
When FairSharing weight=0, we even preempt even workloads using nominal quota

**What you expected to happen**:
Nominal quota workloads should be protected. Only borrowing should be immediately reclaimed/preempted

**How to reproduce it (as minimally and precisely as possible)**:
Create Queues/Cohorts of the following structure, with ReclaimWithinCohort=Any

- Root-Cohort
  - Best-Effort-Cohort(weight 0, nominal 1)
    - Best-Effort-Queue
  - High-Priority-Queue(weight 1, nominal 0)

Submit a workload to Best-Effort-Queue of size 1, then to High-Priority-Queue. Remark that high-priority-queue can preempt from best-effort, even when it is not borrowing. I'm not sure if this is also a problem in the flat case; this should also be tested:

- Root-Cohort
  - Best-Effort-Queue(weight 0, nominal 1)
  - High-Priority-Queue(weight 1, nominal 0)

- Kueue version: 0.11.3

## Discussion

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-04-14T14:29:26Z

/assign

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-05-06T09:43:02Z

Another consequence of this is that a Queue/Cohort with weight 0 is unable to reclaim its nominal quota. #4962 should fix this as well
