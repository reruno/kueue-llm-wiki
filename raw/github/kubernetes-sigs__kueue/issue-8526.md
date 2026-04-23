# Issue #8526: [MultiKueue] Support Long running services

**Summary**: [MultiKueue] Support Long running services

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8526

**Last updated**: 2026-02-16T10:50:41Z

---

## Metadata

- **State**: open
- **Author**: [@ravisantoshgudimetla](https://github.com/ravisantoshgudimetla)
- **Created**: 2026-01-12T06:18:49Z
- **Updated**: 2026-02-16T10:50:41Z
- **Closed**: —
- **Labels**: `kind/feature`, `area/multikueue`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
When a serving workload needs to move clusters (e.g., GPU type change), Multi-Kueue immediately deletes the old serving when quota moves, causing a service gap until the new serving is ready in the target cluster.
I know other long-running jobs like RayJobs might have similar concerns around service continuity.

**Why is this needed**:
For serving workloads, we'd ideally wait for the replacement to be "Ready" before cleaning up the old one to maintain service availability during cross-cluster transitions. There could be other replacements policies if needed

We can define a new interface:

```go
type MultiKueueAdapterWithCleanupPolicy interface {
      MultiKueueAdapter
      CleanupPolicy() CleanupPolicy
  }
```
I am planning to use this interface(or a modification of that) and extending elasticJobs implementation to allow for what is a called a replacement workload slice. 

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-12T08:13:57Z

cc @mwielgus @mwysokin

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-02-16T10:50:39Z

/area multikueue
