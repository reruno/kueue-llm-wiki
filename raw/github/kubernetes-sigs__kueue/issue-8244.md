# Issue #8244: TAS: scheduler should log the name of the node for which we cannot find replacement

**Summary**: TAS: scheduler should log the name of the node for which we cannot find replacement

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8244

**Last updated**: 2025-12-18T13:11:18Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-15T15:08:55Z
- **Updated**: 2025-12-18T13:11:18Z
- **Closed**: 2025-12-18T13:11:18Z
- **Labels**: `kind/feature`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 2

## Description


**What would you like to be added**:

Make sure NodeName is logged for the node for which we fail to find replacement, if eviction fails in https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/scheduler.go#L251-L256

**Why is this needed**:

For debuggability.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-15T15:09:03Z

cc @PBundyra @mbobrovskyi

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-18T11:57:38Z

/assign
Let me take that
