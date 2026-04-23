# Issue #3975: Document using AppWrappers to manage unsupported types with Kueue

**Summary**: Document using AppWrappers to manage unsupported types with Kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3975

**Last updated**: 2025-01-16T15:36:36Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@dgrove-oss](https://github.com/dgrove-oss)
- **Created**: 2025-01-15T14:24:24Z
- **Updated**: 2025-01-16T15:36:36Z
- **Closed**: 2025-01-16T15:36:35Z
- **Labels**: `kind/feature`
- **Assignees**: [@dgrove-oss](https://github.com/dgrove-oss)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Add a page to the running-workloads section of the webpage to document how the AppWrapper integration
can be used to enable Kueue to manage kinds containing PodSpecTemplates that do not yet have full fledged Kueue integrations.

Use LeaderWorkerSets as a concrete example. 

**Why is this needed**:

This will be useful to Kueue users.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ x ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-01-15T14:24:42Z

/assign dgrove-oss
