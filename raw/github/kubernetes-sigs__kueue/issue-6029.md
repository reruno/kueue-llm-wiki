# Issue #6029: Simplify handling of nil status in flavor assigner

**Summary**: Simplify handling of nil status in flavor assigner

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6029

**Last updated**: 2025-07-23T16:04:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-18T17:11:29Z
- **Updated**: 2025-07-23T16:04:29Z
- **Closed**: 2025-07-23T16:04:29Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

In particular, we could eliminate this if we just instantiate status early: https://github.com/kubernetes-sigs/kueue/pull/5878/files#diff-0870ec2c0ea330a7d087a6ef599905bf9b7164a0dd889d1b00ba17c31a1bfd05R517

**Why is this needed**:

See comment https://github.com/kubernetes-sigs/kueue/pull/5878#discussion_r2216084445

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-18T17:11:48Z

/assign 
tentatively, let me propose something
