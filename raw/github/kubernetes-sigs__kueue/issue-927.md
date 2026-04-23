# Issue #927: Ability to install controller in other namespaces

**Summary**: Ability to install controller in other namespaces

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/927

**Last updated**: 2023-06-29T14:43:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@stuton](https://github.com/stuton)
- **Created**: 2023-06-29T12:54:00Z
- **Updated**: 2023-06-29T14:43:39Z
- **Closed**: 2023-06-29T14:43:39Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@stuton](https://github.com/stuton)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
Get the current namespace instead of its declaration in the configuration
**Why is this needed**:
This will allow you to install the manager controller in any namespaces instead of ```kueue-system``` as it is done now. This will give us the opportunity to install the operator using the helm without keeping in mind having to change the configuration

## Discussion

### Comment by [@stuton](https://github.com/stuton) — 2023-06-29T12:54:08Z

/assign
