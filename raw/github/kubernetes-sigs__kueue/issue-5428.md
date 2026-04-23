# Issue #5428: Preempt Mode Assigned by FlavorAssigner when no preemption targets, BorrowWithinCohort=enabled

**Summary**: Preempt Mode Assigned by FlavorAssigner when no preemption targets, BorrowWithinCohort=enabled

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5428

**Last updated**: 2025-06-16T10:29:00Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2025-05-30T15:58:20Z
- **Updated**: 2025-06-16T10:29:00Z
- **Closed**: 2025-06-16T10:29:00Z
- **Labels**: `kind/bug`
- **Assignees**: [@pajakd](https://github.com/pajakd)
- **Comments**: 1

## Description

**What happened**:
with `FlavorFungibility.WhenCanPreempt=Preempt`, and `preemption.borrowWithinCohort=LowerPriority`, a borrowing workload may decide to preempt within a flavor in which preemption is not actually possible, due to no candidates being valid (e.g. candidates all protected by nominal quota)

**What you expected to happen**:
We should try preempting in a flavor which preemptions may actually succeed

**How to reproduce it (as minimally and precisely as possible)**:
See integ test https://github.com/kubernetes-sigs/kueue/commit/5904ed2ef8a03523a59f2bddc833a2365eb1a049

After changing the preemption policy to remove borrowWithinCohort, the test passes

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@pajakd](https://github.com/pajakd) — 2025-05-30T16:20:26Z

/assign
