# Issue #1873: Make queueingStrategy mutable

**Summary**: Make queueingStrategy mutable

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1873

**Last updated**: 2024-04-04T17:11:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-03-20T19:59:19Z
- **Updated**: 2024-04-04T17:11:51Z
- **Closed**: 2024-04-04T17:11:51Z
- **Labels**: `kind/feature`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Make queueingStrategy in a ClusterQueue mutable.
This would cause a regeneration of the ClusterQueue priority queue in the kueue cache.

**Why is this needed**:

Currently, changing the strategy is only possible by draining the ClusterQueue, deleting and recreating.
Users might want to experiment with one strategy and later switch if they find that it doesn't suite their needs.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-26T14:01:55Z

/assign @mimowo
