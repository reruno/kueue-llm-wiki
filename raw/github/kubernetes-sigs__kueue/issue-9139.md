# Issue #9139: Ensure the `lessFunc(a,a)=false` for all workloads

**Summary**: Ensure the `lessFunc(a,a)=false` for all workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9139

**Last updated**: 2026-02-12T17:08:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-12T06:19:42Z
- **Updated**: 2026-02-12T17:08:03Z
- **Closed**: 2026-02-12T17:08:03Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I think this is a bug, because for sticky workloads we can get `lessFunc(a,a)=true`, if a is a "sticky workload".

https://github.com/kubernetes-sigs/kueue/blob/main/pkg/cache/queue/cluster_queue.go#L609-L614

I'm categorizing as a cleanup, because I'm not sure the sorter would ever invoke `lessFunc` with the same argument.

**Why is this needed**:

To make sure the implementation of `lessFunc(a,a)` returns false. Otherwise it may be source of subtle bugs, depending on the sorter implementation.

Realized when reviewing https://github.com/kubernetes-sigs/kueue/pull/9101/changes#r2796953037

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-12T06:19:52Z

cc @sohankunkerkar @gabesaba

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-02-12T12:28:54Z

/assign
