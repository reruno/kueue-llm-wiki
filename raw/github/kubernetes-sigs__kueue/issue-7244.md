# Issue #7244: Expose contextualized FairSharing Weights for ClusterQueues as metrics

**Summary**: Expose contextualized FairSharing Weights for ClusterQueues as metrics

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7244

**Last updated**: 2025-10-27T09:41:38Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-13T12:27:08Z
- **Updated**: 2025-10-27T09:41:38Z
- **Closed**: 2025-10-27T09:41:38Z
- **Labels**: `kind/feature`
- **Assignees**: [@j-skiba](https://github.com/j-skiba)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Expose "precise" fair sharing weights for ClusterQueus and Cohorts as metrics.

**Why is this needed**:

To improve observability as discussed in https://github.com/kubernetes-sigs/kueue/issues/6938

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-13T12:27:19Z

cc @amy @gabesaba @tenzen-y @mwysokin

### Comment by [@amy](https://github.com/amy) — 2025-10-13T20:34:22Z

Adding some notes. The specific context that matters here is which CQ + DRS values are grouped in the same tournament / decision.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-15T16:41:30Z

cc @PBundyra who is also looking into debuggability of fair sharing

### Comment by [@j-skiba](https://github.com/j-skiba) — 2025-10-17T08:52:31Z

/assign
