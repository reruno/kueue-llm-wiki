# Issue #2701: Kueuectl doesn't allow "-" in ResourceFlavor name in create cq

**Summary**: Kueuectl doesn't allow "-" in ResourceFlavor name in create cq

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2701

**Last updated**: 2024-07-26T14:31:42Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mwielgus](https://github.com/mwielgus)
- **Created**: 2024-07-25T16:37:20Z
- **Updated**: 2024-07-26T14:31:42Z
- **Closed**: 2024-07-26T14:31:42Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 1

## Description

**What happened**:

Kueuectl doesn't allow "-" in ResourceFlavor name in create cq.

**What you expected to happen**:

Kueuectl allows "-" in ResourceFlavor name in create cq. 

**How to reproduce it (as minimally and precisely as possible)**:

kueue create cq cluster-queue --nominal-quota=default-flavor:cpu=2;memory=5Gi

**Anything else we need to know?**:

**Environment**:
- Kueue version:  0.8

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2024-07-25T18:04:36Z

/assign
