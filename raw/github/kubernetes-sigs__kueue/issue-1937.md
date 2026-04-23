# Issue #1937: In some scenarios the ClusterQueue status shows wrong count for PendingWorkloads

**Summary**: In some scenarios the ClusterQueue status shows wrong count for PendingWorkloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1937

**Last updated**: 2024-04-03T17:38:08Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-04-02T12:51:48Z
- **Updated**: 2024-04-03T17:38:08Z
- **Closed**: 2024-04-03T17:38:07Z
- **Labels**: `kind/bug`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

The count for the number of pending workloads in ClusterQueue is down-counted by one.
This stays like that for a long time.

**What you expected to happen**:

The number of pending workloads correspond to reality. 

**How to reproduce it (as minimally and precisely as possible)**:

Create the following setup:

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
  queueingStrategy: StrictFIFO
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

Create the "blocker" job that gets admitted:
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  generateName: blocker-job-
  namespace: default
  labels:
    kueue.x-k8s.io/queue-name: user-queue
spec:
  parallelism: 9
  completions: 9
  suspend: true
  template:
    spec:
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:v0.0.3
        args: ["3600s"]
        resources:
          requests:
            cpu: "1"
            memory: "200Mi"
      restartPolicy: Never
```

Then create the sample job:
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: sample-job
  namespace: default
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
        image: gcr.io/k8s-staging-perf-tests/sleep:v0.0.3
        args: ["1800s"]
        resources:
          requests:
            cpu: "1"
            memory: "200Mi"
      restartPolicy: Never
```

Now, the sample job is "blocked", and it is pending, `kubectl describe workload` returns:
```
Status:
  Conditions:
    Last Transition Time:  2024-04-02T12:46:27Z
    Message:               couldn't assign flavors to pod set main: insufficient unused quota for cpu in flavor default-flavor, 3 more needed
    Reason:                Pending
    Status:                False
    Type:                  QuotaReserved
Events:
  Type    Reason   Age                   From             Message
  ----    ------   ----                  ----             -------
  Normal  Pending  116s (x25 over 116s)  kueue-admission  couldn't assign flavors to pod set main: insufficient unused quota for cpu in flavor default-flavor, 3 more needed
```
However, the workload is not shown in the status of the ClusterQueue, `clusterQueue.status.pendingWorkloads=0`.

**Anything else we need to know?**:

I suspect this is because the number of pending workloads is taken from the cache, which decrements by 1 on Pop (from the heap). Then, at the end of each cycle it returns to the cache by RequeueIfNotPresent. So, it might flake.

I suppose this is not so much of an issue for BestEffortFIFO, because in that case the workload is moved to inadmissibleWorkloads queue, so it is not continuously popped.

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-02T16:45:38Z

Is this impacted only for https://github.com/kubernetes-sigs/kueue/tree/main/keps/168-pending-workloads-visibility#kep-168-pending-workloads-visibility?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-02T16:53:46Z

It affects the cache, and so it affects on-demand visibility, visibility in status, `status.pendingWorkloads` field, and metrics.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-02T16:54:08Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-02T16:57:28Z

> It affects the cache, and so it affects on-demand visibility, visibility in status, `status.pendingWorkloads` field, and metrics.

I see.
