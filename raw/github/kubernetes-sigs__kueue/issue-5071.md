# Issue #5071: Create a metric to track the number of workloads evicted due to PodsReady timeouts

**Summary**: Create a metric to track the number of workloads evicted due to PodsReady timeouts

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5071

**Last updated**: 2025-05-20T09:23:18Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-04-23T10:50:58Z
- **Updated**: 2025-05-20T09:23:18Z
- **Closed**: 2025-05-20T09:23:17Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

**What would you like to be added**:

A metric which will count the number of workloads evicted due to PodsReady timeout

```golang
WaitForPodsReadyWorkloadEvictionTotal  = prometheus.NewCounterVec(
        prometheus.CounterOpts{
            Subsystem: constants.KueueName,
            Name:      "wait_for_pods_ready_workload_eviction_total",
            Help:      "The number of workloads evicted due to hitting one of the WaitForPodsReady timeouts at least once",
        }, []string{"reason”}, // RecoveryTimeout, StartupTimeout
    )
```

This probably requires extending the API to track the number of evictions each timeout specifically.

**Why is this needed**:

For alerting, to track the number of workloads evicted due to hitting of the timeouts.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-23T10:51:10Z

cc @mwielgus @mwysokin @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-04-23T11:06:04Z

/assign
