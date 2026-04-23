# Issue #3706: TAS: Kueue crashes on admittision when kubernetes.io/hostname is in the lowest level

**Summary**: TAS: Kueue crashes on admittision when kubernetes.io/hostname is in the lowest level

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3706

**Last updated**: 2024-12-03T13:25:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-12-02T15:37:38Z
- **Updated**: 2024-12-03T13:25:02Z
- **Closed**: 2024-12-03T13:25:02Z
- **Labels**: `kind/bug`
- **Assignees**: [@PBundyra](https://github.com/PBundyra)
- **Comments**: 1

## Description

**What happened**:

Kueue crashes with panic when admitting workload, when kuberntes.io/hostname is in the lowest level.

**What you expected to happen**:

No crash.

**How to reproduce it (as minimally and precisely as possible)**:

This commits reproduces the issue: https://github.com/kubernetes-sigs/kueue/commit/5587f0671b6719e4e015450dc8bd8daa7f3aa892

**Anything else we need to know?**:

This is because the usage copies here is based on only the last value (node name).

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-02T15:37:47Z

/assign @PBundyra
