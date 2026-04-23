# Issue #7362: v1beta2: Remove .spec.AdmissionChecks field in ClusterQueue

**Summary**: v1beta2: Remove .spec.AdmissionChecks field in ClusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7362

**Last updated**: 2025-11-06T09:44:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-23T11:20:29Z
- **Updated**: 2025-11-06T09:44:55Z
- **Closed**: 2025-11-06T09:44:55Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@nerdeveloper](https://github.com/nerdeveloper)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

and convert its content to .spec.AdmissionCheckStrategy

**Why is this needed**:

Part of https://docs.google.com/document/d/1VpSKMZP5cWXvr7NbVM2ay2HyQA6XeymwVGXxdqdhE6Q

https://github.com/kubernetes-sigs/kueue/issues/7113

## Discussion

### Comment by [@nerdeveloper](https://github.com/nerdeveloper) — 2025-10-27T03:10:49Z

please can i have  this docs to see what is needed, i have requested access

### Comment by [@nerdeveloper](https://github.com/nerdeveloper) — 2025-10-27T03:15:17Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-27T06:47:48Z

Access shared, what is needed here is the conversion from the old CQ's .spec.AdmissionChecks to spec.AdmissionCheckStrategy. The new field is more generic  - when "OnFlavors" is empty then it applies to all flavors as spec.AdmissionChecks would do.
