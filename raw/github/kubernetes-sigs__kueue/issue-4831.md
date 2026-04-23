# Issue #4831: Missing Topology rbac in helm chart

**Summary**: Missing Topology rbac in helm chart

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4831

**Last updated**: 2025-04-04T06:44:38Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@hy00nc](https://github.com/hy00nc)
- **Created**: 2025-03-31T05:13:19Z
- **Updated**: 2025-04-04T06:44:38Z
- **Closed**: 2025-04-04T06:44:38Z
- **Labels**: `kind/feature`
- **Assignees**: [@KPostOffice](https://github.com/KPostOffice)
- **Comments**: 2

## Description

**What would you like to be added**:

Add rbac for Topology resource in Kueue helm chart. It'd be also great to include it in batch_admin_role.yaml

**Why is this needed**:

I'm using SA which is using batch admin role and it'd be great to if Topology is also covered by this existing cluster role.

**Completion requirements**:

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-31T08:07:14Z

If we are missing rbac permissions in helm then it sounds like a bug. I would assume the rbac for Topology should be configured the same as for ResourceFlavor.

### Comment by [@KPostOffice](https://github.com/KPostOffice) — 2025-04-01T21:41:08Z

/assign
