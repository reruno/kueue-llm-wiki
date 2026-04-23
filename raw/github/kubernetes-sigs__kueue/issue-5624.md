# Issue #5624: TAS cleanup: move optional parameters for FindTopologyAssignmentsForFlavor to options

**Summary**: TAS cleanup: move optional parameters for FindTopologyAssignmentsForFlavor to options

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5624

**Last updated**: 2025-06-12T17:08:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-11T13:55:36Z
- **Updated**: 2025-06-12T17:08:57Z
- **Closed**: 2025-06-12T17:08:57Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to move optional parameters to FindTopologyAssignmentsForFlavor as [cache options](https://github.com/kubernetes-sigs/kueue/blob/9535437ade9479a691994dad69dbe093de50a3ef/pkg/cache/cache.go#L62-L99) (simulateEmpty and Workload). 

Similar pattern as for example 

**Why is this needed**:

Improve code readability by skipping optional parameters. 

These parameters are not essential for the function. For example when calling in [unit tests](https://github.com/kubernetes-sigs/kueue/blob/9535437ade9479a691994dad69dbe093de50a3ef/pkg/cache/tas_cache_test.go#L1928C26-L1928C58) we pass false and nil.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-11T13:56:54Z

 @PBundyra @lchrzaszcz  ptal

cc @kaisoz @mbobrovskyi

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-12T16:22:39Z

I think we should also use the opts for FindTopologyAssignmentsForWorkload, then we can just propagate them when calling `FindTopologyAssignmentsForFlavor` from that function.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-12T16:30:15Z

/assign
