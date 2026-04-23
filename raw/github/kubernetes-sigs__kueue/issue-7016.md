# Issue #7016: Clusterqueues must prefer borrowing within a cohort before borrowing across cohorts.

**Summary**: Clusterqueues must prefer borrowing within a cohort before borrowing across cohorts.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7016

**Last updated**: 2025-09-29T06:26:17Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@varunsyal](https://github.com/varunsyal)
- **Created**: 2025-09-25T18:03:46Z
- **Updated**: 2025-09-29T06:26:17Z
- **Closed**: 2025-09-29T06:26:17Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

When hierarchical cohorts are used with multiple flavors, a clusterqueue should prefer scheduling in the flavor such that borrowing first happens from other clusterqueues within its parent cohort, before borrowing from clusterqueues of other cohorts. However that does not happen with multiple flavors. 
Due to this, even when the cohort has nominal quota in the second flavor, it tends to borrow in the first flavor, making the workloads prone to preemption.



**What you expected to happen**:

If a cohort's usage is below its nominal quota, it should not try to borrow from another cohort in case of multiple flavors. This leads to unnecessary preemptions when the other cohort needs to reclaim it nominal quota

**How to reproduce it (as minimally and precisely as possible)**:

Example:
Total Size of Cluster:
- Flavor-1 = 10
- Flavor-2 = 10

<img width="1493" height="1150" alt="Image" src="https://github.com/user-attachments/assets/9f81e0f5-769d-42bb-ad4d-71adc403e648" />

If we submit 18 workloads each using resources = 1 to clusterqueue cq-p1, we observe that it schedules 10 workloads in Flavor-1 and 8 workloads in Flavor-2. This makes the cohort-A which has a total nominal quota of 18 in its subtree to be borrowing 2 resources from cohort-B, and thus has a positive fair sharing weighted share, even though its total usage is within its total nominal quota.

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): v1.32.7
- Kueue version (use `git describe --tags --dirty --always`): 0.13.4
- Feature Flag enabled: **FlavorFungibilityImplicitPreferenceDefault=True**

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-09-25T18:37:13Z

/cc

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-09-26T09:36:46Z

https://github.com/kubernetes-sigs/kueue/blob/50ae9545051ed20c15888b63ece31f39ea037abe/pkg/scheduler/flavorassigner/flavorassigner.go#L712

I think that the key is this line. We need to not treat this as a boolean, but as an integer, if we want to find a better assignment in hierarchical case
