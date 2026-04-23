# Issue #3583: [Hierarchical Cohorts] Preemption only fetches candidates of ClusterQueue's parent Cohort

**Summary**: [Hierarchical Cohorts] Preemption only fetches candidates of ClusterQueue's parent Cohort

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3583

**Last updated**: 2024-12-02T13:49:00Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2024-11-18T15:35:16Z
- **Updated**: 2024-12-02T13:49:00Z
- **Closed**: 2024-12-02T13:49:00Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 1

## Description

**What happened**:
We need to traverse entire Cohort tree for preemption candidates, not just the ClusterQueues in the preempting ClusterQueue's parent Cohort

https://github.com/kubernetes-sigs/kueue/blob/94d829235a701d464b67f3f107d88bd178abfadb/pkg/scheduler/preemption/preemption.go#L516

## Discussion

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-11-18T15:35:30Z

cc @mimowo
