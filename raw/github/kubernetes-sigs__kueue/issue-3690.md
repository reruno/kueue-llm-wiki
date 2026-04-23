# Issue #3690: Rolling update does not work for StatefulSet integration

**Summary**: Rolling update does not work for StatefulSet integration

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3690

**Last updated**: 2024-12-04T13:43:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-11-29T13:34:46Z
- **Updated**: 2024-12-04T13:43:02Z
- **Closed**: 2024-12-04T13:43:02Z
- **Labels**: `kind/bug`, `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 4

## Description

/kind bug
/kind feature

**What happened**:

When doing a rolling update of StatefulSet it gets stuck after stopping the first pod. 

**What you expected to happen**:

The rolling update of STS is supported as this is a common operation for serving workloads.

**How to reproduce it (as minimally and precisely as possible)**:

1. Create the STS as here: 

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
          image: registry.k8s.io/nginx-slim:0.26
          ports:
            - containerPort: 80
          resources:
            requests:
              cpu: "100m"
  serviceName: "nginx"
```

2. trigger STS rolling update with:

```sh
kubectl set image statefulset/nginx-statefulset nginx=registry.k8s.io/nginx-slim:0.27
```
issue: The update gets stuck, and the pods are:
```
> k get pods      
NAME                  READY   STATUS      RESTARTS   AGE
nginx-statefulset-0   1/1     Running     0          3m33s
nginx-statefulset-1   1/1     Running     0          3m30s
nginx-statefulset-2   0/1     Completed   0          3m29s
```

**Anything else we need to know?**:

After deleting the finalizer from `nginx-statefulset-2` pod manually, the STS update is still stuck, the pods:

```
> k get pods                            
NAME                  READY   STATUS            RESTARTS   AGE
nginx-statefulset-0   1/1     Running           0          5m51s
nginx-statefulset-1   1/1     Running           0          5m48s
nginx-statefulset-2   0/1     SchedulingGated   0          3s
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-29T13:34:53Z

/assign @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-29T13:37:00Z

@mimowo thanks!

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-29T13:52:43Z

cc @gabesaba who recently is getting familiar with the inference support

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-29T14:47:51Z

/kind feature
I mark it both as bug and feature. As bug, because from the end-user perspective this is a bug, but since the fix requires new API (the serving annotation), I would also call it a feature.
