# Issue #1714: Support for fair sharing of unused resources

**Summary**: Support for fair sharing of unused resources

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1714

**Last updated**: 2024-05-08T16:35:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mwielgus](https://github.com/mwielgus)
- **Created**: 2024-02-09T15:56:44Z
- **Updated**: 2024-05-08T16:35:16Z
- **Closed**: 2024-05-08T16:35:16Z
- **Labels**: `kind/feature`
- **Assignees**: [@mwielgus](https://github.com/mwielgus)
- **Comments**: 1

## Description

**What would you like to be added**:

Fair sharing of unused resources between ClusterQueues.

**Why is this needed**:

Currently Kueue distributes unused resources on "first come first served" basis. So users who submit their workloads at, say, 6 am may take over the whole unused capacity for the whole day (assuming that the other jobs have the same priority). 

**Completion requirements**:

This enhancement requires the following artifacts:

- [ x ] Design doc
- [ x ] API change
- [ x ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mwielgus](https://github.com/mwielgus) — 2024-02-09T15:57:05Z

/assign @mwielgus
