# Issue #5048: The workload is not admitted if queue-name is set while manageJobsWithoutQueueName is enabled

**Summary**: The workload is not admitted if queue-name is set while manageJobsWithoutQueueName is enabled

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5048

**Last updated**: 2025-06-23T09:46:56Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-04-18T12:29:29Z
- **Updated**: 2025-06-23T09:46:56Z
- **Closed**: 2025-06-23T09:46:56Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

The workload is not admitted if queue-name is set while manageJobsWithoutQueueName is enabled.

This happens because we are setting labels and annotation only when queue-name is available:

https://github.com/kubernetes-sigs/kueue/blob/f23be17d69a548e5c279140edb6fc26e0d7d6ab0/pkg/controller/jobs/statefulset/statefulset_webhook.go#L88-L95

**What you expected to happen**:

The workload was admitted and the pods are running successfully.

**How to reproduce it (as minimally and precisely as possible)**:

1. Install Kueue with manageJobsWithoutQueueName=true, "pod" enabled and "statefulset" enabled.
2. Apply https://github.com/kubernetes-sigs/kueue/blob/f23be17d69a548e5c279140edb6fc26e0d7d6ab0/site/static/examples/admin/single-clusterqueue-setup.yaml.
3. Create StatefulSet without queue-name:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: nginx-statefulset
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: registry.k8s.io/nginx-slim:0.27
          ports:
            - containerPort: 80
          resources:
            requests:
              cpu: "100m"
  serviceName: "nginx"
```

It creates a workload for a single pod instead of the StatefulSet pod group:
```
kubectl get wl   
NAME                            QUEUE   RESERVED IN   ADMITTED   FINISHED   AGE
pod-nginx-statefulset-0-7b2bd                                               82s

kubectl get pods            
NAME                  READY   STATUS            RESTARTS   AGE
nginx-statefulset-0   0/1     SchedulingGated   0          70s
```

4. Apply StatefulSet with queue-name:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: nginx-statefulset
  labels:
    app: nginx
    kueue.x-k8s.io/queue-name: user-queue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: registry.k8s.io/nginx-slim:0.27
          ports:
            - containerPort: 80
          resources:
            requests:
              cpu: "100m"
  serviceName: "nginx"
```

The workload is still not admitted:
```
kubectl get wl                                               
NAME                            QUEUE   RESERVED IN   ADMITTED   FINISHED   AGE
pod-nginx-statefulset-0-7b2bd                                               116s

kubectl get pods                                                   
NAME                  READY   STATUS            RESTARTS   AGE
nginx-statefulset-0   0/1     SchedulingGated   0          2m31s

```

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):  1.32.3
- Kueue version (use `git describe --tags --dirty --always`): main branch
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-04-18T14:04:51Z

/assign
