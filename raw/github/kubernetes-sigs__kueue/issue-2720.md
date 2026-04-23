# Issue #2720: Prioritize reclamation over priority-based preemption across multiple RFs

**Summary**: Prioritize reclamation over priority-based preemption across multiple RFs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2720

**Last updated**: 2024-08-13T12:01:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-07-30T09:14:42Z
- **Updated**: 2024-08-13T12:01:05Z
- **Closed**: 2024-08-13T12:01:05Z
- **Labels**: `kind/bug`
- **Assignees**: [@gabesaba](https://github.com/gabesaba)
- **Comments**: 1

## Description

**What would you like to be added**:

We have a cohort with CQ with `WhenCanPreempt: TryNextFlavor`.

Assume there are 2 ResourceFlavors and both require preemption to accommodate a new workload. 

The first RF requires priority based preemption inside the CQ, while the second RF could accommodate just based on reclamation. Currently, we would pick the first RF as the second does not "improve" the assignment. 

However, picking the second RF should be considered an improvement of the assignment, because reclamation should be preferred over priority-based preemption. Note that, if there is one RF we prioritize reclamation (preemptions by borrowing workloads).

We may consider a feature gate if this change seems risky.

**Why is this needed**:

To properly prioritize preemptions in case of multiple RFs. This can be useful in a situation when different RF are equivalent in terms of machine price, but they are used to represent node groups in different zones. In that setting, a team has some nominal quota in every zone, and prefers to use the nominal quota first by reclamation.

**How to reproduce it (as minimally and precisely as possible)**:

Create the following structure:

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "zone-a"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "zone-b"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue1"
spec:
  cohort: "cohort"
  flavorFungibility:
    whenCanBorrow: TryNextFlavor
    whenCanPreempt: TryNextFlavor
  preemption:
    withinClusterQueue: LowerPriority
    reclaimWithinCohort: Any
  namespaceSelector: {}
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "zone-a"
      resources:
      - name: "cpu"
        nominalQuota: 3
      - name: "memory"
        nominalQuota: 12Gi
    - name: "zone-b"
      resources:
      - name: "cpu"
        nominalQuota: 3
      - name: "memory"
        nominalQuota: 12Gi
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue2"
spec:
  cohort: "cohort"
  flavorFungibility:
    whenCanBorrow: TryNextFlavor
    whenCanPreempt: TryNextFlavor
  preemption:
    withinClusterQueue: LowerPriority
    reclaimWithinCohort: Any
  namespaceSelector: {}
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "zone-a"
      resources:
      - name: "cpu"
        nominalQuota: 3
      - name: "memory"
        nominalQuota: 12Gi
    - name: "zone-b"
      resources:
      - name: "cpu"
        nominalQuota: 3
      - name: "memory"
        nominalQuota: 12Gi
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "user-queue1"
spec:
  clusterQueue: "cluster-queue1"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "user-queue2"
spec:
  clusterQueue: "cluster-queue2"
```
Then, we have 3 jobs: `sample1-low.yaml`, `sample2-low.yaml` and `sample1-mid.yaml`. 
`sample1-low` is as follows:
```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: low-priority
value: 1
globalDefault: false
description: "This priority class should be used for XYZ service pods only."
---
apiVersion: batch/v1
kind: Job
metadata:
  generateName: sample1-low-job-
  namespace: default
  labels:
    kueue.x-k8s.io/queue-name: user-queue1
spec:
  parallelism: 3
  completions: 3
  suspend: true
  template:
    spec:
      priorityClassName: "low-priority"
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:v0.0.3
        args: ["600s"]
        resources:
          requests:
            cpu: "1"
            memory: "200Mi"
      restartPolicy: Never
```
`sample2-low.yaml` is analogous. but creates the Job is CQ2, whereas `sample1-mid.yaml` is just mid priority.

Now: 
1. create 2 Jobs `sample2-low.yaml` to exhaust nominal capacity of CQ2 in zone-a and zone-b
2. create `sample1-low.yaml` to exhaust nominal quota of CQ1 in zone-a
3. create `sample2-low.yaml`, which borrows from CQ1 in flavor zone-b
3. create `sample1-mid-yaml`

**Issue**
The new workload preempts from zone-a using priority-based preemption while it could still do reclamation in zone-b.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-30T09:14:57Z

/assign @gabesaba
