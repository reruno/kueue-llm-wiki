# Issue #3651: TAS: Validate that the pod's index in the topology ungater falls within the expected range

**Summary**: TAS: Validate that the pod's index in the topology ungater falls within the expected range

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3651

**Last updated**: 2024-12-03T15:23:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-11-26T11:13:53Z
- **Updated**: 2024-12-03T15:23:02Z
- **Closed**: 2024-12-03T15:23:02Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Add new or refactor existing functions to validate if the the pod index in topology ungater is within [0, maxIndex] range. This is the follow-up to [this comment](https://github.com/kubernetes-sigs/kueue/pull/3649#discussion_r1858267176) 

**Why is this needed**:

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Code change

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-26T11:20:51Z

cc @mbobrovskyi 
maybe we could have a helper function like `ReadUIntFromLabelWithMax(pod, labelKey, maxValue)` so that other places can use it too.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-26T11:22:29Z

/assign
