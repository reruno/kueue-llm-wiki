# Issue #2821: Infinite preemption loop is possible when PrioritySortingWithinCohort=false is used with borrowWithinCohort

**Summary**: Infinite preemption loop is possible when PrioritySortingWithinCohort=false is used with borrowWithinCohort

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2821

**Last updated**: 2024-08-22T18:43:53Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-08-12T10:17:05Z
- **Updated**: 2024-08-22T18:43:53Z
- **Closed**: 2024-08-13T13:14:13Z
- **Labels**: `kind/bug`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 2

## Description

**What happened**:

An infinite preemption loop is possible when `PrioritySortingWithingCohort=false` is used together with 
borrowWithinCohort. This is possible when a high-priority workload from CQ running above quota needs
to borrow and preempts a lower priority workload. Then, the lower priority workload may take spot
in front of the high-priority workload (because PrioritySortingWithingCohort=false) and get re-admitted.
The cycle (preempt - admit - preempt) will repeat for the lower-priority workload.

The high-priority workload is never admitted (as long as its CQ is running above it nominal quota), because the lower-priority workload gets in front of it repeatedly.

**What you expected to happen**:

No infinite cycles of preempt - admit - preempt.

**How to reproduce it (as minimally and precisely as possible)**:

1. Set up the cluster as follows:
```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "default-flavor"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue-a"
spec:
  cohort: "all"
  preemption:
    withinClusterQueue: LowerPriority
    reclaimWithinCohort: Any
  namespaceSelector: {} # match all.
  resourceGroups:
  - coveredResources: ["cpu"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 0
        borrowingLimit: 10
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue-b"
spec:
  cohort: "all"
  preemption:
    withinClusterQueue: LowerPriority
    reclaimWithinCohort: Any
    borrowWithinCohort:
      maxPriorityThreshold: 80000
      policy: LowerPriority
  namespaceSelector: {} # match all.
  resourceGroups:
  - coveredResources: ["cpu"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 5
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue-c"
spec:
  cohort: "all"
  preemption:
    withinClusterQueue: LowerPriority
    reclaimWithinCohort: Any
  namespaceSelector: {} # match all.
  resourceGroups:
  - coveredResources: ["cpu"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 5
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "user-queue-a"
spec:
  clusterQueue: "cluster-queue-a"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "user-queue-b"
spec:
  clusterQueue: "cluster-queue-b"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "user-queue-c"
spec:
  clusterQueue: "cluster-queue-c"
---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: low-priority
value: 1
globalDefault: false
description: "This priority class should be used for XYZ service pods only."
---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: mid-priority
value: 2
globalDefault: false
description: "This priority class should be used for XYZ service pods only."
---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 3
globalDefault: false
description: "This priority class should be used for XYZ service pods only."
```
2. create the lower-priority workload in CQa:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  generateName: sample-job-a-
  namespace: default
  labels:
    kueue.x-k8s.io/queue-name: user-queue-a
spec:
  parallelism: 1
  completions: 1
  suspend: true
  template:
    spec:
      priorityClassName: mid-priority
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:v0.1.0
        args: ["300s"]
        resources:
          requests:
            cpu: "4"
      restartPolicy: Never
```
3. Create 2 workloads in CQb:
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  generateName: sample-job-b-
  namespace: default
  labels:
    kueue.x-k8s.io/queue-name: user-queue-b
spec:
  parallelism: 1
  completions: 1
  suspend: true
  template:
    spec:
      priorityClassName: high-priority
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:v0.1.0
        args: ["300s"]
        resources:
          requests:
            cpu: "4"
      restartPolicy: Never
```
**Issue:** workload-a will go through infinite cycle of preemptions and admissions.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-08-12T10:20:58Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-22T18:43:51Z

/retitle Infinite preemption loop is possible when PrioritySortingWithinCohort=false is used with borrowWithinCohort
