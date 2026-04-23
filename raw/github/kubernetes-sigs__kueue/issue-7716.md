# Issue #7716: MultiKueue: support generating MultiKueueCluster from ClusterProfile

**Summary**: MultiKueue: support generating MultiKueueCluster from ClusterProfile

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7716

**Last updated**: 2026-03-15T15:15:41Z

---

## Metadata

- **State**: open
- **Author**: [@hdp617](https://github.com/hdp617)
- **Created**: 2025-11-17T18:25:28Z
- **Updated**: 2026-03-15T15:15:41Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-longterm`, `area/multikueue`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
This is a follow up enhancement for #6714 as discussed [here](https://github.com/kubernetes-sigs/kueue/pull/6786#discussion_r2528480646). We want to automate cluster management by autogenerating MultiKueueCluster objects from ClusterProfile objects. Alternatively, we can also use ClusterProfile as the standardized representation of a cluster.

**Why is this needed**:
Usability - this simplifies cluster management by removing the need to manually create MultiKueueCluster objects and reference ClusterProfile objects.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:20:54Z

/area multikueue
/priority important-longterm

### Comment by [@yashnib](https://github.com/yashnib) — 2026-01-23T05:27:21Z

Hi! I’d be happy to work on this enhancement.

I’ll take a look at the current behavior and see how we can extend it in the way described here. Let me know if there’s any context or constraints I should be aware of.

### Comment by [@andrewseif](https://github.com/andrewseif) — 2026-03-15T15:15:41Z

is there any updates on this? 😄
