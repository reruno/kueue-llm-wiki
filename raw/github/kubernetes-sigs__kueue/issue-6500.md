# Issue #6500: Preemption: commonize code for checking if candidates satisfy preemption policy

**Summary**: Preemption: commonize code for checking if candidates satisfy preemption policy

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6500

**Last updated**: 2025-10-16T11:50:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-08-08T09:48:43Z
- **Updated**: 2025-10-16T11:50:05Z
- **Closed**: 2025-10-16T11:50:05Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@j-skiba](https://github.com/j-skiba)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Commonize the logic responsible for determining if candidates satisfy the preemption policy:
- [findCandidates](https://github.com/kubernetes-sigs/kueue/blob/d9645bd2be2ed7d767a3e71c2f6c3e8906c9eccf/pkg/scheduler/preemption/preemption.go#L417) used for fair sharing
- [satisfiesPreemptionPolicy](https://github.com/kubernetes-sigs/kueue/blob/d9645bd2be2ed7d767a3e71c2f6c3e8906c9eccf/pkg/scheduler/preemption/classical/hierarchical_preemption.go#L105-L122) used for classical preemption

**Why is this needed**:

The logic for filtering candidates is the same for all modes, yet non-trivial, especially when it comes to LowerOrNewerEqualPriority and so we don't want to duplicate the code.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-08T09:48:54Z

cc @gabesaba @pajakd @PBundyra

### Comment by [@j-skiba](https://github.com/j-skiba) — 2025-10-13T12:41:51Z

/assign
