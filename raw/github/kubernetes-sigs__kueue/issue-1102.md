# Issue #1102: Add `QueueVisibility` to featureGate

**Summary**: Add `QueueVisibility` to featureGate

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1102

**Last updated**: 2023-09-20T15:24:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2023-09-08T15:53:44Z
- **Updated**: 2023-09-20T15:24:04Z
- **Closed**: 2023-09-20T15:24:04Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@stuton](https://github.com/stuton)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
Adding `QueueVisibility` to featureGate to manage if Kueue enables the feature for the KEP 168.

**Why is this needed**:
To appropriately manage the new feature.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-09-08T16:51:30Z

/assign @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2023-09-11T13:47:42Z

Let's make the feature disabled by default as suggested by @tenzen-y here https://github.com/kubernetes-sigs/kueue/pull/1069#issuecomment-1711498601

### Comment by [@stuton](https://github.com/stuton) — 2023-09-19T07:56:36Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-09-19T17:41:20Z

/unassign @mimowo
