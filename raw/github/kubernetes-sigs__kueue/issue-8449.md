# Issue #8449: [TAS] Count resource usage of non-TAS Pods in event-driven manner

**Summary**: [TAS] Count resource usage of non-TAS Pods in event-driven manner

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8449

**Last updated**: 2026-01-20T09:02:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2026-01-07T13:00:43Z
- **Updated**: 2026-01-20T09:02:58Z
- **Closed**: 2026-01-20T09:02:58Z
- **Labels**: `kind/bug`, `priority/important-soon`
- **Assignees**: [@gabesaba](https://github.com/gabesaba)
- **Comments**: 10

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
To make scheduling decision in TAS as accurate as possible, Kueue needs information about how much available resources are on nodes in the cluster. Currently, on every scheduling cycle Kueue lists all Nodes and Pods in the cluster and counts how much resources are left after subtracting resources used by running Pods. I'd like to have an alternative approach which would count Pods' usage based on events instead. Then every scheduling cycle could just copy the results.

This requires creating:
1) In Kueue cache, mapping from a Node to it's allocatable/consumed resources
2) A separate controller that would update this mapping based on events   

As the first step we could just count non-TAS Pods, but later I'd like to make this more unified and count both non-TAS and TAS Pods

**Why is this needed**:
At scale, this process can take around 90% of the total time spent on scheduling in Kueue and leads to insufficient throughput. 

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2026-01-07T13:00:50Z

/assign

### Comment by [@PBundyra](https://github.com/PBundyra) — 2026-01-07T13:12:44Z

/kind bug

### Comment by [@PBundyra](https://github.com/PBundyra) — 2026-01-07T13:13:11Z

/remove-kind feature

### Comment by [@PBundyra](https://github.com/PBundyra) — 2026-01-07T13:13:32Z

/priority important-soon

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-01-08T01:46:26Z

/assign

### Comment by [@PBundyra](https://github.com/PBundyra) — 2026-01-08T08:35:00Z

/unassign

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-01-08T21:22:17Z

<img width="4500" height="1828" alt="Image" src="https://github.com/user-attachments/assets/f02d402e-9aef-4573-94d9-df31df291c5c" />

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-01-08T21:33:37Z

The risk of the proposal in issue description is the complexity of computing the cached value accurately, as it can change based on on 1) pod 2) node 3) resource flavor 4) topology changes. I think that doing an incremental update on pod changes, and full rebuild of cache on any other change (with appropriate event filters) would the least risky.

Alternative option: avoid a copy, and use a pointer to the pods in the informer cache. This approach risks of memory corruption if any of our calculations on the pod ends up mutating the pod.

I don't love either of these options. I will try to come up with a third.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-01-08T22:36:30Z

Variant of option 1, but simpler/safer: only cache pod to {node, usage} mapping. We only watch pod events. Use this for calculating non-tas usage during snapshot (where previously we would list all pods here).

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-09T09:53:39Z

> The risk of the proposal in issue description is the complexity of computing the cached value accurately, as it can change based on on 1) pod 2) node 3) resource flavor 4) topology changes. I think that doing an incremental update on pod changes, and full rebuild of cache on any other change (with appropriate event filters) would the least risky.

The risk attribution does not seem accurate, we can move the discussion to the thread: https://github.com/kubernetes-sigs/kueue/pull/8484#discussion_r2675539399
