# Issue #200: introduce priorityFIFO as another QueueingStrategy of ClusterQueue

**Summary**: introduce priorityFIFO as another QueueingStrategy of ClusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/200

**Last updated**: 2022-04-10T15:09:46Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2022-04-10T10:40:08Z
- **Updated**: 2022-04-10T15:09:46Z
- **Closed**: 2022-04-10T15:09:46Z
- **Labels**: `kind/feature`
- **Assignees**: [@kerthcet](https://github.com/kerthcet)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Introduce another queue whose elements are ordered by the workload priority.
**Why is this needed**:
It's a general requirement as in kube-scheduler. We do have priority field introduced in Workload.

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-04-10T10:40:13Z

/assign

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-04-10T10:46:27Z

Well, I found @denkensk has already finished part of the feature https://github.com/kubernetes-sigs/kueue/pull/104, do you still working on the rest part?

### Comment by [@denkensk](https://github.com/denkensk) — 2022-04-10T14:28:21Z

The workloads are already sorted by the priory. It's the default strategy.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-04-10T15:09:46Z

got it.
