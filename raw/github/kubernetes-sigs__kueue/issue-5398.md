# Issue #5398: Align the Helm configuration for the image of KueueViz with the main controller

**Summary**: Align the Helm configuration for the image of KueueViz with the main controller

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5398

**Last updated**: 2025-06-05T08:22:50Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-05-28T10:14:35Z
- **Updated**: 2025-06-05T08:22:50Z
- **Closed**: 2025-06-05T08:22:50Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Currently the configuration assumes the user specifies the full image: https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/values.yaml#L171-L174

**Why is this needed**:

For consistency with the way we specify the image for the main controller: https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/values.yaml#L18-L21

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-28T10:15:22Z

cc @tenzen-y @mbobrovskyi 
This might be change which requires a different command from the user, but I believe we should align it.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-05-28T12:05:12Z

/assign
