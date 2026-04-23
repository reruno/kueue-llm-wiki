# Issue #8277: TAS: performance issue due to unncessary (empty) request by TopologyUngater

**Summary**: TAS: performance issue due to unncessary (empty) request by TopologyUngater

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8277

**Last updated**: 2025-12-18T15:11:20Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-16T16:30:27Z
- **Updated**: 2025-12-18T15:11:20Z
- **Closed**: 2025-12-18T15:11:20Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

**What happened**:

There are many unncessary request sent by TopologyUngater for TAS workloads  (at least for workloads with >50 pods). 

We see that TopologyUngater sends empty requests are it unconditionally returns "true" from the Patch update function, here: https://github.com/kubernetes-sigs/kueue/blob/441fe203453014175d04dba136e4e3de8d96e9b4/pkg/controller/tas/topology_ungater.go#L246-L252


**What you expected to happen**:

TopologyUngater skips sending the request if already ungated.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-16T16:30:36Z

cc @PBundyra @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-16T16:57:39Z

/assign
