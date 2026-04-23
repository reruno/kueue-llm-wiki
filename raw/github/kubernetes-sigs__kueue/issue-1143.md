# Issue #1143: Function ```CmpNoOrder``` in ```pkg/util/slices``` fails for a few edge cases

**Summary**: Function ```CmpNoOrder``` in ```pkg/util/slices``` fails for a few edge cases

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1143

**Last updated**: 2023-09-21T15:20:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2023-09-21T14:21:23Z
- **Updated**: 2023-09-21T15:20:31Z
- **Closed**: 2023-09-21T15:20:31Z
- **Labels**: `kind/bug`
- **Assignees**: [@PBundyra](https://github.com/PBundyra)
- **Comments**: 2

## Description

**What happened**: Given slices A[1,1,2], and B[1,2,2] or  A[1,2] B[1,1] function ```CmpNoOrder``` returns wrong output - as if those slices were equal.

**What you expected to happen**: The function should return ```false``` as those slices differ.

**How to reproduce it (as minimally and precisely as possible)**: Call the function with mentioned arguments.

**Anything else we need to know?**: None

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2023-09-21T14:21:33Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2023-09-21T14:51:41Z

Can we say "Function CmpNoOrder does work correctly in case of duplicated items"? To be more specific.
