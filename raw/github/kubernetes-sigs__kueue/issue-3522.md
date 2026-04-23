# Issue #3522: Optimize memory usage of TAS

**Summary**: Optimize memory usage of TAS

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3522

**Last updated**: 2024-11-20T11:32:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-11-13T13:17:08Z
- **Updated**: 2024-11-20T11:32:57Z
- **Closed**: 2024-11-20T11:32:57Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@PBundyra](https://github.com/PBundyra)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
Replace current tree representation of topology in `TASFlavorSnapshot` to more pointers oriented

**Why is this needed**:
To improve memory usage of Kueue
Improve code clarity

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-11-13T13:17:13Z

/assign
