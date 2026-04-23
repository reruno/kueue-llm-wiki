# Issue #3735: TAS: Support rank-based ordering for StatefulSet

**Summary**: TAS: Support rank-based ordering for StatefulSet

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3735

**Last updated**: 2024-12-06T13:30:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-12-04T11:50:20Z
- **Updated**: 2024-12-06T13:30:03Z
- **Closed**: 2024-12-06T13:30:03Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 3

## Description

**What would you like to be added**:

Support rank-based ordering for StatefulSet.

**Why is this needed**:

To improve performance of running AI inferenced backed-up by StatefulSet when based on NCCL.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-04T11:50:32Z

cc @mbobrovskyi @gabesaba @PBundyra

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-04T11:50:37Z

cc @tenzen-y

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-06T09:17:42Z

/assign
