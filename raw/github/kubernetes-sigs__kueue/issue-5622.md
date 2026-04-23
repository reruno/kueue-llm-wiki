# Issue #5622: Provide a way to display the pending workloads in grafana

**Summary**: Provide a way to display the pending workloads in grafana

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5622

**Last updated**: 2025-06-16T23:10:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-11T11:31:04Z
- **Updated**: 2025-06-16T23:10:59Z
- **Closed**: 2025-06-16T23:10:59Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 5

## Description

**What would you like to be added**:

Currently, we can get the list of Pending workloads via visibility API, but there is no easy way to display that list in grafana.

**Why is this needed**:

Some admins expect to have centralized observability of the Kueue system in one place, that is grafana. Seeing the list of pending workloads is important aspect of observing the state of the Kueue system. So, some users/admins would like to display it in grafana.

**Completion requirements**:

This task might involve developing some extra proxy as an experimental subproject, or just documenting in the "tasks" page how to do it.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-11T11:31:38Z

cc @mwielgus @mwysokin @tenzen-y
/assign @mbobrovskyi 
who is already investigating how to display the pending workloads in grafana

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-11T12:03:09Z

> This task might involve developing some extra proxy as an experimental subproject, or just documenting in the "tasks" page how to do it.

I guess that the Blackbox exporter could resolve this requirement: https://github.com/prometheus/blackbox_exporter
The Blackbox exporter allows admins to deliver arbitrary HTTP responses to Prometheus.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-11T12:06:19Z

@mbobrovskyi ptal

### Comment by [@kannon92](https://github.com/kannon92) — 2025-06-11T13:01:19Z

Do we have a kueue community granfana dashboard?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-12T13:01:22Z

> Do we have a kueue community granfana dashboard?

We do not have any Grafana dashboards.
