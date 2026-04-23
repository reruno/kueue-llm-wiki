# Issue #9854: Consolidate gauge metric cleanup mechanisms

**Summary**: Consolidate gauge metric cleanup mechanisms

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9854

**Last updated**: 2026-04-02T08:28:09Z

---

## Metadata

- **State**: open
- **Author**: [@IrvingMg](https://github.com/IrvingMg)
- **Created**: 2026-03-13T11:30:26Z
- **Updated**: 2026-04-02T08:28:09Z
- **Closed**: —
- **Labels**: `kind/cleanup`
- **Assignees**: [@MatteoFari](https://github.com/MatteoFari)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
There are two different mechanisms used to clean up stale Prometheus gauge series when a label value changes.

1. `StoreAndClear` (`pkg/metrics/custom_labels.go`). This was introduced in #9774 for custom metric labels. Each controller (CQ, LQ, Cohort) tracks its current label values. When a value changes, for example, when a CQ's team annotation changes from `alpha` to `beta`, the controller deletes the old metric series for that object. During the next update cycle, the metrics are created again with the new label value.
2. `ResyncGaugeMetrics` (`pkg/cache/scheduler/cache.go`, `pkg/cache/queue/manager.go`)
This was introduced in #9487 for the `replica_role` label during HA leader election. When a follower becomes the `leader`, it deletes all gauge series that have the old role label. Then it immediately reports all gauge metrics again for every object, using the new role label.

Both approaches solve the same problem: a gauge series with an outdated label value remains in Prometheus unless it is explicitly deleted. However, they use different methods to handle this.

**Why is this needed**:

Aligning these two patterns could reduce duplicated logic and make it easier to manage the lifecycle of gauge metrics in one place.

See https://github.com/kubernetes-sigs/kueue/pull/9774#discussion_r2924664021.

## Discussion

### Comment by [@MatteoFari](https://github.com/MatteoFari) — 2026-04-02T08:28:06Z

/assign
