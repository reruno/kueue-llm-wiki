# Issue #1284: A mechanism to stop a ClusterQueue

**Summary**: A mechanism to stop a ClusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1284

**Last updated**: 2023-12-06T10:12:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-10-27T20:14:26Z
- **Updated**: 2023-12-06T10:12:37Z
- **Closed**: 2023-12-06T10:12:37Z
- **Labels**: `kind/feature`
- **Assignees**: [@stuton](https://github.com/stuton)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

A setting in a ClusterQueue for an administrator to pause new admissions and/or stop all running jobs.

**Why is this needed**:

This is a common admin journey to control usage from a user.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2023-10-30T06:47:37Z

/assign

### Comment by [@trasc](https://github.com/trasc) — 2023-10-30T15:28:36Z

#1299 contains the implementation for the first proposal (no tests)

### Comment by [@trasc](https://github.com/trasc) — 2023-10-31T06:28:12Z

/unassign

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2023-10-31T19:03:42Z

/assign

### Comment by [@stuton](https://github.com/stuton) — 2023-11-15T14:00:18Z

/assign
/unassign @yaroslava-serdiuk
