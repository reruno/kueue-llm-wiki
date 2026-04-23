# Issue #3614: TAS: Updates or deletion of Topology is not reflected in TAS cache resulting in wrong admission

**Summary**: TAS: Updates or deletion of Topology is not reflected in TAS cache resulting in wrong admission

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3614

**Last updated**: 2024-11-26T11:18:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-11-22T08:26:47Z
- **Updated**: 2024-11-26T11:18:59Z
- **Closed**: 2024-11-26T11:18:59Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

**What happened**:

The updates to the TAS topology object are not tracked by the resource_flavor controller.
As a consequence:
- after deletion of the topology workloads continue to be admitted
- after mutating the topology workloads are admitted using the old topology

**What you expected to happen**:

Updates or deletion to the Topology object are observed and reflected by changing the cache status

Fixing both scenarios can be separate PRs (probably preferred). I think we can cover the scenarios at the integration test level (since we don't need to create pods as in e2e).

**How to reproduce it (as minimally and precisely as possible)**:

Scenario 1 (for deletion): 
create the TAS structure 

```
apiVersion: kueue.x-k8s.io/v1alpha1
kind: Topology
metadata:
  name: "gke-default"
spec:
  levels:
  - nodeLabel: "kubernetes.io/hostname"
---
kind: ResourceFlavor
apiVersion: kueue.x-k8s.io/v1beta1
metadata:
  name: "tas-flavor"
spec:
  nodeLabels:
    kubernetes.io/os: "linux"
    #    cloud.google.com/gke-nodepool: "tas-node-pool"
  topologyName: "gke-default"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "tas-cluster-queue"
spec:
  namespaceSelector: {} # match all.
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "tas-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 200 
      - name: "memory"
        nominalQuota: 200Gi
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "tas-user-queue"
spec:
  clusterQueue: "tas-cluster-queue"
```
2. delete the topology
3. create a workload like this 

```
apiVersion: batch/v1
kind: Job 
metadata:
  generateName: tas-sample-small-required-host-
  labels:
    kueue.x-k8s.io/queue-name: tas-user-queue
spec:
  parallelism: 1
  completions: 1
  completionMode: Indexed
  template:
    metadata:
      annotations:
        kueue.x-k8s.io/podset-required-topology: "kubernetes.io/hostname"
    spec:
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:v0.1.0
        args: ["1800s"]
        resources:
          requests:
            cpu: "1" 
            memory: "200Mi"
      restartPolicy: Never
```
issue: the workload gets admitted

**Scenario 2:** 

2. instead of deleting the topology in (2.) change the level label to some non-existing
3. create the same workload - workload gets admitted

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-22T08:27:07Z

/assign @mbobrovskyi 
cc @PBundyra

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-22T08:29:40Z

I think we need to start watching for updates to the Topology objects similarly as we watch Nodes, and we need indexer to quickly find what are the ResourceFlavor objects affected by Topology change (and reconcile them). The Reconcile function itself also needs fixes.
