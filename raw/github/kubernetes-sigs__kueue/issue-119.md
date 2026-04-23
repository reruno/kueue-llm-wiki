# Issue #119: Handle Pod overhead added during pod admission

**Summary**: Handle Pod overhead added during pod admission

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/119

**Last updated**: 2022-04-27T18:10:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-03-15T13:20:20Z
- **Updated**: 2022-04-27T18:10:12Z
- **Closed**: 2022-04-27T18:10:12Z
- **Labels**: `kind/feature`, `kind/productionization`
- **Assignees**: [@kerthcet](https://github.com/kerthcet)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

[Pod overhead](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-overhead/) is currently counted for workloads https://github.com/kubernetes-sigs/kueue/blob/79bde692164610b6fbf67fe1aeb2231e222ab799/pkg/workload/workload.go#L91-L101

However, the Pod overhead is usually added during Pod creation based on the Runtime class. We should handle this.

**Why is this needed**:

The calculations might not be accurate, depending on the Runtime class.

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-03-17T10:26:33Z

/assign
