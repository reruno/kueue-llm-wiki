# Issue #5465: [TAS] Update TAS tests so hostnames are not in lexicographical order

**Summary**: [TAS] Update TAS tests so hostnames are not in lexicographical order

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5465

**Last updated**: 2025-10-07T17:35:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-06-03T10:44:36Z
- **Updated**: 2025-10-07T17:35:01Z
- **Closed**: 2025-10-07T17:35:01Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@ganczak-commits](https://github.com/ganczak-commits)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
In TAS tests unit, integration and e2e we tend to have nodes with hostnames in lexicographical order e.g.:

```
	//      b1                   b2
	//   /      \             /      \
	//  r1       r2          r1       r2
	//  |      /  |  \       |         |
	//  x1    x2  x3  x4     x5       x6
```

 I'd like adjust the tests so it's no longer the case, by either updating it e.g.

```
	//      b1                   b2
	//   /      \             /      \
	//  r1       r2          r1       r2
	//  |      /  |  \       |         |
	//  x3    x5  x1 x6     x2       x4
```


**Why is this needed**:
Make our test more robust and ensure we don't unintentionally cover any bugs

## Discussion

### Comment by [@ganczak-commits](https://github.com/ganczak-commits) — 2025-08-28T08:33:42Z

/assign
