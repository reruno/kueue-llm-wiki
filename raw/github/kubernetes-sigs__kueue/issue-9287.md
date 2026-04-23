# Issue #9287: ReplicaRole is misreported by some components or not reported at all in logs

**Summary**: ReplicaRole is misreported by some components or not reported at all in logs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9287

**Last updated**: 2026-02-24T10:25:38Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-16T13:32:40Z
- **Updated**: 2026-02-24T10:25:38Z
- **Closed**: 2026-02-24T10:25:38Z
- **Labels**: `kind/bug`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 3

## Description

**What happened**:

I have some issues reporting the replica role, some that I found:
1. misreported for `queue/manager.go`, see: `queue/manager.go:722	Obtained ClusterQueue heads	{"replica-role": "follower", "schedulingCycle": 11, "count": 0}`
2. not reported by `jobframework/reconciler.go`, see: `jobframework/reconciler.go:803	stop walking up as the owner is not found	{"currentObj": {"name":"lws","namespace":"lws-e2e-gv6qm"}}`
3. misreported by `scheduler.go`, see `scheduler/scheduler.go:660	Workload successfully admitted and assigned flavors	{"replica-role": "follower", "schedulingCycle": 9, "workload": {"name":"leaderworkerset-lws-0-24c1f","namespace":"lws-e2e-gv6qm"}, "clusterQueue": {"name":"lws-cq-lws-e2e-gv6qm"}, "assignments": [{"name":"main","flavors":{"cpu":"lws-rf-lws-e2e-gv6qm"},"resourceUsage":{"cpu":"600m"},"count":3}]}` 

**What you expected to happen**:

ReplicaRole should be reported consistently for all components.

**How to reproduce it (as minimally and precisely as possible)**:

In our e2e tests: https://storage.googleapis.com/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-main-1-35/2023256437978828800/artifacts/run-test-e2e-singlecluster-1.35.0/kind-worker2/pods/kueue-system_kueue-controller-manager-699d8b5d8d-hwmq2_cdc3138a-daa4-4a7c-b434-d44f3b5de854/manager/0.log

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-16T13:32:47Z

cc @IrvingMg

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2026-02-16T15:10:29Z

/assign

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-02-17T11:08:28Z

1 and 3 are the same, as they share the same `ctx`
