# Issue #992: Add labels to the Workload object matching the job details

**Summary**: Add labels to the Workload object matching the job details

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/992

**Last updated**: 2023-08-03T17:42:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-07-17T16:02:32Z
- **Updated**: 2023-08-03T17:42:23Z
- **Closed**: 2023-08-03T17:42:23Z
- **Labels**: `kind/feature`
- **Assignees**: [@achernevskii](https://github.com/achernevskii)
- **Comments**: 3

## Description

**What would you like to be added**:

The name of a Workload doesn't match the name of the Job, to avoid collisions among different CRDs.

As a result, it's hard to quickly obtain the Workload for a particular job. A pair of labels (for name and GVK) would make it feasible to query.

**Why is this needed**:

For general usability and also to efficiently implement a CLI that gives you all relevant information for a job #487 

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@achernevskii](https://github.com/achernevskii) — 2023-07-17T18:03:26Z

/assign

### Comment by [@trasc](https://github.com/trasc) — 2023-07-18T12:53:21Z

isn't the owner reference sufficient?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-18T15:03:44Z

It's sufficient for a controller (like kueue) which watches every Workload object and is able to maintain an index.
OTOH, a CLI would have to call `List` and filter client-side to find the corresponding workload. A label allows to do the filtering server-side.
