# Issue #2138: [kueuectl] Add resume LocalQueue command

**Summary**: [kueuectl] Add resume LocalQueue command

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2138

**Last updated**: 2024-06-17T18:29:20Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-05-06T07:22:22Z
- **Updated**: 2024-06-17T18:29:20Z
- **Closed**: 2024-06-17T18:29:20Z
- **Labels**: `kind/feature`
- **Assignees**: [@rainfd](https://github.com/rainfd)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Add resume LocalQueue command.

**Why is this needed**:
To resumes admission of Workloads coming from the given LocalQueue. This requires adding StopPolicy to LocalQueue and enforcing its changes in ClusterQueue (#2109).

Design details https://github.com/kubernetes-sigs/kueue/tree/main/keps/2076-kueuectl#resume-localqueue.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@rainfd](https://github.com/rainfd) — 2024-06-11T22:52:40Z

/assign
