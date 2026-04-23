# Issue #7472: v1beta2: remove all unnecessary wrappers for v1beta1

**Summary**: v1beta2: remove all unnecessary wrappers for v1beta1

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7472

**Last updated**: 2025-10-31T13:12:19Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-31T08:32:10Z
- **Updated**: 2025-10-31T13:12:19Z
- **Closed**: 2025-10-31T13:12:19Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

As we moved most of testing to v1beta2 now we can remove most unnecessary testing wrappers for v1beta1 inside https://github.com/kubernetes-sigs/kueue/blob/main/pkg/util/testing/v1beta1/wrappers.go

Part of https://github.com/kubernetes-sigs/kueue/issues/7113

**Why is this needed**:

To avoid keeping dead testing code.
