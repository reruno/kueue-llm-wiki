# Issue #2012: [WaitForPodsReady] There is no event for eviction on the workload

**Summary**: [WaitForPodsReady] There is no event for eviction on the workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2012

**Last updated**: 2024-06-11T14:51:52Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-04-18T16:59:49Z
- **Updated**: 2024-06-11T14:51:52Z
- **Closed**: 2024-06-11T14:41:16Z
- **Labels**: `kind/bug`, `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

**What happened**:

There is no event for eviction on the workload, only on the job.

For comparison, for priority-based preemption we send events both for workload and job.

**What you expected to happen**:

Event to be sent both for Workload and Job.

**How to reproduce it (as minimally and precisely as possible)**:

Example global configuration:
```yaml
waitForPodsReady:
  enable: true
  timeout: 1m
  blockAdmission: false
  requeuingStrategy:
    timestamp: Creation
    backoffLimitCount: 4
 ```
 Example cluster configuration:
 ```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "default-flavor"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue"
spec:
  namespaceSelector: {}
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 200
      - name: "memory"
        nominalQuota: 36Gi
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "user-queue"
spec:
  clusterQueue: "cluster-queue"
 ```
 Example Job:
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: sample-job
  namespace: default
  labels:
    kueue.x-k8s.io/queue-name: user-queue
spec:
  parallelism: 1
  completions: 1
  suspend: true
  template:
    spec:
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:v0.0.3
        args: ["1800s"]
        resources:
          requests:
            cpu: "50"
            memory: "200Mi"
      restartPolicy: Never
```

Then observing the workload events:
```
kubectl describe workloads/job-sample-job-08913
...
  Type    Reason         Age                 From             Message
  ----    ------         ----                ----             -------
  Normal  QuotaReserved  40m (x4 over 43m)   kueue-admission  Quota reserved in ClusterQueue cluster-queue, wait time since queued was 1s
  Normal  QuotaReserved  39m                 kueue-admission  Quota reserved in ClusterQueue cluster-queue, wait time since queued was 2s
  Normal  QuotaReserved  38m                 kueue-admission  Quota reserved in ClusterQueue cluster-queue, wait time since queued was 3s
  Normal  QuotaReserved  37m                 kueue-admission  Quota reserved in ClusterQueue cluster-queue, wait time since queued was 5s
  Normal  QuotaReserved  35m                 kueue-admission  Quota reserved in ClusterQueue cluster-queue, wait time since queued was 7s
  Normal  QuotaReserved  34m                 kueue-admission  Quota reserved in ClusterQueue cluster-queue, wait time since queued was 11s
  Normal  QuotaReserved  33m                 kueue-admission  Quota reserved in ClusterQueue cluster-queue, wait time since queued was 15s
  Normal  QuotaReserved  32m                 kueue-admission  Quota reserved in ClusterQueue cluster-queue, wait time since queued was 22s
  Normal  QuotaReserved  30m                 kueue-admission  Quota reserved in ClusterQueue cluster-queue, wait time since queued was 31s
  Normal  Admitted       26m (x14 over 43m)  kueue-admission  Admitted by ClusterQueue cluster-queue, wait time since reservation was 0s
  Normal  QuotaReserved  12m (x6 over 28m)   kueue-admission  (combined from similar events): Quota reserved in ClusterQueue cluster-queue, wait time since queued was 252s

```
**Issue**: there is no event for eviction, just admissions.

**Anything else we need to know?**:

For comparison, for priority-based evictions we get events also for workloads, example (line 2):
```
  Type    Reason         Age                From             Message
  ----    ------         ----               ----             -------
  Normal  QuotaReserved  10m                kueue-admission  Quota reserved in ClusterQueue cluster-queue, wait time since queued was 1s
  Normal  Preempted      10m                kueue-admission  Preempted to accommodate a workload (UID: b6bc86b7-42f0-4174-ab8d-1ef6a24baacc) in the ClusterQueue
  Normal  Pending        10m (x4 over 10m)  kueue-admission  couldn't assign flavors to pod set main: insufficient unused quota for cpu in flavor default-flavor, 3 more needed
  Normal  Admitted       10m (x2 over 10m)  kueue-admission  Admitted by ClusterQueue cluster-queue, wait time since reservation was 0s
  Normal  QuotaReserved  10m                kueue-admission  Quota reserved in ClusterQueue cluster-queue, wait time since queued was 15s
```

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-06-07T07:04:22Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-11T14:51:49Z

/kind feature
