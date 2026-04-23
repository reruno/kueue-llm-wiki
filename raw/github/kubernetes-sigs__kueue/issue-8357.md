# Issue #8357: TAS NodeHotSwap: make sure QueueSecondPassIfNeeded removes workload from second-queue pass if no longer needed

**Summary**: TAS NodeHotSwap: make sure QueueSecondPassIfNeeded removes workload from second-queue pass if no longer needed

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8357

**Last updated**: 2026-01-15T17:43:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-19T09:34:01Z
- **Updated**: 2026-01-15T17:43:39Z
- **Closed**: 2026-01-15T17:43:39Z
- **Labels**: `priority/important-soon`, `kind/cleanup`
- **Assignees**: [@skools-here](https://github.com/skools-here)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Make sure workload controller calling QueueSecondPassIfNeeded would remove the workload from second pass queue if no longer needed there.

The scenario:
1. node failure controller adds the unhealthyNodes to the workload
2. workload controller adds the workload to QueueSecondPassIfNeeded
3. node failure controller removes the node from unhealtyNodes becuase the node is now healthy
Issue: workload controller does not remove the workload from QueueSecondPassIfNeeded

**Why is this needed**:

To avoid potential race condition bugs, and make the interaction between controllers easier.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:34:37Z

This is follow up to https://github.com/kubernetes-sigs/kueue/issues/8258
cc @PBundyra @mbobrovskyi

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:35:01Z

/priority important-soon

### Comment by [@skools-here](https://github.com/skools-here) — 2025-12-30T09:15:01Z

/assign
