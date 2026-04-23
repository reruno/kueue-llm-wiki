# Issue #4644: Consider PathToRoot(ClusterQueue) iter.Seq[Cohort]

**Summary**: Consider PathToRoot(ClusterQueue) iter.Seq[Cohort]

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4644

**Last updated**: 2025-04-14T09:16:56Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2025-03-17T10:15:56Z
- **Updated**: 2025-04-14T09:16:56Z
- **Closed**: 2025-04-14T09:16:56Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@KPostOffice](https://github.com/KPostOffice)
- **Comments**: 1

## Description

**What would you like to be cleaned**:
https://github.com/kubernetes-sigs/kueue/pull/4572#discussion_r1998270743

Find places this pattern is used, and come up with general code to handle all the cases, potentially by using Iterator. If it is cleaner, create PR. If not, explain why not and close this issue

Known usages:
- [pkg/scheduler/preemption/fairsharing/least_common_ancestor.go](https://github.com/kubernetes-sigs/kueue/blob/fc1aaa51dae1c5e8ed7280b0483e343e575cd5be/pkg/scheduler/preemption/fairsharing/least_common_ancestor.go#L37-L42)
- [scheduler/fair_sharing_iterator.go](https://github.com/kubernetes-sigs/kueue/blob/f82aae0ba5a16cd6e3346d5d8d6b87772eba14f7/pkg/scheduler/fair_sharing_iterator.go#L210-L217)
- [cache/cache.go](https://github.com/kubernetes-sigs/kueue/blob/1863ca7d6bbcc323bbd851d6d08115900dff20f8/pkg/cache/cache.go#L735-L738)

**Why is this needed**:

## Discussion

### Comment by [@KPostOffice](https://github.com/KPostOffice) — 2025-03-25T18:51:12Z

/assign
