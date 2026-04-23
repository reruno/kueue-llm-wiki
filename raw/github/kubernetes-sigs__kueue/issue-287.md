# Issue #287: Missing detail logs in integration tests

**Summary**: Missing detail logs in integration tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/287

**Last updated**: 2022-07-04T14:15:25Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2022-06-27T14:04:46Z
- **Updated**: 2022-07-04T14:15:25Z
- **Closed**: 2022-07-04T14:15:25Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Before https://github.com/kubernetes-sigs/kueue/pull/252, we have logs like this in integration tests:
```
2022-06-27T21:54:16.938124+08:00        INFO    controller.queue        Starting EventSource    {"reconciler group": "kueue.x-k8s.io", "reconciler kind": "Queue", "source": "kind source: *v1alpha1.Queue"}
2022-06-27T21:54:16.938143+08:00        INFO    controller.clusterqueue Starting EventSource    {"reconciler group": "kueue.x-k8s.io", "reconciler kind": "ClusterQueue", "source": "kind source: *v1alpha1.ClusterQueue"}
2022-06-27T21:54:16.93819+08:00 INFO    controller.resourceflavor       Starting EventSource    {"reconciler group": "kueue.x-k8s.io", "reconciler kind": "ResourceFlavor", "source": "kind source: *v1alpha1.ResourceFlavor"}
2022-06-27T21:54:16.938201+08:00        INFO    controller.queue        Starting EventSource    {"reconciler group": "kueue.x-k8s.io", "reconciler kind": "Queue", "source": "channel source: 0xc000215d60"}
2022-06-27T21:54:16.938223+08:00        INFO    controller.resourceflavor       Starting Controller     {"reconciler group": "kueue.x-k8s.io", "reconciler kind": "ResourceFlavor"}
2022-06-27T21:54:16.938222+08:00        INFO    controller.clusterqueue Starting EventSource    {"reconciler group": "kueue.x-k8s.io", "reconciler kind": "ClusterQueue", "source": "channel source: 0xc000215e00"}
2022-06-27T21:54:16.938248+08:00        INFO    controller.queue        Starting Controller     {"reconciler group": "kueue.x-k8s.io", "reconciler kind": "Queue"}
2022-06-27T21:54:16.938303+08:00        INFO    controller.clusterqueue Starting Controller     {"reconciler group": "kueue.x-k8s.io", "reconciler kind": "ClusterQueue"}
2022-06-27T21:54:16.938235+08:00        INFO    controller.workload     Starting EventSource    {"reconciler group": "kueue.x-k8s.io", "reconciler kind": "Workload", "source": "kind source: *v1alpha1.Workload"}
2022-06-27T21:54:16.93832+08:00 INFO    controller.queue        Starting workers        {"reconciler group": "kueue.x-k8s.io", "reconciler kind": "Queue", "worker count": 1}
2022-06-27T21:54:16.938331+08:00        INFO    controller.workload     Starting Controller     {"reconciler group": "kueue.x-k8s.io", "reconciler kind": "Workload"}
2022-06-27T21:54:17.039057+08:00        INFO    controller.workload     Starting workers        {"reconciler group": "kueue.x-k8s.io", "reconciler kind": "Workload", "worker count": 1}
2022-06-27T21:54:17.03912+08:00 INFO    controller.clusterqueue Starting workers        {"reconciler group": "kueue.x-k8s.io", "reconciler kind": "ClusterQueue", "worker count": 1}
2022-06-27T21:54:17.03916+08:00 INFO    controller.resourceflavor       Starting workers        {"reconciler group": "kueue.x-k8s.io", "reconciler kind": "ResourceFlavor", "worker count": 1}
2022-06-27T21:54:18.952396+08:00        LEVEL(-2)       cluster-queue-reconciler        ClusterQueue create event       {"clusterQueue": {"name":"cluster-queue"}}
2022-06-27T21:54:18.952611+08:00        LEVEL(-2)       controller.clusterqueue Reconciling ClusterQueue        {"reconciler group": "kueue.x-k8s.io", "reconciler kind": "ClusterQueue", "name": "cluster-queue", "namespace": "", "clusterQu
eue": {"name":"cluster-queue"}}
2022-06-27T21:54:18.957678+08:00        LEVEL(-2)       cluster-queue-reconciler        ClusterQueue update event       {"clusterQueue": {"name":"cluster-queue"}}
2022-06-27T21:54:18.957943+08:00        LEVEL(-2)       controller.clusterqueue Reconciling ClusterQueue        {"reconciler group": "kueue.x-k8s.io", "reconciler kind": "ClusterQueue", "name": "cluster-queue", "namespace": "", "clusterQu
eue": {"name":"cluster-queue"}}
```

but now we can't see the details. This will help in troubleshooting.

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-06-27T14:05:18Z

cc @cmssczy as the PR author.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-06-27T14:08:25Z

/remove-kind feature
/kind bug
