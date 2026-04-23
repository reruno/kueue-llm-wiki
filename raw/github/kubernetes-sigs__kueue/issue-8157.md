# Issue #8157: Unconstrained workload with LeastFreeCapacity Algorithm Scheduling Bug

**Summary**: Unconstrained workload with LeastFreeCapacity Algorithm Scheduling Bug

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8157

**Last updated**: 2025-12-10T17:01:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@cheng-ml](https://github.com/cheng-ml)
- **Created**: 2025-12-10T05:24:00Z
- **Updated**: 2025-12-10T17:01:34Z
- **Closed**: 2025-12-10T17:01:34Z
- **Labels**: `kind/bug`
- **Assignees**: [@PBundyra](https://github.com/PBundyra)
- **Comments**: 2

## Description

**What happened**:
unconstrained workload cannot be scheduled at all if there is domain with 0 capacity

**What you expected to happen**:
It skips the 0 capacity domains and be assigned to other domains with capacity

**How to reproduce it (as minimally and precisely as possible)**:


**Anything else we need to know?**:
When unconstrainted workload is used with LeastFreeCapacity, the domains are sorted ascend, the domains with 0 capacity will appear in the beginning of the queue which causes the  loop immediately exits.

```
sortedDomain = s.sortedDomains(sortedDomain[idx:], unconstrained)
for idx := 0; remainingSliceCount > 0 && idx < len(sortedDomain) && sortedDomain[idx].sliceState > 0; idx++ {
```
https://github.com/kubernetes-sigs/kueue/blob/main/pkg/cache/scheduler/tas_flavor_snapshot.go#L1102-L1103

By removing the `sortedDomain[idx].sliceState > 0`, the job can be correctly scheduled

**Environment**:
- Kueue version (use `git describe --tags --dirty --always`): 0.15, when mixed profile is being used for unconstrainted workload

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-10T06:53:39Z

Great finding @cheng-ml! Indeed, I think this check `sortedDomain[idx].sliceState > 0` looks like a premature optimization, because it does not impact the asymptotic complexity, nor the constant in any significant way.

I'm happy to drop it if it does not break any other tests (TBD).

cc @PBundyra @pajakd

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-12-10T09:38:24Z

/assign
