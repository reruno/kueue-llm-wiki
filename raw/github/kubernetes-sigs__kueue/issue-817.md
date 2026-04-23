# Issue #817: Using deprecated patchesStrategicMerge in kustomize files

**Summary**: Using deprecated patchesStrategicMerge in kustomize files

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/817

**Last updated**: 2023-06-07T15:58:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-05-29T14:00:15Z
- **Updated**: 2023-06-07T15:58:15Z
- **Closed**: 2023-06-07T15:58:15Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@stuton](https://github.com/stuton)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Use `patches` instead of `patchesStrategicMerge`.

**Why is this needed**:

We are getting this warning when using kustomize:

```
# Warning: 'patchesStrategicMerge' is deprecated. Please use 'patches' instead. Run 'kustomize edit fix' to update your Kustomization automatically.
```

## Discussion

### Comment by [@stuton](https://github.com/stuton) — 2023-06-02T13:54:11Z

/assign
