# Issue #1485: Missing RBAC on finalizers sub-resources when OwnerReferencesPermissionEnforcement admission is enabled

**Summary**: Missing RBAC on finalizers sub-resources when OwnerReferencesPermissionEnforcement admission is enabled

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1485

**Last updated**: 2023-12-18T18:28:36Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@astefanutti](https://github.com/astefanutti)
- **Created**: 2023-12-18T17:00:07Z
- **Updated**: 2023-12-18T18:28:36Z
- **Closed**: 2023-12-18T18:28:35Z
- **Labels**: `kind/bug`
- **Assignees**: [@astefanutti](https://github.com/astefanutti)
- **Comments**: 1

## Description

**What happened**:

On clusters, like OpenShift, where the [OwnerReferencesPermissionEnforcement](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#ownerreferencespermissionenforcement) admission controller is enabled, reconciliation of workloads failed with the following error message:

```
"error":"workloads.kueue.x-k8s.io \"pytorchjob-pytorch-simple-7a162\" is forbidden: cannot set blockOwnerDeletion if an ownerReference refers to a resource you can't set finalizers on: , <nil>"
```

**What you expected to happen**:

The Kueue service account should have the required permissions to update the finalizers.

**How to reproduce it (as minimally and precisely as possible)**:

Create a workload on a cluster that has the OwnerReferencesPermissionEnforcement admission controller enabled.

## Discussion

### Comment by [@astefanutti](https://github.com/astefanutti) — 2023-12-18T17:01:08Z

/assign
