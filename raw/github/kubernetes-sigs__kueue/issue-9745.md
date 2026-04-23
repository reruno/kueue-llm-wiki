# Issue #9745: Request kueue-populator support multi-team use different ClusterQueues in single namespace.

**Summary**: Request kueue-populator support multi-team use different ClusterQueues in single namespace.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9745

**Last updated**: 2026-04-13T18:52:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@samzong](https://github.com/samzong)
- **Created**: 2026-03-09T03:03:42Z
- **Updated**: 2026-04-13T18:52:12Z
- **Closed**: 2026-04-13T18:52:12Z
- **Labels**: `kind/feature`
- **Assignees**: [@samzong](https://github.com/samzong)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Add a `useClusterQueueName` as a option to `kueue-populator` that uses the
ClusterQueue name as the LocalQueue name.

Currently, when multiple ClusterQueues match a namespace via `namespaceSelector`,
only the first ClusterQueue gets a LocalQueue created, subsequent ones are skipped
with a warning event.

With `useClusterQueueName: true`, each matching ClusterQueue creates a LocalQueue
named after itself. Since ClusterQueue names are cluster-unique, there are no naming
conflicts within a namespace.

**Why is this needed**:

In multi-team / multi-tenant clusters, different teams use different ClusterQueues.
A single namespace can legitimately need access to more than one ClusterQueue (e.g.
a shared namespace that both `team-a` and `team-b` can submit workloads to).

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@samzong](https://github.com/samzong) — 2026-03-09T03:04:03Z

/assign
