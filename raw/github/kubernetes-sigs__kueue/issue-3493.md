# Issue #3493: TAS: allow to dump the usage of domains for TAS ResourceFlavors

**Summary**: TAS: allow to dump the usage of domains for TAS ResourceFlavors

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3493

**Last updated**: 2025-03-10T14:01:49Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-11-08T12:18:15Z
- **Updated**: 2025-03-10T14:01:49Z
- **Closed**: 2025-03-10T14:01:49Z
- **Labels**: `kind/feature`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 2

## Description

**What would you like to be added**:

Extend the existing mechanism which allows to dump the state of cache. We could extend [this function](https://github.com/kubernetes-sigs/kueue/blob/0f54466b991a7d198eeca306dc75f2aee518c482/pkg/cache/snapshot.go#L57-L79) to dump the free capacity of TAS snapshots per domain.

**Why is this needed**:

To improve debuggability of TAS.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-23T09:01:42Z

cc @mbobrovskyi

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-02-11T09:50:24Z

/assign
