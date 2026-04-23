# Issue #8303: MultiKueue: prevent starting preemptions in multiple worker clusters

**Summary**: MultiKueue: prevent starting preemptions in multiple worker clusters

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8303

**Last updated**: 2026-03-17T15:31:46Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mwielgus](https://github.com/mwielgus)
- **Created**: 2025-12-17T14:03:19Z
- **Updated**: 2026-03-17T15:31:46Z
- **Closed**: 2026-03-17T15:31:46Z
- **Labels**: `kind/feature`, `priority/important-soon`, `area/multikueue`
- **Assignees**: [@kshalot](https://github.com/kshalot)
- **Comments**: 2

## Description

**What would you like to be added**:

A mechanism that prevents starting preemptions for the same workload in multiple clusters in the same time. 

**Why is this needed**:

A submission of a big, high-priority workload may trigger cluster-wide preemptions in multiple clusters. All but one will be disrupting other workloads for nothing.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change (maybe)
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:18:53Z

/area multikueue
/priority important-soon

### Comment by [@kshalot](https://github.com/kshalot) — 2026-01-09T10:22:00Z

/assign
