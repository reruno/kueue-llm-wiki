# Issue #3601: Cleanup legacy preemption logic (where MultiplePreemptions=false)

**Summary**: Cleanup legacy preemption logic (where MultiplePreemptions=false)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3601

**Last updated**: 2024-11-28T13:00:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2024-11-20T14:01:38Z
- **Updated**: 2024-11-28T13:00:59Z
- **Closed**: 2024-11-28T13:00:59Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@gabesaba](https://github.com/gabesaba)
- **Comments**: 1

## Description

**What would you like to be cleaned**:
The branch where this does not hold.

https://github.com/kubernetes-sigs/kueue/blob/0b0b00305da2ed221c967925614f5409f68095bb/pkg/scheduler/scheduler.go#L259

**Why is this needed**:
Simplify the code base. The new logic allows more accurate preemptions, and easier to understand

## Discussion

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-11-20T14:01:42Z

/assign
