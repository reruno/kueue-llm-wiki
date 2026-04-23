# Issue #9355: Execute all FG validations at a once

**Summary**: Execute all FG validations at a once

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9355

**Last updated**: 2026-03-03T06:02:56Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2026-02-19T07:11:07Z
- **Updated**: 2026-03-03T06:02:56Z
- **Closed**: 2026-03-03T06:02:56Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
I'd propose refining the following `ValidateFeatureGates` and `TestValidateFeatureGates` in the following points:

https://github.com/kubernetes-sigs/kueue/blob/cf49633305c8df2cd7b1a2d944f488962497e304/pkg/config/validation.go#L495

https://github.com/kubernetes-sigs/kueue/blob/cf49633305c8df2cd7b1a2d944f488962497e304/pkg/config/validation_test.go#L975

1. Validate all FGs at once by `field.ErrorList`.
2. Verify actual and expected errors instead of error message matching.

**Why is this needed**:
Improve user experience and error verifications.

## Discussion

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-02-20T14:14:18Z

/assign
