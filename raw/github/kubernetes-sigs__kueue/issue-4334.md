# Issue #4334: Add a column to multikueue indicating if it is connected to worker cluster

**Summary**: Add a column to multikueue indicating if it is connected to worker cluster

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4334

**Last updated**: 2025-02-25T17:36:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@highpon](https://github.com/highpon)
- **Created**: 2025-02-20T17:29:12Z
- **Updated**: 2025-02-25T17:36:31Z
- **Closed**: 2025-02-25T17:36:31Z
- **Labels**: `kind/feature`
- **Assignees**: [@highpon](https://github.com/highpon)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
A column indicating if a multikueue is connected to worker cluster.

**Why is this needed**:
Currently using `kubectl get multikueueclusters.kueue.x-k8s.io` I cannot tell quickly if the multikueue is connected to worker cluster or not.

```
❯ kubectl get multikueueclusters.kueue.x-k8s.io
NAME                      AGE
multikueue-test-worker1   21m
```

## Discussion

### Comment by [@highpon](https://github.com/highpon) — 2025-02-20T17:29:22Z

/assign
