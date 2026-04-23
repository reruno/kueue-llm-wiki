# Issue #4966: Workloads are not automatically removed when the LeaderWorkerSet is deleted.

**Summary**: Workloads are not automatically removed when the LeaderWorkerSet is deleted.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4966

**Last updated**: 2025-04-16T18:27:13Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-04-14T16:39:11Z
- **Updated**: 2025-04-16T18:27:13Z
- **Closed**: 2025-04-16T18:27:13Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
When a LeaderWorkerSet without a queue name is deleted while managedJobWithoutQueueName is set to true, the workloads are not removed.

**What you expected to happen**:

All workloads should be deleted.

**How to reproduce it (as minimally and precisely as possible)**:

1. Apply kueue manifests with `managedJobWithoutQueueName=true`.

2. Create LeaderWorkerSet without queue-name.

```yaml
apiVersion: leaderworkerset.x-k8s.io/v1
kind: LeaderWorkerSet
metadata:
  name: nginx-leaderworkerset
  labels:
    app: nginx
spec:
  replicas: 3
  leaderWorkerTemplate:
    size: 3
    leaderTemplate:
      spec:
        containers:
          - name: nginx-leader
            image: registry.k8s.io/nginx-slim:0.27
            resources:
              requests:
                cpu: "100m"
            ports:
              - containerPort: 80
    workerTemplate:
      spec:
        containers:
          - name: nginx-worker
            image: registry.k8s.io/nginx-slim:0.27
            resources:
              requests:
                cpu: "200m"
            ports:
              - containerPort: 80
```


3. Delete LeaderWorkerSet.

```bash
kubectl delete lws nginx-leaderworkerset
```

4. As a result, all workloads are still here.

```
default     leaderworkerset-nginx-leaderworkerset-0-84517                                               24s
default     leaderworkerset-nginx-leaderworkerset-1-8f23f                                               24s
default     leaderworkerset-nginx-leaderworkerset-2-4fe3c                                               24s
```

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): v1.32.2
- Kueue version (use `git describe --tags --dirty --always`): main branch
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-04-16T12:45:54Z

/assign
