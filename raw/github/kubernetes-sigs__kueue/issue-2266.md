# Issue #2266: List resource prefixes to ignore in Kueue

**Summary**: List resource prefixes to ignore in Kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2266

**Last updated**: 2024-05-24T17:11:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@pajakd](https://github.com/pajakd)
- **Created**: 2024-05-23T13:39:51Z
- **Updated**: 2024-05-24T17:11:12Z
- **Closed**: 2024-05-24T17:11:12Z
- **Labels**: `kind/feature`
- **Assignees**: [@pajakd](https://github.com/pajakd)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
An ability to ignore certain resource names.

**Why is this needed**:
Currently in Kueue, all the resources that are requested by pods should be provided by Cluster Queue. In case of some custom resources that are not present in Cluster Queue but are present in pods this leads to an error.

**Completion requirements**:
An ability to provide (via API) a list of resource prefixes. Ignore resources with such prefixes when processing pod requirements. 

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@pajakd](https://github.com/pajakd) — 2024-05-23T13:39:59Z

/assign
