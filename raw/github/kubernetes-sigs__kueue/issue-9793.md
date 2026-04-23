# Issue #9793: Commonize gauge metric reporting to use cache as single data source

**Summary**: Commonize gauge metric reporting to use cache as single data source

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9793

**Last updated**: 2026-03-13T11:54:39Z

---

## Metadata

- **State**: open
- **Author**: [@IrvingMg](https://github.com/IrvingMg)
- **Created**: 2026-03-10T18:16:05Z
- **Updated**: 2026-03-13T11:54:39Z
- **Closed**: —
- **Labels**: `kind/cleanup`
- **Assignees**: [@reruno](https://github.com/reruno)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Commonize gauge metric reporting so that the cache becomes the single source of truth. In #9487, gauge metrics are currently reported from two different places using different data sources.

1. One path is the cache resync (`ResyncGaugeMetrics()` in `pkg/cache/scheduler/cache.go` and `pkg/cache/queue/manager.go`), which reports metrics by iterating over the cache state. These two methods follow the same pattern and are always called together. 
2. The other path is the controller reconcilers (`pkg/controller/core/clusterqueue_controller.go` and `pkg/controller/core/localqueue_controller.go`), which report metrics based on status updates during reconciliation.

**Why is this needed**:
As discussed in https://github.com/kubernetes-sigs/kueue/pull/9487#discussion_r2904826910, the intended direction is for both status updates and metrics to rely on the cache as the data source, instead of building metrics from controller statuses. 

Moving metric reporting fully to the cache would remove the duplication between cache resync and controller reconcilers and reduce the risk of inconsistencies when new metrics are introduced.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-10T18:28:02Z

cc @kshalot

### Comment by [@reruno](https://github.com/reruno) — 2026-03-13T11:54:13Z

/assing

### Comment by [@reruno](https://github.com/reruno) — 2026-03-13T11:54:36Z

/assign
