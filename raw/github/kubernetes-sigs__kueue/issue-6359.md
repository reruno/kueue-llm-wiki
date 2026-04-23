# Issue #6359: For eviction metrics use the single label value "Deactivated" along with the "underlying_cause"

**Summary**: For eviction metrics use the single label value "Deactivated" along with the "underlying_cause"

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6359

**Last updated**: 2025-08-27T10:24:09Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-08-01T14:26:35Z
- **Updated**: 2025-08-27T10:24:09Z
- **Closed**: 2025-08-27T10:24:09Z
- **Labels**: `kind/feature`
- **Assignees**: [@mykysha](https://github.com/mykysha)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Currently the metrics for eviction have this pattern "DeactivatedDueToXYZ" in label value names. 

Instead, we could have the single "Deactivated" label value, and the XYZ cause can now be exposed in the underlyingCause.

**Why is this needed**:

The current approach introduces many metrics label values and is a bit hard to aggregate in grafana. We prefer a more structured approach.

See for more details  the [discussion](https://github.com/kubernetes-sigs/kueue/pull/6332/files#r2248078820)

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-01T14:26:42Z

cc @tenzen-y

### Comment by [@mykysha](https://github.com/mykysha) — 2025-08-04T10:28:19Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-04T10:35:30Z

I think technically there are two options:
1. introduce a dedicated condition like "Deactivated" which would host the "undrelying_cause".
2. parse out the XYZ from the "DeactivatedDueToXYZ" reason under Evicted condition.

I'm leaning to (1.) as this is more "structured" approach. Similarly as we have "Preempted" or "PodsReady" conditions which host the underlying_cause for other scenarios.

Wdyt @tenzen-y ?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-21T18:21:16Z

> I think technically there are two options:
> 
> 1. introduce a dedicated condition like "Deactivated" which would host the "undrelying_cause".
> 2. parse out the XYZ from the "DeactivatedDueToXYZ" reason under Evicted condition.
> 
> I'm leaning to (1.) as this is more "structured" approach. Similarly as we have "Preempted" or "PodsReady" conditions which host the underlying_cause for other scenarios.
> 
> Wdyt [@tenzen-y](https://github.com/tenzen-y) ?

If we can introduce the `Deactivated` condition only to `schedulingStats.eviction`, we can take (1. Otherwise, we should take (2.

We should keep using "DeactivatedDueToXYZ" in status conditions so that we can avoid making the condition state machine more complex.
The `schedulingStats` is just recording for users, but we act based on any kind of status.conditions change.
