# Issue #4590: TAS: configure PodSetTopologyRequests only when TAS enabled

**Summary**: TAS: configure PodSetTopologyRequests only when TAS enabled

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4590

**Last updated**: 2025-03-26T10:28:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-13T11:48:48Z
- **Updated**: 2025-03-26T10:28:35Z
- **Closed**: 2025-03-26T10:28:35Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mykysha](https://github.com/mykysha)
- **Comments**: 2

## Description

**What would you like to be cleaned**:

This code is currenlty activated all the time: https://github.com/kubernetes-sigs/kueue/blob/a454f0e133682887c8043b10cc360bc24f7d3924/pkg/controller/jobframework/tas.go#L26

However, this should only be applied in case when TopologyAwareScheduling is enabled.

**Why is this needed**:

There should be no TAS related code active when TAS is disabled.

This also complicates testing the fix in https://github.com/kubernetes-sigs/kueue/issues/4573.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-13T11:49:01Z

cc @mbobrovskyi

### Comment by [@mykysha](https://github.com/mykysha) — 2025-03-13T12:05:27Z

/assign
