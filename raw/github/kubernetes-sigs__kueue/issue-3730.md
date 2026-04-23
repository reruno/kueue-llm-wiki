# Issue #3730: [MultiKueue] Do not update Job status while the Job is suspended (for CRDs)

**Summary**: [MultiKueue] Do not update Job status while the Job is suspended (for CRDs)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3730

**Last updated**: 2025-01-29T07:05:26Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@IrvingMg](https://github.com/IrvingMg)
- **Created**: 2024-12-04T09:31:45Z
- **Updated**: 2025-01-29T07:05:26Z
- **Closed**: 2025-01-29T07:05:26Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

As a followup task for #3685 we need to try to catch and fix a potential bug that prevents updates to PodTemplate on unsuspended jobs for other Job CRDs.

**Why is this needed**:

To prevent blocking pod template update issue in other Job CRDs.

## Discussion

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2024-12-16T08:21:07Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-03T19:26:27Z

Is this related to non-Multi cluster env as well?

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-01-08T13:52:09Z

> Is this related to non-Multi cluster env as well?

I think this is just for Multikueue as the original issue was related to syncing jobs.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-08T13:55:05Z

/retitle [MultiKueue] Do not update Job status while the Job is suspended (for CRDs)
