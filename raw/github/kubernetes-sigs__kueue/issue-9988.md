# Issue #9988: Support quota automation in MultiKueue manager cluster

**Summary**: Support quota automation in MultiKueue manager cluster

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9988

**Last updated**: 2026-03-25T13:50:05Z

---

## Metadata

- **State**: open
- **Author**: [@olekzabl](https://github.com/olekzabl)
- **Created**: 2026-03-18T18:41:54Z
- **Updated**: 2026-03-25T13:50:05Z
- **Closed**: —
- **Labels**: `kind/feature`, `area/multikueue`
- **Assignees**: [@olekzabl](https://github.com/olekzabl)
- **Comments**: 2

## Description

**What would you like to be added**:

An option to automatically adjust the quotas for a MultiKueue manager cluster ClusterQueue based on the total worker quotas.

**Why is this needed**:

Currently, MultiKueue docs advise keeping manager quotas in sync with worker quotas: specifically, equal to the sum of worker quotas. There are 2 problems with this:

- When such maintenance is left as user's responsibility, it is inconvenient and error-prone.
- Strict equality may not be optimal for scheduling throughput. A user may want to keep the manager quota _somewhat above_ or _somewhat below_ total workers' quota, depending on the use case.

A relatively simple yet reasonably powerful approach here would be to introduce a configurable _relative multiplier_ (i.e. keep manager quota equal to `customMultiplier * sum(workerQuotas)`).

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-03-18T18:42:21Z

/area multikueue
/assign

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-03-25T13:11:09Z

Note: this is related to #10105, though - as I'm diving into details of both - they're going to be quite independent on the API surface, and even the implementations may end up having a relatively small overlap.

Thus, I found it best to split #10105 out from here as a separate issue. I'm considering driving it in a separate KEP (very likely referring to _some_ parts of the KEP for the issue here).
