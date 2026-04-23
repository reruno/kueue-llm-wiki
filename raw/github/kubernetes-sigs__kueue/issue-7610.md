# Issue #7610: Automate default LocalQueue creation based on ClusterQueue namespaceSelector

**Summary**: Automate default LocalQueue creation based on ClusterQueue namespaceSelector

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7610

**Last updated**: 2025-11-20T12:56:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@j-skiba](https://github.com/j-skiba)
- **Created**: 2025-11-12T10:33:47Z
- **Updated**: 2025-11-20T12:56:02Z
- **Closed**: 2025-11-20T12:56:02Z
- **Labels**: `kind/feature`
- **Assignees**: [@j-skiba](https://github.com/j-skiba)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

This feature would automate the creation of a default `LocalQueue` within a namespace when that namespace is created or labeled to match a `ClusterQueue`'s `namespaceSelector`.

The proposal suggests making this an opt-in feature on the `ClusterQueue` spec, potentially through a new field like `autoLocalQueue`, which would specify the name for the default `LocalQueue` to be created.

**Why is this needed**:

Currently, even when a `ClusterQueue`'s `namespaceSelector` is configured to allow workloads from specific namespaces, an administrator must still manually create a `LocalQueue` in each of those namespaces. This enhancement would automate that manual step, simplifying the setup and management for administrators.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@j-skiba](https://github.com/j-skiba) — 2025-11-12T10:33:55Z

/assign

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-12T16:40:31Z

@Edwinhr716 wdyt of this? Would this satisfy your use case for AutoKueue?

### Comment by [@Edwinhr716](https://github.com/Edwinhr716) — 2025-11-12T16:55:54Z

Yes, this satisfies it. cc @ahg-g
