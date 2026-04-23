# Issue #2136: [kueuectl] Add stop ClusterQueue command

**Summary**: [kueuectl] Add stop ClusterQueue command

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2136

**Last updated**: 2024-05-21T06:28:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-05-06T07:17:43Z
- **Updated**: 2024-05-21T06:28:51Z
- **Closed**: 2024-05-21T06:28:51Z
- **Labels**: `kind/feature`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Add stop ClusterQueue command on kueuectl.

**Why is this needed**:
To stops admission and execution inside the specified ClusterQueue, possibly limiting the action only to the selected ResourceFlavor.

Design details https://github.com/kubernetes-sigs/kueue/tree/main/keps/2076-kueuectl#stop-clusterqueue.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2024-05-13T00:08:26Z

/assign
