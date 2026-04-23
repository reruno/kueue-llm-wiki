# Issue #6028: Extract iteration over findFlavorForPodSetResource to a new helper function

**Summary**: Extract iteration over findFlavorForPodSetResource to a new helper function

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6028

**Last updated**: 2025-09-01T16:59:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-18T17:06:05Z
- **Updated**: 2025-09-01T16:59:15Z
- **Closed**: 2025-09-01T16:59:15Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@olekzabl](https://github.com/olekzabl)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

The findFlavorForPodSetResource is long and the new iteration over PodSets increases indentention and requires helper var flavorUnmatchMessage

**Why is this needed**:

The function is getting hard to read with many nested loops.

See review comment: https://github.com/kubernetes-sigs/kueue/pull/5878#discussion_r2216104567

## Discussion

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-08-28T11:54:13Z

/assign
