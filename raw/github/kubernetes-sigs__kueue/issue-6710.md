# Issue #6710: [AFS] Introduce cache that stores `.admissionFairSharingStatus.ConsumedResources` values

**Summary**: [AFS] Introduce cache that stores `.admissionFairSharingStatus.ConsumedResources` values

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6710

**Last updated**: 2025-11-26T14:12:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-09-03T07:49:43Z
- **Updated**: 2025-11-26T14:12:39Z
- **Closed**: 2025-11-26T14:12:39Z
- **Labels**: `kind/bug`, `kind/feature`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Currently, `admissionFairSharingStatus.ConsumedResources` is only stored in controller runtime informer. I'd like to add a field that represents it in cache.

**Why is this needed**:
With the present implementation it's hard to synchronize usage of this fields across different controllers.
E.g. Let's assume we have a thread that rebuilds the heap and it uses the `.consumedResources` field. It may rebuild a half of the heap but in the meantime some other thread updates the field. This can result in inconsistent sorting a thus, a wrong Workload is picked to be scheduled

Besides the race condition, the change will also make sorting/scheduling process faster

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-09-26T10:14:35Z

/kind bug

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-26T10:15:26Z

> E.g. Let's assume we have a thread that rebuilds the heap and it uses the .consumedResources field. It may rebuild a half of the heap but in the meantime some other thread updates the field. This can result in inconsistent sorting a thus, a wrong Workload is picked to be scheduled

@PBundyra is this phenomemon possible currently? If so I would call the issue a bug. If there is no bug, it is rather a cleanup. I would assume this might be prevented by locks. Or if it exists, then the question is why our tests don't flake due to it.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-09-29T08:59:30Z

I've synced with @mimowo and we agreed that it is a bug but because of it's nature it's hard to test it - mainly because the data race happens of controller-runtime informer layer and we have little leverage on provoking particular behaviors. That's why we don't have tests for it and it will be hard to even prove locally that it was mitigated. However, after we implement the changes we will be able to test if there are any race conditions as we would have better control over provoking some behaviors. I'll post more guidance on implementing this soon
