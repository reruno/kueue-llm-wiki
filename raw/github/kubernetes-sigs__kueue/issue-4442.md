# Issue #4442: Use ClusterQueueReference to improve static code analysis

**Summary**: Use ClusterQueueReference to improve static code analysis

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4442

**Last updated**: 2025-03-10T07:27:49Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-02-28T15:05:14Z
- **Updated**: 2025-03-10T07:27:49Z
- **Closed**: 2025-03-10T07:27:48Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 2

## Description

**What would you like to be added**:

I would like to review all places in code which use string to represent ClusterQueue and replace with ClusterQueueReference. Some candidate places:

https://github.com/kubernetes-sigs/kueue/blob/6e25ebfcf2491236e385f644e4f7280c3d315ead/pkg/cache/snapshot.go#L39C2-L39C26

https://github.com/kubernetes-sigs/kueue/blob/6e25ebfcf2491236e385f644e4f7280c3d315ead/pkg/hierarchy/manager.go#L23

but likely many more. It is ok to miss some, but we would like to set the direction.

**Why is this needed**:

To make it easier to analyze the code and see what the "string" is.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-28T15:05:36Z

Follow up to https://github.com/kubernetes-sigs/kueue/pull/4417

cc @vladikkuzn @PBundyra @tenzen-y

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-03-03T10:24:05Z

/assign
