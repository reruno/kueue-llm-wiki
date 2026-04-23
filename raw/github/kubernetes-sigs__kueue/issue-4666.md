# Issue #4666: Ignore krew release for RC version

**Summary**: Ignore krew release for RC version

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4666

**Last updated**: 2025-03-18T16:47:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-03-18T08:28:00Z
- **Updated**: 2025-03-18T16:47:51Z
- **Closed**: 2025-03-18T16:47:51Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
We want to add publish condition to ignore the publishing krew lib when the release is RC version

https://github.com/kubernetes-sigs/kueue/blob/main/.github/workflows/krew-release.yml

**Why is this needed**:

No need to release krew lib in case of RC version

cc @mimowo

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-18T08:37:54Z

Thanks!

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-18T16:30:56Z

/assign
