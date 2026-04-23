# Issue #8051: Remove the "(requires enabling pod integration)" comment in configMap

**Summary**: Remove the "(requires enabling pod integration)" comment in configMap

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8051

**Last updated**: 2025-12-03T09:00:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-03T07:45:19Z
- **Updated**: 2025-12-03T09:00:29Z
- **Closed**: 2025-12-03T09:00:29Z
- **Labels**: `kind/bug`, `kind/cleanup`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 1

## Description

/kind bug 

**What would you like to be cleaned**:

See here: https://github.com/kubernetes-sigs/kueue/blob/ee02f0f736db312875aaffd2bc911806a94e72dc/charts/kueue/values.yaml#L155-L158

**Why is this needed**:

These comments are no longer accurate, and misleading after https://github.com/kubernetes-sigs/kueue/pull/6736

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-03T07:45:54Z

/assign @IrvingMg 
tentatively as a follow up to enabling the integrations automatically. 
cc @mbobrovskyi
