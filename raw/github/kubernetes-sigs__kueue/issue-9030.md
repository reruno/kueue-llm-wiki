# Issue #9030: Error silencing in AdjustResources (pkg/workload/resources.go)

**Summary**: Error silencing in AdjustResources (pkg/workload/resources.go)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9030

**Last updated**: 2026-02-06T13:48:29Z

---

## Metadata

- **State**: open
- **Author**: [@Singularity23x0](https://github.com/Singularity23x0)
- **Created**: 2026-02-06T13:48:29Z
- **Updated**: 2026-02-06T13:48:29Z
- **Closed**: —
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
The `AdjustResources` function in `pkg/workload/resources.go` ignore any errors encountered when handling Overhead and Limits.
This means when Creating/Updating a workload, scheduling it or updating Limit Ranges or Runtime Classes any issue with performing the adjusting will be ignored.
As a consequence we may schedule a workload incorrectly due to an issue with Runtime Classes or Limit Ranges.

On top of that, we have no reliable way of performing a retry when an error occurs, as `AdjustResources` is performed in multiple places outside of the reconciler.

**What you expected to happen**:
* `AdjustResources` is used only in the WorkloadController -> Reconcile
* When a Runtime Class is missing for any PodSets of a workload, the workload should be marked as inadmissible.
* When any other error occurs upon Getting the RuntimeClass we should also retry the reconcile.
* Similarly we should retry the reconcile when we are unable to fetch the LimitRangeList.
* Workload should not be scheduled until `AdjustResources` is able to adjust it without error.

**How to reproduce it (as minimally and precisely as possible)**:
The case of a missing RuntimeClass is currently covered by the test: **_Workload controller with scheduler when the workload defines only resource limits and the LocalQueue is created late [It] The limits should be used as request values_** in `test/integration/singlecluster/scheduler/workload_controller_test.go` (we currently expect no Overhead to be adjusted in this case).

**Anything else we need to know?**:
The adjustment may be difficult to implement until we have a reliable plan for handling #5310 

**Environment**:
- Kueue version (use `git describe --tags --dirty --always`):  `v0.16.0-devel-397-ga26d4942a-dirty`
