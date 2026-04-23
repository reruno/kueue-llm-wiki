# Issue #5891: MultiKueue the admission check remains Pending and workload is not Admitted for Pod integration

**Summary**: MultiKueue the admission check remains Pending and workload is not Admitted for Pod integration

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5891

**Last updated**: 2025-12-16T16:14:11Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-07T11:30:27Z
- **Updated**: 2025-12-16T16:14:11Z
- **Closed**: 2025-12-16T16:14:11Z
- **Labels**: `kind/bug`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 4

## Description


**What happened**:

When using Pod groups with MultiKueue the admission check remains "Pending", and the workload does not get the "Admitted" condition.

This misleading for cluster admins, because it does not show the workload as "Admitted". 

```
NAME                                    QUEUE        RESERVED IN     ADMITTED   FINISHED   AGE
workload.kueue.x-k8s.io/sample-group1   user-queue   cluster-queue              True       5m52s
workload.kueue.x-k8s.io/sample-group2   user-queue   cluster-queue              True       5m42s
```

This also means that the metrics for workloads are not accounted correctly (don't count running workloads as admitted). Further, WaitForPodsReady does not work.

**What you expected to happen**:

The workload is marked as "Admitted", and the admission check as "Ready".

**How to reproduce it (as minimally and precisely as possible)**:

1. Setup multikueue environment as https://kueue.sigs.k8s.io/docs/tasks/manage/setup_multikueue/
2. Create a pod group as follows:

```yaml
---
apiVersion: v1
kind: Pod
metadata:
  generateName: sample-leader-
  labels:
    kueue.x-k8s.io/queue-name: user-queue
    kueue.x-k8s.io/pod-group-name: "sample-group1"
  annotations:
    kueue.x-k8s.io/pod-group-total-count: "3"
spec:
  restartPolicy: Never
  containers:
  - name: sleep
    image: busybox
    command: ["sh", "-c", 'echo "hello world from the leader pod" && sleep 60']
    resources:
      requests:
        cpu: 1
        memory: "1Gi"
---
apiVersion: v1
kind: Pod
metadata:
  generateName: sample-worker1-
  labels:
    kueue.x-k8s.io/queue-name: user-queue
    kueue.x-k8s.io/pod-group-name: "sample-group1"
  annotations:
    kueue.x-k8s.io/pod-group-total-count: "3"
spec:
  restartPolicy: Never
  containers:
  - name: sleep
    image: busybox
    command: ["sh", "-c", 'echo "hello world from the worker pod" && sleep 60']
    resources:
      requests:
        cpu: 1
        memory: "1Gi"
---
apiVersion: v1
kind: Pod
metadata:
  generateName: sample-worker2-
  labels:
    kueue.x-k8s.io/queue-name: user-queue
    kueue.x-k8s.io/pod-group-name: "sample-group1"
  annotations:
    kueue.x-k8s.io/pod-group-total-count: "3"
spec:
  restartPolicy: Never
  containers:
  - name: sleep
    image: busybox
    command: ["sh", "-c", 'echo "hello world from the worker pod" && sleep 60']
    resources:
      requests:
        cpu: 1
        memory: "1Gi"
```

**Anything else we need to know?**:

The culprit is here: https://github.com/kubernetes-sigs/kueue/blob/d15581acbb5ebb10de1db19f4bec4495c022d3e1/pkg/controller/jobs/pod/pod_multikueue_adapter.go#L90

This is probably not marked as false, because otherwise, when the workload was admitted, the Pod scheduling gate is removed.

One potential solution should be to just skip deleting the feature gate in the pod_controller code https://github.com/kubernetes-sigs/kueue/blob/d15581acbb5ebb10de1db19f4bec4495c022d3e1/pkg/controller/jobs/pod/pod_controller.go#L1373 when the workload has a multiKueue Admission check in its status.

Alternatively we could introduce a dedicated scheduling gate, such as "multikueue", but this seems more involving and not necessary.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-07T11:30:50Z

cc @tenzen-y @mwysokin @mbobrovskyi @Bobbins228

### Comment by [@amy](https://github.com/amy) — 2025-07-16T16:38:08Z

/assign

### Comment by [@amy](https://github.com/amy) — 2025-09-12T15:33:54Z

/unassign

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-12-05T09:16:06Z

/assign
