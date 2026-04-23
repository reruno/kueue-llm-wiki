# Issue #7336: "Nominate Worker Clusters with Incremental Dispatcher" is constantly logged for all workloads at V3

**Summary**: "Nominate Worker Clusters with Incremental Dispatcher" is constantly logged for all workloads at V3

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7336

**Last updated**: 2025-11-13T09:15:44Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-21T10:02:39Z
- **Updated**: 2025-11-13T09:15:44Z
- **Closed**: 2025-11-13T09:15:44Z
- **Labels**: `kind/bug`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 4

## Description

**What happened**:

This log line is constantly logged for all workloads: "Nominate Worker Clusters with Incremental Dispatcher"

**What you expected to happen**:

Log this line only for: MultiKueue workload which is QuotaReserved (and not Finished etc)

**How to reproduce it (as minimally and precisely as possible)**:


Just see our e2e logs (not for MultiKueue even), eg:

https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7318/pull-kueue-test-e2e-main-1-34/1980552609731186688/artifacts/run-test-e2e-singlecluster-1.34.0/kind-worker2/pods/kueue-system_kueue-controller-manager-74948d5f78-8jhm2_9cd4181b-f4d6-4f03-b951-1eecff8060b6/manager/0.log


**Anything else we need to know?**:

```
2025-10-21T08:49:55.133092469Z stderr F 2025-10-21T08:49:55.132883577Z	LEVEL(-3)	workloaddispatcher/incrementaldispatcher.go:77	Nominate Worker Clusters with Incremental Dispatcher	{"controller": "multikueue_incremental_dispatcher", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"job-admission-checked-job-42f2a","namespace":"e2e-metrics-qtdfr"}, "namespace": "e2e-metrics-qtdfr", "name": "job-admission-checked-job-42f2a", "reconcileID": "b8d97723-347d-4740-bee5-f61c4382e49f"}
2025-10-21T08:49:55.133127589Z stderr F 2025-10-21T08:49:55.132932997Z	LEVEL(-3)	workloaddispatcher/incrementaldispatcher.go:80	Not a Incremental Dispatcher, skip the reconciliation	{"controller": "multikueue_incremental_dispatcher", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"job-admission-checked-job-42f2a","namespace":"e2e-metrics-qtdfr"}, "namespace": "e2e-metrics-qtdfr", "name": "job-admission-checked-job-42f2a", "reconcileID": "b8d97723-347d-4740-bee5-f61c4382e49f", "dispatcherName": "kueue.x-k8s.io/multikueue-dispatcher-all-at-once"}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-21T10:02:48Z

cc @mszadkow

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-10-23T13:04:00Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-10-27T08:41:52Z

/unassign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-11-12T11:06:47Z

/assign
