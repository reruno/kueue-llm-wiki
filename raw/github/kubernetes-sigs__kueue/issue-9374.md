# Issue #9374: Extend the v1beta2 migration script with the option to downgrade to v1beta1

**Summary**: Extend the v1beta2 migration script with the option to downgrade to v1beta1

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9374

**Last updated**: 2026-02-20T14:19:44Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-19T17:10:33Z
- **Updated**: 2026-02-20T14:19:44Z
- **Closed**: 2026-02-20T14:19:43Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Extend the migration script with the downgrade option v1beta2 -> v1beta1.

**Why is this needed**:

To allow converting existing resources back to v1beta1. This is needed in an emergency situation to facilitate downgrade 0.16->0.15->0.14.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-19T17:10:53Z

cc @mbobrovskyi @mwielgus @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-19T17:15:35Z

Does this contain a storage version reverting (v1beta2 -> v1beta1)?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-19T17:37:03Z

yes
