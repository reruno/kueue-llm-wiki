# Issue #5614: Parametrize the priority of kueue-controller-manager in Helm

**Summary**: Parametrize the priority of kueue-controller-manager in Helm

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5614

**Last updated**: 2025-06-13T08:48:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-11T06:28:10Z
- **Updated**: 2025-06-13T08:48:57Z
- **Closed**: 2025-06-13T08:48:57Z
- **Labels**: `kind/feature`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 4

## Description

**What would you like to be added**:

Helm parameter to allow setting the priority class for `kueue-controller-manager`.

Name proposal: `controllerManager.manager.priorityClassName`.

**Why is this needed**:

On some deployments Kueue is a critical Pod,  and to reflect that users would like to set the priority as `system-cluster-critical`. 

This, for example, allows to make sure Kueue can find quickly replacement node when the original node fails.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-11T06:28:20Z

cc @tenzen-y @mbobrovskyi

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-11T06:30:06Z

cc @mwysokin

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-11T07:33:47Z

cc @kaisoz in case you have free cycles

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-06-11T10:39:23Z

/assign 

Yes! I can work on this thanks!
