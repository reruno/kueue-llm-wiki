# Issue #3671: TAS: Optimize Workload object size by listing only hostname values in `.status.TopologyAssignment` field

**Summary**: TAS: Optimize Workload object size by listing only hostname values in `.status.TopologyAssignment` field

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3671

**Last updated**: 2024-11-29T10:38:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-11-27T16:40:40Z
- **Updated**: 2024-11-29T10:38:59Z
- **Closed**: 2024-11-29T10:38:59Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Optimization to list only hostname values in TopologyAssignment if a user defines `kubernetes.io/hostname` in `Topology` object

**Why is this needed**:
To optimize Workload object size. Currently etcd object size is limited to 1,5MB and on large scale this can be a blocker for us to support big hero workloads

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-27T17:07:43Z

cc @tenzen-y the reason is that if user specifies the `kubernetes.io/hostname` as the lowest level, then we don't need to pass the entire list of values in the `TopologyAssignment.domain[].values`, because the last value already identifies the node in the cluster. So, having just this in the nodeSelector for the pod is enough. In case "subblock" or "block" being the lowest level we still need to pass the entire path, because they could not be unique in the cluster.

So, assuming 50bytes per level, 4 levels, and 1Mi for the topology assignment, then we could only have 5k domains, as : 4 * 50 bytes * 5000 domains = 10^6 bytes. By setting only the lowest level we can assign 20k domains, which is good enough for most big clusters.
