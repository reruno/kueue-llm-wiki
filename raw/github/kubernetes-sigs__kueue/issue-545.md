# Issue #545: Add a condition to LocalQueue when it points to a ClusterQueue that doesn't exist

**Summary**: Add a condition to LocalQueue when it points to a ClusterQueue that doesn't exist

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/545

**Last updated**: 2023-03-17T17:47:19Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-02-02T21:14:47Z
- **Updated**: 2023-03-17T17:47:19Z
- **Closed**: 2023-03-17T17:47:19Z
- **Labels**: `kind/feature`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

A conditions field in the LocalQueueStatus and add one condition through the LocalQueue that reports if a ClusterQueue doesn't exist.

**Why is this needed**:

Better observability

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-08T16:13:44Z

@alculquicondor Will you take this issue? If not, I'd like to take this one :)

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-08T16:20:55Z

Sure, go ahead

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-08T16:23:05Z

> Sure, go ahead

Thanks. First, I will propose the API changes in this issue.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-08T17:05:16Z

> A conditions field in the LocalQueueStatus and add one condition through the LocalQueue that reports if a ClusterQueue doesn't exist.

I was misunderstanding the above comment. That means just adding a `[]metav1.condition` field to LocalQueueStatus, similar to ClusterQueue. So we may not need a proposal for API changes in this issue :)

/assign
