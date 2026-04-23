# Issue #3530: Rename the reason for Evicted condition for deactivated workloads: WorkloadInactive -> Deactivated

**Summary**: Rename the reason for Evicted condition for deactivated workloads: WorkloadInactive -> Deactivated

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3530

**Last updated**: 2024-11-21T12:04:56Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-11-14T08:42:57Z
- **Updated**: 2024-11-21T12:04:56Z
- **Closed**: 2024-11-21T12:04:56Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 3

## Description

**What would you like to be added**:

Rename the reason InactiveWorkload -> Deactivated. 

[Here](https://github.com/kubernetes-sigs/kueue/blob/b6f39107bdb783c16c0bb17e54fba2f0831e2bbf/apis/kueue/v1beta1/workload_types.go#L517) is the definition.

Deprecate but continue supporting the old one for backwards- compatibility. We need a couple of releases or v1beta2 to drop the old one.

**Why is this needed**:

- the "Workload" is redundant. Other reasons don't contain it, see [here](https://github.com/kubernetes-sigs/kueue/blob/b6f39107bdb783c16c0bb17e54fba2f0831e2bbf/apis/kueue/v1beta1/workload_types.go#L519-L541).
- this is a reason for Evicted=True, so Deactivated reads better
- by analogy to Reactivated

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-14T08:43:08Z

cc @PBundyra @mbobrovskyi @tenzen-y

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-11-14T09:01:32Z

SGTM

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-19T13:57:54Z

/assign
