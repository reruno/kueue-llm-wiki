# Issue #7547: v1beta2: use regex exceptions for api-linter rather than nolint

**Summary**: v1beta2: use regex exceptions for api-linter rather than nolint

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7547

**Last updated**: 2025-11-07T07:10:52Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-06T07:49:03Z
- **Updated**: 2025-11-07T07:10:52Z
- **Closed**: 2025-11-07T07:10:52Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@kannon92](https://github.com/kannon92)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Use regex exceptions for api-linter rather than using //nolint

Part of #7113 

**Why is this needed**:

Because //nolint disables also other linter checks for the field, potentially masking some issues.

This is follow up explained here: https://github.com/kubernetes-sigs/kueue/issues/7119#issuecomment-3493274136

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-06T07:49:35Z

/assign @kannon92 
tenatively, cc @JoelSpeed
