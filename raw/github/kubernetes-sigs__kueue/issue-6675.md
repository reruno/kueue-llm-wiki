# Issue #6675: Replace sort.Slice() with slices.Sort()

**Summary**: Replace sort.Slice() with slices.Sort()

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6675

**Last updated**: 2025-09-12T04:52:08Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-08-26T18:52:31Z
- **Updated**: 2025-09-12T04:52:08Z
- **Closed**: 2025-09-12T04:52:08Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@wzshiming](https://github.com/wzshiming)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would propose to replace `sort.Slice()` with `slices.Sort()` everywhere.

**Why is this needed**:

Both are implemented with the QuickSort base algorithm. But the new `slices.Sort()` function is faster than `sort.Slice()` in many situations as described in Go doc:

> Note: in many situations, the newer [slices.IsSortedFunc](https://pkg.go.dev/slices#IsSortedFunc) function is more ergonomic and runs faster.

https://pkg.go.dev/sort#Slice

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-27T09:36:21Z

/assign @wzshiming
