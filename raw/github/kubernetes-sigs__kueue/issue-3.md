# Issue #3: Match workload affinity with capacity labels

**Summary**: Match workload affinity with capacity labels

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3

**Last updated**: 2022-03-01T14:21:48Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-02-17T22:04:38Z
- **Updated**: 2022-03-01T14:21:48Z
- **Closed**: 2022-03-01T14:21:48Z
- **Labels**: `kind/feature`, `size/L`, `priority/important-longterm`
- **Assignees**: [@ahg-g](https://github.com/ahg-g)
- **Comments**: 1

## Description

During workload scheduling, a workload's node affinities and selectors should be matched against the labels of the resource flavors. This allows a workload to specify which exact flavors to use, or even force a different evaluation order of the flavors than that defined by the capacity.

/kind feature

## Discussion

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-02-25T17:03:54Z

/assign
