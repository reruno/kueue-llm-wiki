# Issue #7063: Inconsistent limit on the number of resources and flavors in a ClusterQueue

**Summary**: Inconsistent limit on the number of resources and flavors in a ClusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7063

**Last updated**: 2025-09-30T06:48:18Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@oyangz](https://github.com/oyangz)
- **Created**: 2025-09-29T18:08:20Z
- **Updated**: 2025-09-30T06:48:18Z
- **Closed**: 2025-09-30T06:48:18Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 1

## Description

**What happened**:

In PR [#6906](https://github.com/kubernetes-sigs/kueue/pull/6906), the coveredResource and Flavors limits where increased to 64, however some fields still use the old limit of 16, including the [Resources under FlavorQuotas](https://github.com/kubernetes-sigs/kueue/blob/c05bfbd980952fd47b9957c9c5952dada41f0996/apis/kueue/v1beta1/clusterqueue_types.go#L215-L216) and [FlavorsReservation and FlavorsUsage under ClusterQueueStatus](https://github.com/kubernetes-sigs/kueue/blob/c05bfbd980952fd47b9957c9c5952dada41f0996/apis/kueue/v1beta1/clusterqueue_types.go#L277-L291).

So when creating ClusterQueues with more than 16 resources per flavor, we will get an error:
```
* spec.resourceGroups[0].flavors[0].resources: Too many: 33: must have at most 16 items
```

**What you expected to happen**:

The above fields should have MaxItems of 64 to match the limit on coveredResources and Flavors in order to successfully create ClusterQueue Flavors with up to 64 resources.

**How to reproduce it (as minimally and precisely as possible)**:

Create a ClusterQueue with more than 16 resources in a resourceGroup.


**Anything else we need to know?**:

**Environment**: 
- Kubernetes version (use `kubectl version`): v1.33.4
- Kueue version (use `git describe --tags --dirty --always`): da94f0576
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-29T18:20:58Z

@oyangz please submit a PR if you want to get this in 0.14
