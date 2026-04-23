# Issue #18: Preserve order of podsets in workload info

**Summary**: Preserve order of podsets in workload info

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/18

**Last updated**: 2022-02-18T16:18:24Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-02-18T13:32:20Z
- **Updated**: 2022-02-18T16:18:24Z
- **Closed**: 2022-02-18T16:18:24Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 0

## Description

[TotalRequests](https://github.com/kubernetes-sigs/kueue/blob/b86eeb134e3721de9428eac99e286fe552ae72ee/pkg/workload/workload.go#L32) in workload.Info is currently a map, when iterating over it to assign resources, we will loose the original order of the podsets. 

When scheduling, a podset gets assigned flavors depending on the iteration order of this map, and so the assignment will not be deterministic. 

This actually caused a flake in the following test: https://github.com/kubernetes-sigs/kueue/blob/b86eeb134e3721de9428eac99e286fe552ae72ee/pkg/scheduler/scheduler_test.go#L406

/kind bug
