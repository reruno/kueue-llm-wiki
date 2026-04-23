# Issue #694: Use admitted condition to check if workload was admitted.

**Summary**: Use admitted condition to check if workload was admitted.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/694

**Last updated**: 2023-04-26T19:18:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mcariatm](https://github.com/mcariatm)
- **Created**: 2023-04-13T09:02:29Z
- **Updated**: 2023-04-26T19:18:16Z
- **Closed**: 2023-04-26T19:18:16Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mcariatm](https://github.com/mcariatm)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
Use only one way to check admission. I propose checking condition.

**Why is this needed**:
Now are used 2 different ways to check if workload is admitted:
`wl.Status.Admission == nil`
and
`apimeta.IsStatusConditionTrue(wl.Status.Conditions, kueue.WorkloadAdmitted)`

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-13T13:46:35Z

+1 both in production and test code

### Comment by [@mcariatm](https://github.com/mcariatm) — 2023-04-13T13:47:59Z

/assign
