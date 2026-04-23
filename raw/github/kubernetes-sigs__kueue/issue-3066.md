# Issue #3066: TestUpdateClusterQueue brittle test

**Summary**: TestUpdateClusterQueue brittle test

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3066

**Last updated**: 2024-09-24T08:52:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2024-09-16T10:48:05Z
- **Updated**: 2024-09-24T08:52:01Z
- **Closed**: 2024-09-24T08:52:01Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 1

## Description

**What would you like to be cleaned**:
in `queue.manager_test.go`, we attempt to create inadmissible workloads, to verify that they are later active when updating a ClusterQueue. Observe that they are never inadmissible, by adding an assertion right after their creation

https://github.com/kubernetes-sigs/kueue/blob/d786072f994668c0240889d93c63f48a620ea6ad/pkg/queue/manager_test.go#L159-L165

```
// also, manager.DumpInadmissible() will be empty
activeWorkloads := manager.Dump()
wantActiveWorkloads := map[string]sets.String{}
if diff := cmp.Diff(wantActiveWorkloads, activeWorkloads); diff != "" {
  t.Errorf("Unexpected active workloads (-want +got):\n%s", diff)
}
```

**Why is this needed**:
Test still passes after deletion of this section:
https://github.com/kubernetes-sigs/kueue/blob/d786072f994668c0240889d93c63f48a620ea6ad/pkg/queue/manager_test.go#L167-L185

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-20T07:30:06Z

/assign
