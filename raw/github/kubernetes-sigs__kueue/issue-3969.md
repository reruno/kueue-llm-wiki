# Issue #3969: Extend GenericJob.GetPodSets() to allow error to be returned

**Summary**: Extend GenericJob.GetPodSets() to allow error to be returned

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3969

**Last updated**: 2025-01-21T09:14:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@dgrove-oss](https://github.com/dgrove-oss)
- **Created**: 2025-01-13T17:45:27Z
- **Updated**: 2025-01-21T09:14:37Z
- **Closed**: 2025-01-21T09:14:37Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@Horiodino](https://github.com/Horiodino)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Add an error to the return value of GetPodSets

**Why is this needed**:

As discussed in #3953 (https://github.com/kubernetes-sigs/kueue/pull/3953#discussion_r1913150063), extending the API would allow better error reporting in the AppWrapper integration.

## Discussion

### Comment by [@Horiodino](https://github.com/Horiodino) — 2025-01-17T16:06:22Z

/assign
