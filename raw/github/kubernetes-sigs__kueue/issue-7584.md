# Issue #7584: v1beta2: Delete .enable field from WaitForPodsReady API in config

**Summary**: v1beta2: Delete .enable field from WaitForPodsReady API in config

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7584

**Last updated**: 2025-11-14T14:15:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-07T16:13:55Z
- **Updated**: 2025-11-14T14:15:40Z
- **Closed**: 2025-11-14T14:15:40Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Remove the "enable" api field from the WaitForPodsReady API in config.

Part of https://github.com/kubernetes-sigs/kueue/issues/7113

**Why is this needed**:

To align the approach with the decision for FairSharing API: https://github.com/kubernetes-sigs/kueue/issues/5032

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-07T16:16:29Z

/assign
