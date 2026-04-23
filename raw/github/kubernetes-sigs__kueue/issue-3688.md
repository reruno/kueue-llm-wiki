# Issue #3688: TAS: validate that kubernetes.io/hostname can only be at the lowest level

**Summary**: TAS: validate that kubernetes.io/hostname can only be at the lowest level

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3688

**Last updated**: 2024-12-03T13:47:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-11-29T10:45:16Z
- **Updated**: 2024-12-03T13:47:01Z
- **Closed**: 2024-12-03T13:47:01Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

**What would you like to be added**:

validation to prevent setting `kubernetes.io/hostname` in the middle of hierarchy.

**Why is this needed**:

To guide user and avoid mis-configuration. This is particularly important because we have dedicated checks in our code, active only when `kubernetes.io/hostname` is at the lowest level.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-29T10:45:29Z

@tenzen-y @mbobrovskyi @PBundyra

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-29T12:56:12Z

/assign
