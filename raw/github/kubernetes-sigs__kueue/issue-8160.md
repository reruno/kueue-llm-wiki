# Issue #8160: TAS: support for ElasticWorkloads

**Summary**: TAS: support for ElasticWorkloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8160

**Last updated**: 2026-02-17T09:27:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-10T10:02:01Z
- **Updated**: 2026-02-17T09:27:05Z
- **Closed**: 2026-02-17T09:27:05Z
- **Labels**: `kind/feature`, `priority/important-soon`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Currently we support [TAS](https://kueue.sigs.k8s.io/docs/concepts/topology_aware_scheduling/) and support [ElasticWorkloads](https://kueue.sigs.k8s.io/docs/concepts/elastic_workload/), but not combined: 

This is not supported for two reasons:
1. the workload annotation will get outdated: https://github.com/kubernetes-sigs/kueue/issues/6480
2. the TopologyAssignment is not copied and adjusted between Workload Slices

An alternative approach which eliminates the need for (1.) is WorkloadResize, but this is also involving: https://github.com/kubernetes-sigs/kueue/issues/5897

**Why is this needed**:

We have users of TAS, and have users for ElasticJobs, unfortunately they cannot yet benefit from both features at the same time.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-10T10:02:55Z

cc @mwysokin @ichekrygin @hiboyang

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-12-15T17:12:42Z

/assign @sohankunkerkar

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:38:33Z

/priority important-soon
