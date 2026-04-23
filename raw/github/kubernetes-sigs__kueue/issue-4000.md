# Issue #4000: Commonize the code for checking if workload is managed by Kueue

**Summary**: Commonize the code for checking if workload is managed by Kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4000

**Last updated**: 2025-02-26T09:38:33Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-01-17T16:23:24Z
- **Updated**: 2025-02-26T09:38:33Z
- **Closed**: 2025-02-26T09:38:33Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

As in the [comment](https://github.com/kubernetes-sigs/kueue/pull/3515/files#r1920426554) we have two instances of the same logic:
1. in [WorkloadShouldBeSuspended](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobframework/defaults.go#L49-L57) - first two checks
2. and in the new LWS PR we have IsManagedByKueue


**Why is this needed**:

To avoid duplication of complex logic, and so to reduce a chance of bugs.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-17T16:23:31Z

/assign @mbobrovskyi

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-28T15:21:54Z

@mbobrovskyi is it still a valid task?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-01-30T07:32:28Z

> [@mbobrovskyi](https://github.com/mbobrovskyi) is it still a valid task?

Yes, we need to use IsManagedByKueue function here https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobframework/defaults.go#L55-L57 and also need to check other places.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-30T07:58:39Z

Thanks!
