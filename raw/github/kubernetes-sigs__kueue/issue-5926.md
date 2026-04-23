# Issue #5926: Fix asserts in TestValidateWorkloadUpdate when TopologyAwareScheduling enabled

**Summary**: Fix asserts in TestValidateWorkloadUpdate when TopologyAwareScheduling enabled

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5926

**Last updated**: 2025-09-01T12:59:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-10T07:05:32Z
- **Updated**: 2025-09-01T12:59:15Z
- **Closed**: 2025-09-01T12:59:15Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@kshalot](https://github.com/kshalot)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Currently the tests declare using enableTopologyAwareScheduling, but don't really use it.

In particular the assert in this test looks wrong: https://github.com/kubernetes-sigs/kueue/commit/3117559223d7d9760bf4f96fb892489c437ddc39#diff-addd962cdfab563e9626f0a94c226fa52725b1a7fd62cefe747971c23bf4dba3R461-R500

**Why is this needed**:

To ensure this block of code is tested: https://github.com/kubernetes-sigs/kueue/blob/401f896579cfdd845b92061ad5ca3661dd1c6754/pkg/webhooks/workload_webhook.go#L293-L303

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-10T07:06:06Z

Thank you @ichekrygin who actually discovered the issue

### Comment by [@kshalot](https://github.com/kshalot) — 2025-08-27T16:20:04Z

/assign
