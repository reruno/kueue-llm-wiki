# Issue #144: Ceiling not set equal zero, it should mean unlimited

**Summary**: Ceiling not set equal zero, it should mean unlimited

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/144

**Last updated**: 2022-03-25T18:05:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-03-23T22:38:13Z
- **Updated**: 2022-03-25T18:05:59Z
- **Closed**: 2022-03-25T18:05:59Z
- **Labels**: `kind/bug`
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor)
- **Comments**: 1

## Description

In the API we mention that [no ceiling means unlimited](https://github.com/kubernetes-sigs/kueue/blob/27b05145f94ac528ff92790efc70d62d8c9feafc/api/v1alpha1/clusterqueue_types.go#L250), which is currently not true and the ceiling must be explicitly set.

We need to change the type to a pointer to distinguish between not set and 0.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-24T18:17:25Z

/assign
