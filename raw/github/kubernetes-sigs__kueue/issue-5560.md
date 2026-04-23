# Issue #5560: TAS: Replace the "NodeToReplace" annotation with a proper status field

**Summary**: TAS: Replace the "NodeToReplace" annotation with a proper status field

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5560

**Last updated**: 2025-09-05T14:21:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-09T08:42:38Z
- **Updated**: 2025-09-05T14:21:29Z
- **Closed**: 2025-09-05T14:21:29Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@pajakd](https://github.com/pajakd)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to replace the "NodeToReplace" with the proper status API.

This was deferred for later due to [uncertainty about the API](https://github.com/kubernetes-sigs/kueue/tree/main/keps/2724-topology-aware-scheduling#failed-nodes-in-workloadstatus).

However, I think could make the API generic enough so that it can be extended, maybe:
```yaml
status:
  topologyAssignmentRecovery:
     nodesToReplace:
     - name: node1
```

**Why is this needed**:

The annotation requires a dedicated API request to update it, aside from status. 

This means it is difficult to reason about the correctness of the code, because it makes the eviction and node replacement  process "two step", examples:
- it was source of subtle bugs https://github.com/kubernetes-sigs/kueue/pull/5272 
- it requires code which is "detached" to cleanup the annotation here https://github.com/kubernetes-sigs/kueue/pull/5287/files#diff-60dd240c20adbd6a189d018d1c216c2d296730f446c341d8bf449fa6657964ffR197-R209
- it triggers an unnecessary second pass in case of https://github.com/kubernetes-sigs/kueue/issues/5511

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-09T08:42:59Z

cc @pajakd @PBundyra @tenzen-y @mwysokin @mwielgus

### Comment by [@pajakd](https://github.com/pajakd) — 2025-08-11T07:22:07Z

/assign
