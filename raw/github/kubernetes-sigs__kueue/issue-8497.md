# Issue #8497: Don't use Kueue finalizers for StatefulSets' Pods

**Summary**: Don't use Kueue finalizers for StatefulSets' Pods

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8497

**Last updated**: 2026-01-13T15:07:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-09T14:40:12Z
- **Updated**: 2026-01-13T15:07:40Z
- **Closed**: 2026-01-13T15:07:40Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Currently we are using finalizers for Pods managed by StatefulSet, because we are using Pod groups. However, 

**Why is this needed**:

- to improve performance
- to reduce confusion : is it needed or not?
- to eliminate code complication related to removal of finalizers, see: https://github.com/kubernetes-sigs/kueue/pull/8268/

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-09T14:44:38Z

cc @mbobrovskyi @sohankunkerkar @j-skiba 

"sibling issues": https://github.com/kubernetes-sigs/kueue/issues/8276 and https://github.com/kubernetes-sigs/kueue/issues/5298

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-12T19:36:20Z

/assign @mbobrovskyi
