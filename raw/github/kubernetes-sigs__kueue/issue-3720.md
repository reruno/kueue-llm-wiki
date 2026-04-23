# Issue #3720: TAS: resource flavor tolerations are not considered during scheduling

**Summary**: TAS: resource flavor tolerations are not considered during scheduling

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3720

**Last updated**: 2024-12-03T15:23:09Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-12-03T12:39:30Z
- **Updated**: 2024-12-03T15:23:09Z
- **Closed**: 2024-12-03T15:23:09Z
- **Labels**: `kind/bug`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 1

## Description

**What happened**:

Resource flavor tolerations (in spec.tolerations) are not considered for scheduling.
Only the tolerations which are already on the pod are considered (see [here](https://github.com/kubernetes-sigs/kueue/blob/86e8b0ba49f2ba5a50b90eb5e1f9c929c113eb6f/pkg/cache/tas_flavor_snapshot.go#L387-L389)).

As a consequence a workload which does not have the necessary tolerations is not scheduled against tained nodes, even thought the RF would add the tolerations later on.

**What you expected to happen**:

Consider the RF tolerations when scheduling since the tolerations are added later on, they would allow scheduling on the nodes
https://github.com/kubernetes-sigs/kueue/blob/86e8b0ba49f2ba5a50b90eb5e1f9c929c113eb6f/pkg/podset/podset.go#L81

**How to reproduce it (as minimally and precisely as possible)**:

1. configure TAS with a group of nodes using the taint `nvidia.com/gpu`
2. create a TAS Resource flavor with tolerations to `nvidia.com/gpu`
3. create a workload which would be scheduled using the TAS RF (without tolerations)

Issue: the workload is not scheduled.

**Anything else we need to know?**:

We have an analogous issue for regular Kueue, but I suggest to handle separately as (1) the fix is in different place, (2) the issue in core Kueue is longer so potentially requires more discussion

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-03T12:39:48Z

/assign @mimowo 
cc @PBundyra @tenzen-y
