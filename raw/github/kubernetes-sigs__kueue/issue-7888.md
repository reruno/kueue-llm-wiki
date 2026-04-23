# Issue #7888: Refactor AfsEntryPenalties: Move to afs subpackage and remove redundant mutex

**Summary**: Refactor AfsEntryPenalties: Move to afs subpackage and remove redundant mutex

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7888

**Last updated**: 2025-11-27T11:02:25Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@IrvingMg](https://github.com/IrvingMg)
- **Created**: 2025-11-25T15:23:24Z
- **Updated**: 2025-11-27T11:02:25Z
- **Closed**: 2025-11-27T11:02:25Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

  1. Move `AfsEntryPenalties` to `pkg/cache/queue/afs/` subpackage to avoid circular dependencies
  2. Remove `sync.RWMutex` from `AfsEntryPenalties`

**Why is this needed**:

Follow-up from #7780. 

See https://github.com/kubernetes-sigs/kueue/pull/7780#discussion_r2545652327 and https://github.com/kubernetes-sigs/kueue/pull/7780#discussion_r2559515036

## Discussion

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-11-25T15:23:33Z

/assign
