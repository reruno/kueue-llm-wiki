# Issue #3996: Kueue prevents scaling StatefulSets which aren't managed by Kueue

**Summary**: Kueue prevents scaling StatefulSets which aren't managed by Kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3996

**Last updated**: 2025-01-17T13:02:36Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-01-17T10:40:49Z
- **Updated**: 2025-01-17T13:02:36Z
- **Closed**: 2025-01-17T13:02:36Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 1

## Description


**What happened**:

Kueue prevents scaling StatefulSets which aren't managed by Kueue, and fails such attampts with the following error:
```
error: statefulsets.apps "nginx-statefulset" could not be patched: admission webhook "vstatefulset.kb.io" denied the request: spec.replicas: Invalid value: 4: field is immutable
```

**What you expected to happen**:

Kueue shouldn't block updating StatefulSets which aren't managed by it.

**How to reproduce it (as minimally and precisely as possible)**:

1. Enable the "statefulset" integration in the configmap (`kubectl edit configmap -nkueue-system -oyaml` and restart the kueue manager)
2. Create the "toy" StatefulSet without "queue-name": 

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
          image: registry.k8s.io/nginx-slim:0.26
          ports:
            - containerPort: 80
          resources:
            requests:
              cpu: "100m"
  serviceName: "nginx"
```
3. Attempt to update the StatefulSet spec.replicas from 3 to 4.


**Anything else we need to know?**:

The issue is present on 0.10 and 0.9.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-17T10:41:27Z

/assign @mbobrovskyi 
cc @tenzen-y I would like to include the fix for it in 0.9 and 0.10
