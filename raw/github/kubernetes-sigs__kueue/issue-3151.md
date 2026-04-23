# Issue #3151: [batch/job] Cannot re-admit a a job which was previously partially admitted

**Summary**: [batch/job] Cannot re-admit a a job which was previously partially admitted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3151

**Last updated**: 2024-09-30T10:04:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@trasc](https://github.com/trasc)
- **Created**: 2024-09-27T09:34:09Z
- **Updated**: 2024-09-30T10:04:04Z
- **Closed**: 2024-09-30T10:04:04Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

A job that was previously partially admitted cannot be re admitted.

**What you expected to happen**:

The job to be re admitted.

**How to reproduce it (as minimally and precisely as possible)**:

. 1 Create the config:

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

2. Create a job.

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  generateName: sample-big-
  labels:
    kueue.x-k8s.io/queue-name: user-queue
  annotations:
    kueue.x-k8s.io/job-min-parallelism: "8"
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

3. Wait for the job to be unsuspended
4. Deactivate the job's workload
5. Reactivate the jobs workload
6. Observe that the job remains suspended.

**Anything else we need to know?**:

The problem looks to be a regression of 
- #2567 

and the condition in 

https://github.com/kubernetes-sigs/kueue/blob/425ece197331d6b0c9b6d2bf4cc82326420c9f0a/pkg/controller/jobs/job/job_webhook.go#L181-L183

should be reworked to allow the Restoration of the parallelism.

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2024-09-27T09:34:18Z

/assign
