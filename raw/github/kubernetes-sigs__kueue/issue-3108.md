# Issue #3108: [PartialAdmission] A partially admitted workload blocks admission when free resources

**Summary**: [PartialAdmission] A partially admitted workload blocks admission when free resources

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3108

**Last updated**: 2024-09-26T08:00:07Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-09-20T17:36:11Z
- **Updated**: 2024-09-26T08:00:07Z
- **Closed**: 2024-09-26T08:00:07Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 1

## Description

**What happened**:

A partially admitted workload does not allow other small workloads to get admitted, even if resources are available.

**What you expected to happen**:

A partially admitted workload does not block admission if there are free resources. 

**How to reproduce it (as minimally and precisely as possible)**:

I have the cluster structure as below:

```yaml
# default-flavor.yaml
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
  namespaceSelector: {} # match all.
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 9
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

we have also two Job types, `small.yaml`:
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  generateName: sample-job-
  labels:
    kueue.x-k8s.io/queue-name: user-queue
spec:
  parallelism: 3
  completions: 3
  suspend: true
  template:
    spec:
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:v0.1.0
        args: ["600s"]
        resources:
          requests:
            cpu: "1"
            memory: "200Mi"
      restartPolicy: Never
```
and `big.yaml`:
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  generateName: sample-job-
  labels:
    kueue.x-k8s.io/queue-name: user-queue
  annotations:
    kueue.x-k8s.io/job-min-parallelism: "1"
spec:
  parallelism: 9
  completions: 9
  suspend: true
  template:
    spec:
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:v0.1.0
        args: ["600s"]
        resources:
          requests:
            cpu: "1"
            memory: "200Mi"
      restartPolicy: Never
```
Steps:
1. create the cluster structure
2. create 2 `small.yaml` jobs, each consuming 3 pods, so 6 pods total.
3. create `big.yaml` Job, 3 pods are created (correctly), but the CQ misreports usage as 15 units (6 + 9).
4. delete the small Jobs, the big Job continues to use 3 pods, but reports consuming 9 resources
5. I create two new small jobs requesting 3 pods which should fit (as the big one only created 3 pods), **but they remain suspended**

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-20T17:36:19Z

/assign @trasc
