# Issue #8748: TAS: re-creating topology instance leads to cache corruption

**Summary**: TAS: re-creating topology instance leads to cache corruption

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8748

**Last updated**: 2026-01-23T13:27:33Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-22T14:36:51Z
- **Updated**: 2026-01-23T13:27:33Z
- **Closed**: 2026-01-23T13:27:33Z
- **Labels**: `kind/bug`, `priority/important-soon`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 2

## Description


**What happened**:

When an instance of a topology is deleted and re-created it leads to cache corruption, and in consequence incorrect admissions:
1. it can lead to unexpected placement on two Pods on the same node which does not have enough capacity
2. it can lead to scheduling another workload on an occupied node

**What you expected to happen**:

Kueue should gracefully handle re-creating of Topology. The usage coming from pre-existing workloads should be correctly taken into account.

**How to reproduce it (as minimally and precisely as possible)**:

1. Create a workload binding a specific node with 1GPU, the workload using 1GPU
2. Re-create the topology
3. Delete the workload
4. Create a new workload 2x size (2 pods with 1 GPU each). 
5. 
Issue: both pods will be placed on the same node by Kueue.

**Anything else we need to know?**:

It is really hard to update a Topology currently, as Topology is immutable. Also, RF using Topology is immutable. 

The only workaround we found for the issue:
1. put all CQs on hold, setting spec.stopPolicy=HOLD
2. update the Topology by re-creating
3. restart Kueue <- essential step to rebuild the cache
4. resume all CQs, by setting spec.stopPolicy=NONE

This works fine, but this is not documented, and tricky to follow.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-22T14:37:13Z

/assign 
Let me try to fix

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-22T14:37:21Z

/priority important-soon
