# Issue #9288: There is no data for the kueue_cluster_queue_nominal_quota with replica_role=leader

**Summary**: There is no data for the kueue_cluster_queue_nominal_quota with replica_role=leader

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9288

**Last updated**: 2026-03-10T18:59:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-16T13:35:52Z
- **Updated**: 2026-03-10T18:59:12Z
- **Closed**: 2026-03-10T18:59:12Z
- **Labels**: `kind/bug`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 3

## Description

**What happened**:

A user reports there is no data reported for the `kueue_cluster_queue_nominal_quota` metric when `replica_role=leader` filter is present. There is data returned for `replica_role=follower` filter.

**What you expected to happen**:

The `kueue_cluster_queue_nominal_quota` metric should also be returned for leader replica.

**How to reproduce it (as minimally and precisely as possible)**:

Forwarding issue reported by a user, but it should be just to create a deployment with two replicas, and check the metric for CQs. If this does not repro the issue we may investigate more. This issue was reported on 0.16.1.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-16T13:36:00Z

cc @IrvingMg

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2026-02-16T15:10:45Z

/assign

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-02-17T11:06:59Z

I suspect that the issue is, after failover, there is nothing that triggers the metrics to be reported again, so we report the old metrics, with the stale role
