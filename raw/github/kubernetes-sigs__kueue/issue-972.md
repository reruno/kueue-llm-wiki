# Issue #972: Add metrics for ClusterQueue usage

**Summary**: Add metrics for ClusterQueue usage

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/972

**Last updated**: 2023-07-19T14:36:07Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-07-11T12:09:27Z
- **Updated**: 2023-07-19T14:36:07Z
- **Closed**: 2023-07-19T14:36:07Z
- **Labels**: `kind/feature`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 1

## Description

**What would you like to be added**:

Usage metrics for ClusterQueue quotas.

To uniquely identify the resources, we need the following labels: `cluster_queue`, `flavor`, `resource`.

Note that, depending on the number of ClusterQueues, ResourceFlavors and resources, these set of labels could have a big cardinality. For this reason, we need to make this metric opt-in. Additionally, we need to make sure to delete the metrics as ClusterQueues get deleted.

**Why is this needed**:

Administrators need these metrics to build dashboards and track usage.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2023-07-11T14:59:12Z

/assign
