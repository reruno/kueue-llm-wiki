# Issue #7753: Refactor updating workload via PatchAdmissionStatus to make sure update is not saved on error

**Summary**: Refactor updating workload via PatchAdmissionStatus to make sure update is not saved on error

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7753

**Last updated**: 2025-11-25T15:06:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-19T09:40:41Z
- **Updated**: 2025-11-25T15:06:41Z
- **Closed**: 2025-11-25T15:06:41Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Calling PatchAdmissionStatus can currently lead to subtle bugs, when the function fails on error, because the object passed to the function is modified.

To achieve that we could have a new helper dedicated to Workloads which, say `workload.PatchStatus`:
1. takes an internal DeepCopy of the workload
2. calls PatchAdmissionStatus or another helper 
3. updates the workload pointer pass to invoke the function on success
4. discards the changes in case of failure

Alternatively, return the new version of the object on succeessful request (but this is more code changes). 


**Why is this needed**:

To avoid modifying the cached valued of the Workload in case the update fails. This inconsistency may result in subtle issues.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-19T09:41:22Z

/assign @mbobrovskyi 
cc @mszadkow 
tentatively as a continuation of https://github.com/kubernetes-sigs/kueue/pull/7709
