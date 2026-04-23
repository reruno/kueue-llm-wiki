# Issue #2447: Flatten FlavorResourceQuantities

**Summary**: Flatten FlavorResourceQuantities

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2447

**Last updated**: 2024-07-30T10:46:54Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2024-06-19T13:48:45Z
- **Updated**: 2024-07-30T10:46:54Z
- **Closed**: 2024-07-30T09:50:37Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@gabesaba](https://github.com/gabesaba)
- **Comments**: 0

## Description

**What would you like to be cleaned**:
`FlavorResourceQuantities`, a `map[string]map[string]int64`, is ubiquitous in the codebase. We have a lot of code that processes it in a nested loop, often allocating the inner map in the middle. It started getting in my way during the implementation of #79, and I started using a flat version of this map, resulting in significantly simpler code.

Unfortunately, this type is everywhere and the refactor is quite involved. I propose the following steps:

- [x] Move `FlavorResourceQuantities` to its own package
- [x] Define new types, a `FlavorResource` tuple, and `FlavorResourceQuantitiesFlat`
- [x] Update tests without changing functionality - we will define test data using the new type, but convert it back to the old type with a helper function
- [x] Update non-test source to use this new type
- [x] Cleanup; rename `FlavorResourceQuantitiesFlat` to `FlavorResourceQuantities`

The first three parts are safe. The 4th part has more risk, and can be done alongside the implementation of #79.

**Why is this needed**:
This old type is a mismatch for the problem, and is resulting in unnecessarily nested/complex code.

To help motivate this change, and see why I think the type is a better fit for the problem, consider the following refactors which were possible:

this was reduced to a single for-loop without branching
https://github.com/kubernetes-sigs/kueue/blob/53a03416bef223eeab9c52113d88bf46c85196cd/pkg/cache/clusterqueue.go#L520-L532

this was reduced to a single for-loop, with only 1 more level of branching (the if statements)
https://github.com/kubernetes-sigs/kueue/blob/53a03416bef223eeab9c52113d88bf46c85196cd/pkg/cache/clusterqueue.go#L534-L555

/assign
