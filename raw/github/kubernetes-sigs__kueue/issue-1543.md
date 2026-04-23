# Issue #1543: Flaky: Scheduler when Scheduling workloads on clusterQueues Should admit workloads according to their priorities

**Summary**: Flaky: Scheduler when Scheduling workloads on clusterQueues Should admit workloads according to their priorities

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1543

**Last updated**: 2024-01-04T09:11:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-01-03T18:23:25Z
- **Updated**: 2024-01-04T09:11:32Z
- **Closed**: 2024-01-04T09:11:32Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 2

## Description

**What happened**:

Flaky test `Scheduler when Scheduling workloads on clusterQueues Should admit workloads according to their priorities`

**What you expected to happen**:

Test to pass

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1541/pull-kueue-test-integration-main/1742606522124341248

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-03T18:24:59Z

/kind flake

No failures for this test in the periodic testgrid, so maybe it's not a new issue.

https://testgrid.k8s.io/sig-scheduling#periodic-kueue-test-integration-main&width=20

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-03T18:59:00Z

This seems to be a very unlucky situation, and not indicative of a bug in the production code:

```
  2024-01-03T18:15:37.542262895Z  LEVEL(-2) localqueue-reconciler core/localqueue_controller.go:118 LocalQueue create event {"localQueue": {"name":"queue","namespace":"core-ls42z"}}
  2024-01-03T18:15:37.542502451Z  LEVEL(-3) scheduler queue/manager.go:447  Obtained ClusterQueue heads {"count": 1}
  2024-01-03T18:15:37.542723186Z  LEVEL(-2) scheduler scheduler/scheduler.go:446  Workload assumed in the cache {"workload": {"name":"wl-high-priority-1","namespace":"core-ls42z"}, "clusterQueue": {"name":"prod-cq"}}
  2024-01-03T18:15:37.542719436Z  LEVEL(-2) workload-reconciler core/workload_controller.go:330 Workload create event {"workload": {"name":"wl-high-priority-2","namespace":"core-ls42z"}, "queue": "queue", "status": "pending"}
  2024-01-03T18:15:37.542805658Z  LEVEL(-3) scheduler queue/manager.go:447  Obtained ClusterQueue heads {"count": 1}
  2024-01-03T18:15:37.542925051Z  LEVEL(-2) scheduler scheduler/scheduler.go:446  Workload assumed in the cache {"workload": {"name":"wl-mid-priority-1","namespace":"core-ls42z"}, "clusterQueue": {"name":"prod-cq"}}
```

What we see in the logs is that `wl-high-priority-2` was observed after the local queue was observed. So it's possible that it only made it into the queues after the scheduler already scheduled `wl-mid-priority-1`. And because there is no preemption in this case, `wl-high-priority-2` can't fit.

I need to find a workaround for a more reliable object creation order.
