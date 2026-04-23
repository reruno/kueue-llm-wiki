# Issue #8114: Bump agnhost to latest

**Summary**: Bump agnhost to latest

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8114

**Last updated**: 2025-12-08T08:23:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-08T08:22:02Z
- **Updated**: 2025-12-08T08:23:32Z
- **Closed**: 2025-12-08T08:23:32Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Currently we are using outdated agnhost image 2.52, but newer are released: 2.59

It would also be great to investigate automated update.

**Why is this needed**:

To make sure we use latest dependencies.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-08T08:23:32Z

/close
My mistake, we are actually testing using the latest: https://github.com/kubernetes-sigs/kueue/blob/50d89e00dad7e2ce896293253beb14c0f2bb291d/hack/agnhost/Dockerfile#L1

It is just that we also test the image update, and for that we start with 2.52
