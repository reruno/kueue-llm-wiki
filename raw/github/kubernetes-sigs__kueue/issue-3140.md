# Issue #3140: [PartialAdmission] Job remains suspended when admitted using partial-admission

**Summary**: [PartialAdmission] Job remains suspended when admitted using partial-admission

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3140

**Last updated**: 2024-09-30T08:12:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-09-26T09:04:15Z
- **Updated**: 2024-09-30T08:12:04Z
- **Closed**: 2024-09-30T08:12:04Z
- **Labels**: `kind/bug`
- **Assignees**: [@mimowo](https://github.com/mimowo), [@trasc](https://github.com/trasc)
- **Comments**: 2

## Description

**What happened**:

If the min-parallelism equals the free resources the Workload gets admitted, but the job remains suspended.

**What you expected to happen**:

Admit the Workload and Unsuspend the job.

**How to reproduce it (as minimally and precisely as possible)**:

1. Create the following config
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

2. Submit the job 
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  generateName: sample-big-
  labels:
    kueue.x-k8s.io/queue-name: user-queue
  annotations:
    kueue.x-k8s.io/job-min-parallelism: "9"
spec:
  parallelism: 10
  completions: 10
  completionMode: Indexed
  suspend: true
  template:
    spec:
      containers:
      - name: job-longrun
        image: python
        command:
        - python3
        - -c
        - |
          import os
          import time
          import sys
          id = int(os.environ.get("JOB_COMPLETION_INDEX"))
          time.sleep(5 + id*5)
        imagePullPolicy: IfNotPresent
        resources:
          requests:
            cpu: "1"
            memory: "200Mi"
      restartPolicy: Never
```
Result, the workload is admitted (resources are reserved), but the Job remains suspended.

**Anything else we need to know?**:

There are webhook errors:

```
{"level":"error","ts":"2024-09-26T09:01:35.944600423Z","caller":"jobframework/reconciler.go:461","msg":"Unsuspending job","controller":"job","controllerGroup":"batch","controllerKind":"Job","Job":{"name":"sample-big-2vw2b","namespace":"default"},"namespace":"default","name":"sample-big-2vw2b","reconcileID":"1095dc93-51ac-4267-b317-83ba27e41a23","job":"default/sample-big-2vw2b","gvk":"batch/v1, Kind=Job","error":"admission webhook \"vjob.kb.io\" denied the request: metadata.annotations[kueue.x-k8s.io/job-min-parallelism]: Invalid value: 9: should be between 0 and 8"

...

```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-26T10:29:40Z

/assign
Assigning initially to myself, feel free to ping me on slack if you are interested to take it

### Comment by [@trasc](https://github.com/trasc) — 2024-09-27T10:08:59Z

/assign
