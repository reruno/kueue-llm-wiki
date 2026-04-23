# Issue #3346: AdmissionChecks should be "reset" (set to pending) on workload deactivation

**Summary**: AdmissionChecks should be "reset" (set to pending) on workload deactivation

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3346

**Last updated**: 2024-11-12T14:30:49Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-10-28T14:42:03Z
- **Updated**: 2024-11-12T14:30:49Z
- **Closed**: 2024-11-12T14:30:49Z
- **Labels**: `kind/bug`
- **Assignees**: [@KPostOffice](https://github.com/KPostOffice)
- **Comments**: 2

## Description

**What happened**:

This is a follow up to https://github.com/kubernetes-sigs/kueue/pull/3323#issuecomment-2441756535.
When we deactivate a workload we should clean its admission check states, as we clean the `.status.requeueState`.

**What you expected to happen**:

To make sure the workload is not immediately evicted after manual reactivation by an admin.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-28T14:42:16Z

cc @PBundyra @tenzen-y

### Comment by [@KPostOffice](https://github.com/KPostOffice) — 2024-10-28T19:08:01Z

/assign
