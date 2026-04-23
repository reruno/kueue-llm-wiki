# Issue #2109: Allow stoping admission from a specific LocalQueue

**Summary**: Allow stoping admission from a specific LocalQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2109

**Last updated**: 2024-06-10T15:00:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mwielgus](https://github.com/mwielgus)
- **Created**: 2024-05-01T16:01:31Z
- **Updated**: 2024-06-10T15:00:28Z
- **Closed**: 2024-06-10T15:00:28Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 1

## Description

**What would you like to be added**:

Option to stop admission from a specific LocalQueue, while keeping ClusterQueue and other LocalQueues pointing to it intact.

**Why is this needed**:

ClusterQueue controls are at the cluster level. So stoping a CQ affects all LQs pointing to it. There is no way to turn admission just for a specific namespace/LQ.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ x ] Design doc
- [ x ] API change
- [ x ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-05-07T05:03:52Z

/assign
