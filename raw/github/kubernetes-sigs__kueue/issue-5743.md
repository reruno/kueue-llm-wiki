# Issue #5743: Cleanup deleteWorkloads from the TestLastSchedulingContext unit test

**Summary**: Cleanup deleteWorkloads from the TestLastSchedulingContext unit test

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5743

**Last updated**: 2025-09-01T16:15:14Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-24T12:15:05Z
- **Updated**: 2025-09-01T16:15:14Z
- **Closed**: 2025-09-01T16:15:14Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@Singularity23x0](https://github.com/Singularity23x0)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like the field `deleteWorkloads` to be just a slice of workload references.

**Why is this needed**:

Specifying the entire workload is not necessary, the test code could just "Get" the latest workload version based on the reference and then delete.

## Discussion

### Comment by [@Singularity23x0](https://github.com/Singularity23x0) — 2025-08-28T10:02:53Z

/assign
