# Issue #40: Match workload tolerations with capacity taints

**Summary**: Match workload tolerations with capacity taints

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/40

**Last updated**: 2022-02-24T01:15:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-02-21T02:05:30Z
- **Updated**: 2022-02-24T01:15:35Z
- **Closed**: 2022-02-24T01:15:35Z
- **Labels**: `kind/feature`, `priority/important-soon`
- **Assignees**: [@ahg-g](https://github.com/ahg-g)
- **Comments**: 1

## Description

During workload scheduling, a workload's tolerations should be matched against the taints of the resource flavors. This allows a workload to opt-in to specific flavors.

/kind feature
/priority important-soon

## Discussion

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-02-22T04:42:57Z

/assign
