# Issue #3645: TAS: CQ is not deactivated when there is no Topology

**Summary**: TAS: CQ is not deactivated when there is no Topology

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3645

**Last updated**: 2024-12-11T16:48:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-11-26T08:16:17Z
- **Updated**: 2024-12-11T16:48:05Z
- **Closed**: 2024-12-11T16:48:05Z
- **Labels**: `kind/bug`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 1

## Description

**What happened**:

When a user creates a CQ pointing to TAS RF without Topology, then the CQ is not deactivated.

There is no way to know the Topology is missing other than creating a workload, but even then the error message is unclear; 

**What you expected to happen**:

Deactivate the CQ, similarly as we deactivate it for other mis-configuration issues, such as a missing RF.

**How to reproduce it (as minimally and precisely as possible)**:

Create the TAS structure without Topology, then create a workload targeting the CQ

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-26T08:16:58Z

cc @tenzen-y @mbobrovskyi @PBundyra 
/assign
