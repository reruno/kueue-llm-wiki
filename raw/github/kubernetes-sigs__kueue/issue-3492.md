# Issue #3492: TAS: introduce TopologyReference by analogy to ResourceFlavorReference

**Summary**: TAS: introduce TopologyReference by analogy to ResourceFlavorReference

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3492

**Last updated**: 2024-11-12T08:08:50Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-11-08T12:09:18Z
- **Updated**: 2024-11-12T08:08:50Z
- **Closed**: 2024-11-12T08:08:49Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Introduce and use consistently in code TopologyReference, analogous to ResourceFlavorReference defined [here](https://github.com/kubernetes-sigs/kueue/blob/0f54466b991a7d198eeca306dc75f2aee518c482/apis/kueue/v1beta1/clusterqueue_types.go#L259-L262).

**Why is this needed**:

To make it strongly typed instead of string.

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-11T14:06:17Z

/assign
