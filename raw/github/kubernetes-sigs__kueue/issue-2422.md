# Issue #2422: [FairSharing] ClusterQueue status does not report stats

**Summary**: [FairSharing] ClusterQueue status does not report stats

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2422

**Last updated**: 2024-06-18T13:00:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-06-17T10:31:11Z
- **Updated**: 2024-06-18T13:00:23Z
- **Closed**: 2024-06-18T05:11:38Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 8

## Description

**What happened**:

When using FairSharing, the ClusterQueue.status.fairSharing field remains empty even if the ClusterQueue is borrowing.

**What you expected to happen**:

The ClusterQueue.status.fairSharing.weightedShare to be updated as soon as the cluster queue starts borrowing.

**How to reproduce it (as minimally and precisely as possible)**:

Create a cluster like this:
```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "default-flavor"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cq-a"
spec:
  cohort: "cohort"
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
kind: ClusterQueue
metadata:
  name: "cq-b"
spec:
  cohort: "cohort"
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
kind: ClusterQueue
metadata:
  name: "cq-c"
spec:
  cohort: "cohort"
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
  name: "queue-a"
spec:
  clusterQueue: "cq-a"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "queue-b"
spec:
  clusterQueue: "cq-b"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "queue-c"
spec:
  clusterQueue: "cq-c"
```
Then create 4 Jobs like this:
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  generateName: sample-job-
  labels:
    kueue.x-k8s.io/queue-name: queue-a
spec:
  parallelism: 3
  completions: 3
  suspend: true
  template:
    spec:
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:v0.0.3
        args: ["10m"]
        resources:
          requests:
            cpu: "1"
            memory: "200Mi"
      restartPolicy: Never
```
Then, inspect the clusterqueue-a:
```yaml
status:
  admittedWorkloads: 4
  conditions:
  - lastTransitionTime: "2024-06-17T10:24:20Z"
    message: Can admit new workloads
    observedGeneration: 1
    reason: Ready
    status: "True"
    type: Active
  fairSharing: {}
  flavorsReservation:
  - name: default-flavor
    resources:
    - borrowed: "3"
      name: cpu
      total: "12"
    - borrowed: "0"
      name: memory
      total: 2400Mi
  flavorsUsage:
  - name: default-flavor
    resources:
    - borrowed: "3"
      name: cpu
      total: "12"
    - borrowed: "0"
      name: memory
      total: 2400Mi
  pendingWorkloads: 0
  reservingWorkloads: 4
```
Issue: `status.fairSharing.weightedShare` is empty.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-17T10:31:18Z

/cc @alculquicondor

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-17T10:35:59Z

It seems the culprit is that we don't initialize the fairSharing option when building options for cache: https://github.com/kubernetes-sigs/kueue/blob/e8e0810115f3bef7518b4c07eb4c2e2579660060/cmd/kueue/main.go#L157-L163

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-06-17T11:42:23Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-18T12:23:20Z

/cherry-pick release-0.7

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-18T12:56:01Z

/cherry-pick release-0.7

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-18T12:56:37Z

Something seems to be going on with the bot.

@mbobrovskyi can you open a manual cherry-pick?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-18T12:57:04Z

oh, this is the issue, not the PR 🤦

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-06-18T12:59:18Z

Yes, this is issue. Don't worry, @mimowo already created cherry-pick and merged it. #2432
