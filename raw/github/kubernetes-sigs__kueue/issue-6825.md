# Issue #6825: Make AFS scheduling logs Level 5 or 6

**Summary**: Make AFS scheduling logs Level 5 or 6

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6825

**Last updated**: 2025-09-15T11:02:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-09-15T06:02:18Z
- **Updated**: 2025-09-15T11:02:12Z
- **Closed**: 2025-09-15T11:02:12Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Make AFS scheduling logs level 5 or 6 as I mentioned in https://github.com/kubernetes-sigs/kueue/pull/6328#pullrequestreview-3223011080.

**Why is this needed**:

Those are very verbose logs, and we should handle those at the debug level.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-15T06:03:33Z

@mimowo @PBundyra If you want to keep these logs as level 3 while Alpha level support, we can consider adding this log level change (3 -> 5/6) to Beta graduation criteria.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-15T06:09:30Z

iirc the logs were set to V3 so that they can be used to debug flakes we had on CI. I think we already solved most of the AFS flakes, so either increasing now or when to Beta is fine for me.

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-09-15T09:15:19Z

/assign
