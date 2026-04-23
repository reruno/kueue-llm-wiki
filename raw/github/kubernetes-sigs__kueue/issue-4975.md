# Issue #4975: Use WorkloadReference to improve static code analysis

**Summary**: Use WorkloadReference to improve static code analysis

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4975

**Last updated**: 2025-06-03T08:14:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-04-15T08:22:03Z
- **Updated**: 2025-06-03T08:14:39Z
- **Closed**: 2025-06-03T08:14:39Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Follow up to https://github.com/kubernetes-sigs/kueue/issues/4530, focused on Workloads.

**Why is this needed**:

To make it easier to reason about the code which is using strings to represent workload Keys. For example in cache https://github.com/kubernetes-sigs/kueue/blob/82f1326d3c292a8381968d584d8ee11d78076f0d/pkg/cache/cache.go#L107

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-15T08:22:17Z

/assign @vladikkuzn 
tentatively
cc @gabesaba
