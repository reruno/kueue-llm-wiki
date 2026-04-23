# Issue #924: Add the helm clusterrole rules that are missing

**Summary**: Add the helm clusterrole rules that are missing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/924

**Last updated**: 2023-06-29T12:55:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@stuton](https://github.com/stuton)
- **Created**: 2023-06-29T12:00:41Z
- **Updated**: 2023-06-29T12:55:39Z
- **Closed**: 2023-06-29T12:55:39Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@stuton](https://github.com/stuton)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
Update ```role.yaml```
**Why is this needed**:
While installing an operator via helm, there are not enough permissions for the kueue controller to work properly.

## Discussion

### Comment by [@stuton](https://github.com/stuton) — 2023-06-29T12:00:54Z

/assign
