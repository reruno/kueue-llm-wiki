# Issue #9830: Kueue cannot handle queue label changes on StatefulSets created with replica=0

**Summary**: Kueue cannot handle queue label changes on StatefulSets created with replica=0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9830

**Last updated**: 2026-03-18T09:24:33Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@lburgazzoli](https://github.com/lburgazzoli)
- **Created**: 2026-03-12T12:32:31Z
- **Updated**: 2026-03-18T09:24:33Z
- **Closed**: 2026-03-18T09:24:33Z
- **Labels**: `kind/bug`
- **Assignees**: [@MaysaMacedo](https://github.com/MaysaMacedo)
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
                                                                                                                                                                                                                                                           
When a StatefulSet is created with replicas: 0 and deliberately pointed to a non-existent queue (e.g., baz) and then updated to replicas: 1 (two-phase pattern), Kueue's mutating webhook injects kueue.x-k8s.io/pod-group-total-count as a pod template annotation, changing it from "0" to "1". This causes a controller revision mismatch (currentRevision != updateRevision) because the pod is SchedulingGated and never becomes Ready, so the StatefulSet controller never promotes the new revision.           
                                                                                                                                                                                                                                                               
In this state, patching kueue.x-k8s.io/queue-name to a valid queue (e.g., from baz to bar) has no effect. The patch succeeds on the StatefulSet object, but:
  - The pod keeps the old queue=baz label
  - The workload stays inadmissible on baz
  - Kueue's StatefulSet reconciler never triggers the suspend → delete → recreate path

**What you expected to happen**:
After patching kueue.x-k8s.io/queue-name from baz to bar, the pod should be recreated with queue-name=bar and admitted by the bar LocalQueue — the same behavior observed when the StatefulSet is created directly with replicas: 1 (single-phase).

**How to reproduce it (as minimally and precisely as possible)**:

Prerequisites: Kubernetes cluster with Kueue installed, a LocalQueue named bar pointing to a valid ClusterQueue.

1. Create a StatefulSet with replicas: 0 and label kueue.x-k8s.io/queue-name: baz (where baz does not exist):

```
cat <<'EOF' | kubectl apply -f -
  apiVersion: apps/v1
  kind: StatefulSet
  metadata:
    name: web
    labels:
      kueue.x-k8s.io/queue-name: baz
  spec:
    serviceName: web
    replicas: 0
    selector:
      matchLabels:
        app: web
    template:
      metadata:
        labels:
          app: web
      spec:
        containers:
          - name: web
            image: nginx:latest
            ports:
              - containerPort: 80
  EOF
```

2. Verify revisions match: 
```kubectl get statefulset web -o jsonpath='currentRev={.status.currentRevision} updateRev={.status.updateRevision}'```

3. Update to replicas: 1:
```kubectl patch statefulset web --type='json' -p='[{"op":"replace","path":"/spec/replicas","value":1}]'```

4. Verify revision mismatch and pod is gated:
```
kubectl get statefulset web -o jsonpath='currentRev={.status.currentRevision} updateRev={.status.updateRevision}'
# currentRev=web-AAAAA updateRev=web-BBBBB (mismatch)

kubectl get pod web-0
# STATUS: SchedulingGated
```

5. Patch the queue label to a valid queue:
``` 
kubectl patch statefulset web --type='json' -p='[{"op":"replace","path":"/metadata/labels/kueue.x-k8s.io~1queue-name","value":"bar"}]'
```

6. Observe the bug:
```
kubectl get pod web-0 -o jsonpath='queue={.metadata.labels.kueue\.x-k8s\.io/queue-name}'
# queue=baz  ← NOT UPDATED
kubectl get workloads.kueue.x-k8s.io -o custom-columns='QUEUE:.spec.queueName'
# baz  ← STILL INADMISSIBLE
```

**Anything else we need to know?**:

**Environment**:
- Kubernetes version: OpenShift 4.19.16, Kubernetes v1.32.9
- Kueue version: 0.14 
- Cloud provider or hardware configuration: OpenShift

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-12T13:03:36Z

@lburgazzoli thank you for the report, would you be able to check if the issue persists on 0.16.2? Asking because we fixed multiple issues for StatefulSets recently
cc @mbobrovskyi

### Comment by [@MaysaMacedo](https://github.com/MaysaMacedo) — 2026-03-12T13:28:41Z

I would like to help with this issue, if fine by everyone.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-12T13:35:22Z

sure

### Comment by [@MaysaMacedo](https://github.com/MaysaMacedo) — 2026-03-12T13:43:46Z

/assign

### Comment by [@kannon92](https://github.com/kannon92) — 2026-03-16T19:51:40Z

https://github.com/kubernetes-sigs/kueue/pull/9910
I drafted a test case and it looks like it is fixed on main.
@lburgazzoli also confirmed internally that we did not see this problem on latest kueue or latest 0.16.
