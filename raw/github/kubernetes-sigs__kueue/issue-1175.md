# Issue #1175: Use apivalidation.ValidateImmutableField instead of field.Forbidden

**Summary**: Use apivalidation.ValidateImmutableField instead of field.Forbidden

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1175

**Last updated**: 2023-10-04T14:45:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@Gekko0114](https://github.com/Gekko0114)
- **Created**: 2023-10-03T08:01:07Z
- **Updated**: 2023-10-04T14:45:40Z
- **Closed**: 2023-10-04T14:45:40Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@Gekko0114](https://github.com/Gekko0114)
- **Comments**: 1

## Description

**What would you like to be cleaned**:
When validating CRDs, we should use apivalidation.ValidateImmutableField instead of field.Forbidden for simplicity.
Also discussed here https://github.com/kubernetes-sigs/kueue/pull/1081

## Discussion

### Comment by [@Gekko0114](https://github.com/Gekko0114) — 2023-10-03T08:01:17Z

/assign
