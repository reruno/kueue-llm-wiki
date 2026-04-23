# Issue #7639: Add validation tests for v1beta2 TopologyAssignment

**Summary**: Add validation tests for v1beta2 TopologyAssignment

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7639

**Last updated**: 2025-11-24T10:42:46Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@olekzabl](https://github.com/olekzabl)
- **Created**: 2025-11-13T12:35:49Z
- **Updated**: 2025-11-24T10:42:46Z
- **Closed**: 2025-11-24T10:42:46Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@olekzabl](https://github.com/olekzabl)
- **Comments**: 1

## Description

**What would you like to be cleaned**:

I'd like to have an integration test for the validation rules in the v1beta2 TopologyAssignment (introduced in #7544).

**Why is this needed**:

The validation rules are specified via Kubebuilder annotations. While the existing automation does some checking of those, I'm not 100% certain if they behave as intended. It'd be nice to have tests for this.

## Discussion

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-11-20T22:21:49Z

/assign
