# Issue #2112: [kueuectl] Add validation for ClusterQueue on creating LocalQueue

**Summary**: [kueuectl] Add validation for ClusterQueue on creating LocalQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2112

**Last updated**: 2024-05-08T18:33:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-05-02T05:46:31Z
- **Updated**: 2024-05-08T18:33:55Z
- **Closed**: 2024-05-08T18:33:55Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
- Error validation when creating a localqueue with an unknown clusterqueue.
- Option to ignore validation of an unknown clusterqueue when creating a localqueue.

**Why is this needed**:
To prevent the creation of a localqueue if a clusterqueue not exist.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-05-02T05:51:43Z

Design details https://github.com/kubernetes-sigs/kueue/tree/main/keps/2076-kueuectl#create-localqueue.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-05-02T07:10:37Z

/assign
