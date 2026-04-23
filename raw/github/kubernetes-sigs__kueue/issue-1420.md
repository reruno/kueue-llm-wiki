# Issue #1420: code refactor for `findFlavorForResourceGroup`

**Summary**: code refactor for `findFlavorForResourceGroup`

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1420

**Last updated**: 2024-02-15T12:19:48Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2023-12-07T09:23:09Z
- **Updated**: 2024-02-15T12:19:48Z
- **Closed**: 2024-02-15T12:19:48Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

This is how this function looks like:
```
func (a *Assignment) findFlavorForResourceGroup(
	log logr.Logger,
	rg *cache.ResourceGroup,
	requests workload.Requests,
	resourceFlavors map[kueue.ResourceFlavorReference]*kueue.ResourceFlavor,
	cq *cache.ClusterQueue,
	spec *corev1.PodSpec,
	lastAssignment int) (ResourceAssignment, *Status) {
}
```

So many parameters and the naming is meaningless, which make the code hard to read now, we should try to reduce the parameters or at least make this field names easy for understanding.

**Why is this needed**:

Maintainability.

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-12-07T09:23:39Z

There maybe other functions as well.

### Comment by [@lowang-bh](https://github.com/lowang-bh) — 2023-12-10T14:41:08Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-09T20:00:15Z

/unassign @lowang-bh 
/assign
